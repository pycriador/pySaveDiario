from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)

INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)


def _build_database_uri() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    engine = os.getenv("DB_ENGINE", "sqlite").lower()
    if engine == "sqlite":
        sqlite_name = os.getenv("SQLITE_DB_NAME", "app.db")
        return f"sqlite:///{INSTANCE_DIR / sqlite_name}"

    user = quote_plus(os.getenv("DB_USER", "user"))
    password = quote_plus(os.getenv("DB_PASSWORD", "password"))
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT")
    db_name = quote_plus(os.getenv("DB_NAME", "pysavediario"))

    if engine in {"mariadb", "mysql"}:
        port = port or "3306"
        return f"mariadb+pymysql://{user}:{password}@{host}:{port}/{db_name}"

    if engine in {"postgresql", "postgres"}:
        port = port or "5432"
        return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}"

    raise RuntimeError(
        "DB_ENGINE inválido. Utilize sqlite, mariadb, mysql ou postgresql ou informe DATABASE_URL."
    )


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
    SQLALCHEMY_DATABASE_URI = _build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_DURATION = 60 * 60 * 24 * 7
    TOKEN_EXPIRATION_MINUTES = int(os.getenv("TOKEN_EXPIRATION_MINUTES", "60"))


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True


def get_config(name: str | None) -> type[Config]:
    mapping = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }
    if not name:
        return mapping.get(os.getenv("FLASK_ENV", "development"), DevelopmentConfig)
    return mapping.get(name, DevelopmentConfig)

