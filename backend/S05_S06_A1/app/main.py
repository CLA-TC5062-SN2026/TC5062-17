import hashlib
import json
import secrets
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Annotated
from uuid import UUID, uuid4

import psycopg
import yaml
from fastapi import Body, Depends, FastAPI, Header, Query, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from psycopg.types.json import Jsonb

from .config import get_settings
from .db import check_connection, connection
from .dependencies import (
    Identity,
    get_current_user,
    get_current_user_with_roles,
    optional_identity,
    require_anonymous,
    require_role,
    require_roles,
    require_user,
    role_required,
)
from .errors import APIError, api_error_handler, validation_error_handler
from .pdf import build_estimate_pdf
from .repository import (
    assert_cobertura,
    assert_draft_access,
    assert_estimate_access,
    calculate_values,
    colonia_response,
    comparables_response,
    create_user,
    draft_response,
    draft_state,
    estimate_response,
    ficha_for_estimate,
    get_user_by_email,
    now_utc,
    replace_ficha,
    user_to_response,
)
from .schemas import (
    ADVERTENCIA,
    ActualizarBorradorRequest,
    AuthRequest,
    AuthResponse,
    BorradorResponse,
    CatalogosResponse,
    ComparablesResponse,
    ConfirmarValoresRequest,
    ConsultaAnonimaResponse,
    CrearBorradorRequest,
    CrearEstimacionRequest,
    ElegibilidadRequest,
    ElegibilidadResponse,
    EstimacionDetalleResponse,
    EstimacionResponse,
    GenerarReporteRequest,
    HistorialResponse,
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegistroRequest,
    Token,
    TokenResponse,
    UserMeResponse,
    UserRegister,
    UserResponse,
    UsuarioResponse,
)
from .security import create_access_token, get_password_hash, hash_password, token_hash, verify_password


API_PREFIX = "/api/v1"
ROOT = Path(__file__).resolve().parents[1]


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        check_connection()
    except Exception as e:
        print(f"[AVISO] No se pudo conectar a la base de datos al iniciar: {e}", flush=True)
    yield


app = FastAPI(
    title="MLState API",
    version="1.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url=f"{API_PREFIX}/openapi.json",
)
app.add_exception_handler(APIError, api_error_handler)
from fastapi.exceptions import RequestValidationError
app.add_exception_handler(RequestValidationError, validation_error_handler)


def contract_openapi():
    if app.openapi_schema is None:
        with (ROOT / "openapi_equipo.yaml").open(encoding="utf-8") as source:
            app.openapi_schema = yaml.safe_load(source)
    return app.openapi_schema


app.openapi = contract_openapi


def _catalogs(conn, estado_id: UUID | None, municipio_id: UUID | None):
    if municipio_id and not estado_id:
        raise APIError(400, "FILTROS_INCOMPATIBLES", "municipioId requiere estadoId")
    filters = ["e.activo"]
    params = []
    if estado_id:
        filters.append("e.estado_id=%s")
        params.append(estado_id)
    states = conn.execute(
        f"SELECT e.estado_id, e.nombre FROM estado_catalogo e WHERE {' AND '.join(filters)} ORDER BY e.nombre",
        params,
    ).fetchall()
    if estado_id and not states:
        raise APIError(404, "ESTADO_NO_ENCONTRADO", "El estado no existe o no está activo")
    result = []
    municipality_found = False
    for state in states:
        municipal_filters = ["estado_id=%s", "activo"]
        municipal_params = [state["estado_id"]]
        if municipio_id:
            municipal_filters.append("municipio_id=%s")
            municipal_params.append(municipio_id)
        municipalities = conn.execute(
            f"SELECT municipio_id, nombre FROM municipio_catalogo WHERE {' AND '.join(municipal_filters)} ORDER BY nombre",
            municipal_params,
        ).fetchall()
        municipality_found = municipality_found or bool(municipalities)
        municipality_result = []
        for municipality in municipalities:
            colonies = conn.execute(
                "SELECT colonia_id FROM colonia_catalogo WHERE municipio_id=%s AND activo ORDER BY nombre",
                (municipality["municipio_id"],),
            ).fetchall()
            municipality_result.append(
                {
                    "municipioId": municipality["municipio_id"],
                    "nombre": municipality["nombre"],
                    "colonias": [colonia_response(conn, row["colonia_id"]) for row in colonies],
                }
            )
        result.append({"estadoId": state["estado_id"], "nombre": state["nombre"], "municipios": municipality_result})
    if municipio_id and not municipality_found:
        raise APIError(404, "MUNICIPIO_NO_ENCONTRADO", "El municipio no pertenece al estado")
    options = conn.execute(
        "SELECT opcion_id, categoria, nombre FROM opcion_catalogo WHERE activo ORDER BY nombre"
    ).fetchall()
    return {
        "estados": result,
        "tiposInmueble": [{"id": row["opcion_id"], "nombre": row["nombre"]} for row in options if row["categoria"] == "tipo_inmueble"],
        "usosSuelo": [{"id": row["opcion_id"], "nombre": row["nombre"]} for row in options if row["categoria"] == "uso_suelo"],
    }


@app.get(f"{API_PREFIX}/catalogos", response_model=CatalogosResponse, response_model_exclude_none=True)
def obtener_catalogos(estadoId: UUID | None = None, municipioId: UUID | None = None):
    with connection() as conn:
        return _catalogs(conn, estadoId, municipioId)


@app.post(f"{API_PREFIX}/evaluaciones-elegibilidad", response_model=ElegibilidadResponse, response_model_exclude_none=True)
def verificar_elegibilidad(payload: ElegibilidadRequest):
    with connection() as conn:
        if payload.coloniaId:
            colony_ids = [payload.coloniaId]
        else:
            rows = conn.execute(
                """
                SELECT c.colonia_id FROM colonia_codigo_postal cp
                JOIN colonia_catalogo c USING (colonia_id)
                WHERE cp.codigo_postal=%s AND c.municipio_id=%s AND c.activo
                """,
                (payload.codigoPostal, payload.municipioId),
            ).fetchall()
            colony_ids = [row["colonia_id"] for row in rows]
            if len(colony_ids) > 1:
                options = [colonia_response(conn, colony_id) for colony_id in colony_ids]
                return JSONResponse(
                    status_code=409,
                    content=jsonable_encoder({
                        "codigo": "COLONIA_AMBIGUA",
                        "mensaje": "El código postal corresponde a más de una colonia",
                        "opciones": options,
                    }),
                )
        if not colony_ids:
            raise APIError(422, "COBERTURA_NO_DISPONIBLE", "No hay cobertura para la ubicación")
        row = conn.execute(
            """
            SELECT co.cobertura_id, co.colonia_id
            FROM cobertura co
            JOIN colonia_catalogo c USING (colonia_id)
            JOIN municipio_catalogo m USING (municipio_id)
            WHERE co.colonia_id=%s AND m.municipio_id=%s AND m.estado_id=%s
              AND co.tipo_inmueble_id=%s AND co.uso_suelo_id=%s AND co.activa
            """,
            (colony_ids[0], payload.municipioId, payload.estadoId, payload.tipoInmuebleId, payload.usoSueloId),
        ).fetchone()
        if not row:
            raise APIError(422, "COBERTURA_NO_DISPONIBLE", "La combinación no es elegible")
        return {"elegible": True, "coberturaId": row["cobertura_id"], "colonia": colonia_response(conn, row["colonia_id"])}


@app.post(f"{API_PREFIX}/borradores", response_model=BorradorResponse, response_model_exclude_none=True, status_code=201, dependencies=[Depends(require_user)])
def crear_borrador(payload: CrearBorradorRequest, request: Request, response: Response):
    identity = optional_identity(request)
    anonymous_token = None
    with connection() as conn:
        assert_cobertura(conn, payload.coberturaId)
        if identity.user_id:
            consulta_id = None
            usuario_id = identity.user_id
        else:
            anonymous_token = secrets.token_urlsafe(32)
            anonymous_hash = token_hash(anonymous_token)
            consulta_id = conn.execute(
                """
                INSERT INTO consulta_anonima (expira_en, session_token_hash)
                VALUES (CURRENT_TIMESTAMP + (%s * INTERVAL '1 hour'), %s)
                RETURNING consulta_id
                """,
                (get_settings().anonymous_session_expire_hours, anonymous_hash),
            ).fetchone()["consulta_id"]
            usuario_id = None
        state = draft_state(payload.ficha)
        borrador_id = conn.execute(
            """
            INSERT INTO borrador (estado, cobertura_id, consulta_id, usuario_id)
            VALUES (%s, %s, %s, %s) RETURNING borrador_id
            """,
            (state, payload.coberturaId, consulta_id, usuario_id),
        ).fetchone()["borrador_id"]
        if payload.ficha is not None:
            replace_ficha(conn, borrador_id, payload.ficha)
        result = draft_response(conn, borrador_id)
    response.headers["Location"] = f"{API_PREFIX}/borradores/{borrador_id}"
    if anonymous_token:
        response.set_cookie(
            "mlstate_anon_session",
            anonymous_token,
            httponly=True,
            secure=get_settings().cookie_secure,
            samesite="lax",
            max_age=get_settings().anonymous_session_expire_hours * 3600,
        )
    return result


@app.get(f"{API_PREFIX}/borradores/{{borradorId}}", response_model=BorradorResponse, response_model_exclude_none=True, dependencies=[Depends(require_user)])
def obtener_borrador(borradorId: UUID, identity: Identity = Depends(optional_identity)):
    with connection() as conn:
        assert_draft_access(conn, borradorId, identity)
        return draft_response(conn, borradorId)


@app.put(f"{API_PREFIX}/borradores/{{borradorId}}", response_model=BorradorResponse, response_model_exclude_none=True, dependencies=[Depends(require_user)])
def reemplazar_borrador(payload: ActualizarBorradorRequest, borradorId: UUID, identity: Identity = Depends(optional_identity)):
    with connection() as conn:
        assert_draft_access(conn, borradorId, identity)
        if conn.execute("SELECT 1 FROM estimacion WHERE borrador_id=%s", (borradorId,)).fetchone():
            raise APIError(409, "BORRADOR_YA_CALCULADO", "No se puede modificar un borrador ya calculado")
        assert_cobertura(conn, payload.coberturaId)
        replace_ficha(conn, borradorId, payload.ficha)
        conn.execute("DELETE FROM field_error WHERE borrador_id=%s", (borradorId,))
        pending = conn.execute("SELECT count(*) AS total FROM confirmacion_pendiente WHERE borrador_id=%s", (borradorId,)).fetchone()["total"]
        state = draft_state(payload.ficha, pending)
        conn.execute(
            "UPDATE borrador SET cobertura_id=%s, estado=%s, actualizado_en=CURRENT_TIMESTAMP WHERE borrador_id=%s",
            (payload.coberturaId, state, borradorId),
        )
        return draft_response(conn, borradorId)


@app.patch(f"{API_PREFIX}/borradores/{{borradorId}}", response_model=BorradorResponse, response_model_exclude_none=True, dependencies=[Depends(require_user)])
def confirmar_valores_borrador(
    payload: ConfirmarValoresRequest,
    borradorId: UUID,
    identity: Identity = Depends(optional_identity),
):
    with connection() as conn:
        assert_draft_access(conn, borradorId, identity)
        if conn.execute("SELECT 1 FROM estimacion WHERE borrador_id=%s", (borradorId,)).fetchone():
            raise APIError(409, "BORRADOR_YA_CALCULADO", "No se puede confirmar un borrador ya calculado")
        deleted = 0
        for confirmation in payload.confirmaciones:
            result = conn.execute(
                """
                DELETE FROM confirmacion_pendiente
                WHERE borrador_id=%s AND campo=%s AND version_politica=%s
                """,
                (borradorId, confirmation.campo, payload.versionPolitica),
            )
            deleted += result.rowcount
        if deleted != len(payload.confirmaciones):
            raise APIError(409, "CONFIRMACION_INVALIDADA", "La confirmación no coincide con la política vigente")
        ficha = ficha_for_estimate(conn, borradorId)
        pending = conn.execute("SELECT count(*) AS total FROM confirmacion_pendiente WHERE borrador_id=%s", (borradorId,)).fetchone()["total"]
        conn.execute(
            "UPDATE borrador SET estado=%s, actualizado_en=CURRENT_TIMESTAMP WHERE borrador_id=%s",
            (draft_state(ficha, pending), borradorId),
        )
        return draft_response(conn, borradorId)


@app.post(f"{API_PREFIX}/estimaciones", response_model=EstimacionResponse, response_model_exclude_none=True, status_code=201, dependencies=[Depends(require_user)])
def crear_estimacion(
    payload: CrearEstimacionRequest,
    response: Response,
    identity: Identity = Depends(optional_identity),
    idempotency_key: Annotated[UUID | None, Header(alias="Idempotency-Key")] = None,
):
    if idempotency_key is None:
        raise APIError(400, "IDEMPOTENCY_KEY_REQUERIDA", "Falta Idempotency-Key")
    request_hash = hashlib.sha256(str(payload.borradorId).encode()).hexdigest()
    with connection() as conn:
        existing = conn.execute(
            "SELECT request_hash, estimacion_id FROM idempotencia_estimacion WHERE idempotency_key=%s",
            (idempotency_key,),
        ).fetchone()
        if existing:
            if existing["request_hash"] != request_hash:
                raise APIError(409, "CLAVE_REUTILIZADA", "La clave fue usada con otra solicitud")
            result = estimate_response(conn, existing["estimacion_id"])
            response.headers["Location"] = f"{API_PREFIX}/estimaciones/{existing['estimacion_id']}"
            return result
        draft = assert_draft_access(conn, payload.borradorId, identity)
        if draft["estado"] != "listo":
            raise APIError(409, "BORRADOR_INCOMPLETO", "El borrador no está listo para estimarse")
        ficha = ficha_for_estimate(conn, payload.borradorId)
        minimum, central, maximum, price_m2 = calculate_values(ficha)
        consulta_id = draft["consulta_id"]
        if consulta_id is None:
            consulta_id = conn.execute(
                """
                INSERT INTO consulta_anonima (estado, expira_en, session_token_hash)
                VALUES ('calculada', CURRENT_TIMESTAMP + (%s * INTERVAL '1 hour'), %s)
                RETURNING consulta_id
                """,
                (get_settings().anonymous_session_expire_hours, token_hash(f"authenticated:{identity.user_id}")),
            ).fetchone()["consulta_id"]
        else:
            conn.execute("UPDATE consulta_anonima SET estado='calculada' WHERE consulta_id=%s", (consulta_id,))
        estimate_id = uuid4()
        conn.execute(
            """
            INSERT INTO estimacion (
                estimacion_id, consulta_id, borrador_id, valor_minimo, valor_central,
                valor_maximo, precio_m2_construccion, margen_error_porcentaje,
                nivel_confianza, explicacion, actualizacion_datos,
                total_referencias_validas, advertencia
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,10,'media',%s,CURRENT_TIMESTAMP,0,%s)
            """,
            (
                estimate_id, consulta_id, payload.borradorId, minimum, central, maximum,
                price_m2, "Estimación calculada con los datos capturados y la cobertura vigente.", ADVERTENCIA,
            ),
        )
        conn.execute(
            "INSERT INTO instantanea_calculo (estimacion_id, modelo, datos, politica) VALUES (%s,'baseline-1.0','catalogo-1.0','politica-1.0')",
            (estimate_id,),
        )
        conn.execute(
            "INSERT INTO idempotencia_estimacion (idempotency_key, request_hash, estimacion_id) VALUES (%s,%s,%s)",
            (idempotency_key, request_hash, estimate_id),
        )
        result = estimate_response(conn, estimate_id)
    response.headers["Location"] = f"{API_PREFIX}/estimaciones/{estimate_id}"
    return result


@app.get(f"{API_PREFIX}/estimaciones/{{estimacionId}}", response_model=EstimacionResponse, response_model_exclude_none=True, dependencies=[Depends(require_user)])
def obtener_estimacion(estimacionId: UUID, response: Response, identity: Identity = Depends(optional_identity)):
    with connection() as conn:
        assert_estimate_access(conn, estimacionId, identity)
        result = estimate_response(conn, estimacionId)
    response.headers["Cache-Control"] = "no-store"
    return result


@app.get(f"{API_PREFIX}/estimaciones/{{estimacionId}}/comparables", response_model=ComparablesResponse, response_model_exclude_none=True, dependencies=[Depends(require_user)])
def obtener_comparables(estimacionId: UUID, identity: Identity = Depends(optional_identity)):
    with connection() as conn:
        assert_estimate_access(conn, estimacionId, identity)
        return comparables_response(conn, estimacionId)


@app.put(f"{API_PREFIX}/estimaciones/{{estimacionId}}/reportes/principal", dependencies=[Depends(require_user)])
def generar_reporte(
    estimacionId: UUID,
    identity: Identity = Depends(optional_identity),
    payload: GenerarReporteRequest | None = Body(default=None),
):
    with connection() as conn:
        assert_estimate_access(conn, estimacionId, identity)
        estimate = estimate_response(conn, estimacionId)
        content = build_estimate_pdf(str(estimacionId), str(estimate["valorCentral"]))
        digest = hashlib.sha256(content).hexdigest()
        conn.execute(
            """
            INSERT INTO reporte_pdf (estimacion_id, hash_contenido, ubicacion_objeto)
            VALUES (%s,%s,%s)
            ON CONFLICT (estimacion_id) DO UPDATE
            SET hash_contenido=EXCLUDED.hash_contenido,
                ubicacion_objeto=EXCLUDED.ubicacion_objeto,
                generado_en=CURRENT_TIMESTAMP
            """,
            (estimacionId, digest, f"db://reportes/{estimacionId}.pdf"),
        )
    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="estimacion-MLState.pdf"', "Cache-Control": "no-store"},
    )


@app.get(f"{API_PREFIX}/consultas/{{consultaId}}", response_model=ConsultaAnonimaResponse, response_model_exclude_none=True)
def obtener_consulta_anonima(
    consultaId: UUID,
    response: Response,
    identity: Identity = Depends(require_anonymous),
):
    with connection() as conn:
        query = conn.execute("SELECT * FROM consulta_anonima WHERE consulta_id=%s", (consultaId,)).fetchone()
        if not query:
            raise APIError(404, "CONSULTA_NO_ENCONTRADA", "La consulta no existe")
        if query["session_token_hash"] != identity.anonymous_hash:
            raise APIError(403, "RECURSO_AJENO", "La consulta pertenece a otra sesión")
        if query["expira_en"] <= now_utc():
            conn.execute("DELETE FROM consulta_anonima WHERE consulta_id=%s", (consultaId,))
            raise APIError(410, "CONSULTA_EXPIRADA", "La consulta expiró")
        draft = conn.execute("SELECT borrador_id FROM borrador WHERE consulta_id=%s", (consultaId,)).fetchone()
        if not draft:
            raise APIError(404, "BORRADOR_NO_ENCONTRADO", "La consulta no tiene borrador")
        estimate = conn.execute("SELECT estimacion_id FROM estimacion WHERE consulta_id=%s", (consultaId,)).fetchone()
        result = {
            "consultaId": consultaId,
            "estado": query["estado"],
            "recibidaEn": query["recibida_en"],
            "expiraEn": query["expira_en"],
            "borrador": draft_response(conn, draft["borrador_id"]),
            "estimacion": estimate_response(conn, estimate["estimacion_id"]) if estimate else None,
        }
    response.headers["Cache-Control"] = "no-store"
    return result


@app.delete(f"{API_PREFIX}/consultas/{{consultaId}}", status_code=204)
def finalizar_consulta_anonima(consultaId: UUID, identity: Identity = Depends(require_anonymous)):
    with connection() as conn:
        row = conn.execute("SELECT session_token_hash FROM consulta_anonima WHERE consulta_id=%s", (consultaId,)).fetchone()
        if not row:
            raise APIError(404, "CONSULTA_NO_ENCONTRADA", "La consulta no existe")
        if row["session_token_hash"] != identity.anonymous_hash:
            raise APIError(403, "RECURSO_AJENO", "La consulta pertenece a otra sesión")
        conn.execute("DELETE FROM consulta_anonima WHERE consulta_id=%s", (consultaId,))
    return Response(status_code=204)


@app.post(f"{API_PREFIX}/usuarios", response_model=UsuarioResponse, response_model_exclude_none=True, status_code=201)
@app.post("/api/auth/register", response_model=UsuarioResponse, response_model_exclude_none=True, status_code=201)
@app.post(f"{API_PREFIX}/auth/register", response_model=UsuarioResponse, response_model_exclude_none=True, status_code=201)
def registrar_broker(payload: RegistroRequest | RegisterRequest | UserRegister, response: Response):
    try:
        nombre = getattr(payload, "nombre", None) or getattr(payload, "name", None)
        correo = getattr(payload, "correo", None) or getattr(payload, "email", None)
        contrasena = getattr(payload, "contrasena", None) or getattr(payload, "password", None)
        if not nombre or not correo or not contrasena:
            raise APIError(422, "DATOS_INVALIDOS", "Datos incompletos")
        with connection() as conn:
            row = conn.execute(
                """
                INSERT INTO usuario (nombre, correo, password_hash)
                VALUES (%s,%s,%s)
                RETURNING usuario_id, nombre, correo, rol, creado_en
                """,
                (str(nombre).strip(), str(correo).lower(), hash_password(str(contrasena))),
            ).fetchone()
    except psycopg.errors.UniqueViolation:
        raise APIError(409, "CORREO_REGISTRADO", "El correo ya está registrado")
    except APIError:
        raise
    except Exception:
        raise APIError(422, "DATOS_INVALIDOS", "No se pudo registrar el usuario")
    response.headers["Location"] = f"{API_PREFIX}/usuarios/{row['usuario_id']}"
    user_resp = {"usuarioId": row["usuario_id"], "nombre": row["nombre"], "correo": row["correo"], "rol": row["rol"], "creadoEn": row["creado_en"]}
    # Return without password field as required
    return user_resp


@app.post(f"{API_PREFIX}/sesiones", response_model=LoginResponse, response_model_exclude_none=True)
@app.post("/api/auth/login", response_model=LoginResponse, response_model_exclude_none=True)
@app.post(f"{API_PREFIX}/auth/login", response_model=LoginResponse, response_model_exclude_none=True)
@app.post("/api/auth/token", response_model=LoginResponse, response_model_exclude_none=True)
@app.post(f"{API_PREFIX}/auth/token", response_model=LoginResponse, response_model_exclude_none=True)
def iniciar_sesion(payload: LoginRequest | AuthRequest):
    correo = getattr(payload, "correo", None) or getattr(payload, "email", None)
    contrasena = getattr(payload, "contrasena", None) or getattr(payload, "password", None)
    if not correo or not contrasena:
        raise APIError(401, "CREDENCIALES_INVALIDAS", "Correo o contraseña inválidos")
    with connection() as conn:
        user = conn.execute(
            "SELECT * FROM usuario WHERE LOWER(correo)=LOWER(%s) AND activo", (str(correo),)
        ).fetchone()
        if not user or not verify_password(str(contrasena), user["password_hash"]):
            raise APIError(401, "CREDENCIALES_INVALIDAS", "Correo o contraseña inválidos")
        session_id = uuid4()
        # El JWT necesita el session_id; se inserta después de firmarlo para guardar sólo su hash.
        access_token = create_access_token(session_id=session_id, user_id=user["usuario_id"])
        conn.execute(
            """
            INSERT INTO sesion_autenticada (sesion_id, usuario_id, token_hash, expira_en)
            VALUES (%s,%s,%s,CURRENT_TIMESTAMP + (%s * INTERVAL '1 second'))
            """,
            (session_id, user["usuario_id"], token_hash(access_token), get_settings().access_token_expire_seconds),
        )
        user_resp = {"usuarioId": user["usuario_id"], "nombre": user["nombre"], "correo": user["correo"], "rol": user["rol"], "creadoEn": user["creado_en"]}
        return {
            "accessToken": access_token,
            "access_token": access_token,
            "token": access_token,
            "tokenType": "Bearer",
            "token_type": "Bearer",
            "expiresIn": get_settings().access_token_expire_seconds,
            "expires_in": get_settings().access_token_expire_seconds,
            "usuario": user_resp,
            "user": user_resp,
        }


@app.delete(f"{API_PREFIX}/sesiones/actual", status_code=204)
@app.post(f"{API_PREFIX}/auth/logout", status_code=204)
@app.post("/api/auth/logout", status_code=204)
def cerrar_sesion(identity: Identity = Depends(require_user)):
    try:
        with connection() as conn:
            if identity.session_id:
                conn.execute("UPDATE sesion_autenticada SET revocada_en=CURRENT_TIMESTAMP WHERE sesion_id=%s", (identity.session_id,))
    except Exception:
        pass
    return Response(status_code=204)


@app.get("/api/auth/me", response_model=UsuarioResponse, response_model_exclude_none=True)
@app.get(f"{API_PREFIX}/auth/me", response_model=UsuarioResponse, response_model_exclude_none=True)
@app.get(f"{API_PREFIX}/usuarios/me", response_model=UsuarioResponse, response_model_exclude_none=True)
def obtener_usuario_actual(user=Depends(get_current_user)):
    return user_to_response(user) if isinstance(user, dict) else user


@app.get(f"{API_PREFIX}/estimaciones-guardadas", response_model=HistorialResponse, response_model_exclude_none=True)
def listar_historial(
    identity: Identity = Depends(require_user),
    municipioId: UUID | None = None,
    fechaDesde: date | None = None,
    fechaHasta: date | None = None,
    pagina: Annotated[int, Query(ge=1)] = 1,
):
    if fechaDesde and fechaHasta and fechaDesde > fechaHasta:
        raise APIError(400, "RANGO_INVALIDO", "fechaDesde no puede ser posterior a fechaHasta")
    filters = ["v.usuario_id=%s"]
    params: list = [identity.user_id]
    if municipioId:
        filters.append("m.municipio_id=%s")
        params.append(municipioId)
    if fechaDesde:
        filters.append("v.fecha_calculo::date >= %s")
        params.append(fechaDesde)
    if fechaHasta:
        filters.append("v.fecha_calculo::date <= %s")
        params.append(fechaHasta)
    where = " AND ".join(filters)
    with connection() as conn:
        total = conn.execute(
            f"""
            SELECT count(*) AS total FROM v_historial_item v
            JOIN estimacion e USING (estimacion_id)
            JOIN borrador b USING (borrador_id)
            JOIN cobertura co USING (cobertura_id)
            JOIN colonia_catalogo c USING (colonia_id)
            JOIN municipio_catalogo m USING (municipio_id)
            WHERE {where}
            """,
            params,
        ).fetchone()["total"]
        rows = conn.execute(
            f"""
            SELECT v.* FROM v_historial_item v
            JOIN estimacion e USING (estimacion_id)
            JOIN borrador b USING (borrador_id)
            JOIN cobertura co USING (cobertura_id)
            JOIN colonia_catalogo c USING (colonia_id)
            JOIN municipio_catalogo m USING (municipio_id)
            WHERE {where}
            ORDER BY v.guardada_en DESC, v.estimacion_id DESC LIMIT 20 OFFSET %s
            """,
            [*params, (pagina - 1) * 20],
        ).fetchall()
    return {
        "pagina": pagina,
        "tamanoPagina": 20,
        "total": total,
        "elementos": [
            {"estimacionId": row["estimacion_id"], "fechaCalculo": row["fecha_calculo"], "municipio": row["municipio"], "colonia": row["colonia"], "valorCentral": row["valor_central"], "moneda": row["moneda"].strip(), "nivelConfianza": row["nivel_confianza"]}
            for row in rows
        ],
    }


@app.put(f"{API_PREFIX}/estimaciones-guardadas/{{estimacionId}}", response_model=EstimacionResponse, response_model_exclude_none=True)
def guardar_estimacion(estimacionId: UUID, response: Response, identity: Identity = Depends(require_user)):
    with connection() as conn:
        estimate = conn.execute("SELECT estimacion_id FROM estimacion WHERE estimacion_id=%s", (estimacionId,)).fetchone()
        if not estimate:
            raise APIError(404, "ESTIMACION_NO_ENCONTRADA", "La estimación no existe")
        owner = conn.execute("SELECT usuario_id FROM estimacion_guardada WHERE estimacion_id=%s", (estimacionId,)).fetchone()
        if owner and owner["usuario_id"] != identity.user_id:
            raise APIError(403, "RECURSO_AJENO", "La estimación ya pertenece a otro broker")
        created = owner is None
        if created:
            conn.execute("INSERT INTO estimacion_guardada (usuario_id, estimacion_id) VALUES (%s,%s)", (identity.user_id, estimacionId))
        result = estimate_response(conn, estimacionId)
    if created:
        response.status_code = 201
        response.headers["Location"] = f"{API_PREFIX}/estimaciones-guardadas/{estimacionId}"
    return result


def _assert_saved(conn, user_id: UUID, estimate_id: UUID):
    row = conn.execute(
        "SELECT 1 FROM estimacion_guardada WHERE usuario_id=%s AND estimacion_id=%s",
        (user_id, estimate_id),
    ).fetchone()
    if not row:
        raise APIError(404, "ESTIMACION_GUARDADA_NO_ENCONTRADA", "La estimación no está en el historial")


@app.get(f"{API_PREFIX}/estimaciones-guardadas/{{estimacionId}}", response_model=EstimacionDetalleResponse, response_model_exclude_none=True)
def obtener_estimacion_guardada(estimacionId: UUID, identity: Identity = Depends(require_user)):
    with connection() as conn:
        _assert_saved(conn, identity.user_id, estimacionId)
        result = estimate_response(conn, estimacionId)
        estimate = conn.execute("SELECT borrador_id FROM estimacion WHERE estimacion_id=%s", (estimacionId,)).fetchone()
        result["ficha"] = draft_response(conn, estimate["borrador_id"])["ficha"]
        result["comparables"] = comparables_response(conn, estimacionId)["comparables"]
        return result


@app.delete(f"{API_PREFIX}/estimaciones-guardadas/{{estimacionId}}", status_code=204)
def eliminar_estimacion_guardada(estimacionId: UUID, identity: Identity = Depends(require_user)):
    with connection() as conn:
        result = conn.execute(
            "DELETE FROM estimacion_guardada WHERE usuario_id=%s AND estimacion_id=%s",
            (identity.user_id, estimacionId),
        )
        if result.rowcount == 0:
            raise APIError(404, "ESTIMACION_GUARDADA_NO_ENCONTRADA", "La estimación no está en el historial")
    return Response(status_code=204)
