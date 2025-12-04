# ✏️ Edição de Perfil de Usuário

## 📋 Visão Geral

Sistema completo de edição de perfis de usuários, permitindo que qualquer usuário edite seu próprio perfil e administradores editem qualquer perfil. Inclui atualização de senha, informações de contato e redes sociais.

---

## 🎯 Funcionalidades

### 1. **Página Dedicada de Edição**
- Rota: `/usuarios/<id>/editar`
- Template: `user_edit.html`
- Layout consistente com outras páginas de edição do projeto

### 2. **Permissões**
- ✅ **Usuário**: Pode editar seu **próprio** perfil
- ✅ **Admin**: Pode editar **qualquer** perfil
- ✅ **Admin**: Pode alterar o papel (role) de outros usuários
- ⚠️ **Usuário comum**: Não pode alterar seu próprio papel

### 3. **Campos Editáveis**

#### Informações Básicas
- Nome Exibido *
- E-mail *
- Papel (apenas admins podem alterar)

#### Alteração de Senha (Opcional)
- Nova Senha (mínimo 6 caracteres)
- Confirmar Nova Senha
- ⚠️ Deixar em branco para não alterar a senha

#### Informações de Contato
- Celular (namespace: `{celular}`)
- Endereço (namespace: `{endereco}`)
- Website (namespace: `{site}`)

#### Redes Sociais
- Instagram (namespace: `{instagram}`)
- Facebook (namespace: `{facebook}`)
- Twitter/X (namespace: `{twitter}`)
- LinkedIn (namespace: `{linkedin}`)
- YouTube (namespace: `{youtube}`)
- TikTok (namespace: `{tiktok}`)

---

## 🖥️ Interface

### Botões de Acesso

#### Na Listagem de Usuários (`/usuarios`)

**Para o próprio usuário:**
```html
<a href="/usuarios/1/editar" class="btn btn-primary btn-sm">
  <i class="bi bi-pencil-square"></i> Editar Meu Perfil
</a>
```

**Para administradores (em outros perfis):**
```html
<a href="/usuarios/2/editar" class="btn btn-outline-primary btn-sm">
  <i class="bi bi-pencil-square"></i> Editar
</a>
```

### Página de Edição

**Estrutura:**
1. **Cabeçalho**: Nome do usuário e botão "Voltar para Lista"
2. **Seção 1**: Informações Básicas (nome, e-mail, papel)
3. **Seção 2**: Alterar Senha (opcional)
4. **Seção 3**: Informações de Contato
5. **Seção 4**: Redes Sociais
6. **Rodapé**: Botões "Cancelar" e "Salvar Alterações"

---

## 🔧 Implementação Técnica

### Formulário (`UserEditForm`)

**Arquivo:** `app/forms.py`

```python
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
```

**Diferenças do `UserCreateForm`:**
- ✅ Senha é **opcional** (só atualiza se preenchida)
- ✅ Inclui campo de confirmação de senha
- ✅ Label "Nova senha" em vez de "Senha inicial"
- ✅ Submit button: "Salvar alterações" em vez de "Cadastrar usuário"

---

### Rota (`edit_user`)

**Arquivo:** `app/routes/web.py`

```python
@web_bp.route("/usuarios/<int:user_id>/editar", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    """Edit user page"""
    user = User.query.get_or_404(user_id)
    
    # Permission check: user can edit own profile, or admin can edit any
    if current_user.id != user.id and current_user.role != RoleEnum.ADMIN:
        flash("Você não tem permissão para editar este usuário.", "danger")
        return redirect(url_for("web.users"))
    
    from ..forms import UserEditForm
    form = UserEditForm(obj=user)
    
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
        
        # Only admin can change role
        if current_user.role == RoleEnum.ADMIN:
            user.role = RoleEnum(form.role.data)
        
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
        
        db.session.commit()
        flash(f"Usuário '{user.display_name}' atualizado com sucesso!", "success")
        return redirect(url_for("web.users"))
    
    return render_template("user_edit.html", form=form, user=user)
```

**Lógica de Segurança:**
1. ✅ Verifica se o usuário tem permissão (próprio perfil ou admin)
2. ✅ Valida e-mail único (exceto o próprio e-mail do usuário)
3. ✅ Valida confirmação de senha
4. ✅ Apenas admin pode alterar `role`
5. ✅ Campos vazios são salvos como `None` (não string vazia)

---

### Template (`user_edit.html`)

**Arquivo:** `app/templates/user_edit.html`

**Características:**
- ✅ Extends `base.html`
- ✅ Layout responsivo com Bootstrap grid (`col-md-6`, `col-12`)
- ✅ Seções organizadas com separadores visuais
- ✅ Ícones do Bootstrap Icons para cada campo
- ✅ Hints de namespaces globais nos campos de contato/redes sociais
- ✅ Campo `role` desabilitado para não-admins
- ✅ Botões "Cancelar" e "Salvar Alterações" no rodapé

**Exemplo de Campo:**
```html
<div class="col-md-6">
  <label class="form-label" for="{{ form.phone.id }}">
    <i class="bi bi-phone"></i> Celular
  </label>
  {{ form.phone(class="form-control", placeholder="(11) 98765-4321") }}
  <small class="text-muted">
    <i class="bi bi-info-circle"></i> Usado em namespaces globais: <code>{celular}</code>
  </small>
</div>
```

---

## ✅ Validações

### 1. E-mail Único
```python
if form.email.data != user.email:
    existing = User.query.filter_by(email=form.email.data).first()
    if existing:
        flash("E-mail já em uso por outro usuário.", "warning")
```

### 2. Confirmação de Senha
```python
if form.password.data:
    if form.password.data != form.confirm_password.data:
        flash("As senhas não coincidem.", "warning")
```

### 3. Permissões de Acesso
```python
if current_user.id != user.id and current_user.role != RoleEnum.ADMIN:
    flash("Você não tem permissão para editar este usuário.", "danger")
    return redirect(url_for("web.users"))
```

### 4. Alteração de Papel (Role)
```python
# Only admin can change role
if current_user.role == RoleEnum.ADMIN:
    user.role = RoleEnum(form.role.data)
```

---

## 🎨 Experiência do Usuário

### Fluxo de Edição (Usuário Comum)

1. **Acessar `/usuarios`**
2. **Ver seu próprio card** com botão "Editar Meu Perfil"
3. **Clicar no botão** → Redireciona para `/usuarios/1/editar`
4. **Preencher formulário**:
   - Atualizar nome, e-mail
   - Opcionalmente alterar senha
   - Adicionar/editar contato e redes sociais
5. **Clicar "Salvar Alterações"**
6. **Ver notificação** de sucesso (Toast do Bootstrap)
7. **Retornar automaticamente** para `/usuarios`

### Fluxo de Edição (Administrador)

1. **Acessar `/usuarios`**
2. **Ver card de qualquer usuário** com botão "Editar"
3. **Clicar no botão** → Redireciona para `/usuarios/<id>/editar`
4. **Ter acesso total**:
   - Alterar nome, e-mail
   - Redefinir senha
   - **Alterar papel** (member/editor/admin)
   - Editar contato e redes sociais
5. **Clicar "Salvar Alterações"**
6. **Ver notificação** de sucesso
7. **Retornar automaticamente** para `/usuarios`

---

## 🔒 Segurança

### Proteção Implementada

1. ✅ **Login Required**: Apenas usuários autenticados podem acessar
2. ✅ **Permissão de Edição**: Verifica se é próprio perfil ou admin
3. ✅ **E-mail Único**: Impede duplicatas no sistema
4. ✅ **Hash de Senha**: Senhas sempre criptografadas com `generate_password_hash`
5. ✅ **Proteção de Papel**: Usuários comuns não podem auto-promover
6. ✅ **CSRF Token**: Proteção contra ataques CSRF via Flask-WTF
7. ✅ **Validação de Campos**: WTForms valida comprimentos e formatos

### Hierarquia de Permissões

| Ação | Membro | Editor | Admin |
|------|--------|--------|-------|
| Ver listagem | ✅ | ✅ | ✅ |
| Editar próprio perfil | ✅ | ✅ | ✅ |
| Alterar próprio papel | ❌ | ❌ | ❌ |
| Editar outros perfis | ❌ | ❌ | ✅ |
| Alterar papéis | ❌ | ❌ | ✅ |
| Resetar senhas | ❌ | ❌ | ✅ |
| Deletar usuários | ❌ | ❌ | ✅ |

---

## 📱 Responsividade

O template utiliza classes Bootstrap para garantir boa experiência em todos os dispositivos:

- **Desktop**: Campos em 2 colunas (`col-md-6`)
- **Tablet**: Campos em 2 colunas (`col-md-6`)
- **Mobile**: Campos em 1 coluna (automático com Bootstrap)

---

## 🎯 Casos de Uso

### 1. Usuário Atualiza Telefone
Um usuário divulgador adiciona seu número de WhatsApp no campo "Celular". Todos os templates que usam `{celular}` agora mostram seu número automaticamente.

### 2. Admin Promove Usuário
Um administrador acessa o perfil de um membro ativo e altera o papel de "Membro" para "Editor", dando-lhe permissões de gerenciamento.

### 3. Usuário Redefine Senha
Um usuário que esqueceu sua senha antiga pode redefini-la preenchendo os campos "Nova Senha" e "Confirmar Nova Senha".

### 4. Influenciador Adiciona Redes Sociais
Um influenciador preenche todos os campos de redes sociais. Templates passam a incluir automaticamente seus perfis usando namespaces como `{instagram}`, `{youtube}`, etc.

---

## 📚 Documentação Relacionada

- [USER_PROFILE_FEATURE.md](USER_PROFILE_FEATURE.md) - Cadastro de usuários
- [README.md](../README.md) - Documentação principal
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Referência rápida

---

**Última Atualização:** 04/12/2025  
**Versão:** 1.0  
**Status:** ✅ Completo e Funcional

