from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    DecimalField,
    HiddenField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


class UserActionForm(FlaskForm):
    user_id = HiddenField(validators=[DataRequired()])
    action = HiddenField(validators=[DataRequired()])


class UserCreateForm(FlaskForm):
    display_name = StringField("Nome exibido", validators=[DataRequired(), Length(max=120)])
    email = StringField("E-mail", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Senha inicial", validators=[DataRequired(), Length(min=6)])
    role = SelectField(
        "Papel",
        choices=[
            ("member", "Membro"),
            ("editor", "Editor"),
            ("admin", "Administrador"),
        ],
        default="member",
        validators=[DataRequired()],
    )
    submit_user = SubmitField("Cadastrar usuário")


class GroupCreateForm(FlaskForm):
    name = StringField("Nome do grupo", validators=[DataRequired(), Length(max=120)])
    slug = StringField("Slug", validators=[Length(max=120)])
    description = TextAreaField("Descrição", validators=[Length(max=255)])
    submit_group = SubmitField("Criar grupo")


class GroupMemberForm(FlaskForm):
    group_id = HiddenField(validators=[DataRequired()])
    user_id = HiddenField(validators=[DataRequired()])
    action = HiddenField(validators=[DataRequired()])


class OfferCreateForm(FlaskForm):
    product_name = StringField("Nome do produto", validators=[DataRequired(), Length(max=200)])
    product_slug = StringField("Slug do produto", validators=[DataRequired(), Length(max=200)])
    product_description = TextAreaField("Descrição do produto", validators=[Optional(), Length(max=500)])
    category = StringField("Categoria", validators=[Optional(), Length(max=120)])
    manufacturer = StringField("Fabricante", validators=[Optional(), Length(max=120)])
    vendor_name = StringField("Vendedor", validators=[DataRequired(), Length(max=120)])
    price = DecimalField("Preço", validators=[DataRequired(), NumberRange(min=0)], places=2)
    currency = StringField("Moeda", default="BRL", validators=[DataRequired(), Length(max=3)])
    offer_url = StringField("URL da oferta", validators=[Optional(), Length(max=255)])
    expires_at = StringField("Expira em (ISO 8601)", validators=[Optional(), Length(max=30)])
    submit_offer = SubmitField("Publicar oferta")


class TemplateCreateForm(FlaskForm):
    name = StringField("Nome do template", validators=[DataRequired(), Length(max=120)])
    slug = StringField("Slug", validators=[DataRequired(), Length(max=120)])
    description = TextAreaField("Descrição", validators=[Optional(), Length(max=255)])
    body = TextAreaField("Corpo do template", validators=[DataRequired()])
    channels = StringField("Canais (separados por vírgula)", default="instagram,facebook,whatsapp,telegram")
    submit_template = SubmitField("Salvar template")

