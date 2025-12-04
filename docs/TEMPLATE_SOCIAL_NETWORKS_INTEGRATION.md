# 🔗 Integração Templates - Redes Sociais

**Data:** 3 de Dezembro, 2025  
**Versão:** 3.7.0  
**Status:** ✅ IMPLEMENTADO

---

## 🎯 O que foi implementado?

Sistema completo de associação entre **Templates** e **Redes Sociais**, substituindo o campo de texto "channels" por uma seleção de checkboxes das redes cadastradas em `/admin/social-networks`.

---

## 📋 Mudanças Principais

### 1. Templates ➔ Seleção de Redes Sociais ✅

**Antes:**
- Campo de texto: `instagram, facebook, whatsapp`
- Manual, propenso a erros de digitação

**Agora:**
- Checkboxes visuais com ícones coloridos
- Somente redes cadastradas em `/admin/social-networks`
- Associação many-to-many no banco de dados

---

### 2. Admin Social Networks ➔ CRUD Completo ✅

**Antes:**
- Apenas edição das 4 redes fixas
- Não havia como adicionar ou remover

**Agora:**
- ✅ **Criar** novas redes sociais
- ✅ **Editar** configurações existentes
- ✅ **Deletar** redes sociais

---

## 🗃️ Estrutura de Banco de Dados

### Nova Tabela de Associação

```sql
CREATE TABLE template_social_networks (
    template_id INTEGER NOT NULL,
    social_network_id INTEGER NOT NULL,
    PRIMARY KEY (template_id, social_network_id),
    FOREIGN KEY (template_id) REFERENCES templates(id) ON DELETE CASCADE,
    FOREIGN KEY (social_network_id) REFERENCES social_network_configs(id) ON DELETE CASCADE
);
```

**Tipo:** Many-to-Many (um template pode ter várias redes, uma rede pode estar em vários templates)

---

## 💻 Implementação Técnica

### 1. Model (SQLAlchemy)

```python
# Association table
template_social_networks = db.Table('template_social_networks',
    db.Column('template_id', db.Integer, db.ForeignKey('templates.id'), primary_key=True),
    db.Column('social_network_id', db.Integer, db.ForeignKey('social_network_configs.id'), primary_key=True)
)

class Template(TimestampMixin, db.Model):
    # ... outros campos ...
    
    # Relationship to social networks
    social_networks = db.relationship('SocialNetworkConfig', 
                                     secondary=template_social_networks,
                                     backref=db.backref('templates', lazy='dynamic'))
    
    @property
    def channel_list(self) -> list[str]:
        # Return social networks if available, otherwise fall back to channels
        if self.social_networks:
            return [sn.network for sn in self.social_networks]
        return [channel.strip() for channel in self.channels.split(",") if channel.strip()]
```

---

### 2. Rotas

#### Criar Template
```python
@web_bp.route("/templates/novo", methods=["GET", "POST"])
def create_template():
    # Get all social networks
    social_configs = SocialNetworkConfig.query.order_by(SocialNetworkConfig.network).all()
    
    if request.method == "POST":
        # Get selected social networks from form
        selected_network_ids = request.form.getlist('social_networks')
        if selected_network_ids:
            selected_networks = SocialNetworkConfig.query.filter(
                SocialNetworkConfig.id.in_(selected_network_ids)
            ).all()
            template.social_networks = selected_networks
        # ...
```

#### Editar Template
```python
@web_bp.route("/templates/<int:template_id>/editar", methods=["GET", "POST"])
def edit_template(template_id):
    # Get all social networks
    social_configs = SocialNetworkConfig.query.order_by(SocialNetworkConfig.network).all()
    
    if request.method == "POST":
        # Update selected social networks
        selected_network_ids = request.form.getlist('social_networks')
        if selected_network_ids:
            selected_networks = SocialNetworkConfig.query.filter(
                SocialNetworkConfig.id.in_(selected_network_ids)
            ).all()
            template.social_networks = selected_networks
        else:
            template.social_networks = []
        # ...
```

#### Admin Social Networks (CRUD)
```python
@web_bp.route("/admin/social-networks", methods=["GET", "POST"])
def admin_social_networks():
    configs = SocialNetworkConfig.query.all()
    form = SocialNetworkConfigForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            # Create new
            new_config = SocialNetworkConfig(
                network=form.network.data.lower(),
                prefix_text=form.prefix_text.data or '',
                suffix_text=form.suffix_text.data or '',
                active=form.active.data
            )
            db.session.add(new_config)
            db.session.commit()
            # ...

@web_bp.route("/admin/social-networks/<int:config_id>/delete", methods=["POST"])
def admin_social_network_delete(config_id):
    config = SocialNetworkConfig.query.get_or_404(config_id)
    db.session.delete(config)
    db.session.commit()
    # ...
```

---

### 3. Templates HTML

#### Criar/Editar Template

**Antes:**
```html
<input type="text" name="channels" placeholder="instagram, facebook, whatsapp">
```

**Agora:**
```html
<div class="row g-3">
  {% for config in social_configs %}
  <div class="col-md-6">
    <div class="form-check">
      <input class="form-check-input" 
             type="checkbox" 
             name="social_networks" 
             value="{{ config.id }}" 
             id="social_{{ config.id }}"
             {% if config.id in selected_network_ids %}checked{% endif %}>
      <label class="form-check-label" for="social_{{ config.id }}">
        {% if config.network == 'instagram' %}
        <i class="bi bi-instagram text-danger"></i> Instagram
        {% elif config.network == 'facebook' %}
        <i class="bi bi-facebook text-primary"></i> Facebook
        {% endif %}
      </label>
    </div>
  </div>
  {% endfor %}
</div>
```

#### Admin Social Networks

**Novo: Botão para criar**
```html
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#newSocialNetworkModal">
  <i class="bi bi-plus-circle"></i> Nova Rede Social
</button>
```

**Novo: Botão para deletar**
```html
<form method="POST" action="{{ url_for('web.admin_social_network_delete', config_id=config.id) }}" 
      onsubmit="return confirm('Tem certeza que deseja deletar?')">
  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
  <button type="submit" class="btn btn-sm btn-outline-danger">
    <i class="bi bi-trash"></i> Deletar
  </button>
</form>
```

**Novo: Modal para criar**
```html
<div class="modal fade" id="newSocialNetworkModal">
  <form method="POST">
    {{ form.hidden_tag() }}
    <input type="text" name="network" placeholder="twitter, linkedin, tiktok">
    <textarea name="prefix_text"></textarea>
    <textarea name="suffix_text"></textarea>
    <input type="checkbox" name="active">
    <button type="submit">Adicionar</button>
  </form>
</div>
```

#### Listagem de Templates

**Antes:**
```html
{% for channel in template.channel_list %}
<span class="tag">{{ channel }}</span>
{% endfor %}
```

**Agora:**
```html
{% if template.social_networks %}
  {% for network in template.social_networks %}
  <span class="tag">
    <i class="bi bi-instagram text-danger"></i>
    {{ network.network.title() }}
  </span>
  {% endfor %}
{% else %}
  <span class="tag text-muted">
    <i class="bi bi-exclamation-triangle"></i> Nenhuma rede selecionada
  </span>
{% endif %}
```

---

## 📂 Arquivos Modificados

### Backend

```
app/models.py
  ✅ Adicionada tabela template_social_networks
  ✅ Adicionado relacionamento em Template.social_networks
  ✅ Atualizado Template.channel_list() para usar social_networks

app/forms.py
  ✅ Removido readonly do campo network em SocialNetworkConfigForm

app/routes/web.py
  ✅ create_template(): Adicionar social_configs e processar seleções
  ✅ edit_template(): Adicionar social_configs e atualizar seleções
  ✅ admin_social_networks(): Adicionar lógica de criação
  ✅ admin_social_network_delete(): Nova rota para deletar
```

### Frontend

```
app/templates/template_create.html
  ✅ Substituído campo text por checkboxes de social_configs

app/templates/template_edit.html
  ✅ Substituído campo text por checkboxes de social_configs
  ✅ Adicionado marcação automática das redes já selecionadas

app/templates/templates_list.html
  ✅ Atualizado para mostrar social_networks ao invés de channel_list

app/templates/admin/social_networks.html
  ✅ Adicionado botão "Nova Rede Social"
  ✅ Adicionado modal para criar nova rede
  ✅ Adicionado botão "Deletar" em cada card
```

### Banco de Dados

```
scripts/add_template_social_networks.sql
  ✅ Script SQL para criar tabela de associação

instance/app.db
  ✅ Tabela template_social_networks criada
```

---

## 🎨 Interface do Usuário

### 1. Criar/Editar Template

**Seção "Redes Sociais":**
```
┌─────────────────────────────────────────┐
│ 🔊 Redes Sociais                        │
├─────────────────────────────────────────┤
│ ℹ️ Selecione as redes sociais onde     │
│    este template poderá ser usado       │
│                                          │
│ ☐ 📷 Instagram   ☐ 📘 Facebook          │
│ ☐ 💬 WhatsApp    ☐ ✈️ Telegram          │
│ ☐ 🐦 Twitter     ☐ 💼 LinkedIn          │
└─────────────────────────────────────────┘
```

### 2. Listagem de Templates

**Card de Template:**
```
┌─────────────────────────────────────────┐
│ 📄 Nome do Template          [3 redes]  │
│                                          │
│ 🔊 REDES SOCIAIS                        │
│ [📷 Instagram] [💬 WhatsApp] [✈️ Telegram] │
│                                          │
│ [✏️ Editar] [🗑️ Deletar]                 │
└─────────────────────────────────────────┘
```

### 3. Admin Social Networks

**Topo da Página:**
```
┌─────────────────────────────────────────┐
│ 🔊 Redes Sociais                        │
│ Configuração de Compartilhamento        │
│                                          │
│            [➕ Nova Rede Social] [⬅ Voltar] │
└─────────────────────────────────────────┘
```

**Card de Rede:**
```
┌─────────────────────────────────────────┐
│ 📷 Instagram                [✓ Ativa]   │
│                                          │
│ ⬆️ Texto Inicial:                       │
│ [_____________________________]         │
│                                          │
│ ⬇️ Texto Final / Hashtags:              │
│ [#ofertas #descontos #promoção]         │
│                                          │
│ [🗑️ Deletar]           [💾 Salvar]      │
└─────────────────────────────────────────┘
```

---

## 🔄 Fluxo de Uso

### Cenário 1: Criar Nova Rede Social

```
1. Admin acessa /admin/social-networks
2. Clica em "Nova Rede Social"
3. Modal abre
4. Preenche:
   - Nome: "twitter"
   - Texto Inicial: "🐦 NOVO POST!\n\n"
   - Texto Final: "#ofertas #twitter"
   - Ativa: ☑
5. Clica em "Adicionar"
6. Rede aparece na lista
7. Agora está disponível ao criar templates
```

### Cenário 2: Criar Template com Redes Específicas

```
1. Usuário acessa /templates/novo
2. Preenche nome, slug, descrição e corpo
3. Na seção "Redes Sociais":
   ☑ Instagram
   ☐ Facebook
   ☑ WhatsApp
   ☐ Telegram
   ☑ Twitter
4. Clica em "Salvar template"
5. Template criado com 3 redes associadas
6. Ao listar, mostra: [Instagram] [WhatsApp] [Twitter]
```

### Cenário 3: Editar Redes de um Template

```
1. Usuário acessa /templates/4/editar
2. Vê checkboxes:
   ☑ Instagram (já marcado)
   ☐ Facebook
   ☑ WhatsApp (já marcado)
   ☐ Telegram
3. Desmarca Instagram
4. Marca Facebook
5. Clica em "Atualizar Template"
6. Agora tem: [Facebook] [WhatsApp]
```

### Cenário 4: Deletar Rede Social

```
1. Admin acessa /admin/social-networks
2. Vê card do Twitter
3. Clica em "Deletar"
4. Confirma: "Tem certeza? Todos os templates perderão esta associação."
5. Clica em "OK"
6. Rede deletada
7. Todos os templates que tinham Twitter perdem essa associação automaticamente (CASCADE)
```

---

## ⚠️ Comportamento de Deleção

**Quando uma rede social é deletada:**

```sql
ON DELETE CASCADE
```

- ✅ A rede é removida de `social_network_configs`
- ✅ Todas as associações em `template_social_networks` são removidas automaticamente
- ✅ Os templates continuam existindo, apenas perdem aquela rede
- ✅ Os textos (prefix/suffix) são perdidos permanentemente

**Exemplo:**
```
Template "Oferta Black Friday" tinha:
- Instagram
- Facebook
- Twitter

Deletei Twitter →

Template "Oferta Black Friday" agora tem:
- Instagram
- Facebook
```

---

## 🆕 Compatibilidade com Código Antigo

O campo `channels` foi mantido por compatibilidade:

```python
@property
def channel_list(self) -> list[str]:
    # Return social networks if available, otherwise fall back to channels
    if self.social_networks:
        return [sn.network for sn in self.social_networks]
    return [channel.strip() for channel in self.channels.split(",") if channel.strip()]
```

**Comportamento:**
- Templates novos: usam `social_networks`
- Templates antigos sem redes associadas: usam `channels` (texto)
- Ao editar template antigo e selecionar redes: passa a usar `social_networks`

---

## 🧪 Testes

### Teste 1: Criar Nova Rede Social
```
1. Acesse /admin/social-networks
2. Clique em "Nova Rede Social"
3. Preencha: network="linkedin", prefix="💼", suffix="#networking"
4. Clique em "Adicionar"
5. Verifique que LinkedIn aparece na lista ✅
```

### Teste 2: Criar Template com Redes
```
1. Acesse /templates/novo
2. Preencha os campos
3. Marque Instagram e WhatsApp
4. Salve
5. Vá para /templates
6. Verifique que mostra [Instagram] [WhatsApp] ✅
```

### Teste 3: Editar Redes de Template
```
1. Acesse /templates/4/editar
2. Veja quais estão marcadas
3. Mude as seleções
4. Salve
5. Vá para /templates
6. Verifique que as redes foram atualizadas ✅
```

### Teste 4: Deletar Rede Social
```
1. Acesse /admin/social-networks
2. Clique em "Deletar" no LinkedIn
3. Confirme
4. Vá para /templates/novo
5. Verifique que LinkedIn não aparece mais ✅
```

---

## ✅ Checklist de Implementação

- [x] Criar tabela de associação `template_social_networks`
- [x] Adicionar relacionamento em model `Template`
- [x] Atualizar `Template.channel_list()` para usar social_networks
- [x] Remover readonly do campo network em form
- [x] Atualizar rota `create_template()` para processar seleções
- [x] Atualizar rota `edit_template()` para atualizar seleções
- [x] Adicionar lógica de criação em `admin_social_networks()`
- [x] Criar rota `admin_social_network_delete()`
- [x] Substituir campo text por checkboxes em template_create.html
- [x] Substituir campo text por checkboxes em template_edit.html
- [x] Adicionar marcação automática das redes já selecionadas
- [x] Atualizar templates_list.html para mostrar social_networks
- [x] Adicionar botão "Nova Rede Social"
- [x] Adicionar modal para criar nova rede
- [x] Adicionar botão "Deletar" em cada card
- [x] Aplicar migration SQL
- [x] Testar criação de rede social
- [x] Testar criação de template com redes
- [x] Testar edição de redes de template
- [x] Testar deleção de rede social

---

## 🎊 Status Final

**✅ 100% IMPLEMENTADO E FUNCIONAL!**

### O que está funcionando:
- ✅ Relacionamento many-to-many entre Templates e Redes Sociais
- ✅ Seleção visual de redes ao criar/editar templates
- ✅ Criação de novas redes sociais em /admin/social-networks
- ✅ Deleção de redes sociais existentes
- ✅ Listagem de templates mostrando redes associadas
- ✅ Compatibilidade com templates antigos
- ✅ Cascata automática ao deletar redes

---

**Sistema completo de integração entre Templates e Redes Sociais implementado! 🎉**

