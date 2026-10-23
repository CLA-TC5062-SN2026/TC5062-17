from uuid import uuid4

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class APIError(Exception):
    def __init__(self, status_code: int, codigo: str, mensaje: str, errores=None):
        self.status_code = status_code
        self.codigo = codigo
        self.mensaje = mensaje
        self.errores = errores


def api_error_handler(_: Request, exc: APIError) -> JSONResponse:
    body = {"codigo": exc.codigo, "mensaje": exc.mensaje, "traceId": str(uuid4())}
    if exc.errores:
        body["errores"] = exc.errores
    return JSONResponse(status_code=exc.status_code, content=body)


def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    errores = []
    for error in exc.errors():
        errores.append(
            {
                "campo": ".".join(str(part) for part in error["loc"] if part != "body"),
                "regla": error["msg"],
                "valorRecibido": str(error.get("input"))[:200],
            }
        )
    return JSONResponse(
        status_code=422,
        content={
            "codigo": "DATOS_INVALIDOS",
            "mensaje": "La solicitud contiene datos inválidos",
            "errores": errores,
            "traceId": str(uuid4()),
        },
    )
