# 🚀 Referência Rápida - pySaveDiário

Comandos, rotas e atalhos essenciais para uso diário do sistema.

---

## 📦 Instalação e Setup

### Instalação Inicial

```bash
# Clone e entre no diretório
git clone https://github.com/seu-usuario/pySaveDiario.git
cd pySaveDiario

# Crie ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\Activate.ps1  # Windows

# Instale dependências
pip install -r requirements.txt

# Configure ambiente
cp env.example .env
# Edite .env com suas configurações

# Inicialize banco de dados
flask --app run.py db upgrade

# Crie admin
python -m scripts.create_admin --email admin@local --display-name "Admin"

# Execute aplicação
flask --app run.py run --reload
```

### Comandos Úteis

```bash
# Gerar SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Criar novo usuário admin
python -m scripts.create_admin --email user@email.com --display-name "Nome"

# Criar usuário editor
python -m scripts.create_admin --email editor@email.com --display-name "Editor" --role editor

# Nova migração
flask --app run.py db migrate -m "descrição da mudança"

# Aplicar migrações
flask --app run.py db upgrade

# Reverter última migração
flask --app run.py db downgrade

# Resetar banco de dados
rm instance/app.db
flask --app run.py db upgrade
```

### Scripts de Setup Opcionais

```bash
# Adicionar cores aos vendedores
python scripts/add_color_to_sellers.py

# Adicionar namespaces de parcelas
python scripts/add_installment_namespaces.py

# Adicionar namespaces de descrição
python scripts/add_description_namespaces.py

# Adicionar namespaces de preço com cupom
python scripts/add_price_with_coupon_namespace.py
```

---

## 🌐 Rotas Web Principais

### Autenticação

| Rota | Descrição |
|------|-----------|
| `/` | Página inicial |
| `/login` | Login |
| `/logout` | Logout |
| `/dashboard` | Dashboard do usuário |

### Ofertas

| Rota | Descrição |
|------|-----------|
| `/ofertas` | Listagem (com filtros) |
| `/ofertas/nova` | Criar nova oferta |
| `/ofertas/<id>/editar` | Editar oferta |
| `/ofertas/<id>/compartilhar` | Compartilhar oferta |
| `/ofertas/<id>/compartilhar?channel=whatsapp` | Compartilhar pré-selecionando rede |
| `/ofertas/<id>/delete` | Deletar oferta (POST) |

### Cupons

| Rota | Descrição |
|------|-----------|
| `/cupons` | Listagem (com filtros) |
| `/cupons/novo` | Criar novo cupom |
| `/cupons/<id>/editar` | Editar cupom |
| `/cupons/<id>/delete` | Deletar cupom (POST) |
| `/cupons/<id>/toggle-active` | Ativar/desativar (POST) |

### Templates

| Rota | Descrição |
|------|-----------|
| `/templates` | Listagem (com filtros) |
| `/templates/novo` | Criar novo template |
| `/templates/<id>/editar` | Editar template |
| `/templates/<id>/delete` | Deletar template (POST) |

### Administração

| Rota | Descrição |
|------|-----------|
| `/admin` | Painel administrativo |
| `/admin/sellers` | Gerenciar vendedores |
| `/admin/sellers/<id>/editar` | Editar vendedor |
| `/admin/categories` | Gerenciar categorias |
| `/admin/categories/<id>/editar` | Editar categoria |
| `/admin/manufacturers` | Gerenciar fabricantes |
| `/admin/manufacturers/<id>/editar` | Editar fabricante |
| `/admin/social-networks` | Configurar redes sociais |
| `/admin/settings` | Configurações do sistema |

### Usuários e Grupos

| Rota | Descrição |
|------|-----------|
| `/usuarios` | Gerenciar usuários |
| `/grupos` | Gerenciar grupos |

### Documentação

| Rota | Descrição |
|------|-----------|
| `/api-docs` | Documentação interativa da API |

---

## 🔌 API REST

### Autenticação

```bash
# Obter token
curl -X POST http://localhost:5000/api/auth/token \
  -u "admin@local:senha"

# Login via JSON
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@local", "password": "senha"}'
```

### Usar Token

```bash
# Incluir em todas as requisições autenticadas
-H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### Endpoints Rápidos

```bash
# Health check
curl http://localhost:5000/api/health

# Listar vendedores
curl http://localhost:5000/api/sellers \
  -H "Authorization: Bearer TOKEN"

# Criar vendedor
curl -X POST http://localhost:5000/api/sellers \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Loja", "slug": "loja", "color": "#FF0000"}'

# Atualizar vendedor
curl -X PUT http://localhost:5000/api/sellers/1 \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Loja Nova"}'

# Deletar vendedor
curl -X DELETE http://localhost:5000/api/sellers/1 \
  -H "Authorization: Bearer TOKEN"

# Listar ofertas (com filtros)
curl "http://localhost:5000/api/offers?vendor=mercado&min_price=100"

# Listar namespaces
curl http://localhost:5000/api/namespaces \
  -H "Authorization: Bearer TOKEN"
```

---

## 🔍 Filtros nas URLs

### Ofertas (`/ofertas`)

```
?search=ps5
?seller=1
?manufacturer=2
?category=3
?min_price=100
?max_price=500
?active_only=true
```

**Exemplo completo:**
```
/ofertas?search=controle&seller=1&min_price=100&max_price=300&active_only=true
```

### Templates (`/templates`)

```
?search=promocao
?social_network=whatsapp
```

### Cupons (`/cupons`)

```
?search=DESC10         (busca por código do cupom)
?seller=1
?discount_type=percentage
?active_only=true
```

---

## 🎨 Namespaces (Variáveis)

### Produto/Oferta

```
{product_name}              - Nome do produto
{product_description}       - Descrição formatada
{price}                     - Preço com símbolo (R$ 100,00)
{old_price}                 - Preço antigo
{discount}                  - Desconto em % (-20%)
{vendor_name}               - Nome do vendedor
{seller}                    - Alias de vendor_name
{offer_url}                 - Link da oferta
{category}                  - Categoria
{manufacturer}              - Fabricante
```

### Parcelas

```
{installment_count}         - Quantidade (5)
{installment_value}         - Valor (R$ 72,00)
{installment_interest_free} - Sim/Não
{installment_full}          - "5x de R$ 72 sem juros"
{parcelamento}              - Alias de installment_full
```

### Cupons

**Identificação:**
```
{coupon_code} ou {code}              - Código (DESC10)
{coupon_seller} ou {seller}          - Vendedor (Amazon)
```

**Desconto Percentual (%):**
```
{porcentagem}                        - 10%
{percentual}                         - 10%
{desconto_porcentagem}               - 10%
```

**Desconto Fixo (R$):**
```
{desconto_fixo}                      - R$ 20,00
{valor_fixo}                         - R$ 20,00
```

**Limites:**
```
{valor_minimo_compra} ou {minimo}    - R$ 100,00 (compra mínima)
{valor_maximo_desconto} ou {maximo}  - R$ 50,00 (desconto máximo)
{limite}                             - R$ 50,00
```

**Validade:**
```
{coupon_expires}                     - 31/12/2025
{validade_cupom}                     - 31/12/2025
{expira_em}                          - 31/12/2025
```

**Múltiplos Cupons:**
```
{all_coupons}                        - CUPONS: DESC10, FRETE
{price_with_coupon}                  - 89.91 (preço com desconto)
```

### Globais (Informações do Usuário)

**Contato:**
```
{celular} ou {user_phone}         - Telefone/celular
{endereco} ou {user_address}      - Endereço completo
{site} ou {user_website}          - Website pessoal
```

**Redes Sociais:**
```
{instagram} ou {user_instagram}   - Perfil do Instagram
{facebook} ou {user_facebook}     - Perfil do Facebook
{twitter} ou {user_twitter}       - Perfil do Twitter/X
{linkedin} ou {user_linkedin}     - Perfil do LinkedIn
{youtube} ou {user_youtube}       - Canal do YouTube
{tiktok} ou {user_tiktok}         - Perfil do TikTok
```

---

## 💡 Dicas Rápidas

### Tema Escuro

- Toggle no canto superior direito do header
- Preferência salva no localStorage
- Todas as páginas adaptadas

### Quick-Create

1. Em **Ofertas** ou **Cupons**:
   - Clique no `[+]` ao lado do dropdown
   - Preencha o formulário no modal
   - Item criado automaticamente selecionado

2. Disponível para:
   - Vendedores (ofertas e cupons)
   - Categorias (ofertas)
   - Fabricantes (ofertas)

### Compartilhamento Rápido

**Via URL:**
```
/ofertas/1/compartilhar?channel=whatsapp
```

Redes disponíveis:
- `whatsapp`
- `telegram`
- `instagram`
- `facebook`
- `twitter`
- `linkedin`

### Filtros Dinâmicos

- Digite no campo de busca
- Aguarde 500ms
- Lista atualiza automaticamente
- URL reflete filtros aplicados
- Compartilhe a URL filtrada

### Toast Notifications

- Aparecem automaticamente após ações
- Duração: 5 segundos
- Posição: canto superior direito (abaixo do menu)
- Tipos: Success (verde), Error (vermelho), Warning (laranja), Info (azul)

---

## 🎨 Colorpicker

### 3 Modos Disponíveis

**1. Cor Sólida**
- Clique no colorpicker HTML5
- Ou digite código hex: `#FFE600`

**2. Gradientes Pré-definidos**
- Instagram: `linear-gradient(45deg, #f09433, #bc1888)`
- Roxo, Rosa, Azul, Verde, Pôr do Sol

**3. CSS Customizado**
- Cole qualquer valor CSS válido
- Exemplo: `linear-gradient(90deg, #667eea 0%, #764ba2 100%)`

### Onde Usar

- Vendedores (`/admin/sellers/<id>/editar`)
- Redes Sociais (`/admin/social-networks`)

---

## 📝 Editor HTML (Quill.js)

### Atalhos

| Atalho | Ação |
|--------|------|
| `Ctrl + B` | Negrito |
| `Ctrl + I` | Itálico |
| `Ctrl + U` | Sublinhado |
| `Ctrl + Shift + 7` | Lista ordenada |
| `Ctrl + Shift + 8` | Lista não ordenada |
| `Ctrl + K` | Adicionar link |

### Onde Está Disponível

- Descrição de ofertas
- Descrição de cupons
- Corpo de templates

### Conversão Automática

- **HTML → Texto Puro** ao salvar
- **Texto → Formatado** ao compartilhar:
  - WhatsApp: `*negrito*`
  - Telegram: `**negrito**`
  - Instagram: texto puro

---

## 🏪 Vendedores Padrão e Cores

| Vendedor | Cor Hex | Visual |
|----------|---------|--------|
| Mercado Livre | `#FFE600` | 🟡 Amarelo |
| Amazon | `#FF9900` | 🟠 Laranja |
| Shopee | `#EE4D2D` | 🔴 Laranja avermelhado |
| Magazine Luiza | `#DC143C` | 🔴 Vermelho |
| AliExpress | `#E62129` | 🔴 Vermelho |
| Kabum | `#003DA5` | 🔵 Azul |
| Casas Bahia | `#0070C0` | 🔵 Azul claro |
| Extra | `#00A859` | 🟢 Verde |

---

## 💰 Moedas Suportadas

| Código | Símbolo | Nome |
|--------|---------|------|
| BRL | R$ | Real Brasileiro |
| USD | $ | Dólar Americano |
| EUR | € | Euro |
| GBP | £ | Libra Esterlina |
| JPY | ¥ | Iene Japonês |
| CAD | C$ | Dólar Canadense |
| AUD | A$ | Dólar Australiano |
| CHF | CHF | Franco Suíço |
| CNY | ¥ | Yuan Chinês |
| ARS | $ | Peso Argentino |
| MXN | $ | Peso Mexicano |
| CLP | $ | Peso Chileno |

**Configurar moeda padrão:** `/admin/settings`

---

## 🔒 Permissões por Papel

| Ação | Viewer | Editor | Admin |
|------|--------|--------|-------|
| Ver ofertas | ✅ | ✅ | ✅ |
| Criar ofertas | ❌ | ✅ | ✅ |
| Editar ofertas | ❌ | ✅ | ✅ |
| Deletar ofertas | ❌ | ❌ | ✅ |
| Ver admin | ❌ | ✅ | ✅ |
| Criar usuários | ❌ | ❌ | ✅ |
| Gerenciar usuários | ❌ | ❌ | ✅ |

---

## 🚨 Solução de Problemas

### Erro: "no such table"

```bash
flask --app run.py db upgrade
```

### Ambiente virtual não ativa (Windows)

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### Resetar banco de dados

```bash
rm instance/app.db
flask --app run.py db upgrade
python -m scripts.create_admin --email admin@local --display-name "Admin"
```

### Token expirado

- Tokens expiram em 1 hora
- Obtenha novo token via `/api/auth/token`

### CSRF Token Missing

- Verifique se o formulário inclui `{{ csrf_token() }}`
- Ou use `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`

---

## 📚 Links Úteis

- **Documentação Completa:** `/docs`
- **API Docs:** `/api-docs`
- **README:** `/README.md`
- **Features:** `/docs/FEATURES.md`

---

## 🎯 Workflows Comuns

### Criar Oferta Completa

```
1. /ofertas/nova
2. Upload imagem
3. Preencha descrição (editor HTML)
4. Defina preços e parcelas
5. Selecione vendedor/categoria/fabricante
6. Defina expiração
7. Salvar
```

### Compartilhar em WhatsApp

```
1. /ofertas/<id>/compartilhar?channel=whatsapp
2. Selecione template
3. Confirme cupons (todos por padrão)
4. Copiar texto
5. Colar no WhatsApp
```

### Criar Vendedor com Cor

```
1. /admin/sellers
2. Criar vendedor ou editar existente
3. Escolher cor (colorpicker)
4. Salvar
5. Cor aplicada em todas ofertas
```

### Configurar Rede Social

```
1. /admin/social-networks
2. Encontre a rede
3. Defina prefixo (ex: "🔥 PROMOÇÃO\n\n")
4. Defina sufixo (ex: "\n\n#oferta #desconto")
5. Escolha cor/gradiente
6. Ativar/desativar
7. Salvar
```

---

**Última Atualização:** 04/12/2025  
**Versão:** 2.0
