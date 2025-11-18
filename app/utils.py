from __future__ import annotations

import re
import unicodedata


def slugify(value: str) -> str:
    normalized = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    cleaned = re.sub(r"[^\w\s-]", "", normalized).strip().lower()
    return re.sub(r"[-\s]+", "-", cleaned) or "item"

