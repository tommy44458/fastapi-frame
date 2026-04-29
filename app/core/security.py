from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import jwt

from config import SERVER_CONFIG


_BCRYPT_ROUNDS = 12
_BCRYPT_MAX_BYTES = 72


def _encode(password: str) -> bytes:
    encoded = password.encode("utf-8")
    if len(encoded) > _BCRYPT_MAX_BYTES:
        raise ValueError(
            f"Password exceeds bcrypt's {_BCRYPT_MAX_BYTES}-byte limit"
        )
    return encoded


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=_BCRYPT_ROUNDS)
    return bcrypt.hashpw(_encode(password), salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(_encode(password), password_hash.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(subject: str, extra_claims: dict[str, Any] | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=SERVER_CONFIG.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload: dict[str, Any] = {"sub": subject, "exp": expire}
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(
        payload,
        SERVER_CONFIG.JWT_SECRET_KEY,
        algorithm=SERVER_CONFIG.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        SERVER_CONFIG.JWT_SECRET_KEY,
        algorithms=[SERVER_CONFIG.JWT_ALGORITHM],
    )
