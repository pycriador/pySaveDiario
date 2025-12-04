# 🎯 pySaveDiário

**Central moderna para gestão de ofertas, cupons, templates de compartilhamento social e equipes.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Stack Tecnológico](#-stack-tecnológico)
- [Funcionalidades](#-funcionalidades-principais)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [API](#-api)
- [Documentação](#-documentação)
- [Estrutura do Projeto](#-estrutura-do-projeto)

---

## 🚀 Visão Geral

O **pySaveDiário** é um sistema completo para gerenciar ofertas, criar templates de compartilhamento para redes sociais, organizar cupons de desconto e administrar equipes com diferentes níveis de permissão.

### Destaques:

- ✅ **Sistema CRUD Completo** para Ofertas, Cupons, Templates, Vendedores, Categorias e Fabricantes
- ✅ **Compartilhamento Social** com templates personalizados e variáveis dinâmicas
- ✅ **Sistema de Cupons** integrado ao compartilhamento de ofertas
- ✅ **Filtros Dinâmicos** com busca em tempo real e URL compartilhável
- ✅ **Quick-Create** para criar entidades sem sair da página atual
- ✅ **Tema Escuro** completo e responsivo
- ✅ **Toast Notifications** estilo macOS
- ✅ **API RESTful** com autenticação por token
- ✅ **Documentação Interativa** com exemplos em múltiplas linguagens

---

## 🛠️ Stack Tecnológico

### Backend
- **Python 3.11+**
- **Flask 3.0+** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **Flask-Migrate / Alembic** - Gerenciamento de migrações
- **Flask-Login** - Autenticação de usuários
- **Flask-WTF** - Formulários e CSRF protection
- **Flask-HTTPAuth** - Autenticação para API (Basic + Bearer Token)

### Frontend
- **HTML5 + CSS3 + JavaScript**
- **Bootstrap 5.3.3** - Framework CSS
- **Bootstrap Icons** - Ícones modernos
- **Vanilla JavaScript** - Interações dinâmicas

### Banco de Dados
- **SQLite** (desenvolvimento)
- **PostgreSQL / MySQL / MariaDB** (produção - suportado)

---

## ✨ Funcionalidades Principais

### 1. Gerenciamento de Ofertas

- ✅ Criar, editar, deletar e listar ofertas
- ✅ Campo `old_price` com cálculo automático de desconto
- ✅ Badge visual mostrando percentual de economia
- ✅ Filtros dinâmicos (busca, preço, categoria, fabricante, vendedor)
- ✅ Quick-create de vendedores, categorias e fabricantes
- ✅ Data de expiração com seletor de data/hora

### 2. Sistema de Templates

- ✅ Criar templates reutilizáveis para redes sociais
- ✅ Variáveis dinâmicas (namespaces) substituídas automaticamente
- ✅ Suporte a múltiplas redes sociais (Instagram, Facebook, WhatsApp, Telegram, Twitter)
- ✅ Preview e compartilhamento

**Variáveis disponíveis:**
- `{product_name}` - Nome do produto
- `{price}` - Preço atual
- `{old_price}` - Preço antigo
- `{discount}` - Percentual de desconto
- `{vendor_name}` - Nome do vendedor
- `{offer_url}` - Link da oferta
- `{category}` - Categoria
- `{manufacturer}` - Fabricante
- `{all_coupons}` - Todos os cupons selecionados inline (ex: CUPOM1 / CUPOM2)

### 3. Sistema de Cupons

- ✅ Criar, editar, deletar e listar cupons
- ✅ Ativar/desativar cupons
- ✅ Data de expiração opcional
- ✅ Associação com vendedores
- ✅ Integração com compartilhamento de ofertas

### 4. Configuração de Redes Sociais

- ✅ Personalizar prefixos e sufixos para cada rede social
- ✅ Adicionar hashtags específicas por plataforma
- ✅ Ativar/desativar redes sociais
- ✅ Aplicação automática ao gerar textos de compartilhamento

### 5. Compartilhamento Social

- ✅ Página dedicada para compartilhamento (`/ofertas/<id>/compartilhar`)
- ✅ Seleção de rede social (Instagram, Facebook, WhatsApp, Telegram, Twitter)
- ✅ Seleção de cupons ativos para incluir no texto
- ✅ Seleção de template
- ✅ Geração automática do texto com todas as substituições
- ✅ Botão de copiar texto
- ✅ Preview em tempo real

### 6. Filtros Dinâmicos

**7 tipos de filtros nas ofertas:**
- 🔍 Busca geral (nome do produto, slug, vendedor)
- 🏭 Fabricante
- 🏷️ Categoria
- 🏪 Vendedor
- 💰 Faixa de preço (min/max)
- ✅ Apenas ofertas ativas (padrão)

**Recursos:**
- Filtragem em tempo real (delay 500ms)
- URL compartilhável com parâmetros
- Contador de resultados
- Botão para limpar filtros

### 7. Administração

**Menu dropdown organizado:**
```
Administração ▼
  ├─ Painel
  ├─ ─────────
  ├─ Usuários
  ├─ Grupos
  ├─ ─────────
  ├─ Vendedores
  ├─ Categorias
  ├─ Fabricantes
  ├─ ─────────
  ├─ Redes Sociais
  └─ Configurações
```

### 8. Quick-Create

**Criar sem sair da página atual:**
- Vendedores (em ofertas e cupons)
- Categorias (em ofertas)
- Fabricantes (em ofertas)

**Funcionamento:**
1. Clique no botão `[+]`
2. Modal abre
3. Preencha os dados
4. Salve
5. Dropdown atualiza automaticamente
6. Item já vem selecionado

### 9. UX/UI Moderna

- ✅ Toast notifications estilo macOS
- ✅ Tema escuro completo
- ✅ Design responsivo (mobile-first)
- ✅ Ícones Bootstrap Icons
- ✅ Animações suaves
- ✅ Feedback visual em todas as ações

---

## 📦 Instalação

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

#### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/pySaveDiario.git
cd pySaveDiario
```

#### 2. Crie um ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

**Windows (Prompt de Comando):**
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
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

Edite o arquivo `.env` conforme necessário.

#### 5. Inicialize o banco de dados

```bash
flask --app run.py db init
flask --app run.py db migrate -m "initial migration"
flask --app run.py db upgrade
```

#### 6. Crie o primeiro administrador

```bash
python -m scripts.create_admin --email admin@local --display-name "Admin"
```

Você será solicitado a criar uma senha.

**Para criar um editor:**
```bash
python -m scripts.create_admin --email editor@local --display-name "Editor" --role editor
```

#### 7. Execute a aplicação

```bash
flask --app run.py run --reload
```

Acesse: `http://localhost:5000`

---

## ⚙️ Configuração

### Arquivo `.env`

O arquivo `.env` contém as configurações do ambiente. Exemplo:

```env
# Database
DB_ENGINE=sqlite
# Para PostgreSQL: DB_ENGINE=postgresql
# Para MySQL/MariaDB: DB_ENGINE=mysql ou mariadb

# Se usando PostgreSQL ou MySQL/MariaDB:
# DB_HOST=localhost
# DB_PORT=5432  # 5432 para PostgreSQL, 3306 para MySQL
# DB_USER=seu_usuario
# DB_PASSWORD=sua_senha
# DB_NAME=pysavediario

# Ou use DATABASE_URL diretamente:
# DATABASE_URL=postgresql+psycopg://user:senha@host:5432/db

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

### Bancos de Dados Suportados

#### SQLite (Padrão - Desenvolvimento)
```env
DB_ENGINE=sqlite
```
Cria automaticamente `instance/app.db`

#### PostgreSQL (Recomendado - Produção)
```env
DB_ENGINE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=pysavediario
```

#### MySQL / MariaDB
```env
DB_ENGINE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=pysavediario
```

---

## 🎯 Uso

### Acesso Web

Após executar a aplicação, acesse:

- **Home:** `http://localhost:5000`
- **Login:** `http://localhost:5000/login`
- **Dashboard:** `http://localhost:5000/dashboard`
- **Ofertas:** `http://localhost:5000/ofertas`
- **Cupons:** `http://localhost:5000/cupons`
- **Templates:** `http://localhost:5000/templates`
- **Administração:** `http://localhost:5000/admin`

### Principais Rotas Web

| Rota | Descrição |
|------|-----------|
| `/` | Página inicial |
| `/login` | Autenticação |
| `/dashboard` | Painel após login |
| `/ofertas` | Listagem de ofertas |
| `/ofertas/nova` | Criar nova oferta |
| `/ofertas/<id>/editar` | Editar oferta |
| `/ofertas/<id>/compartilhar` | Compartilhar oferta em redes sociais |
| `/cupons` | Listagem de cupons |
| `/cupons/novo` | Criar novo cupom |
| `/cupons/<id>/editar` | Editar cupom |
| `/templates` | Listagem de templates |
| `/templates/novo` | Criar novo template |
| `/templates/<id>/editar` | Editar template |
| `/admin` | Painel administrativo |
| `/admin/sellers` | Gerenciar vendedores |
| `/admin/categories` | Gerenciar categorias |
| `/admin/manufacturers` | Gerenciar fabricantes |
| `/admin/social-networks` | Configurar redes sociais |
| `/admin/settings` | Configurações do sistema |
| `/usuarios` | Gerenciar usuários (admin) |
| `/grupos` | Gerenciar grupos (admin) |

---

## 🔌 API

### Autenticação

O sistema oferece duas formas de autenticação para a API:

#### 1. Obter Token via HTTP Basic Auth

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

#### 2. Login via JSON

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@local",
    "password": "sua_senha"
  }'
```

### Usando o Token

Inclua o token no header `Authorization`:

```bash
curl http://localhost:5000/api/sellers \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Principais Endpoints da API

#### Sellers (Vendedores)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| GET | `/api/sellers` | Listar todos | Autenticado |
| POST | `/api/sellers` | Criar novo | Admin/Editor |
| GET | `/api/sellers/<id>` | Obter um | Autenticado |
| PUT | `/api/sellers/<id>` | Atualizar | Admin/Editor |
| DELETE | `/api/sellers/<id>` | Deletar | Admin |

#### Categories (Categorias)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| GET | `/api/categories` | Listar todas | Autenticado |
| POST | `/api/categories` | Criar nova | Admin/Editor |
| GET | `/api/categories/<id>` | Obter uma | Autenticado |
| PUT | `/api/categories/<id>` | Atualizar | Admin/Editor |
| DELETE | `/api/categories/<id>` | Deletar | Admin |

#### Manufacturers (Fabricantes)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| GET | `/api/manufacturers` | Listar todos | Autenticado |
| POST | `/api/manufacturers` | Criar novo | Admin/Editor |
| GET | `/api/manufacturers/<id>` | Obter um | Autenticado |
| PUT | `/api/manufacturers/<id>` | Atualizar | Admin/Editor |
| DELETE | `/api/manufacturers/<id>` | Deletar | Admin |

#### Users (Usuários)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| GET | `/api/users` | Listar todos | Admin |
| POST | `/api/users` | Criar novo | Admin |
| GET | `/api/users/<id>` | Obter um | Admin ou próprio usuário |
| PUT | `/api/users/<id>` | Atualizar | Admin ou próprio usuário |
| DELETE | `/api/users/<id>` | Deletar | Admin |

#### Groups (Grupos)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| GET | `/api/groups` | Listar todos | Autenticado |
| POST | `/api/groups` | Criar novo | Admin/Editor |
| GET | `/api/groups/<id>` | Obter um | Autenticado |
| PUT | `/api/groups/<id>` | Atualizar | Admin/Editor |
| DELETE | `/api/groups/<id>` | Deletar | Admin |

### Exemplos em Diferentes Linguagens

Acesse a **documentação interativa completa** em: `http://localhost:5000/api-docs`

A documentação inclui exemplos práticos em:
- 🐍 **Python** (com `requests`)
- 🟢 **Node.js** (com `axios`)
- 🐘 **PHP** (com `cURL`)
- 💻 **cURL** (linha de comando)

---

## 📚 Documentação

### Documentação Completa

Toda a documentação técnica está organizada em `/docs`:

- **[FEATURES.md](/docs/FEATURES.md)** - Lista completa de funcionalidades
- **[QUICK_REFERENCE.md](/docs/QUICK_REFERENCE.md)** - Referência rápida de comandos
- **[API_COMPLETE_INVENTORY.md](/docs/API_COMPLETE_INVENTORY.md)** - Inventário completo da API
- **[GUIA_USO_REDES_SOCIAIS.md](/docs/GUIA_USO_REDES_SOCIAIS.md)** - Como usar redes sociais e cupons
- **[RESUMO_FINAL_IMPLEMENTACOES.md](/docs/RESUMO_FINAL_IMPLEMENTACOES.md)** - Resumo de todas as implementações

### Documentação da API

**Documentação Interativa:** `http://localhost:5000/api-docs`

Inclui:
- Todos os endpoints disponíveis
- Parâmetros esperados
- Exemplos de request/response
- Códigos de exemplo em Python, Node.js, PHP e cURL
- Tratamento de erros

---

## 📁 Estrutura do Projeto

```
pySaveDiario/
├── app/
│   ├── __init__.py           # Inicialização do app Flask
│   ├── config.py             # Configurações
│   ├── extensions.py         # Extensões (SQLAlchemy, Login, etc)
│   ├── models.py             # Modelos do banco de dados
│   ├── forms.py              # Formulários (WTForms)
│   ├── security.py           # Funções de segurança
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── web.py            # Rotas web (~38 rotas)
│   │   └── api.py            # Rotas API (~34 rotas)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # Estilos customizados
│   │   └── js/
│   │       └── main.js       # JavaScript customizado
│   └── templates/
│       ├── base.html         # Template base
│       ├── index.html        # Página inicial
│       ├── login.html        # Login
│       ├── dashboard.html    # Dashboard
│       ├── offers_list.html  # Listagem de ofertas
│       ├── offer_create.html # Criar oferta
│       ├── offer_edit.html   # Editar oferta
│       ├── offer_share.html  # Compartilhar oferta
│       ├── coupons_list.html # Listagem de cupons
│       ├── coupon_create.html # Criar cupom
│       ├── coupon_edit.html  # Editar cupom
│       ├── templates_list.html # Listagem de templates
│       ├── template_create.html # Criar template
│       ├── template_edit.html # Editar template
│       ├── admin/            # Templates administrativos
│       └── api_docs.html     # Documentação da API
├── migrations/               # Migrações do banco de dados
│   └── versions/
├── scripts/
│   ├── create_admin.py       # Criar usuário admin
│   └── ...                   # Outros scripts utilitários
├── docs/                     # Documentação técnica
│   ├── README.md             # Índice da documentação
│   ├── FEATURES.md           # Features do sistema
│   ├── QUICK_REFERENCE.md    # Referência rápida
│   ├── api/                  # Documentação da API
│   └── ...                   # Outras docs
├── instance/
│   └── app.db                # Banco de dados SQLite (não commitado)
├── .env                      # Variáveis de ambiente (não commitado)
├── env.example               # Template do .env
├── .gitignore                # Arquivos ignorados pelo Git
├── requirements.txt          # Dependências Python
├── run.py                    # Ponto de entrada da aplicação
└── README.md                 # Este arquivo
```

---

## 🎨 Temas e Customização

### Tema Escuro

O sistema possui suporte completo ao tema escuro, com toggle no header.

**CSS Variables usadas:**
```css
--bg-primary
--bg-secondary
--panel-solid
--panel-bg
--text-primary
--text-secondary
--text-muted
--border-color
--link-color
```

### Customização de Cores

Edite `app/static/css/style.css` para personalizar:
- Cores do tema claro e escuro
- Gradientes dos botões
- Cores dos toasts
- Espaçamentos e tipografia

---

## 🔒 Segurança

- ✅ **CSRF Protection** em todos os formulários
- ✅ **@login_required** em rotas protegidas
- ✅ **Role-Based Access Control** (Admin, Editor, Viewer)
- ✅ **Validação de dados** no backend e frontend
- ✅ **Sanitização de inputs**
- ✅ **Proteção contra SQL Injection** (ORM)
- ✅ **Senhas hasheadas** com Werkzeug
- ✅ **Tokens JWT** para autenticação da API

---

## 🐛 Solução de Problemas

### "no such table" Error

Se receber `sqlite3.OperationalError: no such table`:

```bash
flask --app run.py db migrate -m "sync schema"
flask --app run.py db upgrade
```

### Ambiente Virtual não Ativa (Windows)

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### Dependências não Instaladas

```bash
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### Reset do Banco de Dados

```bash
rm instance/app.db
flask --app run.py db upgrade
python -m scripts.create_admin --email admin@local --display-name "Admin"
```

---

## 📊 Estatísticas do Projeto

- **Total de funcionalidades:** 20+
- **Total de rotas web:** ~38
- **Total de rotas API:** ~34
- **Suporte a temas:** Claro + Escuro
- **Idioma do código:** Inglês
- **Idioma da interface:** Português (BR)
- **Responsivo:** Sim (mobile-first)

---

## 🚀 Roadmap

### Features Planejadas

- [ ] Paginação nas listagens
- [ ] Exportação de dados (CSV, Excel, PDF)
- [ ] Gráficos e estatísticas
- [ ] Histórico de alterações
- [ ] Notificações por email
- [ ] Auto-post em redes sociais (integração)
- [ ] PWA (Progressive Web App)
- [ ] Multi-idioma (EN, ES)
- [ ] Sistema de comentários em ofertas
- [ ] Sistema de favoritos

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fork o projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👨‍💻 Autor

**Willian Jesus**

---

## 🙏 Agradecimentos

- [Flask](https://flask.palletsprojects.com/) - Framework web
- [Bootstrap](https://getbootstrap.com/) - Framework CSS
- [Bootstrap Icons](https://icons.getbootstrap.com/) - Ícones
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM

---

## 📞 Suporte

Para suporte, abra uma issue no GitHub ou entre em contato.

---

**Desenvolvido com ❤️ e Python**

