from datetime import date, datetime
from decimal import Decimal
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class FieldError(ContractModel):
    campo: str
    regla: str
    valorRecibido: str | None = None


class ErrorResponse(ContractModel):
    codigo: str
    mensaje: str
    errores: list[FieldError] | None = None
    traceId: str | None = None


class ColoniaCatalogo(ContractModel):
    coloniaId: UUID
    nombre: str
    codigosPostales: list[str]


class MunicipioCatalogo(ContractModel):
    municipioId: UUID
    nombre: str
    colonias: list[ColoniaCatalogo]


class EstadoCatalogo(ContractModel):
    estadoId: UUID
    nombre: str
    municipios: list[MunicipioCatalogo]


class OpcionCatalogo(ContractModel):
    id: UUID
    nombre: str


class CatalogosResponse(ContractModel):
    estados: list[EstadoCatalogo]
    tiposInmueble: list[OpcionCatalogo]
    usosSuelo: list[OpcionCatalogo]


class ElegibilidadRequest(ContractModel):
    estadoId: UUID
    municipioId: UUID
    coloniaId: UUID | None = None
    codigoPostal: str | None = Field(default=None, pattern=r"^\d{5}$")
    tipoInmuebleId: UUID
    usoSueloId: UUID

    @model_validator(mode="after")
    def una_ubicacion(self):
        if (self.coloniaId is None) == (self.codigoPostal is None):
            raise ValueError("Debe enviar exactamente coloniaId o codigoPostal")
        return self


class ElegibilidadResponse(ContractModel):
    elegible: Literal[True]
    coberturaId: UUID
    colonia: ColoniaCatalogo


class FichaInmuebleInput(ContractModel):
    superficieTerrenoM2: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    superficieConstruidaM2: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    habitaciones: int | None = Field(default=None, ge=1)
    banosCompletos: int | None = Field(default=None, ge=1)
    mediosBanos: int | None = Field(default=None, ge=0)
    estacionamientos: int | None = Field(default=None, ge=0)
    antiguedadAnos: int | None = Field(default=None, ge=0)
    conservacion: Literal["buena", "regular", "mala"] | None = None
    tipoEntrega: str | None = None
    amenidades: list[str] | None = None
    remodelada: bool | None = None
    anioRemodelacion: int | None = Field(default=None, ge=1800)
    cuartoServicio: bool | None = None
    cercaniaParque: bool | None = None

    @model_validator(mode="after")
    def amenidades_unicas(self):
        if self.amenidades is not None and len(self.amenidades) != len(set(self.amenidades)):
            raise ValueError("amenidades debe contener valores únicos")
        return self


class CrearBorradorRequest(ContractModel):
    coberturaId: UUID
    ficha: FichaInmuebleInput | None = None


class ActualizarBorradorRequest(ContractModel):
    coberturaId: UUID
    ficha: FichaInmuebleInput


class ConfirmacionValor(ContractModel):
    campo: str
    valor: Any
    confirmado: Literal[True]


class ConfirmarValoresRequest(ContractModel):
    versionPolitica: str
    confirmaciones: list[ConfirmacionValor] = Field(min_length=1)


class ConfirmacionPendiente(ContractModel):
    campo: str
    valor: Any
    unidad: str | None = None
    causa: str


class BorradorResponse(ContractModel):
    borradorId: UUID
    estado: Literal["incompleto", "requiere_confirmacion", "listo"]
    coberturaId: UUID
    ficha: FichaInmuebleInput
    actualizadoEn: datetime
    errores: list[FieldError]
    confirmacionesPendientes: list[ConfirmacionPendiente]


class CrearEstimacionRequest(ContractModel):
    borradorId: UUID


class InstantaneaCalculo(ContractModel):
    modelo: str
    datos: str
    politica: str


ADVERTENCIA = (
    "Estimación orientativa de MLState. No sustituye un avalúo profesional, "
    "bancario u oficial ni garantiza el precio final de venta"
)


class EstimacionResponse(ContractModel):
    estimacionId: UUID
    consultaId: UUID
    valorMinimo: Decimal = Field(gt=0)
    valorCentral: Decimal = Field(gt=0)
    valorMaximo: Decimal = Field(gt=0)
    moneda: Literal["MXN"]
    precioM2Construccion: Decimal = Field(ge=0)
    margenErrorPorcentaje: Decimal = Field(ge=0)
    nivelConfianza: Literal["baja", "media", "alta"]
    causaConfianza: str | None = None
    explicacion: str = Field(min_length=15, max_length=300)
    fechaCalculo: datetime
    actualizacionDatos: datetime
    versiones: InstantaneaCalculo
    advertencia: Literal[
        "Estimación orientativa de MLState. No sustituye un avalúo profesional, bancario u oficial ni garantiza el precio final de venta"
    ]


class Comparable(ContractModel):
    comparableId: UUID
    orden: int = Field(ge=1, le=5)
    colonia: str
    tipoInmueble: str
    usoSuelo: str
    superficieTerrenoM2: Decimal = Field(gt=0)
    superficieConstruidaM2: Decimal = Field(gt=0)
    precioMXN: Decimal = Field(gt=0)
    fechaReferencia: date
    naturaleza: Literal["cierre", "publicacion", "avaluo"]


class ComparablesResponse(ContractModel):
    estimacionId: UUID
    totalReferenciasValidas: int = Field(ge=0)
    comparables: list[Comparable] = Field(max_length=5)


class GenerarReporteRequest(ContractModel):
    formato: Literal["pdf"] = "pdf"


class ConsultaAnonimaResponse(ContractModel):
    consultaId: UUID
    estado: Literal["borrador", "calculada"]
    recibidaEn: datetime
    expiraEn: datetime
    borrador: BorradorResponse
    estimacion: EstimacionResponse | None = None


class RegistroRequest(ContractModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=120)
    name: str | None = Field(default=None, min_length=1, max_length=120)
    correo: EmailStr | None = Field(default=None, max_length=254)
    email: EmailStr | None = Field(default=None, max_length=254)
    contrasena: str | None = Field(default=None, min_length=10)
    password: str | None = Field(default=None, min_length=10)
    contrasena_confirmacion: str | None = None

    @model_validator(mode="after")
    def normalizar(self):
        if self.nombre is None and self.name is not None:
            self.nombre = self.name
        if self.correo is None and self.email is not None:
            self.correo = self.email
        if self.contrasena is None and self.password is not None:
            self.contrasena = self.password
        if self.nombre is None or self.correo is None or self.contrasena is None:
            raise ValueError("nombre/correo/contrasena son requeridos")
        return self

    @field_validator("contrasena")
    @classmethod
    def validar_complejidad(cls, value: str) -> str:
        if not any(char.islower() for char in value) or not any(char.isupper() for char in value) or not any(char.isdigit() for char in value):
            raise ValueError("Debe incluir mayúscula, minúscula y dígito")
        return value


# Aliases
UserRegister = RegistroRequest
RegisterRequest = RegistroRequest


class UsuarioResponse(ContractModel):
    usuarioId: UUID | None = None
    id: UUID | None = None
    nombre: str | None = None
    name: str | None = None
    correo: EmailStr | None = None
    email: EmailStr | None = None
    rol: Literal["broker"] | str | None = "broker"
    role: str | None = None
    creadoEn: datetime | None = None
    created_at: datetime | None = None

    @model_validator(mode="after")
    def normalizar(self):
        if self.usuarioId is None and self.id is not None:
            self.usuarioId = self.id
        if self.nombre is None and self.name is not None:
            self.nombre = self.name
        if self.correo is None and self.email is not None:
            self.correo = self.email
        if self.creadoEn is None and self.created_at is not None:
            self.creadoEn = self.created_at
        if self.rol is None and self.role is not None:
            self.rol = self.role
        return self


UserResponse = UsuarioResponse


class LoginRequest(ContractModel):
    correo: EmailStr | None = None
    email: EmailStr | None = None
    contrasena: str | None = None
    password: str | None = None

    @model_validator(mode="after")
    def normalizar(self):
        if self.correo is None and self.email is not None:
            self.correo = self.email
        if self.contrasena is None and self.password is not None:
            self.contrasena = self.password
        if self.correo is None or self.contrasena is None:
            raise ValueError("correo/contrasena son requeridos")
        return self


AuthRequest = LoginRequest


class LoginResponse(ContractModel):
    accessToken: str | None = None
    access_token: str | None = None
    token: str | None = None
    tokenType: Literal["Bearer"] | str | None = "Bearer"
    token_type: str | None = None
    expiresIn: int | None = None
    expires_in: int | None = None
    usuario: UsuarioResponse | None = None
    user: UsuarioResponse | None = None

    @model_validator(mode="after")
    def normalizar(self):
        if self.accessToken is None and self.access_token is not None:
            self.accessToken = self.access_token
        if self.accessToken is None and self.token is not None:
            self.accessToken = self.token
        if self.tokenType is None and self.token_type is not None:
            self.tokenType = self.token_type
        if self.expiresIn is None and self.expires_in is not None:
            self.expiresIn = self.expires_in
        if self.usuario is None and self.user is not None:
            self.usuario = self.user
        return self


Token = LoginResponse
AuthResponse = LoginResponse


class TokenResponse(ContractModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int | None = None


class UserMeResponse(UsuarioResponse):
    pass


class HistorialItem(ContractModel):
    estimacionId: UUID
    fechaCalculo: datetime
    municipio: str
    colonia: str
    valorCentral: Decimal = Field(gt=0)
    moneda: Literal["MXN"]
    nivelConfianza: Literal["baja", "media", "alta"]


class HistorialResponse(ContractModel):
    pagina: int = Field(ge=1)
    tamanoPagina: Literal[20]
    total: int = Field(ge=0)
    elementos: list[HistorialItem] = Field(max_length=20)


class EstimacionDetalleResponse(EstimacionResponse):
    ficha: FichaInmuebleInput
    comparables: list[Comparable] = Field(max_length=5)
