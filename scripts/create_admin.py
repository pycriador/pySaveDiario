from __future__ import annotations

import argparse
import getpass

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.extensions import db
from app.models import RoleEnum, User


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Criar usuário administrador inicial para pySave Diário."
    )
    parser.add_argument("--email", required=True, help="E-mail único do administrador.")
    parser.add_argument(
        "--display-name",
        default="Administrador",
        help="Nome de exibição do administrador.",
    )
    parser.add_argument(
        "--password",
        help="Senha do administrador. Se omitido, será solicitado com segurança.",
    )
    parser.add_argument(
        "--role",
        choices=[role.value for role in RoleEnum if role != RoleEnum.MEMBER],
        default=RoleEnum.ADMIN.value,
        help="Papel do usuário (admin ou editor).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    password = args.password or getpass.getpass("Senha para o usuário: ")
    if not password:
        raise SystemExit("Senha obrigatória.")

    app = create_app()
    with app.app_context():
        existing = User.query.filter_by(email=args.email).first()
        if existing:
            raise SystemExit("Usuário já existe. Nada foi alterado.")

        user = User(
            email=args.email,
            display_name=args.display_name,
            role=RoleEnum(args.role),
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"Usuário {user.display_name} ({user.role.value}) criado com sucesso.")


if __name__ == "__main__":
    main()

