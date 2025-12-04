from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DecimalField,
    HiddenField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.fields import DateField, TimeField
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
    seller_id = SelectField("Vendedor", coerce=int, validators=[Optional()])
    category_id = SelectField("Categoria", coerce=int, validators=[Optional()])
    manufacturer_id = SelectField("Fabricante", coerce=int, validators=[Optional()])
    vendor_name = StringField("Nome do vendedor (legado)", validators=[Optional(), Length(max=120)])
    price = DecimalField("Preço", validators=[DataRequired(), NumberRange(min=0)], places=2)
    old_price = DecimalField("Preço antigo", validators=[Optional(), NumberRange(min=0)], places=2)
    currency = SelectField("Moeda", validators=[DataRequired()], 
                          choices=[
                              ('BRL', 'BRL - Real Brasileiro'),
                              ('USD', 'USD - Dólar Americano'),
                              ('EUR', 'EUR - Euro'),
                              ('GBP', 'GBP - Libra Esterlina'),
                              ('JPY', 'JPY - Iene Japonês'),
                              ('CAD', 'CAD - Dólar Canadense'),
                              ('AUD', 'AUD - Dólar Australiano'),
                              ('CHF', 'CHF - Franco Suíço'),
                              ('CNY', 'CNY - Yuan Chinês'),
                              ('ARS', 'ARS - Peso Argentino'),
                              ('MXN', 'MXN - Peso Mexicano'),
                              ('CLP', 'CLP - Peso Chileno'),
                          ],
                          default='BRL')
    offer_url = StringField("URL da oferta", validators=[Optional(), Length(max=255)])
    expires_date = DateField("Data de expiração", validators=[Optional()], format='%Y-%m-%d')
    expires_time = TimeField("Hora de expiração", validators=[Optional()], format='%H:%M')
    submit_offer = SubmitField("Publicar oferta")


class TemplateCreateForm(FlaskForm):
    name = StringField("Nome do template", validators=[DataRequired(), Length(max=120)])
    slug = StringField("Slug", validators=[DataRequired(), Length(max=120)])
    description = TextAreaField("Descrição", validators=[Optional(), Length(max=255)])
    body = TextAreaField("Corpo do template", validators=[DataRequired()])
    channels = StringField("Canais (separados por vírgula)", default="instagram,facebook,whatsapp,telegram")
    submit_template = SubmitField("Salvar template")


class SellerForm(FlaskForm):
    name = StringField("Nome do vendedor", validators=[DataRequired(), Length(max=120)])
    slug = StringField("Slug", validators=[DataRequired(), Length(max=120)])
    description = TextAreaField("Descrição", validators=[Optional()])
    website = StringField("Website", validators=[Optional(), Length(max=255)])
    active = BooleanField("Ativo", default=True)
    submit = SubmitField("Salvar vendedor")


class CategoryForm(FlaskForm):
    name = StringField("Nome da categoria", validators=[DataRequired(), Length(max=120)])
    slug = StringField("Slug", validators=[DataRequired(), Length(max=120)])
    description = TextAreaField("Descrição", validators=[Optional()])
    icon = StringField("Ícone (classe Bootstrap Icons)", validators=[Optional(), Length(max=50)])
    active = BooleanField("Ativa", default=True)
    submit = SubmitField("Salvar categoria")


class ManufacturerForm(FlaskForm):
    name = StringField("Nome do fabricante", validators=[DataRequired(), Length(max=120)])
    slug = StringField("Slug", validators=[DataRequired(), Length(max=120)])
    description = TextAreaField("Descrição", validators=[Optional()])
    website = StringField("Website", validators=[Optional(), Length(max=255)])
    logo = StringField("URL do logo", validators=[Optional(), Length(max=255)])
    active = BooleanField("Ativo", default=True)
    submit = SubmitField("Salvar fabricante")


class CouponForm(FlaskForm):
    seller_id = SelectField("Vendedor", coerce=int, validators=[DataRequired()])
    code = StringField("Código do cupom", validators=[DataRequired(), Length(max=120)])
    active = BooleanField("Ativo", default=True)
    expires_date = DateField("Data de expiração", validators=[Optional()], format='%Y-%m-%d')
    expires_time = TimeField("Hora de expiração", validators=[Optional()], format='%H:%M')
    submit = SubmitField("Salvar cupom")


class SocialNetworkConfigForm(FlaskForm):
    network = StringField("Rede Social", validators=[DataRequired(), Length(max=50)])
    prefix_text = TextAreaField("Texto Inicial", validators=[Optional()], 
                                 render_kw={'rows': 3, 'placeholder': 'Texto que aparece antes do conteúdo do template'})
    suffix_text = TextAreaField("Texto Final / Hashtags", validators=[Optional()],
                                render_kw={'rows': 3, 'placeholder': 'Texto que aparece depois do conteúdo (ex: hashtags)'})
    active = BooleanField("Ativa", default=True)
    submit = SubmitField("Salvar configuração")

