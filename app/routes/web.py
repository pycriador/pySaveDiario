from __future__ import annotations

from datetime import datetime
from functools import wraps
from secrets import token_urlsafe

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..extensions import csrf, db
from ..utils.upload import save_image, delete_image
from ..forms import (
    GroupCreateForm,
    GroupMemberForm,
    LoginForm,
    UserActionForm,
    UserCreateForm,
    OfferCreateForm,
    TemplateCreateForm,
    SellerForm,
    CategoryForm,
    ManufacturerForm,
    CouponForm,
    SocialNetworkConfigForm,
)
from ..models import (
    AppSettings,
    Category,
    Coupon,
    Group,
    Manufacturer,
    Namespace,
    NamespaceScope,
    Offer,
    Product,
    RoleEnum,
    Seller,
    SocialNetworkConfig,
    Template,
    User,
    Wishlist,
)
from ..utils import slugify

web_bp = Blueprint("web", __name__)


# Custom decorator for JSON routes that require login
def json_login_required(f):
    """Decorator for routes that return JSON and require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({"error": "Autenticação necessária. Por favor, faça login."}), 401
        return f(*args, **kwargs)
    return decorated_function


@web_bp.route("/api-docs")
def api_documentation():
    """API documentation page"""
    return render_template("api_docs.html")


@web_bp.route("/")
def index():
    from datetime import datetime
    
    # Get recent offers (only from active sellers)
    offers = Offer.query.outerjoin(Seller, Offer.seller_id == Seller.id)\
        .filter(
            db.or_(
                Seller.active == True,
                Offer.seller_id.is_(None)
            )
        ).order_by(Offer.created_at.desc()).limit(6).all()
    templates = Template.query.limit(4).all()
    
    # Calculate statistics
    total_offers = Offer.query.count()
    total_coupons = Coupon.query.filter_by(active=True).count()
    total_templates = Template.query.count()
    
    # Active offers (not expired)
    active_offers = Offer.query.filter(
        db.or_(
            Offer.expires_at.is_(None),
            Offer.expires_at > datetime.now()
        )
    ).count()
    
    # Calculate total savings (sum of discounts)
    total_savings = 0
    offers_with_discount = Offer.query.filter(Offer.old_price.isnot(None)).all()
    for offer in offers_with_discount:
        if offer.old_price and offer.price:
            savings = float(offer.old_price) - float(offer.price)
            if savings > 0:
                total_savings += savings
    
    return render_template(
        "index.html",
        offers=offers,
        templates=templates,
        total_offers=total_offers,
        total_coupons=total_coupons,
        total_templates=total_templates,
        active_offers=active_offers,
        total_savings=total_savings,
    )


@web_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("web.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Bem-vindo(a) de volta!", "success")
            return redirect(url_for("web.dashboard"))
        flash("Credenciais inválidas.", "danger")
    return render_template("login.html", form=form)


@web_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sessão encerrada.", "info")
    return redirect(url_for("web.index"))


@web_bp.route("/dashboard")
@login_required
def dashboard():
    # Get recent offers (only from active sellers)
    offers = Offer.query.outerjoin(Seller, Offer.seller_id == Seller.id)\
        .filter(
            db.or_(
                Seller.active == True,
                Offer.seller_id.is_(None)
            )
        ).order_by(Offer.created_at.desc()).limit(5).all()
    wishlists = Wishlist.query.filter_by(owner_id=current_user.id).all()
    return render_template(
        "dashboard.html",
        offers=offers,
        wishlists=wishlists,
    )


@web_bp.route("/usuarios", methods=["GET", "POST"])
def users():
    # Get filter parameters from URL
    search = request.args.get("search", "").strip()
    role_filter = request.args.get("role", "")
    active_only = request.args.get("active_only", "true").lower() == "true"
    
    # Build query
    query = User.query
    
    # Apply search filter (email, name, social media)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            db.or_(
                User.email.ilike(search_pattern),
                User.display_name.ilike(search_pattern),
                User.phone.ilike(search_pattern),
                User.address.ilike(search_pattern),
                User.website.ilike(search_pattern),
                User.instagram.ilike(search_pattern),
                User.facebook.ilike(search_pattern),
                User.twitter.ilike(search_pattern),
                User.linkedin.ilike(search_pattern),
                User.youtube.ilike(search_pattern),
                User.tiktok.ilike(search_pattern),
            )
        )
    
    # Apply role filter
    if role_filter:
        try:
            query = query.filter_by(role=RoleEnum(role_filter))
        except ValueError:
            role_filter = ""
    
    # Apply active filter
    if active_only:
        query = query.filter_by(is_active=True)
    
    # Get results
    users = query.order_by(User.created_at.desc()).all()
    
    action_form = UserActionForm() if current_user.is_authenticated else None
    user_form = UserCreateForm(prefix="user")
    can_manage = current_user.is_authenticated and current_user.role == RoleEnum.ADMIN

    if can_manage and user_form.submit_user.data and user_form.validate_on_submit():
        email = user_form.email.data.lower()
        if User.query.filter_by(email=email).first():
            flash("E-mail já cadastrado.", "warning")
        else:
            new_user = User(
                email=email,
                display_name=user_form.display_name.data,
                role=RoleEnum(user_form.role.data),
                phone=user_form.phone.data if user_form.phone.data else None,
                address=user_form.address.data if user_form.address.data else None,
                website=user_form.website.data if user_form.website.data else None,
                instagram=user_form.instagram.data if user_form.instagram.data else None,
                facebook=user_form.facebook.data if user_form.facebook.data else None,
                twitter=user_form.twitter.data if user_form.twitter.data else None,
                linkedin=user_form.linkedin.data if user_form.linkedin.data else None,
                youtube=user_form.youtube.data if user_form.youtube.data else None,
                tiktok=user_form.tiktok.data if user_form.tiktok.data else None,
            )
            new_user.set_password(user_form.password.data)
            visitor_group = Group.query.filter_by(slug="visitantes").first()
            if visitor_group and visitor_group not in new_user.groups:
                new_user.groups.append(visitor_group)
            db.session.add(new_user)
            db.session.commit()
            flash(f"Usuário {new_user.display_name} criado e adicionado a Visitantes.", "success")
            return redirect(url_for("web.users"))
    elif request.method == "POST" and not can_manage and user_form.submit_user.data:
        flash("Apenas administradores podem criar usuários.", "danger")
        return redirect(url_for("web.login"))

    return render_template(
        "users.html",
        users=users,
        action_form=action_form,
        user_form=user_form,
        can_manage=can_manage,
        role_enum=RoleEnum,
        # Filter parameters
        search=search,
        role_filter=role_filter,
        active_only=active_only,
    )


@web_bp.route("/usuarios/<int:user_id>/editar", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    """Edit user page"""
    user = User.query.get_or_404(user_id)
    
    # Permission check: user can edit own profile, or admin can edit any
    if current_user.id != user.id and current_user.role != RoleEnum.ADMIN:
        flash("Você não tem permissão para editar este usuário.", "danger")
        return redirect(url_for("web.users"))
    
    # CRITICAL: Check if user is editing themselves
    is_editing_self = (current_user.id == user.id)
    
    # CRITICAL: Store original role to prevent accidental changes
    original_user_role = user.role
    original_current_user_role = current_user.role
    
    from ..forms import UserEditForm
    form = UserEditForm(obj=user)
    
    # If user is editing own profile, remove role and is_active fields to prevent tampering
    if is_editing_self:
        if hasattr(form, 'role'):
            delattr(form, 'role')
        if hasattr(form, 'is_active'):
            delattr(form, 'is_active')
    
    if form.validate_on_submit():
        # Check if email is already taken by another user
        if form.email.data != user.email:
            existing = User.query.filter_by(email=form.email.data).first()
            if existing:
                flash("E-mail já em uso por outro usuário.", "warning")
                return render_template("user_edit.html", form=form, user=user)
        
        # Update basic fields
        user.display_name = form.display_name.data
        user.email = form.email.data
        
        # Update password if provided
        if form.password.data:
            if form.password.data != form.confirm_password.data:
                flash("As senhas não coincidem.", "warning")
                return render_template("user_edit.html", form=form, user=user)
            user.set_password(form.password.data)
        
        # CRITICAL: Only admin can change role, but NEVER allow changing own role
        if current_user.role == RoleEnum.ADMIN and not is_editing_self:
            # Admin editing another user - allow role change
            user.role = RoleEnum(form.role.data)
        elif is_editing_self:
            # User editing own profile - NEVER change role
            user.role = original_user_role
            print(f"🔒 PROTECTION: Prevented self role change for {user.email}")
        
        # Update contact information
        user.phone = form.phone.data if form.phone.data else None
        user.address = form.address.data if form.address.data else None
        user.website = form.website.data if form.website.data else None
        
        # Update social media
        user.instagram = form.instagram.data if form.instagram.data else None
        user.facebook = form.facebook.data if form.facebook.data else None
        user.twitter = form.twitter.data if form.twitter.data else None
        user.linkedin = form.linkedin.data if form.linkedin.data else None
        user.youtube = form.youtube.data if form.youtube.data else None
        user.tiktok = form.tiktok.data if form.tiktok.data else None
        
        # CRITICAL: Flush and verify current_user wasn't modified
        db.session.flush()
        
        if current_user.role != original_current_user_role:
            print(f"⚠️  WARNING: current_user.role changed from {original_current_user_role} to {current_user.role}! Reverting...")
            current_user.role = original_current_user_role
        
        db.session.commit()
        flash(f"Usuário '{user.display_name}' atualizado com sucesso!", "success")
        return redirect(url_for("web.users"))
    
    return render_template("user_edit.html", form=form, user=user)


@web_bp.route("/usuarios/acao", methods=["POST"])
@login_required
def user_action():
    if current_user.role != RoleEnum.ADMIN:
        abort(403)
    form = UserActionForm()
    if not form.validate_on_submit():
        flash("Solicitação inválida.", "danger")
        return redirect(url_for("web.users"))

    user = User.query.get_or_404(int(form.user_id.data))
    action = form.action.data

    if user.id == current_user.id and action in {"delete", "toggle_active"}:
        flash("Não é possível executar essa ação em si mesmo.", "warning")
        return redirect(url_for("web.users"))

    def last_admin_block() -> bool:
        admins = User.query.filter_by(role=RoleEnum.ADMIN, is_active=True).count()
        return user.role == RoleEnum.ADMIN and admins <= 1

    if action == "delete":
        if last_admin_block():
            flash("Mantenha ao menos um administrador ativo.", "warning")
        else:
            db.session.delete(user)
            db.session.commit()
            flash(f"Usuário {user.display_name} removido.", "success")
    elif action == "reset_password":
        new_password = token_urlsafe(8)
        user.set_password(new_password)
        db.session.commit()
        flash(
            f"Senha de {user.display_name} redefinida. Nova senha temporária: {new_password}",
            "info",
        )
    elif action == "toggle_active":
        if last_admin_block():
            flash("Mantenha ao menos um administrador ativo.", "warning")
        else:
            user.is_active = not user.is_active
            state = "reativado" if user.is_active else "inativado"
            db.session.commit()
            flash(f"Usuário {user.display_name} {state}.", "success")
    elif action == "promote_admin":
        if user.role == RoleEnum.ADMIN:
            flash("Usuário já é administrador.", "info")
        else:
            user.role = RoleEnum.ADMIN
            user.is_active = True
            db.session.commit()
            flash(f"{user.display_name} agora é administrador.", "success")
    else:
        flash("Ação desconhecida.", "danger")

    return redirect(url_for("web.users"))


@web_bp.route("/grupos", methods=["GET", "POST"])
def groups():
    groups = Group.query.order_by(Group.name).all()
    all_users = User.query.order_by(User.display_name).all()
    available_users = {}
    for group in groups:
        member_ids = {member.id for member in group.members}
        available_users[group.id] = [user for user in all_users if user.id not in member_ids]

    form = GroupCreateForm(prefix="group")
    member_form = GroupMemberForm()
    can_manage = current_user.is_authenticated and current_user.role == RoleEnum.ADMIN

    if can_manage and form.submit_group.data and form.validate_on_submit():
        slug_value = form.slug.data.strip().lower() if form.slug.data else slugify(form.name.data)
        if Group.query.filter_by(slug=slug_value).first():
            flash("Este slug já está em uso.", "warning")
        else:
            group = Group(
                name=form.name.data,
                slug=slug_value,
                description=form.description.data,
            )
            db.session.add(group)
            db.session.commit()
            flash("Grupo criado com sucesso.", "success")
            return redirect(url_for("web.groups"))
    elif request.method == "POST" and not can_manage and form.submit_group.data:
        flash("Apenas administradores podem criar grupos.", "danger")
        return redirect(url_for("web.login"))

    if can_manage and member_form.validate_on_submit():
        group = Group.query.get_or_404(int(member_form.group_id.data))
        user = User.query.get_or_404(int(member_form.user_id.data))
        action = member_form.action.data
        if action == "add":
            if user in group.members:
                flash(f"{user.display_name} já está neste grupo.", "info")
            else:
                group.members.append(user)
                db.session.commit()
                flash(f"{user.display_name} adicionado a {group.name}.", "success")
        elif action == "remove":
            if user not in group.members:
                flash("Usuário não faz parte do grupo.", "warning")
            else:
                group.members.remove(user)
                db.session.commit()
                flash(f"{user.display_name} removido de {group.name}.", "info")
        return redirect(url_for("web.groups"))
    elif request.method == "POST" and member_form.action.data and not can_manage:
        flash("Apenas administradores podem gerenciar membros.", "danger")
        return redirect(url_for("web.login"))

    return render_template(
        "groups.html",
        groups=groups,
        form=form,
        can_manage=can_manage,
        member_form=member_form,
        available_users=available_users,
    )


@web_bp.route("/ofertas", methods=["GET"])
def offers():
    """List offers with dynamic filters"""
    from datetime import datetime
    
    # Get filter parameters
    search = request.args.get("search", "").strip()
    manufacturer_id = request.args.get("manufacturer", type=int)
    category_id = request.args.get("category", type=int)
    seller_id = request.args.get("seller", type=int)
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    active_only = request.args.get("active_only", "true").lower() == "true"
    
    # Build query
    query = Offer.query.join(Product)
    
    # Filter by search term (product name, slug, vendor name)
    if search:
        search_filter = db.or_(
            Product.name.ilike(f"%{search}%"),
            Product.slug.ilike(f"%{search}%"),
            Offer.vendor_name.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Filter by manufacturer
    if manufacturer_id:
        query = query.filter(Offer.manufacturer_id == manufacturer_id)
    
    # Filter by category
    if category_id:
        query = query.filter(Offer.category_id == category_id)
    
    # Filter by seller
    if seller_id:
        query = query.filter(Offer.seller_id == seller_id)
    
    # Filter by price range
    if min_price is not None:
        query = query.filter(Offer.price >= min_price)
    if max_price is not None:
        query = query.filter(Offer.price <= max_price)
    
    # Filter by active offers (not expired)
    if active_only:
        query = query.filter(
            db.or_(
                Offer.expires_at.is_(None),
                Offer.expires_at > datetime.utcnow()
            )
        )
    
    # Filter to show only offers from active sellers
    query = query.outerjoin(Seller, Offer.seller_id == Seller.id)\
        .filter(
            db.or_(
                Seller.active == True,
                Offer.seller_id.is_(None)
            )
        )
    
    offers = query.order_by(Offer.created_at.desc()).all()
    
    can_manage = current_user.is_authenticated and current_user.role in (RoleEnum.ADMIN, RoleEnum.EDITOR)
    
    # For share functionality
    templates = Template.query.all()
    namespaces = Namespace.query.filter(
        Namespace.scope.in_([NamespaceScope.OFFER, NamespaceScope.COUPON, NamespaceScope.GLOBAL])
    ).order_by(Namespace.scope, Namespace.name).all()
    
    # Get all manufacturers, categories, and sellers for filter dropdowns
    manufacturers = Manufacturer.query.filter_by(active=True).order_by(Manufacturer.name).all()
    categories = Category.query.filter_by(active=True).order_by(Category.name).all()
    sellers = Seller.query.filter_by(active=True).order_by(Seller.name).all()
    
    # Get active coupons for sharing
    active_coupons = Coupon.query.filter_by(active=True).filter(
        db.or_(
            Coupon.expires_at.is_(None),
            Coupon.expires_at > datetime.utcnow()
        )
    ).order_by(Coupon.code).all()
    
    # Get social network configurations
    social_configs = SocialNetworkConfig.query.filter_by(active=True).all()
    
    return render_template("offers_list.html", 
                         offers=offers, 
                         can_manage=can_manage,
                         templates=templates,
                         namespaces=namespaces,
                         manufacturers=manufacturers,
                         categories=categories,
                         sellers=sellers,
                         active_coupons=active_coupons,
                         social_configs=social_configs,
                         filters={
                             'search': search,
                             'manufacturer': manufacturer_id,
                             'category': category_id,
                             'seller': seller_id,
                             'min_price': min_price,
                             'max_price': max_price,
                             'active_only': active_only
                         })


@web_bp.route("/ofertas/nova", methods=["GET", "POST"])
@login_required
def create_offer():
    """Create new offer page"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.offers"))
    
    form = OfferCreateForm(prefix="offer")
    
    # Populate select fields with existing data
    sellers = Seller.query.filter_by(active=True).order_by(Seller.name).all()
    categories = Category.query.filter_by(active=True).order_by(Category.name).all()
    manufacturers = Manufacturer.query.filter_by(active=True).order_by(Manufacturer.name).all()
    templates = Template.query.all()
    namespaces = Namespace.query.filter(
        Namespace.scope.in_([NamespaceScope.OFFER, NamespaceScope.COUPON, NamespaceScope.GLOBAL])
    ).order_by(Namespace.scope, Namespace.name).all()
    
    # Get default currency
    default_currency = AppSettings.get_default_currency()
    
    form.seller_id.choices = [(0, '-- Selecione --')] + [(s.id, s.name) for s in sellers]
    form.category_id.choices = [(0, '-- Selecione --')] + [(c.id, c.name) for c in categories]
    form.manufacturer_id.choices = [(0, '-- Selecione --')] + [(m.id, m.name) for m in manufacturers]

    if request.method == "POST" and form.validate_on_submit():
        slug_value = slugify(form.product_slug.data)
        product_obj = Product.query.filter_by(slug=slug_value).first()
        
        # Get the selected category and manufacturer names
        category_name = None
        manufacturer_name = None
        
        if form.category_id.data and form.category_id.data > 0:
            category_obj = Category.query.get(form.category_id.data)
            category_name = category_obj.name if category_obj else None
            
        if form.manufacturer_id.data and form.manufacturer_id.data > 0:
            manufacturer_obj = Manufacturer.query.get(form.manufacturer_id.data)
            manufacturer_name = manufacturer_obj.name if manufacturer_obj else None
        
        # Handle image upload
        image_url = None
        if form.product_image.data:
            success, filepath, error_msg = save_image(form.product_image.data, 'products')
            if success:
                image_url = filepath
            else:
                flash(f"Erro ao fazer upload da imagem: {error_msg}", "warning")
        
        if not product_obj:
            product_obj = Product(
                name=form.product_name.data,
                slug=slug_value,
                description=form.product_description.data,
                category=category_name,
                manufacturer=manufacturer_name,
                image_url=image_url,
            )
            db.session.add(product_obj)
            db.session.flush()
        else:
            # Update existing product image if new one uploaded
            if image_url:
                # Delete old image if exists
                if product_obj.image_url:
                    delete_image(product_obj.image_url)
                product_obj.image_url = image_url

        # Combine date and time fields into datetime
        expires_at = None
        if form.expires_date.data:
            if form.expires_time.data:
                expires_at = datetime.combine(form.expires_date.data, form.expires_time.data)
            else:
                # If only date is provided, use 00:00
                from datetime import time as dt_time
                expires_at = datetime.combine(form.expires_date.data, dt_time(0, 0))
        
        # Get vendor name from seller or use legacy field
        vendor_name = form.vendor_name.data
        if form.seller_id.data and form.seller_id.data > 0:
            seller_obj = Seller.query.get(form.seller_id.data)
            vendor_name = seller_obj.name if seller_obj else vendor_name

        new_offer = Offer(
            product=product_obj,
            vendor_name=vendor_name,
            price=form.price.data,
            old_price=form.old_price.data if form.old_price.data else None,
            currency=form.currency.data.upper(),
            offer_url=form.offer_url.data,
            expires_at=expires_at,
            seller_id=form.seller_id.data if form.seller_id.data and form.seller_id.data > 0 else None,
            category_id=form.category_id.data if form.category_id.data and form.category_id.data > 0 else None,
            manufacturer_id=form.manufacturer_id.data if form.manufacturer_id.data and form.manufacturer_id.data > 0 else None,
            created_by=current_user if current_user.is_authenticated else None,
            # Installment fields
            installment_count=form.installment_count.data if form.installment_count.data else None,
            installment_value=form.installment_value.data if form.installment_value.data else None,
            installment_interest_free=form.installment_interest_free.data,
        )
        db.session.add(new_offer)
        db.session.commit()
        flash("Oferta criada com sucesso!", "success")
        return redirect(url_for("web.offers"))

    return render_template("offer_create.html", 
                         form=form,
                         sellers=sellers,
                         categories=categories,
                         manufacturers=manufacturers,
                         default_currency=default_currency)


@web_bp.route("/ofertas/<int:offer_id>/editar", methods=["GET", "POST"])
@login_required
def edit_offer(offer_id):
    """Edit offer page"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.offers"))
    
    offer = Offer.query.get_or_404(offer_id)
    form = OfferCreateForm(prefix="offer", obj=offer)
    
    # Populate select fields
    sellers = Seller.query.filter_by(active=True).order_by(Seller.name).all()
    categories = Category.query.filter_by(active=True).order_by(Category.name).all()
    manufacturers = Manufacturer.query.filter_by(active=True).order_by(Manufacturer.name).all()
    
    form.seller_id.choices = [(0, '-- Selecione --')] + [(s.id, s.name) for s in sellers]
    form.category_id.choices = [(0, '-- Selecione --')] + [(c.id, c.name) for c in categories]
    form.manufacturer_id.choices = [(0, '-- Selecione --')] + [(m.id, m.name) for m in manufacturers]
    
    if request.method == "GET":
        # Pre-fill form with existing data
        if offer.product:
            form.product_name.data = offer.product.name
            form.product_slug.data = offer.product.slug
            form.product_description.data = offer.product.description
        
        form.seller_id.data = offer.seller_id if offer.seller_id else 0
        form.category_id.data = offer.category_id if offer.category_id else 0
        form.manufacturer_id.data = offer.manufacturer_id if offer.manufacturer_id else 0
        form.vendor_name.data = offer.vendor_name
        form.price.data = float(offer.price) if offer.price else None
        form.old_price.data = float(offer.old_price) if offer.old_price else None
        form.currency.data = offer.currency
        form.offer_url.data = offer.offer_url
        
        # Installment fields
        form.installment_count.data = offer.installment_count
        form.installment_value.data = float(offer.installment_value) if offer.installment_value else None
        form.installment_interest_free.data = offer.installment_interest_free if offer.installment_interest_free is not None else True
        
        # Split datetime into date and time fields
        if offer.expires_at:
            form.expires_date.data = offer.expires_at.date()
            form.expires_time.data = offer.expires_at.time()

    if request.method == "POST" and form.validate_on_submit():
        # Handle image upload
        if form.product_image.data:
            success, filepath, error_msg = save_image(form.product_image.data, 'products')
            if success:
                # Delete old image if exists
                if offer.product and offer.product.image_url:
                    delete_image(offer.product.image_url)
                # Update image URL
                if offer.product:
                    offer.product.image_url = filepath
            else:
                flash(f"Erro ao fazer upload da imagem: {error_msg}", "warning")
        
        # Update product
        if offer.product:
            offer.product.name = form.product_name.data
            offer.product.slug = slugify(form.product_slug.data)
            offer.product.description = form.product_description.data
            
            # Update category and manufacturer names in product
            if form.category_id.data and form.category_id.data > 0:
                category_obj = Category.query.get(form.category_id.data)
                offer.product.category = category_obj.name if category_obj else None
            
            if form.manufacturer_id.data and form.manufacturer_id.data > 0:
                manufacturer_obj = Manufacturer.query.get(form.manufacturer_id.data)
                offer.product.manufacturer = manufacturer_obj.name if manufacturer_obj else None
        
        # Get vendor name
        vendor_name = form.vendor_name.data
        if form.seller_id.data and form.seller_id.data > 0:
            seller_obj = Seller.query.get(form.seller_id.data)
            vendor_name = seller_obj.name if seller_obj else vendor_name
        
        # Update offer
        offer.vendor_name = vendor_name
        offer.price = form.price.data
        offer.old_price = form.old_price.data if form.old_price.data else None
        offer.currency = form.currency.data.upper()
        offer.offer_url = form.offer_url.data
        offer.seller_id = form.seller_id.data if form.seller_id.data and form.seller_id.data > 0 else None
        offer.category_id = form.category_id.data if form.category_id.data and form.category_id.data > 0 else None
        offer.manufacturer_id = form.manufacturer_id.data if form.manufacturer_id.data and form.manufacturer_id.data > 0 else None
        
        # Update installment fields
        offer.installment_count = form.installment_count.data if form.installment_count.data else None
        offer.installment_value = form.installment_value.data if form.installment_value.data else None
        offer.installment_interest_free = form.installment_interest_free.data
        
        # Combine date and time fields into datetime
        if form.expires_date.data:
            if form.expires_time.data:
                offer.expires_at = datetime.combine(form.expires_date.data, form.expires_time.data)
            else:
                # If only date is provided, use 00:00
                from datetime import time as dt_time
                offer.expires_at = datetime.combine(form.expires_date.data, dt_time(0, 0))
        else:
            offer.expires_at = None
        
        db.session.commit()
        flash("Oferta atualizada com sucesso!", "success")
        return redirect(url_for("web.offers"))
    
    default_currency = AppSettings.get_default_currency()
    
    return render_template("offer_edit.html", 
                         form=form,
                         offer=offer,
                         sellers=sellers,
                         categories=categories,
                         manufacturers=manufacturers,
                         default_currency=default_currency)


@web_bp.route("/ofertas/<int:offer_id>/compartilhar", methods=["GET", "POST"])
@login_required
def share_offer(offer_id):
    """Share offer page - select template, coupons and generate text"""
    offer = Offer.query.get_or_404(offer_id)
    
    # Get channel from URL parameter (e.g., ?channel=whatsapp)
    selected_channel = request.args.get('channel', '').lower()
    
    # Get all active templates
    templates = Template.query.order_by(Template.name).all()
    
    # Get active coupons from the same seller as the offer
    active_coupons = Coupon.query.filter_by(
        active=True,
        seller_id=offer.seller_id
    ).order_by(Coupon.code).all()
    
    # Get active social network configurations
    social_networks = SocialNetworkConfig.query.filter_by(active=True).order_by(SocialNetworkConfig.network).all()
    
    # Create dict for JS (prefix/suffix)
    social_configs = {
        config.network.lower(): {
            'prefix_text': config.prefix_text or '',
            'suffix_text': config.suffix_text or ''
        } for config in social_networks
    }
    
    # Get all namespaces for display
    namespaces = Namespace.query.filter(
        Namespace.scope.in_([NamespaceScope.OFFER, NamespaceScope.COUPON, NamespaceScope.GLOBAL])
    ).order_by(Namespace.scope, Namespace.name).all()
    
    return render_template("offer_share.html",
                         offer=offer,
                         templates=templates,
                         active_coupons=active_coupons,
                         social_networks=social_networks,
                         social_configs=social_configs,
                         namespaces=namespaces,
                         selected_channel=selected_channel,
                         user=current_user)


@web_bp.route("/template-social-network/save", methods=["POST"])
@csrf.exempt
@login_required
def save_custom_template():
    """Save or update custom template for specific social network"""
    from ..models import Template, TemplateSocialNetwork
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"message": "Nenhum dado recebido.", "success": False}), 400
        
        template_id = data.get("template_id")
        social_network = data.get("social_network")
        custom_body = data.get("custom_body")
        
        print(f"🔍 Recebido: template_id={template_id}, social_network={social_network}, custom_body length={len(custom_body) if custom_body else 0}")
        
        if not all([template_id, social_network, custom_body]):
            return jsonify({
                "message": "template_id, social_network e custom_body são obrigatórios.",
                "success": False,
                "received": {
                    "template_id": template_id,
                    "social_network": social_network,
                    "custom_body": bool(custom_body)
                }
            }), 400
        
        # Verify template exists
        template = Template.query.get(template_id)
        if not template:
            return jsonify({"message": "Template não encontrado."}), 404
        
        # Check if custom template already exists
        existing = TemplateSocialNetwork.query.filter_by(
            template_id=template_id,
            social_network=social_network.lower()
        ).first()
        
        if existing:
            # Update existing
            existing.custom_body = custom_body
            from datetime import datetime
            existing.updated_at = datetime.utcnow()
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
        return jsonify({"message": message, "success": True}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao salvar: {str(e)}", "success": False}), 500


@web_bp.route("/template-social-network/<int:template_id>/<social_network>", methods=["GET"])
@csrf.exempt
def get_custom_template(template_id: int, social_network: str):
    """Get custom template for specific social network (public endpoint, no auth required)"""
    from ..models import TemplateSocialNetwork
    
    try:
        custom = TemplateSocialNetwork.query.filter_by(
            template_id=template_id,
            social_network=social_network.lower()
        ).first()
        
        if not custom:
            # Return 200 with found=false instead of 404
            # This is not an error, just means no custom template exists yet
            return jsonify({"message": "Usando template padrão", "found": False}), 200
        
        return jsonify({"data": custom.to_dict(), "found": True}), 200
    
    except Exception as e:
        print(f"❌ Erro ao buscar template: {e}")
        return jsonify({"message": f"Erro ao buscar: {str(e)}", "found": False}), 500


@web_bp.route("/ofertas/<int:offer_id>/delete", methods=["POST"])
@login_required
def delete_offer(offer_id):
    """Delete an offer"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso negado.", "warning")
        return redirect(url_for("web.offers"))
    
    offer = Offer.query.get_or_404(offer_id)
    product_name = offer.product.name if offer.product else "Oferta"
    db.session.delete(offer)
    db.session.commit()
    flash(f"Oferta de '{product_name}' deletada com sucesso!", "success")
    return redirect(url_for("web.offers"))


# ============================================================================
# COUPONS ROUTES
# ============================================================================

@web_bp.route("/cupons", methods=["GET"])
@login_required
def coupons():
    """List all coupons with filters"""
    from datetime import datetime
    
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.index"))
    
    # Get filter parameters
    search = request.args.get("search", "").strip()
    seller_id = request.args.get("seller", type=int)
    active_only = request.args.get("active_only", "true").lower() == "true"
    discount_type = request.args.get("discount_type", "").strip()
    
    # Build query
    query = Coupon.query
    
    # Filter by search term (code only)
    if search:
        query = query.filter(Coupon.code.ilike(f"%{search}%"))
    
    # Filter by seller
    if seller_id:
        query = query.filter(Coupon.seller_id == seller_id)
    
    # Filter by active status
    if active_only:
        query = query.filter(Coupon.active == True)
    
    # Filter by discount type
    if discount_type:
        query = query.filter(Coupon.discount_type == discount_type)
    
    # Filter to show only coupons from active sellers
    query = query.outerjoin(Seller, Coupon.seller_id == Seller.id)\
        .filter(
            db.or_(
                Seller.active == True,
                Coupon.seller_id.is_(None)
            )
        )
    
    coupons = query.order_by(Coupon.created_at.desc()).all()
    can_manage = current_user.role in (RoleEnum.ADMIN, RoleEnum.EDITOR)
    
    # For share functionality
    templates = Template.query.all()
    namespaces = Namespace.query.filter(
        Namespace.scope.in_([NamespaceScope.OFFER, NamespaceScope.COUPON, NamespaceScope.GLOBAL])
    ).order_by(Namespace.scope, Namespace.name).all()
    
    # Get social network configurations
    social_configs = SocialNetworkConfig.query.filter_by(active=True).all()
    
    # Get all sellers for filter dropdown
    sellers = Seller.query.filter_by(active=True).order_by(Seller.name).all()
    
    return render_template("coupons_list.html", 
                         coupons=coupons, 
                         can_manage=can_manage,
                         templates=templates,
                         namespaces=namespaces,
                         social_configs=social_configs,
                         sellers=sellers)


@web_bp.route("/cupons/novo", methods=["GET", "POST"])
@login_required
def create_coupon():
    """Create new coupon page"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.coupons"))
    
    form = CouponForm()
    
    # Populate seller dropdown
    sellers = Seller.query.filter_by(active=True).order_by(Seller.name).all()
    form.seller_id.choices = [(0, "Selecione um vendedor...")] + [(s.id, s.name) for s in sellers]
    
    if request.method == "POST" and form.validate_on_submit():
        # Validate seller
        if form.seller_id.data == 0:
            flash("Por favor, selecione um vendedor.", "warning")
            return render_template("coupon_create.html", form=form, sellers=sellers)
        
        # Combine date and time fields into datetime
        expires_at = None
        if form.expires_date.data:
            if form.expires_time.data:
                expires_at = datetime.combine(form.expires_date.data, form.expires_time.data)
            else:
                # If only date is provided, use 00:00
                from datetime import time as dt_time
                expires_at = datetime.combine(form.expires_date.data, dt_time(0, 0))
        
        # Create coupon
        coupon = Coupon(
            seller_id=form.seller_id.data,
            code=form.code.data.upper(),  # Convert to uppercase
            active=form.active.data,
            expires_at=expires_at,
            discount_type=form.discount_type.data if form.discount_type.data else 'percentage',
            discount_value=form.discount_value.data if form.discount_value.data else None,
            min_purchase_value=form.min_purchase_value.data if form.min_purchase_value.data else None,
            max_discount_value=form.max_discount_value.data if form.max_discount_value.data else None,
            created_by=current_user
        )
        
        db.session.add(coupon)
        db.session.commit()
        flash(f"Cupom '{coupon.code}' criado com sucesso!", "success")
        return redirect(url_for("web.coupons"))
    
    return render_template("coupon_create.html", form=form, sellers=sellers)


@web_bp.route("/cupons/<int:coupon_id>/editar", methods=["GET", "POST"])
@login_required
def edit_coupon(coupon_id):
    """Edit coupon page"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.coupons"))
    
    coupon = Coupon.query.get_or_404(coupon_id)
    form = CouponForm(obj=coupon)
    
    # Populate seller dropdown
    sellers = Seller.query.filter_by(active=True).order_by(Seller.name).all()
    form.seller_id.choices = [(0, "Selecione um vendedor...")] + [(s.id, s.name) for s in sellers]
    
    if request.method == "GET":
        # Pre-fill form
        form.seller_id.data = coupon.seller_id
        form.code.data = coupon.code
        form.active.data = coupon.active
        form.discount_type.data = coupon.discount_type or 'percentage'
        form.discount_value.data = float(coupon.discount_value) if coupon.discount_value else None
        form.min_purchase_value.data = float(coupon.min_purchase_value) if coupon.min_purchase_value else None
        form.max_discount_value.data = float(coupon.max_discount_value) if coupon.max_discount_value else None
        
        # Split datetime into date and time fields
        if coupon.expires_at:
            form.expires_date.data = coupon.expires_at.date()
            form.expires_time.data = coupon.expires_at.time()
    
    if request.method == "POST" and form.validate_on_submit():
        if form.seller_id.data == 0:
            flash("Por favor, selecione um vendedor.", "warning")
            return render_template("coupon_edit.html", form=form, coupon=coupon, sellers=sellers)
        
        coupon.seller_id = form.seller_id.data
        coupon.code = form.code.data.upper()
        coupon.active = form.active.data
        coupon.discount_type = form.discount_type.data if form.discount_type.data else 'percentage'
        coupon.discount_value = form.discount_value.data if form.discount_value.data else None
        coupon.min_purchase_value = form.min_purchase_value.data if form.min_purchase_value.data else None
        coupon.max_discount_value = form.max_discount_value.data if form.max_discount_value.data else None
        
        # Combine date and time fields into datetime
        if form.expires_date.data:
            if form.expires_time.data:
                coupon.expires_at = datetime.combine(form.expires_date.data, form.expires_time.data)
            else:
                # If only date is provided, use 00:00
                from datetime import time as dt_time
                coupon.expires_at = datetime.combine(form.expires_date.data, dt_time(0, 0))
        else:
            coupon.expires_at = None
        
        db.session.commit()
        flash(f"Cupom '{coupon.code}' atualizado com sucesso!", "success")
        return redirect(url_for("web.coupons"))
    
    return render_template("coupon_edit.html", form=form, coupon=coupon, sellers=sellers)


@web_bp.route("/cupons/<int:coupon_id>/delete", methods=["POST"])
@login_required
def delete_coupon(coupon_id):
    """Delete a coupon"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso negado.", "warning")
        return redirect(url_for("web.coupons"))
    
    coupon = Coupon.query.get_or_404(coupon_id)
    code = coupon.code
    db.session.delete(coupon)
    db.session.commit()
    flash(f"Cupom '{code}' deletado com sucesso!", "success")
    return redirect(url_for("web.coupons"))


@web_bp.route("/cupons/<int:coupon_id>/toggle-active", methods=["POST"])
@login_required
def toggle_coupon_active(coupon_id):
    """Toggle coupon active status"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso negado.", "warning")
        return redirect(url_for("web.coupons"))
    
    coupon = Coupon.query.get_or_404(coupon_id)
    coupon.active = not coupon.active
    db.session.commit()
    
    status = "ativado" if coupon.active else "desativado"
    flash(f"Cupom '{coupon.code}' {status} com sucesso!", "success")
    return redirect(url_for("web.coupons"))


# ============================================================================
# TEMPLATES ROUTES
# ============================================================================

@web_bp.route("/templates", methods=["GET"])
@login_required
def share_templates():
    """List all templates with filters"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.dashboard"))
    
    # Get filter parameters
    search = request.args.get("search", "").strip()
    social_network = request.args.get("social_network", "").strip()
    
    # Build query
    query = Template.query
    
    # Filter by search term (name, slug, description)
    if search:
        search_filter = db.or_(
            Template.name.ilike(f"%{search}%"),
            Template.slug.ilike(f"%{search}%"),
            Template.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Filter by social network
    if social_network:
        query = query.join(Template.social_networks).filter(
            TemplateSocialNetwork.network.ilike(f"%{social_network}%")
        )
    
    templates = query.order_by(Template.created_at.desc()).all()
    can_manage = current_user.role in (RoleEnum.ADMIN, RoleEnum.EDITOR)
    
    # Get available namespaces for template variables
    namespaces = Namespace.query.filter(
        Namespace.scope.in_([NamespaceScope.OFFER, NamespaceScope.COUPON, NamespaceScope.GLOBAL])
    ).order_by(Namespace.scope, Namespace.name).all()
    
    # Get all social networks for filter dropdown
    social_networks = SocialNetworkConfig.query.filter_by(active=True).order_by(SocialNetworkConfig.network).all()

    return render_template(
        "templates_list.html", 
        templates=templates, 
        can_manage=can_manage, 
        namespaces=namespaces,
        social_networks=social_networks
    )


@web_bp.route("/templates/novo", methods=["GET", "POST"])
@login_required
def create_template():
    """Create new template page"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.share_templates"))
    
    form = TemplateCreateForm(prefix="template")
    
    # Get available namespaces for template variables
    namespaces = Namespace.query.filter(
        Namespace.scope.in_([NamespaceScope.OFFER, NamespaceScope.COUPON, NamespaceScope.GLOBAL])
    ).order_by(Namespace.scope, Namespace.name).all()
    
    # Get all social networks
    social_configs = SocialNetworkConfig.query.order_by(SocialNetworkConfig.network).all()

    if request.method == "POST" and form.validate_on_submit():
        slug_value = slugify(form.slug.data)
        if Template.query.filter_by(slug=slug_value).first():
            flash("Já existe um template com esse slug.", "warning")
            return render_template("template_create.html", form=form, namespaces=namespaces, social_configs=social_configs)
        
        # Create template
        template = Template(
            name=form.name.data,
            slug=slug_value,
            description=form.description.data,
            body=form.body.data,
            channels="",  # Keep empty for backwards compatibility
        )
        
        # Get selected social networks from form
        selected_network_ids = request.form.getlist('social_networks')
        if selected_network_ids:
            selected_networks = SocialNetworkConfig.query.filter(
                SocialNetworkConfig.id.in_(selected_network_ids)
            ).all()
            template.social_networks = selected_networks
        
        db.session.add(template)
        db.session.commit()
        flash("Template criado com sucesso!", "success")
        return redirect(url_for("web.share_templates"))

    return render_template("template_create.html", form=form, namespaces=namespaces, social_configs=social_configs)


@web_bp.route("/templates/<int:template_id>/editar", methods=["GET", "POST"])
@login_required
def edit_template(template_id):
    """Edit template page"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.share_templates"))
    
    template = Template.query.get_or_404(template_id)
    form = TemplateCreateForm(prefix="template", obj=template)
    
    # Get available namespaces
    namespaces = Namespace.query.filter(
        Namespace.scope.in_([NamespaceScope.OFFER, NamespaceScope.COUPON, NamespaceScope.GLOBAL])
    ).order_by(Namespace.scope, Namespace.name).all()
    
    # Get all social networks
    social_configs = SocialNetworkConfig.query.order_by(SocialNetworkConfig.network).all()
    
    if request.method == "GET":
        # Pre-fill form
        form.name.data = template.name
        form.slug.data = template.slug
        form.description.data = template.description
        form.body.data = template.body

    if request.method == "POST" and form.validate_on_submit():
        slug_value = slugify(form.slug.data)
        existing = Template.query.filter_by(slug=slug_value).first()
        if existing and existing.id != template.id:
            flash("Já existe outro template com esse slug.", "warning")
            return render_template("template_edit.html", form=form, template=template, namespaces=namespaces, social_configs=social_configs)
        
        template.name = form.name.data
        template.slug = slug_value
        template.description = form.description.data
        template.body = form.body.data
        
        # Update selected social networks
        selected_network_ids = request.form.getlist('social_networks')
        if selected_network_ids:
            selected_networks = SocialNetworkConfig.query.filter(
                SocialNetworkConfig.id.in_(selected_network_ids)
            ).all()
            template.social_networks = selected_networks
        else:
            template.social_networks = []
        
        db.session.commit()
        flash("Template atualizado com sucesso!", "success")
        return redirect(url_for("web.share_templates"))
    
    return render_template("template_edit.html", form=form, template=template, namespaces=namespaces, social_configs=social_configs)


@web_bp.route("/templates/<int:template_id>/delete", methods=["POST"])
@login_required
def delete_template(template_id):
    """Delete a template"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso negado.", "warning")
        return redirect(url_for("web.share_templates"))
    
    template = Template.query.get_or_404(template_id)
    template_name = template.name
    db.session.delete(template)
    db.session.commit()
    flash(f"Template '{template_name}' deletado com sucesso!", "success")
    return redirect(url_for("web.share_templates"))


# ========================================
# ADMINISTRATION ROUTES
# ========================================

@web_bp.route("/admin")
@login_required
def admin_dashboard():
    """Administration dashboard"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.dashboard"))
    
    sellers_count = Seller.query.count()
    categories_count = Category.query.count()
    manufacturers_count = Manufacturer.query.count()
    
    return render_template(
        "admin/dashboard.html",
        sellers_count=sellers_count,
        categories_count=categories_count,
        manufacturers_count=manufacturers_count,
    )


@web_bp.route("/admin/sellers", methods=["GET", "POST"])
@login_required
def admin_sellers():
    """Manage sellers"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.dashboard"))
    
    sellers = Seller.query.order_by(Seller.name).all()
    form = SellerForm(prefix="seller")
    
    if request.method == "POST" and form.validate_on_submit():
        slug_value = slugify(form.slug.data)
        if Seller.query.filter_by(slug=slug_value).first():
            flash("Já existe um vendedor com esse slug.", "warning")
            return redirect(url_for("web.admin_sellers"))
        
        seller = Seller(
            name=form.name.data,
            slug=slug_value,
            description=form.description.data,
            website=form.website.data,
            color=form.color.data or '#6b7280',
            active=form.active.data,
        )
        db.session.add(seller)
        db.session.commit()
        flash(f"Vendedor '{seller.name}' criado com sucesso!", "success")
        return redirect(url_for("web.admin_sellers"))
    
    return render_template("admin/sellers.html", sellers=sellers, form=form)


@web_bp.route("/admin/sellers/<int:seller_id>/delete", methods=["POST"])
@login_required
def admin_seller_delete(seller_id):
    """Delete a seller"""
    if current_user.role != RoleEnum.ADMIN:
        flash("Apenas administradores podem deletar vendedores.", "warning")
        return redirect(url_for("web.admin_sellers"))
    
    seller = Seller.query.get_or_404(seller_id)
    db.session.delete(seller)
    db.session.commit()
    flash(f"Vendedor '{seller.name}' deletado com sucesso!", "success")
    return redirect(url_for("web.admin_sellers"))


@web_bp.route("/admin/sellers/<int:seller_id>/toggle", methods=["POST"])
@login_required
def admin_seller_toggle(seller_id):
    """Toggle seller active status"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso negado.", "warning")
        return redirect(url_for("web.admin_sellers"))
    
    seller = Seller.query.get_or_404(seller_id)
    seller.active = not seller.active
    db.session.commit()
    
    status = "ativado" if seller.active else "desativado"
    flash(f"Vendedor '{seller.name}' {status} com sucesso!", "success")
    return redirect(url_for("web.admin_sellers"))


@web_bp.route("/admin/sellers/<int:seller_id>/editar", methods=["GET", "POST"])
@login_required
def admin_seller_edit(seller_id):
    """Edit seller page"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.admin_sellers"))
    
    seller = Seller.query.get_or_404(seller_id)
    form = SellerForm(prefix="seller", obj=seller)
    
    if request.method == "GET":
        form.name.data = seller.name
        form.slug.data = seller.slug
        form.description.data = seller.description
        form.website.data = seller.website
        form.color.data = seller.color
        form.active.data = seller.active
    
    if request.method == "POST" and form.validate_on_submit():
        # Check if slug is being changed and if new slug already exists
        slug_value = slugify(form.slug.data)
        if slug_value != seller.slug:
            if Seller.query.filter_by(slug=slug_value).first():
                flash("Já existe um vendedor com esse slug.", "warning")
                return redirect(url_for("web.admin_seller_edit", seller_id=seller_id))
        
        seller.name = form.name.data
        seller.slug = slug_value
        seller.description = form.description.data
        seller.website = form.website.data
        seller.color = form.color.data or '#6b7280'
        seller.active = form.active.data
        
        db.session.commit()
        flash(f"Vendedor '{seller.name}' atualizado com sucesso!", "success")
        return redirect(url_for("web.admin_sellers"))
    
    return render_template("admin/seller_edit.html", seller=seller, form=form)


@web_bp.route("/admin/categories", methods=["GET", "POST"])
@login_required
def admin_categories():
    """Manage categories"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.dashboard"))
    
    categories = Category.query.order_by(Category.name).all()
    form = CategoryForm(prefix="category")
    
    if request.method == "POST" and form.validate_on_submit():
        slug_value = slugify(form.slug.data)
        if Category.query.filter_by(slug=slug_value).first():
            flash("Já existe uma categoria com esse slug.", "warning")
            return redirect(url_for("web.admin_categories"))
        
        category = Category(
            name=form.name.data,
            slug=slug_value,
            description=form.description.data,
            icon=form.icon.data,
            active=form.active.data,
        )
        db.session.add(category)
        db.session.commit()
        flash(f"Categoria '{category.name}' criada com sucesso!", "success")
        return redirect(url_for("web.admin_categories"))
    
    return render_template("admin/categories.html", categories=categories, form=form)


@web_bp.route("/admin/categories/<int:category_id>/delete", methods=["POST"])
@login_required
def admin_category_delete(category_id):
    """Delete a category"""
    if current_user.role != RoleEnum.ADMIN:
        flash("Apenas administradores podem deletar categorias.", "warning")
        return redirect(url_for("web.admin_categories"))
    
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash(f"Categoria '{category.name}' deletada com sucesso!", "success")
    return redirect(url_for("web.admin_categories"))


@web_bp.route("/admin/categories/<int:category_id>/toggle", methods=["POST"])
@login_required
def admin_category_toggle(category_id):
    """Toggle category active status"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso negado.", "warning")
        return redirect(url_for("web.admin_categories"))
    
    category = Category.query.get_or_404(category_id)
    category.active = not category.active
    db.session.commit()
    
    status = "ativada" if category.active else "desativada"
    flash(f"Categoria '{category.name}' {status} com sucesso!", "success")
    return redirect(url_for("web.admin_categories"))


@web_bp.route("/admin/categories/<int:category_id>/editar", methods=["GET", "POST"])
@login_required
def admin_category_edit(category_id):
    """Edit category page"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.admin_categories"))
    
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(prefix="category", obj=category)
    
    if request.method == "GET":
        form.name.data = category.name
        form.slug.data = category.slug
        form.description.data = category.description
        form.icon.data = category.icon
        form.active.data = category.active
    
    if request.method == "POST" and form.validate_on_submit():
        # Check if slug is being changed and if new slug already exists
        slug_value = slugify(form.slug.data)
        if slug_value != category.slug:
            if Category.query.filter_by(slug=slug_value).first():
                flash("Já existe uma categoria com esse slug.", "warning")
                return redirect(url_for("web.admin_category_edit", category_id=category_id))
        
        category.name = form.name.data
        category.slug = slug_value
        category.description = form.description.data
        category.icon = form.icon.data
        category.active = form.active.data
        
        db.session.commit()
        flash(f"Categoria '{category.name}' atualizada com sucesso!", "success")
        return redirect(url_for("web.admin_categories"))
    
    return render_template("admin/category_edit.html", category=category, form=form)


@web_bp.route("/admin/manufacturers", methods=["GET", "POST"])
@login_required
def admin_manufacturers():
    """Manage manufacturers"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.dashboard"))
    
    manufacturers = Manufacturer.query.order_by(Manufacturer.name).all()
    form = ManufacturerForm(prefix="manufacturer")
    
    if request.method == "POST" and form.validate_on_submit():
        slug_value = slugify(form.slug.data)
        if Manufacturer.query.filter_by(slug=slug_value).first():
            flash("Já existe um fabricante com esse slug.", "warning")
            return redirect(url_for("web.admin_manufacturers"))
        
        manufacturer = Manufacturer(
            name=form.name.data,
            slug=slug_value,
            description=form.description.data,
            website=form.website.data,
            logo=form.logo.data,
            active=form.active.data,
        )
        db.session.add(manufacturer)
        db.session.commit()
        flash(f"Fabricante '{manufacturer.name}' criado com sucesso!", "success")
        return redirect(url_for("web.admin_manufacturers"))
    
    return render_template("admin/manufacturers.html", manufacturers=manufacturers, form=form)


@web_bp.route("/admin/manufacturers/<int:manufacturer_id>/delete", methods=["POST"])
@login_required
def admin_manufacturer_delete(manufacturer_id):
    """Delete a manufacturer"""
    if current_user.role != RoleEnum.ADMIN:
        flash("Apenas administradores podem deletar fabricantes.", "warning")
        return redirect(url_for("web.admin_manufacturers"))
    
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
    db.session.delete(manufacturer)
    db.session.commit()
    flash(f"Fabricante '{manufacturer.name}' deletado com sucesso!", "success")
    return redirect(url_for("web.admin_manufacturers"))


@web_bp.route("/admin/manufacturers/<int:manufacturer_id>/toggle", methods=["POST"])
@login_required
def admin_manufacturer_toggle(manufacturer_id):
    """Toggle manufacturer active status"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso negado.", "warning")
        return redirect(url_for("web.admin_manufacturers"))
    
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
    manufacturer.active = not manufacturer.active
    db.session.commit()
    
    status = "ativado" if manufacturer.active else "desativado"
    flash(f"Fabricante '{manufacturer.name}' {status} com sucesso!", "success")
    return redirect(url_for("web.admin_manufacturers"))


@web_bp.route("/admin/manufacturers/<int:manufacturer_id>/editar", methods=["GET", "POST"])
@login_required
def admin_manufacturer_edit(manufacturer_id):
    """Edit manufacturer page"""
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.admin_manufacturers"))
    
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
    form = ManufacturerForm(prefix="manufacturer", obj=manufacturer)
    
    if request.method == "GET":
        form.name.data = manufacturer.name
        form.slug.data = manufacturer.slug
        form.description.data = manufacturer.description
        form.website.data = manufacturer.website
        form.active.data = manufacturer.active
    
    if request.method == "POST" and form.validate_on_submit():
        # Check if slug is being changed and if new slug already exists
        slug_value = slugify(form.slug.data)
        if slug_value != manufacturer.slug:
            if Manufacturer.query.filter_by(slug=slug_value).first():
                flash("Já existe um fabricante com esse slug.", "warning")
                return redirect(url_for("web.admin_manufacturer_edit", manufacturer_id=manufacturer_id))
        
        manufacturer.name = form.name.data
        manufacturer.slug = slug_value
        manufacturer.description = form.description.data
        manufacturer.website = form.website.data
        manufacturer.active = form.active.data
        
        db.session.commit()
        flash(f"Fabricante '{manufacturer.name}' atualizado com sucesso!", "success")
        return redirect(url_for("web.admin_manufacturers"))
    
    return render_template("admin/manufacturer_edit.html", manufacturer=manufacturer, form=form)


@web_bp.route("/admin/settings", methods=["GET", "POST"])
@login_required
def admin_settings():
    """Manage application settings"""
    if current_user.role != RoleEnum.ADMIN:
        flash("Acesso permitido apenas para administradores.", "warning")
        return redirect(url_for("web.dashboard"))
    
    if request.method == "POST":
        # Update default currency
        default_currency = request.form.get('default_currency')
        if default_currency:
            AppSettings.set_default_currency(default_currency)
            flash(f"Moeda padrão atualizada para {default_currency}!", "success")
            return redirect(url_for("web.admin_settings"))
    
    # Get current settings
    default_currency = AppSettings.get_default_currency()
    
    # Available currencies with symbols
    from app.utils.currency import get_currency_symbol
    currencies = [
        ('BRL', 'BRL - Real Brasileiro', get_currency_symbol('BRL')),
        ('USD', 'USD - Dólar Americano', get_currency_symbol('USD')),
        ('EUR', 'EUR - Euro', get_currency_symbol('EUR')),
        ('GBP', 'GBP - Libra Esterlina', get_currency_symbol('GBP')),
        ('JPY', 'JPY - Iene Japonês', get_currency_symbol('JPY')),
        ('CAD', 'CAD - Dólar Canadense', get_currency_symbol('CAD')),
        ('AUD', 'AUD - Dólar Australiano', get_currency_symbol('AUD')),
        ('CHF', 'CHF - Franco Suíço', get_currency_symbol('CHF')),
        ('CNY', 'CNY - Yuan Chinês', get_currency_symbol('CNY')),
        ('ARS', 'ARS - Peso Argentino', get_currency_symbol('ARS')),
        ('MXN', 'MXN - Peso Mexicano', get_currency_symbol('MXN')),
        ('CLP', 'CLP - Peso Chileno', get_currency_symbol('CLP')),
    ]
    
    return render_template("admin/settings.html", 
                         default_currency=default_currency,
                         currencies=currencies)


@web_bp.route("/admin/social-networks", methods=["GET", "POST"])
@login_required
def admin_social_networks():
    """Manage social network configurations"""
    if current_user.role != RoleEnum.ADMIN:
        flash("Acesso permitido apenas para administradores.", "warning")
        return redirect(url_for("web.dashboard"))
    
    # CRITICAL: Store current user's role to prevent accidental changes
    original_user_role = current_user.role
    original_user_id = current_user.id
    
    # Get all social network configs
    configs = SocialNetworkConfig.query.all()
    form = SocialNetworkConfigForm()
    
    # Handle form submission (update existing)
    if request.method == "POST":
        network_id = request.form.get('network_id')
        if network_id:
            # Update existing
            config = SocialNetworkConfig.query.get_or_404(network_id)
            config.color = request.form.get('color', '#1877f2')
            config.prefix_text = request.form.get('prefix_text', '')
            config.suffix_text = request.form.get('suffix_text', '')
            config.active = 'active' in request.form
            
            # CRITICAL: Ensure current user's role is not changed
            db.session.flush()  # Flush changes but don't commit yet
            
            # Verify current_user wasn't accidentally modified
            if current_user.role != original_user_role:
                print(f"⚠️  WARNING: User role changed from {original_user_role} to {current_user.role}! Reverting...")
                current_user.role = original_user_role
            
            db.session.commit()
            flash(f"Configuração de {config.network.title()} atualizada com sucesso!", "success")
            return redirect(url_for("web.admin_social_networks"))
        elif form.validate_on_submit():
            # Create new
            existing = SocialNetworkConfig.query.filter_by(network=form.network.data.lower()).first()
            if existing:
                flash(f"Já existe uma configuração para {form.network.data}.", "warning")
            else:
                new_config = SocialNetworkConfig(
                    network=form.network.data.lower(),
                    color=form.color.data or '#1877f2',
                    prefix_text=form.prefix_text.data or '',
                    suffix_text=form.suffix_text.data or '',
                    active=form.active.data
                )
                db.session.add(new_config)
                
                # CRITICAL: Flush and verify current_user wasn't modified
                db.session.flush()
                if current_user.role != original_user_role:
                    print(f"⚠️  WARNING: User role changed from {original_user_role} to {current_user.role}! Reverting...")
                    current_user.role = original_user_role
                
                db.session.commit()
                flash(f"Rede social {form.network.data} adicionada com sucesso!", "success")
                return redirect(url_for("web.admin_social_networks"))
    
    return render_template("admin/social_networks.html", configs=configs, form=form)


@web_bp.route("/admin/social-networks/<int:config_id>/delete", methods=["POST"])
@login_required
def admin_social_network_delete(config_id):
    """Delete a social network configuration"""
    if current_user.role != RoleEnum.ADMIN:
        flash("Acesso permitido apenas para administradores.", "warning")
        return redirect(url_for("web.dashboard"))
    
    # CRITICAL: Store current user's role to prevent accidental changes
    original_user_role = current_user.role
    
    config = SocialNetworkConfig.query.get_or_404(config_id)
    network_name = config.network.title()
    
    db.session.delete(config)
    
    # CRITICAL: Flush and verify current_user wasn't modified
    db.session.flush()
    if current_user.role != original_user_role:
        print(f"⚠️  WARNING: User role changed from {original_user_role} to {current_user.role}! Reverting...")
        current_user.role = original_user_role
    
    db.session.commit()
    
    flash(f"Rede social {network_name} deletada com sucesso!", "success")
    return redirect(url_for("web.admin_social_networks"))


# ========================================
# QUICK CREATE API (JSON) - Session-based
# ========================================

@web_bp.route("/quick-create/sellers", methods=["POST"])
@csrf.exempt
@json_login_required
def quick_create_seller():
    """Quick create seller from offers page"""
    try:
        if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json() or {}
        
        if not data.get("name") or not data.get("slug"):
            return jsonify({"error": "Nome e slug são obrigatórios"}), 400
        
        slug_value = slugify(data["slug"])
        
        # Check if slug already exists
        if Seller.query.filter_by(slug=slug_value).first():
            return jsonify({"error": "Já existe um vendedor com esse slug"}), 400
        
        seller = Seller(
            name=data["name"],
            slug=slug_value,
            description=data.get("description"),
            website=data.get("website"),
            color=data.get("color", '#6b7280'),
            active=data.get("active", True),
        )
        
        db.session.add(seller)
        db.session.commit()
        
        # Return data explicitly
        return jsonify({
            "id": seller.id,
            "name": seller.name,
            "slug": seller.slug,
            "description": seller.description,
            "website": seller.website,
            "active": seller.active
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@web_bp.route("/quick-create/categories", methods=["POST"])
@csrf.exempt
@json_login_required
def quick_create_category():
    """Quick create category from offers page"""
    try:
        if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados JSON inválidos"}), 400
        
        if not data.get("name") or not data.get("slug"):
            return jsonify({"error": "Nome e slug são obrigatórios"}), 400
        
        slug_value = slugify(data["slug"])
        
        if Category.query.filter_by(slug=slug_value).first():
            return jsonify({"error": "Já existe uma categoria com esse slug"}), 400
        
        category = Category(
            name=data["name"],
            slug=slug_value,
            description=data.get("description"),
            icon=data.get("icon"),
            active=data.get("active", True),
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            "id": category.id,
            "name": category.name,
            "slug": category.slug,
            "description": category.description,
            "icon": category.icon,
            "active": category.active
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@web_bp.route("/quick-create/manufacturers", methods=["POST"])
@csrf.exempt
@json_login_required
def quick_create_manufacturer():
    """Quick create manufacturer from offers page"""
    try:
        if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json() or {}
        
        if not data.get("name") or not data.get("slug"):
            return jsonify({"error": "Nome e slug são obrigatórios"}), 400
        
        slug_value = slugify(data["slug"])
        
        # Check if slug already exists
        if Manufacturer.query.filter_by(slug=slug_value).first():
            return jsonify({"error": "Já existe um fabricante com esse slug"}), 400
        
        manufacturer = Manufacturer(
            name=data["name"],
            slug=slug_value,
            description=data.get("description"),
            website=data.get("website"),
            logo=data.get("logo"),
            active=data.get("active", True),
        )
        
        db.session.add(manufacturer)
        db.session.commit()
        
        # Return data explicitly
        return jsonify({
            "id": manufacturer.id,
            "name": manufacturer.name,
            "slug": manufacturer.slug,
            "description": manufacturer.description,
            "website": manufacturer.website,
            "logo": manufacturer.logo,
            "active": manufacturer.active
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

