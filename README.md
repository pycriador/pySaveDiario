# pySave Diário

**A modern hub for managing offers, coupons, social-sharing templates, and teams. Full CRUD, REST API, dark theme, secure image upload, and first-run setup in the browser.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [First-Run Setup](#first-run-setup)
- [Project Structure](#project-structure)
- [API](#api)
- [Documentation](#documentation)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Development & Production](#development--production)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**pySave Diário** is a web application for managing product offers, discount coupons, reusable sharing templates for social networks, and user/team administration with role-based access.

### Highlights

- **Offers**: CRUD, image upload, installments, old price/discount, multi-currency, filters.
- **Coupons**: Percentage or fixed discount, min purchase, max discount cap, per-seller.
- **Templates**: Dynamic variables (50+ namespaces), per-network prefix/suffix, HTML editor.
- **Social sharing**: Per-network formatting (WhatsApp, Telegram, Instagram, etc.), copy and share.
- **Admin**: Sellers, categories, manufacturers (with colors), social network config, app settings.
- **First-run**: Create the first administrator and initialize default social networks from the browser—no CLI scripts required.
- **REST API**: Bearer token auth, full resource endpoints, interactive docs at `/api-docs`.
- **UI**: Dark/light theme, Bootstrap 5, toasts, responsive layout. Interface language: Brazilian Portuguese.

---

## Features

### Offers

- Create, edit, delete, list with dynamic filters (seller, category, manufacturer, price range, active/expired).
- Image upload with validation (extension, content-type, Pillow check, size limit, safe path).
- Old price and automatic discount percentage badge.
- Installments: count, value, interest-free flag; full installment text in templates.
- Multi-currency with configurable default and symbols (BRL, USD, EUR, etc.).
- Quick-create for sellers, categories, and manufacturers from the offer form.

### Coupons

- Percentage or fixed discount; optional min purchase and max discount value.
- Active/inactive and expiration date.
- Filter by seller, discount type, active only.
- Used in sharing flow and in templates via namespaces (e.g. `{price_with_coupon}`, `{all_coupons}`).

### Templates

- Reusable text templates with 50+ variable namespaces (product, offer, installments, coupons, user profile, etc.).
- HTML body with Quill.js editor; conversion to plain/text per network when sharing.
- Per–social network prefix/suffix and saved custom text per channel.

### Social Sharing

- Dedicated page per offer: choose network, template, coupons; edit generated text; copy.
- Per-network formatting (e.g. WhatsApp `*bold*`, Telegram `**bold**`).
- Configurable button colors (solid, gradients, or custom CSS) and prefix/suffix per network.
- Default networks (Instagram, Facebook, WhatsApp, Telegram) can be initialized from the admin UI.

### Administration

- **Users & groups**: Roles (Admin, Editor, Member), profile fields, group membership.
- **Sellers, categories, manufacturers**: CRUD, active toggle, optional color for sellers (solid/gradient/CSS).
- **Social networks**: Prefix/suffix, color, active flag; “Configure initial networks” when none exist.
- **Settings**: Default currency and currency symbols.

### First-Run Behavior

- **First administrator**: If no admin user exists, the login page shows “Create first administrator”. After creation, the option is hidden. To show it again (e.g. forgotten password), delete the file `instance/local_setup.ini` (or remove the line `first_admin_created=1`). This file is local only and not committed to Git.
- **Migrations**: Applied automatically on startup when the `migrations` folder exists. If it does not, run `flask db init` (see [Troubleshooting](#troubleshooting)).
- **Social networks**: If no network configs exist, the admin social-networks page shows a button to create the default set (Instagram, Facebook, WhatsApp, Telegram) from the browser.

---

## Tech Stack

| Layer        | Technologies |
|-------------|--------------|
| Backend     | Python 3.11+, Flask 3.x, SQLAlchemy 2, Flask-Login, Flask-WTF, Flask-Migrate (Alembic), Flask-HTTPAuth |
| Frontend    | HTML5, CSS3, JavaScript, Bootstrap 5, Bootstrap Icons, Quill.js |
| Database    | SQLite (default), PostgreSQL or MySQL/MariaDB via env config |
| Auth        | Session (web), HTTP Basic / Bearer token (API) |
| Other       | Pillow (images), python-dotenv, python-slugify |

---

## Installation

### Prerequisites

- **Python 3.11+**
- **pip**
- **Git** (optional, for cloning)

### Steps

1. **Clone the repository** (or download and extract):

   ```bash
   git clone https://github.com/pycriador/pySaveDiario.git
   cd pySaveDiario
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv .venv
   ```

   - **Linux / macOS:** `source .venv/bin/activate`
   - **Windows:** `.\.venv\Scripts\Activate.ps1` or `.\.venv\Scripts\activate.bat`

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:

   ```bash
   cp env.example .env
   ```

   Edit `.env` and set at least:

   - `SECRET_KEY` (use a long random string; see [Configuration](#configuration)).
   - Optionally adjust database and `FLASK_ENV` (see [Configuration](#configuration)).

5. **Run the application** (see [Running the Application](#running-the-application)).

   On first start, migrations run automatically (if the `migrations` folder exists). Then open the app, go to **Login**, and use **“Create first administrator”** if no admin exists. Optionally, in **Administration → Social networks**, use **“Configure initial networks”** to create the default social configs.

---

## Configuration

### Environment variables (`.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment: `development`, `testing`, `production` | `development` |
| `SECRET_KEY` | Secret key for sessions and CSRF | `change-this-secret-key` |
| `TOKEN_EXPIRATION_MINUTES` | API token validity in minutes | `60` |
| `DB_ENGINE` | Database: `sqlite`, `postgresql`, `mariadb`, `mysql` | `sqlite` |
| `SQLITE_DB_NAME` | SQLite filename (under `instance/`) | `app.db` |
| `DATABASE_URL` | Full database URL (overrides DB_* if set) | — |
| `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME` | Used when `DB_ENGINE` is not sqlite and `DATABASE_URL` is not set | — |

### Generate a secure `SECRET_KEY`

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Paste the output into `SECRET_KEY` in `.env`. Never commit `.env` or real secrets to version control.

### Database examples

- **SQLite (default):** `DB_ENGINE=sqlite` and optionally `SQLITE_DB_NAME=app.db`.
- **PostgreSQL:** Set `DB_ENGINE=postgresql` and `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`, or use `DATABASE_URL=postgresql+psycopg://user:pass@host:5432/dbname`.
- **MySQL/MariaDB:** Set `DB_ENGINE=mariadb` (or `mysql`) and the same variables, or `DATABASE_URL=mariadb+pymysql://user:pass@host:3306/dbname`.

---

## Running the Application

### Development

```bash
python run.py
```

Or with the Flask CLI:

```bash
export FLASK_APP=run.py   # Linux/macOS
set FLASK_APP=run.py      # Windows
flask run --reload
```

Open **http://127.0.0.1:5000** in your browser.

### Production

Use a WSGI server (e.g. Gunicorn):

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "run:app"
```

Set `FLASK_ENV=production` and a strong `SECRET_KEY`. Prefer PostgreSQL or MySQL in production. See [Development & Production](#development--production).

---

## First-Run Setup

1. **Start the app** (see [Running the Application](#running-the-application)).
2. **Migrations**: If the `migrations` folder exists, they run on startup. Otherwise see [Troubleshooting](#troubleshooting).
3. **First administrator**:
   - Go to **Login**.
   - If no admin user exists, click **“Create first administrator”**.
   - Fill in name, email, and password; submit.
   - Log in with that account.
4. **Social networks** (optional):
   - Go to **Administration → Social networks**.
   - If the list is empty, click **“Configure initial networks”** to create Instagram, Facebook, WhatsApp, and Telegram with default prefix/suffix. You can edit them afterward.
5. **Other settings**: Configure default currency and options under **Administration → Settings**.

---

## Project Structure

```
pySaveDiario/
├── app/
│   ├── __init__.py           # App factory, migrations on startup
│   ├── config.py              # Configuration from env
│   ├── extensions.py          # Flask extensions (db, migrate, login, csrf)
│   ├── models.py              # SQLAlchemy models
│   ├── forms.py               # WTForms forms
│   ├── security.py            # Auth helpers, role checks
│   ├── routes/
│   │   ├── web.py             # Web routes (login, offers, coupons, admin, etc.)
│   │   └── api.py             # REST API routes
│   ├── utils/
│   │   ├── setup_state.py     # Local first-admin state (instance/local_setup.ini)
│   │   ├── upload.py          # Secure image upload
│   │   ├── currency.py        # Currency symbols
│   │   └── __init__.py        # slugify, etc.
│   ├── static/                # CSS, JS, uploads
│   └── templates/            # Jinja2 templates
├── migrations/                # Alembic migrations (create with flask db init if missing)
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── instance/                  # Instance folder (not in Git)
│   ├── app.db                 # SQLite DB (if used)
│   └── local_setup.ini        # First-admin-created flag (not in Git)
├── docs/                      # Additional documentation
├── .env                       # Local env (not in Git)
├── env.example                # Example env file
├── requirements.txt
├── run.py                     # Entry point
└── README.md
```

---

## API

- **Base URL:** `http://localhost:5000` (or your deployment URL).
- **Auth:** Obtain a token via `POST /api/auth/token` with HTTP Basic (email + password), then send `Authorization: Bearer <token>` on protected endpoints.
- **Interactive docs:** Open **http://localhost:5000/api-docs** in the browser for endpoints, parameters, and examples (cURL, Python, Node.js, PHP).

### Main resource groups

| Resource      | Endpoints (typical)              | Notes |
|---------------|----------------------------------|--------|
| Auth          | `POST /api/auth/token`           | Get Bearer token |
| Users         | GET/POST/PUT/DELETE `/api/users` | Admin or self |
| Offers        | GET/POST/PUT/DELETE `/api/offers` | Filters: vendor, min_price, max_price, etc. |
| Sellers       | GET/POST/PUT/DELETE `/api/sellers` | |
| Categories    | GET/POST/PUT/DELETE `/api/categories` | |
| Manufacturers | GET/POST/PUT/DELETE `/api/manufacturers` | |
| Coupons       | GET/POST/PUT/DELETE `/api/coupons` | |
| Templates     | GET/POST/PUT/DELETE `/api/templates` | |

Details, request/response shapes, and examples are in the in-app docs at `/api-docs`.

---

## Documentation

- **In-app:** `/api-docs` for the REST API.
- **Repo:** The `docs/` folder contains feature and technical notes, for example:
  - `docs/FEATURES.md` – Feature list
  - `docs/SECURE_IMAGE_UPLOAD.md` – Image upload security
  - `docs/INACTIVE_SELLER_FILTER.md` – Inactive seller behavior
  - `docs/QUICK_REFERENCE.md` – Quick reference
  - And other topic-specific guides.

---

## Security

- **CSRF** protection on web forms (Flask-WTF).
- **Authentication**: session-based for the web app; HTTP Basic or Bearer token for the API.
- **Roles**: Admin, Editor, Member; route and API checks by role.
- **Passwords**: hashed (Werkzeug); never stored in plain text.
- **Secrets**: `SECRET_KEY` and credentials via environment variables (e.g. `.env`), not hardcoded.
- **Uploads**: extension, content-type, and Pillow validation; size limit; safe filenames and directory layout.
- **SQL**: ORM (SQLAlchemy) to avoid raw SQL injection.

---

## Troubleshooting

### "Path doesn't exist: migrations"

The `migrations` folder is missing. The app skips running migrations when it does not exist. To create it:

1. Ensure the app can load (it will, because migration run is skipped when the folder is missing).
2. Run:

   ```bash
   export FLASK_APP=run.py
   flask db init
   flask db migrate -m "initial schema from models"
   flask db upgrade
   ```

3. Restart the app. Future starts will run migrations automatically.

### Forgot first administrator password

1. Delete the file `instance/local_setup.ini` (or remove the line `first_admin_created=1` inside it).
2. Restart the app and open **Login**.
3. The **“Create first administrator”** option will appear again. Create a new admin account (you can use the same or a new email if you prefer).

### Database errors (e.g. "no such column")

Migrations may be out of date. From the project root:

```bash
export FLASK_APP=run.py
flask db upgrade
```

If the DB was created from an older set of migrations and you have a new single “initial” migration, you may need to either:

- Start with a fresh DB (e.g. remove `instance/app.db` and run the app again), or  
- Resolve migration history manually (e.g. `flask db stamp` and/or new migrations). Prefer a backup before changing production data.

### Git push / GitHub authentication

GitHub no longer accepts account passwords for Git over HTTPS. Use either:

- A **Personal Access Token (PAT)** as the password when prompted, or  
- **SSH**: add your SSH key to GitHub and switch the remote to `git@github.com:user/pySaveDiario.git`, then use `git push` without a token.

---

## Development & Production

### Development

- Use `FLASK_ENV=development` and `python run.py` or `flask run --reload`.
- SQLite in `instance/app.db` is fine for local work.
- Set a strong `SECRET_KEY` even in dev (e.g. from `secrets.token_hex(32)`).

### Production

- Set `FLASK_ENV=production`.
- Use a production WSGI server (e.g. **Gunicorn**):  
  `gunicorn -w 4 -b 0.0.0.0:5000 "run:app"`.
- Prefer **PostgreSQL** or **MySQL/MariaDB**; set `DATABASE_URL` or the `DB_*` variables accordingly.
- Use a long, random `SECRET_KEY` and keep it only in the server environment (or a secure secret store).
- Serve the app behind a reverse proxy (e.g. Nginx) with HTTPS.
- Do not commit `.env`, `instance/local_setup.ini`, or any file containing secrets.

---

## Contributing

1. Fork the repository.
2. Create a branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Code, comments, and commit messages should be in English; user-facing UI remains in Brazilian Portuguese as per project standards.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

**Built with Python and Flask**
