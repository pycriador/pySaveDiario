from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
from secrets import token_hex

from flask import current_app
from flask_login import UserMixin
from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class RoleEnum(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    MEMBER = "member"


class NamespaceScope(str, Enum):
    PROFILE = "PROFILE"
    OFFER = "OFFER"
    COUPON = "COUPON"
    GLOBAL = "GLOBAL"


class WishlistVisibility(str, Enum):
    PRIVATE = "private"
    SHARED = "shared"
    PUBLIC = "public"


user_groups = db.Table(
    "user_groups",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("group_id", db.Integer, db.ForeignKey("groups.id"), primary_key=True),
)


class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.MEMBER, nullable=False)
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)

    tokens = db.relationship("UserToken", back_populates="user", lazy="dynamic")
    wishlists = db.relationship("Wishlist", back_populates="owner", lazy="dynamic")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def issue_token(self) -> "UserToken":
        minutes = current_app.config.get("TOKEN_EXPIRATION_MINUTES", 60)
        token = UserToken(
            token=token_hex(24),
            user=self,
            expires_at=datetime.utcnow() + timedelta(minutes=minutes),
        )
        db.session.add(token)
        return token

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "display_name": self.display_name,
            "role": self.role.value,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at.isoformat(),
        }


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return User.query.get(int(user_id))


class UserToken(TimestampMixin, db.Model):
    __tablename__ = "user_tokens"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(128), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked = db.Column(db.Boolean, default=False)

    user = db.relationship("User", back_populates="tokens")

    def is_valid(self) -> bool:
        return not self.revoked and datetime.utcnow() < self.expires_at


class Group(TimestampMixin, db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    is_featured = db.Column(db.Boolean, default=False)

    members = db.relationship("User", secondary=user_groups, backref="groups")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "is_featured": self.is_featured,
        }


class Wishlist(TimestampMixin, db.Model):
    __tablename__ = "wishlists"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    visibility = db.Column(db.Enum(WishlistVisibility), default=WishlistVisibility.PRIVATE)
    notes = db.Column(db.Text)

    owner = db.relationship("User", back_populates="wishlists")
    items = db.relationship("WishlistItem", back_populates="wishlist", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "visibility": self.visibility.value,
            "notes": self.notes,
            "owner_id": self.owner_id,
        }


class Product(TimestampMixin, db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(120))
    manufacturer = db.Column(db.String(120))

    offers = db.relationship("Offer", back_populates="product", lazy="dynamic")

    @validates("slug")
    def validate_slug(self, key, slug: str) -> str:
        if not slug:
            raise ValueError("Slug é obrigatório para o produto.")
        return slug

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "category": self.category,
            "manufacturer": self.manufacturer,
        }


class Offer(TimestampMixin, db.Model):
    __tablename__ = "offers"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    vendor_name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    old_price = db.Column(db.Numeric(10, 2), nullable=True)
    currency = db.Column(db.String(3), default="BRL")
    offer_url = db.Column(db.String(255))
    expires_at = db.Column(db.DateTime)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    
    # New relationships for administration
    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey("manufacturers.id"), nullable=True)

    product = db.relationship("Product", back_populates="offers")
    created_by = db.relationship("User")
    namespaces = db.relationship("OfferNamespaceValue", back_populates="offer", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "product": self.product.to_dict() if self.product else None,
            "vendor_name": self.vendor_name,
            "price": self.price_value,
            "currency": self.currency,
            "offer_url": self.offer_url,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }

    @property
    def price_value(self) -> float:
        return float(self.price or 0)


class WishlistItem(TimestampMixin, db.Model):
    __tablename__ = "wishlist_items"

    id = db.Column(db.Integer, primary_key=True)
    wishlist_id = db.Column(db.Integer, db.ForeignKey("wishlists.id"), nullable=False)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=False)
    desired_price = db.Column(db.Numeric(10, 2))
    notes = db.Column(db.Text)

    wishlist = db.relationship("Wishlist", back_populates="items")
    offer = db.relationship("Offer")

    __table_args__ = (
        db.UniqueConstraint("wishlist_id", "offer_id", name="uq_wishlist_offer"),
    )


# Association table for Template and SocialNetworkConfig (many-to-many)
template_social_networks = db.Table('template_social_networks',
    db.Column('template_id', db.Integer, db.ForeignKey('templates.id'), primary_key=True),
    db.Column('social_network_id', db.Integer, db.ForeignKey('social_network_configs.id'), primary_key=True)
)


class Template(TimestampMixin, db.Model):
    __tablename__ = "templates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    body = db.Column(db.Text, nullable=False)
    channels = db.Column(db.String(255), default="instagram,facebook,whatsapp,telegram")  # Keep for backwards compatibility
    
    # Relationship to social networks
    social_networks = db.relationship('SocialNetworkConfig', 
                                     secondary=template_social_networks,
                                     backref=db.backref('templates', lazy='dynamic'))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "channels": [channel.strip() for channel in self.channels.split(",")],
            "social_networks": [sn.network for sn in self.social_networks]
        }

    @property
    def channel_list(self) -> list[str]:
        # Return social networks if available, otherwise fall back to channels
        if self.social_networks:
            return [sn.network for sn in self.social_networks]
        return [channel.strip() for channel in self.channels.split(",") if channel.strip()]


class Namespace(TimestampMixin, db.Model):
    __tablename__ = "namespaces"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    label = db.Column(db.String(120), nullable=False)
    scope = db.Column(db.Enum(NamespaceScope), default=NamespaceScope.GLOBAL)
    description = db.Column(db.Text)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "label": self.label,
            "scope": self.scope.value,
            "description": self.description,
        }


class UserNamespaceValue(TimestampMixin, db.Model):
    __tablename__ = "user_namespace_values"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    namespace_id = db.Column(db.Integer, db.ForeignKey("namespaces.id"), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    namespace = db.relationship("Namespace")
    user = db.relationship("User")

    __table_args__ = (
        db.UniqueConstraint("user_id", "namespace_id", name="uq_user_namespace"),
    )


class OfferNamespaceValue(TimestampMixin, db.Model):
    __tablename__ = "offer_namespace_values"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=False)
    namespace_id = db.Column(db.Integer, db.ForeignKey("namespaces.id"), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    offer = db.relationship("Offer", back_populates="namespaces")
    namespace = db.relationship("Namespace")

    __table_args__ = (
        db.UniqueConstraint("offer_id", "namespace_id", name="uq_offer_namespace"),
    )


class Publication(TimestampMixin, db.Model):
    __tablename__ = "publications"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey("templates.id"), nullable=False)
    caption = db.Column(db.Text, nullable=False)
    published_at = db.Column(db.DateTime)
    published_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    channels = db.Column(db.String(255))

    offer = db.relationship("Offer")
    template = db.relationship("Template")
    published_by = db.relationship("User")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "offer_id": self.offer_id,
            "template_id": self.template_id,
            "caption": self.caption,
            "channels": self.channels.split(",") if self.channels else [],
            "published_at": self.published_at.isoformat() if self.published_at else None,
        }


class Seller(TimestampMixin, db.Model):
    """Marketplace sellers/vendors"""
    __tablename__ = "sellers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    website = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)

    # Relationships
    offers = db.relationship("Offer", backref="seller", lazy="dynamic")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "website": self.website,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Category(TimestampMixin, db.Model):
    """Product categories"""
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Icon class (e.g., "bi bi-laptop")
    active = db.Column(db.Boolean, default=True)

    # Relationships
    offers = db.relationship("Offer", backref="category", lazy="dynamic")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "icon": self.icon,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Manufacturer(TimestampMixin, db.Model):
    """Product manufacturers/brands"""
    __tablename__ = "manufacturers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    website = db.Column(db.String(255))
    logo = db.Column(db.String(255))  # URL or path to logo
    active = db.Column(db.Boolean, default=True)

    # Relationships
    offers = db.relationship("Offer", backref="manufacturer", lazy="dynamic")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "website": self.website,
            "logo": self.logo,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class SocialNetworkConfig(db.Model):
    """Configuration for social network sharing"""
    __tablename__ = "social_network_configs"
    
    id = db.Column(db.Integer, primary_key=True)
    network = db.Column(db.String(50), unique=True, nullable=False)  # instagram, facebook, whatsapp, telegram
    prefix_text = db.Column(db.Text, nullable=True)  # Text to add before template content
    suffix_text = db.Column(db.Text, nullable=True)  # Text to add after template content (hashtags, etc)
    active = db.Column(db.Boolean, default=True)
    
    @staticmethod
    def get_config(network_name):
        """Get configuration for a specific network"""
        config = SocialNetworkConfig.query.filter_by(network=network_name.lower()).first()
        return config
    
    @staticmethod
    def get_all_configs():
        """Get all network configurations"""
        return SocialNetworkConfig.query.filter_by(active=True).all()
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "network": self.network,
            "prefix_text": self.prefix_text,
            "suffix_text": self.suffix_text,
            "active": self.active,
        }


class AppSettings(db.Model):
    """Application settings/configuration"""
    __tablename__ = "app_settings"
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    
    @staticmethod
    def get_default_currency():
        """Get default currency from settings"""
        setting = AppSettings.query.filter_by(key='default_currency').first()
        return setting.value if setting and setting.value else 'BRL'
    
    @staticmethod
    def set_default_currency(currency_code):
        """Set default currency"""
        setting = AppSettings.query.filter_by(key='default_currency').first()
        if not setting:
            setting = AppSettings(
                key='default_currency',
                value=currency_code,
                description='Moeda padrão do sistema'
            )
            db.session.add(setting)
        else:
            setting.value = currency_code
        db.session.commit()
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value,
            "description": self.description,
        }


class Coupon(TimestampMixin, db.Model):
    """Discount coupons for sellers"""
    __tablename__ = "coupons"

    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"), nullable=False)
    code = db.Column(db.String(120), nullable=False)
    active = db.Column(db.Boolean, default=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # Relationships
    seller = db.relationship("Seller", backref=db.backref("coupons", lazy="dynamic"))
    created_by = db.relationship("User")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "seller_name": self.seller.name if self.seller else None,
            "code": self.code,
            "active": self.active,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

