from __future__ import annotations

from datetime import datetime
from secrets import token_urlsafe

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..extensions import db
from ..forms import (
    GroupCreateForm,
    GroupMemberForm,
    LoginForm,
    UserActionForm,
    UserCreateForm,
    OfferCreateForm,
    TemplateCreateForm,
)
from ..models import Group, Offer, Product, RoleEnum, Template, User, Wishlist
from ..utils import slugify

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    offers = Offer.query.order_by(Offer.created_at.desc()).limit(6).all()
    templates = Template.query.limit(4).all()
    return render_template(
        "index.html",
        offers=offers,
        templates=templates,
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
    offers = Offer.query.order_by(Offer.created_at.desc()).limit(5).all()
    wishlists = Wishlist.query.filter_by(owner_id=current_user.id).all()
    return render_template(
        "dashboard.html",
        offers=offers,
        wishlists=wishlists,
    )


@web_bp.route("/usuarios", methods=["GET", "POST"])
def users():
    role = request.args.get("role")
    query = User.query
    if role:
        try:
            query = query.filter_by(role=RoleEnum(role))
        except ValueError:
            role = None
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
    )


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


@web_bp.route("/ofertas", methods=["GET", "POST"])
def offers():
    vendor = request.args.get("vendor")
    product = request.args.get("product")
    query = Offer.query.join(Product)
    if vendor:
        query = query.filter(Offer.vendor_name.ilike(f"%{vendor}%"))
    if product:
        query = query.filter(Product.slug == product)
    offers = query.order_by(Offer.created_at.desc()).all()
    form = OfferCreateForm(prefix="offer")
    can_manage = current_user.is_authenticated and current_user.role in (RoleEnum.ADMIN, RoleEnum.EDITOR)

    if can_manage and form.submit_offer.data and form.validate_on_submit():
        slug_value = slugify(form.product_slug.data)
        product_obj = Product.query.filter_by(slug=slug_value).first()
        if not product_obj:
            product_obj = Product(
                name=form.product_name.data,
                slug=slug_value,
                description=form.product_description.data,
                category=form.category.data,
                manufacturer=form.manufacturer.data,
            )
            db.session.add(product_obj)
            db.session.flush()

        expires_at = None
        if form.expires_at.data:
            try:
                expires_at = datetime.fromisoformat(form.expires_at.data)
            except ValueError:
                flash("Formato de data inválido. Use ISO 8601 (ex: 2025-12-31T12:00).", "danger")
                return redirect(url_for("web.offers"))

        new_offer = Offer(
            product=product_obj,
            vendor_name=form.vendor_name.data,
            price=form.price.data,
            currency=form.currency.data.upper(),
            offer_url=form.offer_url.data,
            expires_at=expires_at,
            created_by=current_user if current_user.is_authenticated else None,
        )
        db.session.add(new_offer)
        db.session.commit()
        flash("Oferta criada com sucesso!", "success")
        return redirect(url_for("web.offers"))
    elif request.method == "POST" and form.submit_offer.data and not can_manage:
        flash("Apenas administradores ou editores podem criar ofertas.", "danger")
        return redirect(url_for("web.login"))

    return render_template("offers.html", offers=offers, form=form, can_manage=can_manage)


@web_bp.route("/templates", methods=["GET", "POST"])
@login_required
def share_templates():
    if current_user.role not in (RoleEnum.ADMIN, RoleEnum.EDITOR):
        flash("Acesso permitido apenas para administradores e editores.", "warning")
        return redirect(url_for("web.dashboard"))
    templates = Template.query.all()
    form = TemplateCreateForm(prefix="template")

    if form.submit_template.data and form.validate_on_submit():
        slug_value = slugify(form.slug.data)
        if Template.query.filter_by(slug=slug_value).first():
            flash("Já existe um template com esse slug.", "warning")
            return redirect(url_for("web.share_templates"))
        channels = [channel.strip() for channel in form.channels.data.split(",") if channel.strip()]
        template = Template(
            name=form.name.data,
            slug=slug_value,
            description=form.description.data,
            body=form.body.data,
            channels=",".join(channels) if channels else "instagram,facebook",
        )
        db.session.add(template)
        db.session.commit()
        flash("Template criado com sucesso!", "success")
        return redirect(url_for("web.share_templates"))

    return render_template("templates.html", templates=templates, form=form)

