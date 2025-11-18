# pySaveDiário

Central moderna para gestão de ofertas, wishlists, templates de compartilhamento e equipes.

## Stack

- Python 3.11+
- Flask + Blueprints
- SQLAlchemy + Flask-Migrate
- Flask-Login + Flask-WTF
- Flask-HTTPAuth para Basic e Bearer token
- HTML + CSS + jQuery

## Estrutura

```
pySaveDiario/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── forms.py
│   ├── models.py
│   ├── routes/
│   │   ├── api.py
│   │   └── web.py
│   ├── security.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/main.js
│   └── templates/...
├── requirements.txt
└── run.py
```

## Configuração de ambiente

1. Duplique o arquivo `env.example` para `.env` e ajuste os valores.
2. Para uso local basta manter `DB_ENGINE=sqlite`, que cria `instance/app.db`.
3. Para MariaDB/MySQL defina `DB_ENGINE=mariadb` (ou `mysql`) e ajuste `DB_HOST`, `DB_PORT=3306`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.
4. Para PostgreSQL defina `DB_ENGINE=postgresql` (ou use `DATABASE_URL=postgresql+psycopg://user:senha@host:5432/db`).
5. Também é possível setar `DATABASE_URL` diretamente e ignorar os demais campos.

> Os drivers opcionais já estão listados em `requirements.txt`: `PyMySQL` (MariaDB/MySQL) e `psycopg[binary]` (PostgreSQL).

## Primeiros passos

### Preparar o ambiente virtual

**Windows (PowerShell)**

```powershell
python -m venv .venv
# Se aparecer erro de política de execução, rode:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

**Windows (Prompt de Comando)**

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Inicializar a aplicação

```bash
pip install -r requirements.txt
cp env.example .env  # ajuste os valores conforme necessário
flask --app run.py db init
flask --app run.py db migrate -m "base schema"
flask --app run.py db upgrade
```

### Criar o primeiro administrador

Use o script utilitário (ele pede senha se não informar `--password`):

```bash
python -m scripts.create_admin --email admin@local --display-name "Admin"
```

Também é possível criar um editor inicial:

```bash
python -m scripts.create_admin --email editor@local --display-name "Editor" --role editor
```

## Executar

```
flask --app run.py run --reload
```

### Rotas Web

- `/` resumo do projeto
- `/login` autenticação
- `/dashboard` painel pós login
- `/usuarios`, `/grupos`, `/ofertas`, `/templates`

### Rotas API principais

| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/api/auth/login` | Login por JSON (email/senha) |
| POST | `/api/auth/token` | HTTP Basic Auth &rarr; Bearer token |
| POST | `/api/users` | Cadastro de usuário |
| GET | `/api/users` | Listagem (admin) |
| GET | `/api/groups` | Grupos disponíveis |
| POST | `/api/groups` | Criar grupo (admin/editor) |
| POST/GET | `/api/wishlists` | Gerenciar wishlists |
| POST/GET | `/api/offers` | Criar e filtrar ofertas via URL (?vendor=, ?product= etc.) |
| POST/GET | `/api/templates` | Templates reutilizáveis |
| POST/GET | `/api/namespaces` | Namespaces globais ou por oferta |
| POST/GET | `/api/publications` | Registros de posts compartilhados |

Inclua o header `Authorization: Bearer <token>` após gerar o token em `/api/auth/login` ou `/api/auth/token`.

### Resolvendo “no such table”

Se você receber `sqlite3.OperationalError: no such table`, significa que o banco ainda não foi migrado. Execute novamente:

```bash
flask --app run.py db migrate -m "sync schema"
flask --app run.py db upgrade
```

Certifique-se de que o arquivo `.env` aponta para o banco correto antes de rodar os comandos.

## Namespaces sugeridos

- Perfil: `instagram`, `facebook`, `telegram`, `whatsapp`, `tiktok`, `site`, `email`
- Oferta: `url_oferta`, `fabricante`, `distribuidora`, `empresa`, `lancamento`, `cupom`

## Estilo

O front utiliza um tema escuro com foco em tipografia Inter, cards modernos e responsivos para desktop e mobile. Você pode ajustar cores e interações em `app/static/css/style.css`.
