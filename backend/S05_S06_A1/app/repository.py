from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
from uuid import UUID

from psycopg import Connection

from .dependencies import Identity
from .errors import APIError
from .schemas import ADVERTENCIA, FichaInmuebleInput


FICHA_COLUMNAS = {
    "superficieTerrenoM2": "superficie_terreno_m2",
    "superficieConstruidaM2": "superficie_construida_m2",
    "habitaciones": "habitaciones",
    "banosCompletos": "banos_completos",
    "mediosBanos": "medios_banos",
    "estacionamientos": "estacionamientos",
    "antiguedadAnos": "antiguedad_anos",
    "conservacion": "conservacion",
    "tipoEntrega": "tipo_entrega",
    "remodelada": "remodelada",
    "anioRemodelacion": "anio_remodelacion",
    "cuartoServicio": "cuarto_servicio",
    "cercaniaParque": "cercania_parque",
}


def colonia_response(conn: Connection, colonia_id: UUID) -> dict[str, Any]:
    row = conn.execute(
        "SELECT colonia_id, nombre FROM colonia_catalogo WHERE colonia_id=%s AND activo",
        (colonia_id,),
    ).fetchone()
    if not row:
        raise APIError(404, "COLONIA_NO_ENCONTRADA", "La colonia no existe o no está activa")
    codigos = conn.execute(
        "SELECT codigo_postal FROM colonia_codigo_postal WHERE colonia_id=%s ORDER BY codigo_postal",
        (colonia_id,),
    ).fetchall()
    return {
        "coloniaId": row["colonia_id"],
        "nombre": row["nombre"],
        "codigosPostales": [item["codigo_postal"].strip() for item in codigos],
    }


def assert_cobertura(conn: Connection, cobertura_id: UUID) -> dict[str, Any]:
    row = conn.execute(
        "SELECT * FROM cobertura WHERE cobertura_id=%s AND activa", (cobertura_id,)
    ).fetchone()
    if not row:
        raise APIError(422, "COBERTURA_INVALIDA", "La cobertura no existe o no está activa")
    return row


def assert_draft_access(conn: Connection, borrador_id: UUID, identity: Identity) -> dict[str, Any]:
    if identity.user_id is None and identity.anonymous_hash is None:
        raise APIError(401, "AUTENTICACION_REQUERIDA", "Se requiere token o sesión anónima")
    row = conn.execute(
        """
        SELECT b.*, q.session_token_hash
        FROM borrador b
        LEFT JOIN consulta_anonima q ON q.consulta_id=b.consulta_id
        WHERE b.borrador_id=%s
        """,
        (borrador_id,),
    ).fetchone()
    if not row:
        raise APIError(404, "BORRADOR_NO_ENCONTRADO", "El borrador no existe")
    allowed = (
        identity.user_id is not None and row["usuario_id"] == identity.user_id
    ) or (
        identity.anonymous_hash is not None
        and row["session_token_hash"] == identity.anonymous_hash
    )
    if not allowed:
        raise APIError(403, "RECURSO_AJENO", "El borrador pertenece a otra sesión")
    return row


def assert_estimate_access(conn: Connection, estimacion_id: UUID, identity: Identity) -> dict[str, Any]:
    if identity.user_id is None and identity.anonymous_hash is None:
        raise APIError(401, "AUTENTICACION_REQUERIDA", "Se requiere token o sesión anónima")
    row = conn.execute(
        """
        SELECT e.*, b.usuario_id, q.session_token_hash
        FROM estimacion e
        JOIN borrador b ON b.borrador_id=e.borrador_id
        JOIN consulta_anonima q ON q.consulta_id=e.consulta_id
        WHERE e.estimacion_id=%s
        """,
        (estimacion_id,),
    ).fetchone()
    if not row:
        raise APIError(404, "ESTIMACION_NO_ENCONTRADA", "La estimación no existe")
    allowed = (
        identity.user_id is not None and row["usuario_id"] == identity.user_id
    ) or (
        identity.anonymous_hash is not None
        and row["session_token_hash"] == identity.anonymous_hash
    )
    if not allowed:
        raise APIError(403, "RECURSO_AJENO", "La estimación pertenece a otra sesión")
    return row


def replace_ficha(conn: Connection, borrador_id: UUID, ficha: FichaInmuebleInput) -> None:
    values = ficha.model_dump(exclude={"amenidades"})
    columns = ["borrador_id", *FICHA_COLUMNAS.values()]
    params = [borrador_id, *(values[name] for name in FICHA_COLUMNAS)]
    updates = ", ".join(f"{column}=EXCLUDED.{column}" for column in FICHA_COLUMNAS.values())
    placeholders = ", ".join(["%s"] * len(columns))
    conn.execute(
        f"""
        INSERT INTO ficha_inmueble ({', '.join(columns)}) VALUES ({placeholders})
        ON CONFLICT (borrador_id) DO UPDATE SET {updates}
        """,
        params,
    )
    conn.execute("DELETE FROM ficha_amenidad WHERE borrador_id=%s", (borrador_id,))
    for amenidad in ficha.amenidades or []:
        conn.execute(
            "INSERT INTO ficha_amenidad (borrador_id, amenidad) VALUES (%s, %s)",
            (borrador_id, amenidad),
        )


def draft_state(ficha: FichaInmuebleInput | None, pending: int = 0) -> str:
    if pending:
        return "requiere_confirmacion"
    if ficha is None:
        return "incompleto"
    required = (
        ficha.superficieTerrenoM2,
        ficha.superficieConstruidaM2,
        ficha.habitaciones,
        ficha.banosCompletos,
        ficha.conservacion,
    )
    return "listo" if all(value is not None for value in required) else "incompleto"


def draft_response(conn: Connection, borrador_id: UUID) -> dict[str, Any]:
    draft = conn.execute("SELECT * FROM borrador WHERE borrador_id=%s", (borrador_id,)).fetchone()
    if not draft:
        raise APIError(404, "BORRADOR_NO_ENCONTRADO", "El borrador no existe")
    ficha_row = conn.execute(
        "SELECT * FROM ficha_inmueble WHERE borrador_id=%s", (borrador_id,)
    ).fetchone()
    ficha: dict[str, Any] = {}
    if ficha_row:
        ficha = {api: ficha_row[column] for api, column in FICHA_COLUMNAS.items() if ficha_row[column] is not None}
        amenidades = conn.execute(
            "SELECT amenidad FROM ficha_amenidad WHERE borrador_id=%s ORDER BY amenidad",
            (borrador_id,),
        ).fetchall()
        if amenidades:
            ficha["amenidades"] = [row["amenidad"] for row in amenidades]
    errores = conn.execute(
        "SELECT campo, regla, valor_recibido FROM field_error WHERE borrador_id=%s ORDER BY creado_en",
        (borrador_id,),
    ).fetchall()
    pendientes = conn.execute(
        "SELECT campo, valor, unidad, causa FROM confirmacion_pendiente WHERE borrador_id=%s ORDER BY creada_en",
        (borrador_id,),
    ).fetchall()
    return {
        "borradorId": draft["borrador_id"],
        "estado": draft["estado"],
        "coberturaId": draft["cobertura_id"],
        "ficha": ficha,
        "actualizadoEn": draft["actualizado_en"],
        "errores": [
            {"campo": row["campo"], "regla": row["regla"], "valorRecibido": row["valor_recibido"]}
            for row in errores
        ],
        "confirmacionesPendientes": [
            {"campo": row["campo"], "valor": row["valor"], "unidad": row["unidad"], "causa": row["causa"]}
            for row in pendientes
        ],
    }


def estimate_response(conn: Connection, estimacion_id: UUID) -> dict[str, Any]:
    row = conn.execute(
        """
        SELECT e.*, i.modelo, i.datos, i.politica
        FROM estimacion e JOIN instantanea_calculo i USING (estimacion_id)
        WHERE e.estimacion_id=%s
        """,
        (estimacion_id,),
    ).fetchone()
    if not row:
        raise APIError(404, "ESTIMACION_NO_ENCONTRADA", "La estimación no existe")
    return {
        "estimacionId": row["estimacion_id"],
        "consultaId": row["consulta_id"],
        "valorMinimo": row["valor_minimo"],
        "valorCentral": row["valor_central"],
        "valorMaximo": row["valor_maximo"],
        "moneda": row["moneda"].strip(),
        "precioM2Construccion": row["precio_m2_construccion"],
        "margenErrorPorcentaje": row["margen_error_porcentaje"],
        "nivelConfianza": row["nivel_confianza"],
        "causaConfianza": row["causa_confianza"],
        "explicacion": row["explicacion"],
        "fechaCalculo": row["fecha_calculo"],
        "actualizacionDatos": row["actualizacion_datos"],
        "versiones": {"modelo": row["modelo"], "datos": row["datos"], "politica": row["politica"]},
        "advertencia": row["advertencia"],
    }


def comparables_response(conn: Connection, estimacion_id: UUID) -> dict[str, Any]:
    estimate = conn.execute(
        "SELECT total_referencias_validas FROM estimacion WHERE estimacion_id=%s", (estimacion_id,)
    ).fetchone()
    if not estimate:
        raise APIError(404, "ESTIMACION_NO_ENCONTRADA", "La estimación no existe")
    rows = conn.execute(
        "SELECT * FROM comparable WHERE estimacion_id=%s ORDER BY orden", (estimacion_id,)
    ).fetchall()
    return {
        "estimacionId": estimacion_id,
        "totalReferenciasValidas": estimate["total_referencias_validas"],
        "comparables": [
            {
                "comparableId": row["comparable_id"],
                "orden": row["orden"],
                "colonia": row["colonia"],
                "tipoInmueble": row["tipo_inmueble"],
                "usoSuelo": row["uso_suelo"],
                "superficieTerrenoM2": row["superficie_terreno_m2"],
                "superficieConstruidaM2": row["superficie_construida_m2"],
                "precioMXN": row["precio_mxn"],
                "fechaReferencia": row["fecha_referencia"],
                "naturaleza": row["naturaleza"],
            }
            for row in rows
        ],
    }


def ficha_for_estimate(conn: Connection, borrador_id: UUID) -> FichaInmuebleInput:
    response = draft_response(conn, borrador_id)
    return FichaInmuebleInput.model_validate(response["ficha"])


def calculate_values(ficha: FichaInmuebleInput) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    construida = ficha.superficieConstruidaM2 or Decimal("1")
    terreno = ficha.superficieTerrenoM2 or construida
    price_m2 = Decimal("25000.00")
    central = (construida * price_m2 + terreno * Decimal("3500.00")).quantize(Decimal("0.01"))
    return (
        (central * Decimal("0.90")).quantize(Decimal("0.01")),
        central,
        (central * Decimal("1.10")).quantize(Decimal("0.01")),
        price_m2,
    )


def now_utc() -> datetime:
    return datetime.now(timezone.utc)
