from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

import jwt
from fastapi import Request

from .db import connection
from .errors import APIError
from .security import decode_access_token, token_hash


@dataclass(frozen=True)
class Identity:
    user_id: UUID | None = None
    session_id: UUID | None = None
    anonymous_hash: str | None = None


def optional_identity(request: Request) -> Identity:
    authorization = request.headers.get("Authorization")
    if authorization:
        if not authorization.startswith("Bearer "):
            raise APIError(401, "CREDENCIALES_INVALIDAS", "Esquema de autenticación inválido")
        raw = authorization[7:]
        try:
            payload = decode_access_token(raw)
            user_id, session_id = UUID(payload["sub"]), UUID(payload["sid"])
        except (jwt.PyJWTError, KeyError, ValueError):
            raise APIError(401, "CREDENCIALES_INVALIDAS", "Token inválido o expirado")
        with connection() as conn:
            row = conn.execute(
                """
                SELECT 1 FROM sesion_autenticada
                WHERE sesion_id=%s AND usuario_id=%s AND token_hash=%s
                  AND revocada_en IS NULL AND expira_en > CURRENT_TIMESTAMP
                """,
                (session_id, user_id, token_hash(raw)),
            ).fetchone()
        if not row:
            raise APIError(401, "SESION_EXPIRADA", "La sesión no está vigente")
        return Identity(user_id=user_id, session_id=session_id)

    anonymous = request.cookies.get("mlstate_anon_session")
    return Identity(anonymous_hash=token_hash(anonymous) if anonymous else None)


def require_user(request: Request) -> Identity:
    identity = optional_identity(request)
    if identity.user_id is None:
        raise APIError(401, "AUTENTICACION_REQUERIDA", "Se requiere una sesión de broker")
    return identity


def require_anonymous(request: Request) -> Identity:
    identity = optional_identity(request)
    if identity.anonymous_hash is None:
        raise APIError(401, "SESION_ANONIMA_REQUERIDA", "Falta la cookie de sesión anónima")
    return identity
