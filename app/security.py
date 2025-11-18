from __future__ import annotations

from functools import wraps
from typing import Callable

from flask import abort
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from .models import RoleEnum, User, UserToken

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme="Bearer")


@basic_auth.verify_password
def verify_password(email: str, password: str) -> User | None:
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None


@token_auth.verify_token
def verify_token(token: str) -> User | None:
    user_token = UserToken.query.filter_by(token=token, revoked=False).first()
    if user_token and user_token.is_valid():
        return user_token.user
    return None


def role_required(*roles: RoleEnum) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = token_auth.current_user()
            if not user or user.role not in roles:
                abort(403, "Permissão insuficiente.")
            return func(*args, **kwargs)

        return wrapper

    return decorator

