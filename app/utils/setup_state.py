"""
Local setup state for first-run configuration.

State is stored in instance/local_setup.ini (not in Git).
To allow creating the first administrator again (e.g. forgotten password),
delete the file or remove the line first_admin_created=1.
"""
from __future__ import annotations

from pathlib import Path

from flask import current_app

SETUP_FILENAME = "local_setup.ini"
KEY_FIRST_ADMIN = "first_admin_created"


def _get_setup_path() -> Path:
    return Path(current_app.instance_path) / SETUP_FILENAME


def is_first_admin_created() -> bool:
    """Return True if the first admin was already created (setup complete)."""
    path = _get_setup_path()
    if not path.exists():
        return False
    try:
        text = path.read_text(encoding="utf-8").strip()
        return f"{KEY_FIRST_ADMIN}=1" in text or f"{KEY_FIRST_ADMIN}=true" in text
    except OSError:
        return False


def set_first_admin_created() -> None:
    """Mark that the first administrator was created (do not show setup again)."""
    path = _get_setup_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{KEY_FIRST_ADMIN}=1\n", encoding="utf-8")
