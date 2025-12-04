# 🎯 pySaveDiário

**Central moderna para gestão de ofertas, cupons, templates de compartilhamento social e equipes. Sistema completo com API REST, tema escuro, upload de imagens e muito mais!**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades-principais)
- [Stack Tecnológico](#-stack-tecnológico)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [API](#-api)
- [Documentação](#-documentação)
- [Estrutura do Projeto](#-estrutura-do-projeto)

---

## 🚀 Visão Geral

O **pySaveDiário** é um sistema completo e moderno para gerenciar ofertas, criar templates de compartilhamento para redes sociais, organizar cupons de desconto e administrar equipes com diferentes níveis de permissão.

### 🎯 Principais Destaques:

- ✅ **CRUD Completo** para Ofertas, Cupons, Templates, Vendedores, Categorias e Fabricantes
- ✅ **Upload de Imagens** com validação de segurança e pré-visualização
- ✅ **Editor HTML Visual** (Quill.js) para descrições ricas
- ✅ **Cores Personalizadas** para vendedores com colorpicker visual
- ✅ **Sistema de Cupons Inteligente** com desconto % ou fixo e limite máximo
- ✅ **Sistema de Parcelas** com cálculo automático
- ✅ **Compartilhamento Social** com formatação específica por rede
- ✅ **Filtros Dinâmicos** em tempo real com URL compartilhável
- ✅ **Quick-Create** para criar entidades sem sair da página
- ✅ **Tema Escuro** completo e responsivo
- ✅ **Toast Notifications** estilo macOS (sem piscadas)
- ✅ **API RESTful** com autenticação Bearer Token
- ✅ **Documentação Interativa** com exemplos em 4 linguagens

---

## ✨ Funcionalidades Principais

### 1. 🏷️ Gerenciamento de Ofertas

**Funcionalidades:**
- ✅ Criar, editar, deletar e listar ofertas
- ✅ **Upload de imagens** com validação de segurança (7 camadas)
- ✅ **Editor HTML** para descrições ricas
- ✅ Campo `old_price` com **cálculo automático de desconto**
- ✅ **Sistema de parcelas** (quantidade, valor, com/sem juros)
- ✅ Badge visual mostrando **percentual de economia**
- ✅ **Data de expiração** com seletor separado (data + hora)
- ✅ Associação com vendedores, categorias e fabricantes
- ✅ **Multi-moedas** com símbolos (R$, $, €, £, etc.)

**Filtros Dinâmicos (7 tipos):**
- 🔍 Busca geral (nome, slug, vendedor)
- 🏭 Fabricante
- 🏷️ Categoria
- 🏪 Vendedor
- 💰 Faixa de preço (min/max)
- ✅ Apenas ofertas ativas (padrão)
- 📅 Por data de expiração

**Recursos Avançados:**
- Quick-create de vendedores, categorias e fabricantes
- Preview de imagem antes do upload
- Lazy loading de imagens
- Cálculo automático do nome da parcela (ex: "5x de R$ 72 sem juros")

### 2. 🎨 Cores Personalizadas para Vendedores

**Colorpicker Visual com 3 Modos:**

**Modo 1: Cor Sólida**
- Colorpicker HTML5 nativo
- Input manual de código hexadecimal (#FFE600)
- Preview em tempo real

**Modo 2: Gradientes Pré-definidos**
- Instagram (multi-color)
- Roxo
- Rosa
- Azul
- Verde
- Pôr do Sol

**Modo 3: CSS Customizado**
- Cole qualquer valor CSS válido
- Suporte a `linear-gradient`, `radial-gradient`, etc.

**Cores Padrão:**
- Mercado Livre: `#FFE600` (Amarelo)
- Amazon: `#FF9900` (Laranja)
- Shopee: `#EE4D2D` (Laranja avermelhado)
- Magazine Luiza: `#DC143C` (Vermelho)
- AliExpress: `#E62129` (Vermelho)
- Kabum: `#003DA5` (Azul)

**Aplicação Automática:**
- Badge colorido nas listagens de ofertas
- Texto sempre branco para legibilidade
- Funciona em tema claro E escuro

### 3. 🎫 Sistema de Cupons Inteligente

**Funcionalidades:**
- ✅ Criar, editar, deletar e listar cupons
- ✅ **Editor HTML** para descrições
- ✅ Ativar/desativar cupons
- ✅ Data de expiração opcional (data + hora separados)
- ✅ Associação com vendedores

**Tipos de Desconto:**

**1. Porcentagem (%)**
```
Exemplo: 10% de desconto
Com limite máximo: 10% até R$ 50
```

**2. Valor Fixo (R$)**
```
Exemplo: R$ 20 de desconto
Aplicado diretamente no preço
```

**Cálculo Automático:**
- `{price_with_coupon}` - Mostra preço com desconto aplicado
- Considera limite máximo em descontos percentuais
- Nunca resulta em preço negativo

**Filtros Disponíveis:**
- 🔍 Busca (código do cupom)
- 🏪 Vendedor
- 💰 Tipo de desconto (% ou R$)
- ✅ Apenas cupons ativos

**Integração:**
- Seleção múltipla ao compartilhar ofertas
- Namespace `{all_coupons}` para listar todos
- Formato: `CUPONS: CUPOM1, CUPOM2, CUPOM3`

### 4. 📝 Sistema de Templates

**Funcionalidades:**
- ✅ Criar templates reutilizáveis
- ✅ **Editor HTML** para corpo do template
- ✅ **Variáveis dinâmicas** (50+ namespaces)
- ✅ Suporte a **múltiplas redes sociais**
- ✅ Preview e compartilhamento
- ✅ Configuração de prefixo/sufixo por rede

**Variáveis Disponíveis (Namespaces):**

**Produto/Oferta:**
- `{product_name}` - Nome do produto
- `{product_description}` - Descrição (formatada por rede)
- `{price}` - Preço atual (com símbolo)
- `{old_price}` - Preço antigo
- `{discount}` - Percentual de desconto
- `{vendor_name}` ou `{seller}` - Nome do vendedor
- `{offer_url}` - Link da oferta
- `{category}` - Categoria
- `{manufacturer}` - Fabricante

**Parcelas:**
- `{installment_count}` - Número de parcelas (ex: 5)
- `{installment_value}` - Valor da parcela (ex: R$ 72.00)
- `{installment_interest_free}` - Sim/Não
- `{installment_full}` ou `{parcelamento}` - Texto completo (ex: "5x de R$ 72 sem juros")

**Cupons:**
- `{coupon_code}` ou `{code}` - Código do cupom (ex: DESC10)
- `{coupon_seller}` ou `{seller}` - Vendedor do cupom
- `{porcentagem}` ou `{percentual}` - Desconto em % (ex: 10%)
- `{desconto_fixo}` ou `{valor_fixo}` - Desconto fixo em R$ (ex: R$ 20,00)
- `{valor_minimo_compra}` ou `{minimo}` - Valor mínimo da compra (ex: R$ 100,00)
- `{valor_maximo_desconto}` ou `{maximo}` - Limite máximo do desconto (ex: R$ 50,00)
- `{coupon_expires}` ou `{validade_cupom}` - Data de validade (ex: 31/12/2025)
- `{all_coupons}` - Todos os cupons selecionados (ex: CUPONS: DESC10, FRETE)
- `{price_with_coupon}` - Preço com cupom aplicado (cálculo automático)

**Globais (Informações do Usuário):**
- `{celular}` ou `{user_phone}` - Celular do usuário
- `{endereco}` ou `{user_address}` - Endereço do usuário
- `{site}` ou `{user_website}` - Website do usuário
- `{instagram}` ou `{user_instagram}` - Instagram do usuário
- `{facebook}` ou `{user_facebook}` - Facebook do usuário
- `{twitter}` ou `{user_twitter}` - Twitter/X do usuário
- `{linkedin}` ou `{user_linkedin}` - LinkedIn do usuário
- `{youtube}` ou `{user_youtube}` - YouTube do usuário
- `{tiktok}` ou `{user_tiktok}` - TikTok do usuário

**Filtros Disponíveis:**
- 🔍 Busca (nome, slug, descrição)
- 📱 Rede social específica

### 5. 📤 Compartilhamento Social

**Página Dedicada** (`/ofertas/<id>/compartilhar`)

**Recursos:**
- ✅ Seleção de rede social (Instagram, Facebook, WhatsApp, Telegram, Twitter, LinkedIn, TikTok)
- ✅ **Conversão automática de formatação** HTML → Formato da rede social
- ✅ **Barra de ferramentas de formatação** com 7 botões interativos
- ✅ **Seletor de emojis** com 100+ opções organizadas por categoria
- ✅ **Edição livre** do texto gerado
- ✅ **Salvamento de templates personalizados** por rede social
- ✅ Botões coloridos com cores configuráveis
- ✅ Seleção de template
- ✅ **Seleção múltipla de cupons** (todos ativos por padrão)
- ✅ Checkbox para calcular preço com cupom
- ✅ **Formatação automática** por rede social:
  - WhatsApp: `*negrito*`, `_itálico_`
  - Telegram: `**negrito**`, `__itálico__`
  - Instagram/Facebook: texto puro
- ✅ Conversão HTML → Texto formatado
- ✅ Geração automática do texto
- ✅ Botão de copiar
- ✅ Preview em tempo real
- ✅ Pré-seleção via URL (`?channel=whatsapp`)

**Exemplo de Texto Gerado:**
```
*Controle PS5 DualSense*

De R$ 499,00 por R$ 399,00 (-20%)

5x de R$ 79,80 sem juros

CUPONS: DESC10, FRETEGRATIS

💰 Com cupom: R$ 359,10

🔗 https://exemplo.com/oferta

📍 Vendedor: Amazon

#ps5 #controle #oferta
```

### 6. 🖼️ Upload de Imagens Seguro

**7 Camadas de Segurança:**

1. **Validação de Extensão**
   ```
   Permitidas: .jpg, .jpeg, .png, .gif, .webp
   ```

2. **Validação de Content-Type**
   ```
   Apenas image/jpeg, image/png, image/gif, image/webp
   ```

3. **Validação com Pillow**
   ```
   Tenta abrir como imagem real
   Detecta arquivos corrompidos ou falsos
   ```

4. **Limite de Tamanho**
   ```
   Máximo: 5MB por imagem
   ```

5. **Nome Seguro**
   ```
   Gera: product_<timestamp>_<random>.jpg
   Remove caracteres especiais
   ```

6. **Diretório Isolado**
   ```
   app/static/uploads/products/
   Separado do código da aplicação
   ```

7. **Permissões do Sistema**
   ```
   Diretórios: 755 (rwxr-xr-x)
   Arquivos: 644 (rw-r--r--)
   ```

**Exibição:**
- Preview na criação de oferta
- Imagem na listagem de ofertas
- Imagem na página de compartilhamento
- Placeholder quando não há imagem
- Lazy loading para performance

### 7. 📝 Editor HTML Visual (Quill.js)

**Funcionalidades:**
- ✅ Editor WYSIWYG moderno
- ✅ Barra de ferramentas completa
- ✅ **Compatível com temas claro e escuro**
- ✅ Salvamento como **texto puro** (sem tags HTML)
- ✅ Conversão automática para formato de rede social

**Ferramentas Disponíveis:**
- Negrito, Itálico, Sublinhado
- Listas (ordenadas e não ordenadas)
- Links
- Alinhamento de texto
- Limpeza de formatação

**Campos com Editor:**
- Descrição de produtos (ofertas)
- Descrição de cupons
- Corpo de templates

**Conversão Inteligente:**
```
HTML Input:
<p><strong>Oferta</strong></p>
<ul><li>Item 1</li><li>Item 2</li></ul>

WhatsApp Output:
*Oferta*
• Item 1
• Item 2

Telegram Output:
**Oferta**
• Item 1
• Item 2
```

### 8. 🎨 Configuração de Redes Sociais

**Funcionalidades:**
- ✅ Personalizar prefixos e sufixos
- ✅ **Colorpicker visual** para botões
- ✅ Ativar/desativar redes
- ✅ Preview em tempo real

**Colorpicker com 3 Modos:**
- Cor sólida (#hex)
- 6 gradientes pré-definidos
- CSS customizado

**Configurações Por Rede:**
```
Instagram:
  Prefixo: "📸 OFERTA DO DIA\n\n"
  Sufixo: "\n\n#oferta #desconto #instagram"
  Cor: linear-gradient(45deg, #f09433, #bc1888)

WhatsApp:
  Prefixo: "🔥 APROVEITE!\n\n"
  Sufixo: "\n\n✅ Clique e compre agora!"
  Cor: #25D366

Facebook:
  Prefixo: "🎁 PROMOÇÃO EXCLUSIVA\n\n"
  Sufixo: "\n\n👉 Compartilhe com amigos!"
  Cor: #1877F2
```

### 9. 🔍 Filtros Dinâmicos

**Ofertas** (`/ofertas`)
- 🔍 Busca geral
- 🏪 Vendedor
- 🏭 Fabricante
- 🏷️ Categoria
- 💰 Faixa de preço
- ✅ Apenas ativas

**Templates** (`/templates`)
- 🔍 Busca (nome, slug, descrição)
- 📱 Rede social

**Cupons** (`/cupons`)
- 🔍 Busca (código do cupom)
- 🏪 Vendedor
- 💰 Tipo de desconto (% ou R$)
- ✅ Apenas ativos

**Recursos:**
- Atualização em tempo real (500ms debounce)
- URL compartilhável
- Botão "Limpar Filtros"
- Valores persistem após filtrar

### 10. 👥 Administração

**Menu Dropdown Organizado:**
```
Administração ▼
  ├─ 📊 Painel
  ├─ ─────────────
  ├─ 👥 Usuários
  ├─ 👨‍👩‍👧‍👦 Grupos
  ├─ ─────────────
  ├─ 🏪 Vendedores
  ├─ 🏷️ Categorias
  ├─ 🏭 Fabricantes
  ├─ ─────────────
  ├─ 📱 Redes Sociais
  └─ ⚙️ Configurações
```

**Vendedores, Categorias e Fabricantes:**
- ✅ Criar, editar, deletar
- ✅ Ativar/desativar
- ✅ **Páginas dedicadas para edição**
- ✅ Colorpicker visual (vendedores)
- ✅ **Filtro automático**: Inativos não aparecem

**Configurações:**
- ✅ Moeda padrão do sistema
- ✅ Símbolos de moedas
- ✅ 12 moedas disponíveis

**Redes Sociais:**
- ✅ Configurar prefixo/sufixo
- ✅ Escolher cor/gradiente
- ✅ Ativar/desativar
- ✅ Preview em tempo real

### 11. ⚡ Quick-Create

**Criar sem sair da página:**

**Ofertas:**
- Vendedores
- Categorias
- Fabricantes

**Cupons:**
- Vendedores

**Funcionamento:**
1. Clique no botão `[+]`
2. Modal abre
3. Preencha os dados
4. Salve
5. **Dropdown atualiza automaticamente**
6. **Item já vem selecionado**
7. Continua no formulário atual

### 12. 🎨 UX/UI Moderna

**Interface:**
- ✅ **Toast notifications** estilo macOS (sem piscadas!)
- ✅ **Tema escuro** completo e responsivo
- ✅ **Design mobile-first**
- ✅ **Bootstrap Icons** em toda interface
- ✅ **Animações suaves** (fade-in/out)
- ✅ **Feedback visual** em todas as ações
- ✅ **Cards elegantes** com hover effects
- ✅ **Gradientes modernos** em hero sections
- ✅ **Menu sempre no topo** (z-index otimizado)

**Home Page Repaginada:**
- Hero section com gradiente
- Estatísticas em tempo real (cards)
- Seção de funcionalidades (6 cards)
- Ofertas em destaque
- Call-to-action section
- Footer informativo

### 13. 💰 Sistema de Moedas

**12 Moedas Disponíveis:**
- 🇧🇷 **BRL** - R$ (Real Brasileiro)
- 🇺🇸 **USD** - $ (Dólar Americano)
- 🇪🇺 **EUR** - € (Euro)
- 🇬🇧 **GBP** - £ (Libra Esterlina)
- 🇯🇵 **JPY** - ¥ (Iene Japonês)
- 🇨🇦 **CAD** - C$ (Dólar Canadense)
- 🇦🇺 **AUD** - A$ (Dólar Australiano)
- 🇨🇭 **CHF** - CHF (Franco Suíço)
- 🇨🇳 **CNY** - ¥ (Yuan Chinês)
- 🇦🇷 **ARS** - $ (Peso Argentino)
- 🇲🇽 **MXN** - $ (Peso Mexicano)
- 🇨🇱 **CLP** - $ (Peso Chileno)

**Recursos:**
- Moeda padrão configurável
- Símbolos em toda interface
- Conversão automática em templates

---

## 🛠️ Stack Tecnológico

### Backend
- **Python 3.11+**
- **Flask 3.0+** - Framework web
- **SQLAlchemy** - ORM
- **Flask-Migrate / Alembic** - Migrações
- **Flask-Login** - Autenticação
- **Flask-WTF** - Formulários e CSRF
- **Flask-HTTPAuth** - API Auth (Basic + Bearer)
- **Pillow** - Processamento de imagens
- **python-slugify** - Geração de slugs

### Frontend
- **HTML5 + CSS3 + JavaScript**
- **Bootstrap 5.3.3** - Framework CSS
- **Bootstrap Icons** - Ícones
- **Quill.js** - Editor HTML WYSIWYG
- **Vanilla JavaScript** - Interações dinâmicas

### Banco de Dados
- **SQLite** (desenvolvimento)
- **PostgreSQL** (produção recomendado)
- **MySQL / MariaDB** (suportado)

---

## 📦 Instalação

### Pré-requisitos

- Python 3.11 ou superior
- pip
- Git

### Passo a Passo

#### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/pySaveDiario.git
cd pySaveDiario
```

#### 2. Crie um ambiente virtual

**Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

#### 4. Configure o ambiente

```bash
cp env.example .env
```

Edite o `.env` conforme necessário.

#### 5. Inicialize o banco de dados

```bash
flask --app run.py db upgrade
```

#### 6. Rode scripts de setup (opcional mas recomendado)

```bash
# Adicionar cores aos vendedores
python scripts/add_color_to_sellers.py

# Adicionar namespaces de parcelas
python scripts/add_installment_namespaces.py

# Adicionar namespaces de descrição
python scripts/add_description_namespaces.py
```

#### 7. Crie o primeiro administrador

```bash
python -m scripts.create_admin --email admin@local --display-name "Admin"
```

#### 8. Execute a aplicação

```bash
flask --app run.py run --reload
```

Acesse: `http://localhost:5000`

---

## ⚙️ Configuração

### Arquivo `.env`

```env
# Database
DB_ENGINE=sqlite

# Para PostgreSQL:
# DB_ENGINE=postgresql
# DB_HOST=localhost
# DB_PORT=5432
# DB_USER=seu_usuario
# DB_PASSWORD=sua_senha
# DB_NAME=pysavediario

# Security
SECRET_KEY=sua-chave-secreta-aqui

# Application
FLASK_ENV=development
FLASK_DEBUG=1
```

### Gerar SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🎯 Uso

### Principais Rotas Web

| Rota | Descrição |
|------|-----------|
| `/` | Página inicial |
| `/login` | Autenticação |
| `/dashboard` | Dashboard do usuário |
| `/ofertas` | Listagem de ofertas (com filtros) |
| `/ofertas/nova` | Criar nova oferta |
| `/ofertas/<id>/editar` | Editar oferta |
| `/ofertas/<id>/compartilhar` | Compartilhar oferta |
| `/cupons` | Listagem de cupons (com filtros) |
| `/cupons/novo` | Criar novo cupom |
| `/cupons/<id>/editar` | Editar cupom |
| `/templates` | Listagem de templates (com filtros) |
| `/templates/novo` | Criar novo template |
| `/templates/<id>/editar` | Editar template |
| `/admin` | Painel administrativo |
| `/admin/sellers` | Gerenciar vendedores |
| `/admin/sellers/<id>/editar` | Editar vendedor |
| `/admin/categories` | Gerenciar categorias |
| `/admin/categories/<id>/editar` | Editar categoria |
| `/admin/manufacturers` | Gerenciar fabricantes |
| `/admin/manufacturers/<id>/editar` | Editar fabricante |
| `/admin/social-networks` | Configurar redes sociais |
| `/admin/settings` | Configurações do sistema |
| `/usuarios` | Gerenciar usuários |
| `/grupos` | Gerenciar grupos |
| `/api-docs` | Documentação interativa da API |

---

## 🔌 API

### Autenticação

#### Obter Token

```bash
curl -X POST http://localhost:5000/api/auth/token \
  -u "admin@local:sua_senha"
```

**Resposta:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expires_in": 3600
}
```

#### Usar Token

```bash
curl http://localhost:5000/api/sellers \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### Principais Endpoints

#### Users (Usuários)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| POST | `/api/users` | Registrar novo usuário | Público |
| GET | `/api/users` | Listar todos | Admin |
| GET | `/api/users/<id>` | Obter um usuário | Próprio/Admin |
| PUT/PATCH | `/api/users/<id>` | Atualizar usuário | Próprio/Admin |

**Exemplo POST (Registro Completo):**
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@email.com",
    "password": "senha123",
    "display_name": "Nome Completo",
    "role": "member",
    "phone": "(11) 98765-4321",
    "address": "Rua Exemplo, 123 - São Paulo, SP",
    "website": "https://meusite.com.br",
    "instagram": "@meuinstagram",
    "facebook": "https://facebook.com/meuperfil",
    "twitter": "@meutwitter",
    "linkedin": "https://linkedin.com/in/meuperfil",
    "youtube": "https://youtube.com/@meucanal",
    "tiktok": "@meutiktok"
  }'
```

**Exemplo PUT (Atualizar Perfil):**
```bash
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "(11) 91234-5678",
    "website": "https://novosite.com.br",
    "instagram": "@novoinstagram"
  }'
```

**Campos Disponíveis:**
- **Obrigatórios** (no registro): `email`, `password`, `display_name`
- **Opcionais**: `role`, `phone`, `address`, `website`
- **Redes Sociais**: `instagram`, `facebook`, `twitter`, `linkedin`, `youtube`, `tiktok`

**Namespaces Globais:**
Informações do usuário podem ser usadas em templates via:
- `{celular}` - Telefone do usuário
- `{endereco}` - Endereço
- `{site}` - Website
- `{instagram}`, `{facebook}`, `{twitter}`, `{linkedin}`, `{youtube}`, `{tiktok}` - Redes sociais

#### Sellers (Vendedores)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| GET | `/api/sellers` | Listar todos | Autenticado |
| POST | `/api/sellers` | Criar novo | Admin/Editor |
| GET | `/api/sellers/<id>` | Obter um | Autenticado |
| PUT | `/api/sellers/<id>` | Atualizar | Admin/Editor |
| DELETE | `/api/sellers/<id>` | Deletar | Admin |

**Exemplo POST:**
```bash
curl -X POST http://localhost:5000/api/sellers \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Novo Vendedor",
    "slug": "novo-vendedor",
    "color": "#FF5733",
    "active": true
  }'
```

#### Categories (Categorias)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| GET | `/api/categories` | Listar todas | Autenticado |
| POST | `/api/categories` | Criar nova | Admin/Editor |
| PUT | `/api/categories/<id>` | Atualizar | Admin/Editor |
| DELETE | `/api/categories/<id>` | Deletar | Admin |

#### Manufacturers (Fabricantes)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| GET | `/api/manufacturers` | Listar todos | Autenticado |
| POST | `/api/manufacturers` | Criar novo | Admin/Editor |
| PUT | `/api/manufacturers/<id>` | Atualizar | Admin/Editor |
| DELETE | `/api/manufacturers/<id>` | Deletar | Admin |

#### Offers (Ofertas)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| GET | `/api/offers` | Listar ofertas | Público |
| POST | `/api/offers` | Criar oferta | Admin/Editor |
| GET | `/api/offers/<id>` | Obter oferta | Público |
| PUT | `/api/offers/<id>` | Atualizar | Admin/Editor |
| DELETE | `/api/offers/<id>` | Deletar | Admin |

**Filtros GET:**
```
?vendor=mercado
?product=ps5
?min_price=100
?max_price=500
```

#### Users (Usuários)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| GET | `/api/users` | Listar todos | Admin |
| POST | `/api/users` | Criar novo | Admin |
| PUT | `/api/users/<id>` | Atualizar | Admin ou próprio |
| DELETE | `/api/users/<id>` | Deletar | Admin |

### Documentação Completa

Acesse: **`http://localhost:5000/api-docs`**

Inclui exemplos em:
- 🐍 Python (requests)
- 🟢 Node.js (axios)
- 🐘 PHP (cURL)
- 💻 cURL (linha de comando)

---

## 📚 Documentação

### `/docs` - Documentação Técnica

- **[FEATURES.md](docs/FEATURES.md)** - Lista completa de funcionalidades
- **[SELLER_COLORS_FEATURE.md](docs/SELLER_COLORS_FEATURE.md)** - Cores personalizadas
- **[FILTERS_FEATURE.md](docs/FILTERS_FEATURE.md)** - Sistema de filtros
- **[SECURE_IMAGE_UPLOAD.md](docs/SECURE_IMAGE_UPLOAD.md)** - Upload seguro
- **[INSTALLMENT_FEATURE.md](docs/INSTALLMENT_FEATURE.md)** - Sistema de parcelas
- **[COUPON_DISCOUNT_FEATURE.md](docs/COUPON_DISCOUNT_FEATURE.md)** - Descontos com cupons
- **[HTML_EDITOR_FEATURE.md](docs/HTML_EDITOR_FEATURE.md)** - Editor Quill.js
- **[CURRENCY_SYMBOLS.md](docs/CURRENCY_SYMBOLS.md)** - Símbolos de moedas
- **[INACTIVE_SELLER_FILTER.md](docs/INACTIVE_SELLER_FILTER.md)** - Filtro de inativos
- **[MAX_DISCOUNT_LIMIT.md](docs/MAX_DISCOUNT_LIMIT.md)** - Limite de desconto
- **[HTML_TO_TEXT_CONVERSION.md](docs/HTML_TO_TEXT_CONVERSION.md)** - Conversão para redes

---

## 📁 Estrutura do Projeto

```
pySaveDiario/
├── app/
│   ├── __init__.py              # App factory
│   ├── config.py                # Configurações
│   ├── extensions.py            # Extensões Flask
│   ├── models.py                # Modelos (15+ tabelas)
│   ├── forms.py                 # Formulários WTForms
│   ├── security.py              # Autenticação
│   ├── routes/
│   │   ├── web.py               # ~40 rotas web
│   │   └── api.py               # ~35 rotas API
│   ├── utils/
│   │   ├── upload.py            # Upload seguro
│   │   ├── currency.py          # Moedas
│   │   └── slugify.py           # Slugs
│   ├── static/
│   │   ├── css/
│   │   │   └── theme.css        # CSS centralizado
│   │   ├── js/
│   │   └── uploads/             # Imagens
│   │       └── products/
│   └── templates/
│       ├── base.html            # Template base
│       ├── index.html           # Home repaginada
│       ├── offers_list.html     # Lista de ofertas
│       ├── offer_create.html    # Criar oferta
│       ├── offer_edit.html      # Editar oferta
│       ├── offer_share.html     # Compartilhar oferta
│       ├── coupons_list.html    # Lista de cupons
│       ├── templates_list.html  # Lista de templates
│       ├── admin/               # Templates admin
│       │   ├── sellers.html
│       │   ├── seller_edit.html
│       │   ├── categories.html
│       │   └── ...
│       ├── components/
│       │   └── html_editor.html # Editor Quill
│       └── api_docs.html        # Docs da API
├── migrations/                  # Migrações Alembic
├── scripts/                     # Scripts utilitários
│   ├── create_admin.py
│   ├── add_color_to_sellers.py
│   ├── add_installment_namespaces.py
│   └── ...
├── docs/                        # Documentação
├── instance/
│   └── app.db                   # SQLite (dev)
├── .env                         # Variáveis (não commitado)
├── requirements.txt             # Dependências
├── run.py                       # Entry point
└── README.md                    # Este arquivo
```

---

## 🔒 Segurança

- ✅ **CSRF Protection** em todos os formulários
- ✅ **@login_required** em rotas protegidas
- ✅ **Role-Based Access Control** (Admin, Editor, Viewer)
- ✅ **Validação de upload** (7 camadas de segurança)
- ✅ **Sanitização de inputs**
- ✅ **SQL Injection** protegido (ORM)
- ✅ **Senhas hasheadas** (Werkzeug)
- ✅ **Tokens JWT** para API
- ✅ **Permissões de arquivo** (755/644)

---

## 📊 Estatísticas

- **Funcionalidades:** 30+
- **Rotas Web:** ~40
- **Rotas API:** ~35
- **Tabelas no banco:** 15+
- **Namespaces disponíveis:** 50+
- **Idioma código:** Inglês
- **Idioma interface:** Português (BR)
- **Responsivo:** Sim (mobile-first)
- **PWA Ready:** Não (planejado)

---

## 🚀 Roadmap

### Próximas Features

- [ ] Paginação nas listagens
- [ ] Exportação (CSV, Excel, PDF)
- [ ] Gráficos e dashboard analytics
- [ ] Histórico de alterações
- [ ] Notificações por email
- [ ] Auto-post em redes sociais
- [ ] PWA (offline-first)
- [ ] Multi-idioma (EN, ES)
- [ ] Sistema de favoritos
- [ ] API webhooks

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Add NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

---

## 📝 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**Willian Jesus**

---

## 🙏 Agradecimentos

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Quill.js](https://quilljs.com/)
- [Pillow](https://python-pillow.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

---

**Desenvolvido com ❤️ e Python**
