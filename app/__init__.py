from __future__ import annotations

from flask import Flask
from sqlalchemy.exc import OperationalError

from .config import get_config
from .extensions import csrf, db, login_manager, migrate
from .models import Group, User
from .utils import slugify


def create_app(config_name: str | None = None) -> Flask:
    """Application factory."""
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(get_config(config_name))

    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    register_template_filters(app)
    seed_default_groups(app)

    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "web.login"
    login_manager.login_message = "Por favor, faça login para continuar."
    csrf.init_app(app)


def register_blueprints(app: Flask) -> None:
    from .routes.web import web_bp
    from .routes.api import api_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)


def register_template_filters(app: Flask) -> None:
    """Register custom Jinja2 template filters."""
    from .utils.currency import get_currency_symbol
    
    @app.template_filter('currency_symbol')
    def currency_symbol_filter(currency_code):
        """Convert currency code to symbol (e.g., BRL -> R$)"""
        return get_currency_symbol(currency_code)


def register_shellcontext(app: Flask) -> None:
    @app.shell_context_processor
    def shell_context() -> dict[str, object]:
        return {"db": db, "User": User, "Group": Group}


def seed_default_groups(app: Flask) -> None:
    defaults = [
        ("Administradores", "administradores", "Grupo com permissões totais."),
        ("Editores", "editores", "Responsáveis por criar publicações."),
        ("Visitantes", "visitantes", "Grupo padrão para novos usuários."),
    ]

    with app.app_context():
        try:
            created = False
            for name, slug, description in defaults:
                if not Group.query.filter_by(slug=slug).first():
                    db.session.add(
                        Group(name=name, slug=slugify(slug), description=description)
                    )
                    created = True
            if created:
                db.session.commit()
        except OperationalError:
            # Banco ainda não migrado; ignora seed inicial.
            db.session.rollback()
