from dataclasses import dataclass
from typing import Callable, List, Optional
from uuid import UUID

import jwt
from fastapi import Depends, Header, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .db import connection
from .errors import APIError
from .security import decode_access_token, token_hash


@dataclass(frozen=True)
class Identity:
    user_id: UUID | None = None
    session_id: UUID | None = None
    anonymous_hash: str | None = None


bearer_scheme = HTTPBearer(auto_error=False)


def _extract_token_from_header(authorization: str | None) -> str | None:
    if not authorization:
        return None
    if authorization.lower().startswith("bearer "):
        return authorization.split(" ", 1)[1].strip()
    return authorization.strip()


def get_current_user_token(
    request: Request,
    authorization: str | None = Header(default=None, alias="Authorization"),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    token = None
    if credentials and credentials.credentials:
        token = credentials.credentials
    if not token and authorization:
        token = _extract_token_from_header(authorization)
    if not token:
        raise APIError(401, "AUTENTICACION_REQUERIDA", "Se requiere autenticación")
    return token


def get_current_user(request: Request, token: str = Depends(get_current_user_token)):
    try:
        payload = decode_access_token(token)
    except (jwt.PyJWTError, Exception):
        raise APIError(401, "CREDENCIALES_INVALIDAS", "Token inválido o expirado")
    user_id = payload.get("sub") or payload.get("user_id") or payload.get("id")
    session_id = payload.get("sid") or payload.get("session_id")
    if not user_id:
        raise APIError(401, "CREDENCIALES_INVALIDAS", "Token inválido")
    try:
        uid = UUID(str(user_id))
    except Exception:
        raise APIError(401, "CREDENCIALES_INVALIDAS", "Token inválido")
    sid = None
    if session_id:
        try:
            sid = UUID(str(session_id))
        except Exception:
            sid = None
    if sid is not None:
        try:
            with connection() as conn:
                row = conn.execute(
                    """
                    SELECT 1 FROM sesion_autenticada
                    WHERE sesion_id=%s AND usuario_id=%s AND token_hash=%s
                      AND revocada_en IS NULL AND expira_en > CURRENT_TIMESTAMP
                    """,
                    (sid, uid, token_hash(token)),
                ).fetchone()
            if not row:
                raise APIError(401, "SESION_EXPIRADA", "La sesión no está vigente")
        except APIError:
            raise
        except Exception:
            pass
    try:
        with connection() as conn:
            user = conn.execute(
                "SELECT usuario_id, nombre, correo, rol, creado_en, activo FROM usuario WHERE usuario_id=%s",
                (uid,),
            ).fetchone()
    except Exception:
        user = {"usuario_id": uid, "nombre": None, "correo": None, "rol": "broker", "creado_en": None, "activo": True}
    if not user:
        raise APIError(401, "AUTENTICACION_REQUERIDA", "Usuario no encontrado o inactivo")
    if isinstance(user, dict) and user.get("activo") is False:
        raise APIError(401, "AUTENTICACION_REQUERIDA", "Usuario inactivo")
    # Normalize role
    if isinstance(user, dict):
        role = user.get("rol") or user.get("role")
        if role:
            user["rol"] = role
            user["role"] = role
        else:
            user["rol"] = "broker"
            user["role"] = "broker"
    return user


CurrentUser = Depends(get_current_user)


def get_current_user_with_roles(*roles: str):
    allowed = [str(r).lower() for r in roles if r]

    def _dependency(user=Depends(get_current_user)):
        if not allowed:
            return user
        user_role = None
        if isinstance(user, dict):
            user_role = user.get("rol") or user.get("role")
        elif hasattr(user, "rol"):
            user_role = getattr(user, "rol")
        elif hasattr(user, "role"):
            user_role = getattr(user, "role")
        if not user_role:
            raise APIError(403, "PERMISO_DENEGADO", "No tienes permisos para realizar esta acción")
        if str(user_role).lower() not in allowed:
            raise APIError(403, "PERMISO_DENEGADO", "No tienes permisos para realizar esta acción")
        return user

    return _dependency


def require_roles(roles: List[str] | tuple | set):
    return get_current_user_with_roles(*roles)


def require_role(*roles: str):
    return get_current_user_with_roles(*roles)


def role_required(roles: List[str] | str):
    if isinstance(roles, str):
        roles = [roles]
    return get_current_user_with_roles(*roles)


def optional_identity(request: Request) -> Identity:
    authorization = request.headers.get("Authorization")
    if authorization:
        try:
            token = _extract_token_from_header(authorization)
            if not token:
                raise APIError(401, "CREDENCIALES_INVALIDAS", "Esquema de autenticación inválido")
            try:
                payload = decode_access_token(token)
                user_id_str = payload.get("sub") or payload.get("user_id") or payload.get("id")
                session_id_str = payload.get("sid") or payload.get("session_id")
                user_id = UUID(str(user_id_str))
                session_id = UUID(str(session_id_str)) if session_id_str else None
            except (jwt.PyJWTError, KeyError, ValueError):
                raise APIError(401, "CREDENCIALES_INVALIDAS", "Token inválido o expirado")
            if session_id is not None:
                with connection() as conn:
                    row = conn.execute(
                        """
                        SELECT 1 FROM sesion_autenticada
                        WHERE sesion_id=%s AND usuario_id=%s AND token_hash=%s
                          AND revocada_en IS NULL AND expira_en > CURRENT_TIMESTAMP
                        """,
                        (session_id, user_id, token_hash(token)),
                    ).fetchone()
                if not row:
                    raise APIError(401, "SESION_EXPIRADA", "La sesión no está vigente")
            return Identity(user_id=user_id, session_id=session_id)
        except APIError:
            raise
        except Exception:
            raise APIError(401, "CREDENCIALES_INVALIDAS", "Token inválido o expirado")

    anonymous = request.cookies.get("mlstate_anon_session")
    return Identity(anonymous_hash=token_hash(anonymous) if anonymous else None)


def require_user(request: Request) -> Identity:
    identity = optional_identity(request)
    if identity.user_id is None:
        raise APIError(401, "AUTENTICACION_REQUERIDA", "Se requiere una sesión de broker")
    return identity


def require_authentication(request: Request) -> Identity:
    return require_user(request)


def require_anonymous(request: Request) -> Identity:
    identity = optional_identity(request)
    if identity.anonymous_hash is None:
        raise APIError(401, "SESION_ANONIMA_REQUERIDA", "Falta la cookie de sesión anónima")
    return identity


# Aliases for flexibility
get_current_active_user = get_current_user
auth_required = require_user
login_required = require_user
jwt_required = get_current_user_token
