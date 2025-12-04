from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DecimalField,
    FileField,
    HiddenField,
    IntegerField,
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
    
    # Contact information
    phone = StringField("Celular", validators=[Optional(), Length(max=20)])
    address = StringField("Endereço", validators=[Optional(), Length(max=255)])
    website = StringField("Website", validators=[Optional(), Length(max=255)])
    
    # Social media
    instagram = StringField("Instagram", validators=[Optional(), Length(max=255)])
    facebook = StringField("Facebook", validators=[Optional(), Length(max=255)])
    twitter = StringField("Twitter/X", validators=[Optional(), Length(max=255)])
    linkedin = StringField("LinkedIn", validators=[Optional(), Length(max=255)])
    youtube = StringField("YouTube", validators=[Optional(), Length(max=255)])
    tiktok = StringField("TikTok", validators=[Optional(), Length(max=255)])
    
    submit_user = SubmitField("Cadastrar usuário")


class UserEditForm(FlaskForm):
    display_name = StringField("Nome exibido", validators=[DataRequired(), Length(max=120)])
    email = StringField("E-mail", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Nova senha", validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField("Confirmar nova senha", validators=[Optional(), Length(min=6)])
    role = SelectField(
        "Papel",
        choices=[
            ("member", "Membro"),
            ("editor", "Editor"),
            ("admin", "Administrador"),
        ],
        validators=[DataRequired()],
    )
    
    # Contact information
    phone = StringField("Celular", validators=[Optional(), Length(max=20)])
    address = StringField("Endereço", validators=[Optional(), Length(max=255)])
    website = StringField("Website", validators=[Optional(), Length(max=255)])
    
    # Social media
    instagram = StringField("Instagram", validators=[Optional(), Length(max=255)])
    facebook = StringField("Facebook", validators=[Optional(), Length(max=255)])
    twitter = StringField("Twitter/X", validators=[Optional(), Length(max=255)])
    linkedin = StringField("LinkedIn", validators=[Optional(), Length(max=255)])
    youtube = StringField("YouTube", validators=[Optional(), Length(max=255)])
    tiktok = StringField("TikTok", validators=[Optional(), Length(max=255)])
    
    submit = SubmitField("Salvar alterações")


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
    product_image = FileField("Imagem do produto", validators=[Optional()])
    seller_id = SelectField("Vendedor", coerce=int, validators=[Optional()])
    category_id = SelectField("Categoria", coerce=int, validators=[Optional()])
    manufacturer_id = SelectField("Fabricante", coerce=int, validators=[Optional()])
    vendor_name = StringField("Nome do vendedor (legado)", validators=[Optional(), Length(max=120)])
    price = DecimalField("Preço", validators=[DataRequired(), NumberRange(min=0)], places=2)
    old_price = DecimalField("Preço antigo", validators=[Optional(), NumberRange(min=0)], places=2)
    currency = SelectField("Moeda", validators=[DataRequired()], 
                          choices=[
                              ('BRL', 'R$ - Real Brasileiro'),
                              ('USD', '$ - Dólar Americano'),
                              ('EUR', '€ - Euro'),
                              ('GBP', '£ - Libra Esterlina'),
                              ('JPY', '¥ - Iene Japonês'),
                              ('CAD', 'CA$ - Dólar Canadense'),
                              ('AUD', 'AU$ - Dólar Australiano'),
                              ('CHF', 'CHF - Franco Suíço'),
                              ('CNY', '¥ - Yuan Chinês'),
                              ('ARS', 'ARS$ - Peso Argentino'),
                              ('MXN', 'MX$ - Peso Mexicano'),
                              ('CLP', 'CLP$ - Peso Chileno'),
                          ],
                          default='BRL')
    offer_url = StringField("URL da oferta", validators=[Optional(), Length(max=255)])
    expires_date = DateField("Data de expiração", validators=[Optional()], format='%Y-%m-%d')
    expires_time = TimeField("Hora de expiração", validators=[Optional()], format='%H:%M')
    
    # Installment fields
    installment_count = IntegerField("Quantidade de parcelas", validators=[Optional(), NumberRange(min=1, max=99)])
    installment_value = DecimalField("Valor da parcela", validators=[Optional(), NumberRange(min=0)], places=2)
    installment_interest_free = BooleanField("Sem juros", default=True)
    
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
    color = StringField("Cor do vendedor", validators=[Optional(), Length(max=255)], default='#6b7280')
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
    discount_type = SelectField("Tipo de desconto", 
                               choices=[('percentage', 'Porcentagem (%)'), ('fixed', 'Valor fixo (R$)')],
                               default='percentage',
                               validators=[Optional()])
    discount_value = DecimalField("Valor do desconto", validators=[Optional(), NumberRange(min=0)], places=2)
    min_purchase_value = DecimalField("Valor mínimo da compra (R$)", validators=[Optional(), NumberRange(min=0)], places=2)
    max_discount_value = DecimalField("Desconto máximo (R$)", validators=[Optional(), NumberRange(min=0)], places=2)
    submit = SubmitField("Salvar cupom")


class SocialNetworkConfigForm(FlaskForm):
    network = StringField("Rede Social", validators=[DataRequired(), Length(max=50)])
    color = StringField("Cor do Botão", validators=[Optional(), Length(max=200)],
                       render_kw={'type': 'text', 'placeholder': '#1877f2 ou linear-gradient(...)'})
    prefix_text = TextAreaField("Texto Inicial", validators=[Optional()], 
                                 render_kw={'rows': 3, 'placeholder': 'Texto que aparece antes do conteúdo do template'})
    suffix_text = TextAreaField("Texto Final / Hashtags", validators=[Optional()],
                                render_kw={'rows': 3, 'placeholder': 'Texto que aparece depois do conteúdo (ex: hashtags)'})
    active = BooleanField("Ativa", default=True)
    submit = SubmitField("Salvar configuração")

