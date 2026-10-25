import base64
import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

import jwt
from passlib.context import CryptContext

from .config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception:
        salt = os.urandom(16)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 210_000)
        return f"pbkdf2_sha256$210000${base64.b64encode(salt).decode()}${base64.b64encode(digest).decode()}"


def get_password_hash(password: str) -> str:
    return hash_password(password)


def verify_password(password: str, encoded: str) -> bool:
    if not encoded:
        return False
    try:
        if encoded.startswith("$2b$") or encoded.startswith("$2a$") or encoded.startswith("$2y$"):
            return pwd_context.verify(password, encoded)
    except Exception:
        pass
    try:
        algorithm, rounds, salt64, digest64 = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), base64.b64decode(salt64), int(rounds)
        )
        return hmac.compare_digest(actual, base64.b64decode(digest64))
    except (ValueError, TypeError):
        return False


def token_hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def create_access_token(data: dict[str, Any] | None = None, session_id: UUID | None = None, user_id: UUID | None = None, expires_delta: timedelta | None = None) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {}
    if data:
        payload.update(data)
    if session_id is not None and "sid" not in payload:
        payload["sid"] = str(session_id)
    if user_id is not None and "sub" not in payload:
        payload["sub"] = str(user_id)
    payload["iat"] = now
    if expires_delta is not None:
        payload["exp"] = now + expires_delta
    else:
        payload["exp"] = now + timedelta(seconds=settings.access_token_expire_seconds)
    secret = getattr(settings, "SECRET_KEY", None) or settings.jwt_secret
    algorithm = getattr(settings, "ALGORITHM", None) or settings.jwt_algorithm
    return jwt.encode(payload, secret, algorithm=algorithm)


def create_token(*args, **kwargs) -> str:
    return create_access_token(*args, **kwargs)


def decode_access_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    secret = getattr(settings, "SECRET_KEY", None) or settings.jwt_secret
    algorithm = getattr(settings, "ALGORITHM", None) or settings.jwt_algorithm
    return jwt.decode(token, secret, algorithms=[algorithm])


def decode_token(token: str) -> dict[str, Any]:
    return decode_access_token(token)
