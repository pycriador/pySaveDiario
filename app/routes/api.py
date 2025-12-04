from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from flask import Blueprint, jsonify, request
from sqlalchemy import or_

from ..extensions import db
from ..models import (
    Category,
    Group,
    Manufacturer,
    Namespace,
    NamespaceScope,
    Offer,
    OfferNamespaceValue,
    Product,
    Publication,
    RoleEnum,
    Seller,
    Template,
    User,
    Wishlist,
    WishlistItem,
    WishlistVisibility,
)
from ..security import basic_auth, role_required, token_auth

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/health")
def health() -> tuple[dict, int]:
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}, 200


@api_bp.route("/auth/login", methods=["POST"])
def auth_login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return {"message": "Informe e-mail e senha."}, 400
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return {"message": "Credenciais inválidas."}, 401
    token = user.issue_token()
    db.session.commit()
    return {
        "token": token.token,
        "expires_at": token.expires_at.isoformat(),
        "user": user.to_dict(),
    }, 200


@api_bp.route("/auth/token", methods=["POST"])
@basic_auth.login_required
def issue_token():
    user = basic_auth.current_user()
    token = user.issue_token()
    db.session.commit()
    return {
        "token": token.token,
        "expires_at": token.expires_at.isoformat(),
        "user": user.to_dict(),
    }, 201


@api_bp.route("/users", methods=["POST"])
def register_user():
    data = request.get_json() or {}
    required = {"email", "password", "display_name"}
    if not required.issubset(data):
        return {"message": "Campos obrigatórios faltando."}, 400
    if User.query.filter_by(email=data["email"]).first():
        return {"message": "Usuário já cadastrado."}, 409
    role_value = data.get("role", RoleEnum.MEMBER.value)
    try:
        role = RoleEnum(role_value)
    except ValueError:
        return {"message": "Papel inválido."}, 400
    user = User(
        email=data["email"],
        display_name=data["display_name"],
        role=role,
        phone=data.get("phone"),
        address=data.get("address"),
        website=data.get("website"),
        instagram=data.get("instagram"),
        facebook=data.get("facebook"),
        twitter=data.get("twitter"),
        linkedin=data.get("linkedin"),
        youtube=data.get("youtube"),
        tiktok=data.get("tiktok"),
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return user.to_dict(), 201


@api_bp.route("/users", methods=["GET"])
@token_auth.login_required
@role_required(RoleEnum.ADMIN)
def list_users():
    query = User.query
    role = request.args.get("role")
    if role:
        query = query.filter_by(role=RoleEnum(role))
    users = [user.to_dict() for user in query.order_by(User.created_at.desc()).all()]
    return jsonify(users)


@api_bp.route("/users/<int:user_id>", methods=["GET"])
@token_auth.login_required
def get_user(user_id: int):
    user = User.query.get_or_404(user_id)
    current = token_auth.current_user()
    if current.id != user.id and current.role != RoleEnum.ADMIN:
        return {"message": "Acesso negado."}, 403
    return user.to_dict()


@api_bp.route("/users/<int:user_id>", methods=["PUT", "PATCH"])
@token_auth.login_required
def update_user(user_id: int):
    """Update user information (own profile or admin)"""
    user = User.query.get_or_404(user_id)
    current = token_auth.current_user()
    
    # Permission check: user can update own profile, or admin can update any
    if current.id != user.id and current.role != RoleEnum.ADMIN:
        return {"message": "Acesso negado."}, 403
    
    data = request.get_json() or {}
    
    # Update fields if provided
    if "display_name" in data:
        user.display_name = data["display_name"]
    
    if "email" in data:
        # Check if email is already taken by another user
        existing = User.query.filter_by(email=data["email"]).first()
        if existing and existing.id != user.id:
            return {"message": "E-mail já em uso por outro usuário."}, 409
        user.email = data["email"]
    
    if "password" in data:
        user.set_password(data["password"])
    
    # Only admins can change roles
    if "role" in data and current.role == RoleEnum.ADMIN:
        try:
            user.role = RoleEnum(data["role"])
        except ValueError:
            return {"message": "Papel inválido."}, 400
    
    # Update contact information
    if "phone" in data:
        user.phone = data["phone"]
    if "address" in data:
        user.address = data["address"]
    if "website" in data:
        user.website = data["website"]
    
    # Update social media
    if "instagram" in data:
        user.instagram = data["instagram"]
    if "facebook" in data:
        user.facebook = data["facebook"]
    if "twitter" in data:
        user.twitter = data["twitter"]
    if "linkedin" in data:
        user.linkedin = data["linkedin"]
    if "youtube" in data:
        user.youtube = data["youtube"]
    if "tiktok" in data:
        user.tiktok = data["tiktok"]
    
    db.session.commit()
    return user.to_dict()


@api_bp.route("/groups", methods=["POST"])
@token_auth.login_required
@role_required(RoleEnum.ADMIN, RoleEnum.EDITOR)
def create_group():
    data = request.get_json() or {}
    if not data.get("name") or not data.get("slug"):
        return {"message": "Nome e slug são obrigatórios."}, 400
    group = Group(name=data["name"], slug=data["slug"], description=data.get("description"))
    db.session.add(group)
    db.session.commit()
    return group.to_dict(), 201


@api_bp.route("/groups", methods=["GET"])
def list_groups():
    groups = [group.to_dict() for group in Group.query.order_by(Group.name).all()]
    return jsonify(groups)


@api_bp.route("/wishlists", methods=["POST"])
@token_auth.login_required
def create_wishlist():
    data = request.get_json() or {}
    user = token_auth.current_user()
    visibility_value = data.get("visibility", WishlistVisibility.PRIVATE.value)
    try:
        visibility = WishlistVisibility(visibility_value)
    except ValueError:
        return {"message": "Visibilidade inválida."}, 400
    wishlist = Wishlist(
        owner=user,
        name=data.get("name", "Minha lista"),
        visibility=visibility,
        notes=data.get("notes"),
    )
    db.session.add(wishlist)
    db.session.commit()
    return wishlist.to_dict(), 201


@api_bp.route("/wishlists", methods=["GET"])
@token_auth.login_required
def list_wishlists():
    user = token_auth.current_user()
    visibility = request.args.get("visibility")
    query = Wishlist.query
    if user.role != RoleEnum.ADMIN:
        query = query.filter(
            or_(Wishlist.visibility != WishlistVisibility.PRIVATE, Wishlist.owner == user)
        )
    if visibility:
        try:
            query = query.filter_by(visibility=WishlistVisibility(visibility))
        except ValueError:
            return {"message": "Visibilidade inválida."}, 400
    wishlists = [wishlist.to_dict() for wishlist in query.all()]
    return jsonify(wishlists)


@api_bp.route("/wishlists/<int:wishlist_id>/items", methods=["POST"])
@token_auth.login_required
def add_wishlist_item(wishlist_id: int):
    wishlist = Wishlist.query.get_or_404(wishlist_id)
    user = token_auth.current_user()
    if wishlist.owner != user and user.role == RoleEnum.MEMBER:
        return {"message": "Apenas o proprietário pode adicionar itens."}, 403
    data = request.get_json() or {}
    offer = Offer.query.get_or_404(data.get("offer_id"))
    item = WishlistItem(
        wishlist=wishlist,
        offer=offer,
        desired_price=data.get("desired_price"),
        notes=data.get("notes"),
    )
    db.session.add(item)
    db.session.commit()
    return {"message": "Item adicionado com sucesso."}, 201


@api_bp.route("/offers", methods=["POST"])
@token_auth.login_required
@role_required(RoleEnum.ADMIN, RoleEnum.EDITOR)
def create_offer():
    data = request.get_json() or {}
    product_slug = data.get("product_slug")
    if not product_slug:
        return {"message": "Informe o slug do produto."}, 400
    if not data.get("vendor_name") or data.get("price") is None:
        return {"message": "Vendor e preço são obrigatórios."}, 400
    product = Product.query.filter_by(slug=product_slug).first()
    if not product:
        product = Product(
            name=data.get("product_name", "Produto sem nome"),
            slug=product_slug,
            description=data.get("product_description"),
            category=data.get("category"),
            manufacturer=data.get("manufacturer"),
        )
        db.session.add(product)
    try:
        price_value = Decimal(str(data["price"]))
    except Exception:
        return {"message": "Preço inválido."}, 400
    expires_at = None
    if data.get("expires_at"):
        try:
            expires_at = datetime.fromisoformat(data["expires_at"])
        except ValueError:
            return {"message": "Formato de data inválido."}, 400

    offer = Offer(
        product=product,
        vendor_name=data["vendor_name"],
        price=price_value,
        currency=data.get("currency", "BRL"),
        offer_url=data.get("offer_url"),
        expires_at=expires_at,
        created_by=token_auth.current_user(),
    )
    db.session.add(offer)
    db.session.flush()

    namespace_values = data.get("namespaces", {})
    for namespace_name, value in namespace_values.items():
        namespace = Namespace.query.filter_by(name=namespace_name).first()
        if not namespace:
            namespace = Namespace(
                name=namespace_name,
                label=namespace_name.replace("_", " ").title(),
                scope=NamespaceScope.OFFER,
            )
            db.session.add(namespace)
            db.session.flush()
        db.session.add(
            OfferNamespaceValue(
                offer=offer,
                namespace=namespace,
                value=value,
            )
        )

    db.session.commit()
    return offer.to_dict(), 201


@api_bp.route("/offers", methods=["GET"])
def list_offers():
    query = Offer.query.join(Product)
    vendor = request.args.get("vendor")
    product_slug = request.args.get("product")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")

    if vendor:
        query = query.filter(Offer.vendor_name.ilike(f"%{vendor}%"))
    if product_slug:
        query = query.filter(Product.slug == product_slug)
    if min_price:
        try:
            query = query.filter(Offer.price >= Decimal(min_price))
        except Exception:
            return {"message": "Preço mínimo inválido."}, 400
    if max_price:
        try:
            query = query.filter(Offer.price <= Decimal(max_price))
        except Exception:
            return {"message": "Preço máximo inválido."}, 400

    # Filter to show only offers from active sellers
    query = query.outerjoin(Seller, Offer.seller_id == Seller.id)\
        .filter(
            or_(
                Seller.active == True,
                Offer.seller_id.is_(None)
            )
        )

    offers = [offer.to_dict() for offer in query.order_by(Offer.created_at.desc()).all()]
    return jsonify(offers)


@api_bp.route("/templates", methods=["POST"])
@token_auth.login_required
@role_required(RoleEnum.ADMIN, RoleEnum.EDITOR)
def create_template():
    data = request.get_json() or {}
    if not data.get("name") or not data.get("slug"):
        return {"message": "Nome e slug são obrigatórios."}, 400
    template = Template(
        name=data["name"],
        slug=data["slug"],
        description=data.get("description"),
        body=data.get("body", ""),
        channels=",".join(data.get("channels", ["instagram", "facebook"])),
    )
    db.session.add(template)
    db.session.commit()
    return template.to_dict(), 201


@api_bp.route("/templates", methods=["GET"])
def list_templates():
    templates = [template.to_dict() for template in Template.query.all()]
    return jsonify(templates)


@api_bp.route("/template-social-network", methods=["POST"])
@token_auth.login_required
def save_custom_template():
    """Save or update custom template for specific social network"""
    data = request.get_json() or {}
    
    template_id = data.get("template_id")
    social_network = data.get("social_network")
    custom_body = data.get("custom_body")
    
    if not all([template_id, social_network, custom_body]):
        return {"message": "template_id, social_network e custom_body são obrigatórios."}, 400
    
    # Verify template exists
    from ..models import Template, TemplateSocialNetwork
    template = Template.query.get(template_id)
    if not template:
        return {"message": "Template não encontrado."}, 404
    
    # Check if custom template already exists
    existing = TemplateSocialNetwork.query.filter_by(
        template_id=template_id,
        social_network=social_network.lower()
    ).first()
    
    if existing:
        # Update existing
        existing.custom_body = custom_body
        existing.updated_at = db.func.now()
        message = f"Template atualizado para {social_network}"
    else:
        # Create new
        custom_template = TemplateSocialNetwork(
            template_id=template_id,
            social_network=social_network.lower(),
            custom_body=custom_body
        )
        db.session.add(custom_template)
        message = f"Template salvo para {social_network}"
    
    db.session.commit()
    return {"message": message}, 200


@api_bp.route("/template-social-network/<int:template_id>/<social_network>", methods=["GET"])
def get_custom_template(template_id: int, social_network: str):
    """Get custom template for specific social network"""
    from ..models import TemplateSocialNetwork
    
    custom = TemplateSocialNetwork.query.filter_by(
        template_id=template_id,
        social_network=social_network.lower()
    ).first()
    
    if not custom:
        return {"message": "Template customizado não encontrado."}, 404
    
    return jsonify(custom.to_dict())


@api_bp.route("/template-social-network/<int:template_id>", methods=["GET"])
def get_all_custom_templates_for_template(template_id: int):
    """Get all custom templates for a specific template"""
    from ..models import TemplateSocialNetwork
    
    customs = TemplateSocialNetwork.query.filter_by(template_id=template_id).all()
    return jsonify([c.to_dict() for c in customs])


@api_bp.route("/namespaces", methods=["POST"])
@token_auth.login_required
@role_required(RoleEnum.ADMIN, RoleEnum.EDITOR)
def create_namespace():
    data = request.get_json() or {}
    if not data.get("name"):
        return {"message": "Nome é obrigatório."}, 400
    scope_value = data.get("scope", NamespaceScope.GLOBAL.value)
    try:
        scope = NamespaceScope(scope_value)
    except ValueError:
        return {"message": "Escopo inválido."}, 400
    namespace = Namespace(
        name=data["name"],
        label=data.get("label", data["name"].title()),
        scope=scope,
        description=data.get("description"),
    )
    db.session.add(namespace)
    db.session.commit()
    return namespace.to_dict(), 201


@api_bp.route("/namespaces", methods=["GET"])
def list_namespaces():
    scope = request.args.get("scope")
    query = Namespace.query
    if scope:
        try:
            query = query.filter_by(scope=NamespaceScope(scope))
        except ValueError:
            return {"message": "Escopo inválido."}, 400
    return jsonify([namespace.to_dict() for namespace in query.all()])


@api_bp.route("/publications", methods=["POST"])
@token_auth.login_required
@role_required(RoleEnum.ADMIN, RoleEnum.EDITOR)
def publish_offer():
    data = request.get_json() or {}
    offer = Offer.query.get_or_404(data["offer_id"])
    template = Template.query.get_or_404(data["template_id"])
    caption = data.get("caption") or template.body
    publication = Publication(
        offer=offer,
        template=template,
        caption=caption,
        channels=",".join(data.get("channels", template.channels.split(","))),
        published_by=token_auth.current_user(),
        published_at=datetime.utcnow(),
    )
    db.session.add(publication)
    db.session.commit()
    return publication.to_dict(), 201


@api_bp.route("/publications", methods=["GET"])
def list_publications():
    publications = [publication.to_dict() for publication in Publication.query.all()]
    return jsonify(publications)


# ========================================
# SELLERS API
# ========================================

@api_bp.route("/sellers", methods=["POST"])
@token_auth.login_required
@role_required(RoleEnum.ADMIN, RoleEnum.EDITOR)
def create_seller():
    """Create a new seller"""
    data = request.get_json() or {}
    
    if not data.get("name") or not data.get("slug"):
        return {"message": "Name and slug are required."}, 400
    
    # Check if slug already exists
    if Seller.query.filter_by(slug=data["slug"]).first():
        return {"message": "Seller with this slug already exists."}, 400
    
    seller = Seller(
        name=data["name"],
        slug=data["slug"],
        description=data.get("description"),
        website=data.get("website"),
        active=data.get("active", True),
    )
    
    db.session.add(seller)
    db.session.commit()
    
    return seller.to_dict(), 201


@api_bp.route("/sellers", methods=["GET"])
def list_sellers():
    """List all sellers"""
    active_only = request.args.get("active_only", "false").lower() == "true"
    
    query = Seller.query
    if active_only:
        query = query.filter_by(active=True)
    
    sellers = [seller.to_dict() for seller in query.order_by(Seller.name).all()]
    return jsonify(sellers)


@api_bp.route("/sellers/<int:seller_id>", methods=["GET"])
def get_seller(seller_id: int):
    """Get a specific seller"""
    seller = Seller.query.get_or_404(seller_id)
    return seller.to_dict()


@api_bp.route("/sellers/<int:seller_id>", methods=["PUT"])
@token_auth.login_required
@role_required(RoleEnum.ADMIN, RoleEnum.EDITOR)
def update_seller(seller_id: int):
    """Update a seller"""
    seller = Seller.query.get_or_404(seller_id)
    data = request.get_json() or {}
    
    if "name" in data:
        seller.name = data["name"]
    if "slug" in data:
        # Check if new slug already exists (excluding current seller)
        existing = Seller.query.filter(Seller.slug == data["slug"], Seller.id != seller_id).first()
        if existing:
            return {"message": "Seller with this slug already exists."}, 400
        seller.slug = data["slug"]
    if "description" in data:
        seller.description = data["description"]
    if "website" in data:
        seller.website = data["website"]
    if "active" in data:
        seller.active = data["active"]
    
    db.session.commit()
    
    return seller.to_dict()


@api_bp.route("/sellers/<int:seller_id>", methods=["DELETE"])
@token_auth.login_required
@role_required(RoleEnum.ADMIN)
def delete_seller(seller_id: int):
    """Delete a seller"""
    seller = Seller.query.get_or_404(seller_id)
    db.session.delete(seller)
    db.session.commit()
    
    return {"message": "Seller deleted successfully"}, 200


# ========================================
# CATEGORIES API
# ========================================

@api_bp.route("/categories", methods=["POST"])
@token_auth.login_required
@role_required(RoleEnum.ADMIN, RoleEnum.EDITOR)
def create_category():
    """Create a new category"""
    data = request.get_json() or {}
    
    if not data.get("name") or not data.get("slug"):
        return {"message": "Name and slug are required."}, 400
    
    # Check if slug already exists
    if Category.query.filter_by(slug=data["slug"]).first():
        return {"message": "Category with this slug already exists."}, 400
    
    category = Category(
        name=data["name"],
        slug=data["slug"],
        description=data.get("description"),
        icon=data.get("icon"),
        active=data.get("active", True),
    )
    
    db.session.add(category)
    db.session.commit()
    
    return category.to_dict(), 201


@api_bp.route("/categories", methods=["GET"])
def list_categories():
    """List all categories"""
    active_only = request.args.get("active_only", "false").lower() == "true"
    
    query = Category.query
    if active_only:
        query = query.filter_by(active=True)
    
    categories = [category.to_dict() for category in query.order_by(Category.name).all()]
    return jsonify(categories)


@api_bp.route("/categories/<int:category_id>", methods=["GET"])
def get_category(category_id: int):
    """Get a specific category"""
    category = Category.query.get_or_404(category_id)
    return category.to_dict()


@api_bp.route("/categories/<int:category_id>", methods=["PUT"])
@token_auth.login_required
@role_required(RoleEnum.ADMIN, RoleEnum.EDITOR)
def update_category(category_id: int):
    """Update a category"""
    category = Category.query.get_or_404(category_id)
    data = request.get_json() or {}
    
    if "name" in data:
        category.name = data["name"]
    if "slug" in data:
        # Check if new slug already exists (excluding current category)
        existing = Category.query.filter(Category.slug == data["slug"], Category.id != category_id).first()
        if existing:
            return {"message": "Category with this slug already exists."}, 400
        category.slug = data["slug"]
    if "description" in data:
        category.description = data["description"]
    if "icon" in data:
        category.icon = data["icon"]
    if "active" in data:
        category.active = data["active"]
    
    db.session.commit()
    
    return category.to_dict()


@api_bp.route("/categories/<int:category_id>", methods=["DELETE"])
@token_auth.login_required
@role_required(RoleEnum.ADMIN)
def delete_category(category_id: int):
    """Delete a category"""
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    
    return {"message": "Category deleted successfully"}, 200


# ========================================
# MANUFACTURERS API
# ========================================

@api_bp.route("/manufacturers", methods=["POST"])
@token_auth.login_required
@role_required(RoleEnum.ADMIN, RoleEnum.EDITOR)
def create_manufacturer():
    """Create a new manufacturer"""
    data = request.get_json() or {}
    
    if not data.get("name") or not data.get("slug"):
        return {"message": "Name and slug are required."}, 400
    
    # Check if slug already exists
    if Manufacturer.query.filter_by(slug=data["slug"]).first():
        return {"message": "Manufacturer with this slug already exists."}, 400
    
    manufacturer = Manufacturer(
        name=data["name"],
        slug=data["slug"],
        description=data.get("description"),
        website=data.get("website"),
        logo=data.get("logo"),
        active=data.get("active", True),
    )
    
    db.session.add(manufacturer)
    db.session.commit()
    
    return manufacturer.to_dict(), 201


@api_bp.route("/manufacturers", methods=["GET"])
def list_manufacturers():
    """List all manufacturers"""
    active_only = request.args.get("active_only", "false").lower() == "true"
    
    query = Manufacturer.query
    if active_only:
        query = query.filter_by(active=True)
    
    manufacturers = [manufacturer.to_dict() for manufacturer in query.order_by(Manufacturer.name).all()]
    return jsonify(manufacturers)


@api_bp.route("/manufacturers/<int:manufacturer_id>", methods=["GET"])
def get_manufacturer(manufacturer_id: int):
    """Get a specific manufacturer"""
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
    return manufacturer.to_dict()


@api_bp.route("/manufacturers/<int:manufacturer_id>", methods=["PUT"])
@token_auth.login_required
@role_required(RoleEnum.ADMIN, RoleEnum.EDITOR)
def update_manufacturer(manufacturer_id: int):
    """Update a manufacturer"""
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
    data = request.get_json() or {}
    
    if "name" in data:
        manufacturer.name = data["name"]
    if "slug" in data:
        # Check if new slug already exists (excluding current manufacturer)
        existing = Manufacturer.query.filter(Manufacturer.slug == data["slug"], Manufacturer.id != manufacturer_id).first()
        if existing:
            return {"message": "Manufacturer with this slug already exists."}, 400
        manufacturer.slug = data["slug"]
    if "description" in data:
        manufacturer.description = data["description"]
    if "website" in data:
        manufacturer.website = data["website"]
    if "logo" in data:
        manufacturer.logo = data["logo"]
    if "active" in data:
        manufacturer.active = data["active"]
    
    db.session.commit()
    
    return manufacturer.to_dict()


@api_bp.route("/manufacturers/<int:manufacturer_id>", methods=["DELETE"])
@token_auth.login_required
@role_required(RoleEnum.ADMIN)
def delete_manufacturer(manufacturer_id: int):
    """Delete a manufacturer"""
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
    db.session.delete(manufacturer)
    db.session.commit()
    
    return {"message": "Manufacturer deleted successfully"}, 200

