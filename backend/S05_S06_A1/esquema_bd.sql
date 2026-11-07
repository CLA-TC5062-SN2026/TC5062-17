-- MLState: esquema físico PostgreSQL
-- Derivado de diagrama_clases_equipo.puml y openapi_equipo.yaml.

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;

CREATE TYPE categoria_opcion_catalogo AS ENUM ('tipo_inmueble', 'uso_suelo');
CREATE TYPE estado_borrador AS ENUM ('incompleto', 'requiere_confirmacion', 'listo');
CREATE TYPE conservacion_inmueble AS ENUM ('buena', 'regular', 'mala');
CREATE TYPE nivel_confianza AS ENUM ('baja', 'media', 'alta');
CREATE TYPE naturaleza_comparable AS ENUM ('cierre', 'publicacion', 'avaluo');
CREATE TYPE estado_consulta AS ENUM ('borrador', 'calculada');
CREATE TYPE rol_usuario AS ENUM ('broker');

-- Catálogo jerárquico.
CREATE TABLE estado_catalogo (
    estado_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(120) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE UNIQUE INDEX uq_estado_catalogo_nombre
    ON estado_catalogo (LOWER(nombre));

CREATE TABLE municipio_catalogo (
    municipio_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    estado_id UUID NOT NULL,
    nombre VARCHAR(120) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_municipio_estado
        FOREIGN KEY (estado_id) REFERENCES estado_catalogo (estado_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE UNIQUE INDEX uq_municipio_estado_nombre
    ON municipio_catalogo (estado_id, LOWER(nombre));
CREATE INDEX ix_municipio_nombre ON municipio_catalogo (LOWER(nombre));

CREATE TABLE colonia_catalogo (
    colonia_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    municipio_id UUID NOT NULL,
    nombre VARCHAR(160) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_colonia_municipio
        FOREIGN KEY (municipio_id) REFERENCES municipio_catalogo (municipio_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE UNIQUE INDEX uq_colonia_municipio_nombre
    ON colonia_catalogo (municipio_id, LOWER(nombre));
CREATE INDEX ix_colonia_nombre ON colonia_catalogo (LOWER(nombre));

-- El arreglo codigosPostales del API se normaliza para admitir la relación N:M
-- y el caso donde un código postal produce más de una colonia candidata.
CREATE TABLE colonia_codigo_postal (
    colonia_id UUID NOT NULL,
    codigo_postal CHAR(5) NOT NULL,
    PRIMARY KEY (colonia_id, codigo_postal),
    CONSTRAINT fk_codigo_postal_colonia
        FOREIGN KEY (colonia_id) REFERENCES colonia_catalogo (colonia_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT ck_codigo_postal_formato
        CHECK (codigo_postal ~ '^[0-9]{5}$')
);

CREATE INDEX ix_codigo_postal ON colonia_codigo_postal (codigo_postal);

-- OpcionCatalogo representa tanto tipos de inmueble como usos de suelo.
CREATE TABLE opcion_catalogo (
    opcion_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    categoria categoria_opcion_catalogo NOT NULL,
    nombre VARCHAR(120) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT uq_opcion_id_categoria UNIQUE (opcion_id, categoria)
);

CREATE UNIQUE INDEX uq_opcion_categoria_nombre
    ON opcion_catalogo (categoria, LOWER(nombre));
CREATE INDEX ix_opcion_nombre ON opcion_catalogo (LOWER(nombre));

-- Una cobertura es la combinación elegible colonia × tipo × uso.
CREATE TABLE cobertura (
    cobertura_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    colonia_id UUID NOT NULL,
    tipo_inmueble_id UUID NOT NULL,
    tipo_categoria categoria_opcion_catalogo NOT NULL DEFAULT 'tipo_inmueble',
    uso_suelo_id UUID NOT NULL,
    uso_categoria categoria_opcion_catalogo NOT NULL DEFAULT 'uso_suelo',
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT ck_cobertura_tipo_categoria CHECK (tipo_categoria = 'tipo_inmueble'),
    CONSTRAINT ck_cobertura_uso_categoria CHECK (uso_categoria = 'uso_suelo'),
    CONSTRAINT fk_cobertura_colonia
        FOREIGN KEY (colonia_id) REFERENCES colonia_catalogo (colonia_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_cobertura_tipo
        FOREIGN KEY (tipo_inmueble_id, tipo_categoria)
        REFERENCES opcion_catalogo (opcion_id, categoria)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_cobertura_uso
        FOREIGN KEY (uso_suelo_id, uso_categoria)
        REFERENCES opcion_catalogo (opcion_id, categoria)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT uq_cobertura_combinacion
        UNIQUE (colonia_id, tipo_inmueble_id, uso_suelo_id)
);

CREATE INDEX ix_cobertura_colonia_activa ON cobertura (colonia_id, activa);

-- Identidad y sesiones.
CREATE TABLE usuario (
    usuario_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(120) NOT NULL,
    correo CITEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    rol rol_usuario NOT NULL DEFAULT 'broker',
    creado_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT ck_usuario_nombre_no_vacio CHECK (BTRIM(nombre) <> ''),
    CONSTRAINT ck_usuario_correo_longitud CHECK (LENGTH(correo::TEXT) <= 254)
);

-- UNIQUE(correo) crea el índice de búsqueda case-insensitive por ser CITEXT.
CREATE INDEX ix_usuario_nombre ON usuario (LOWER(nombre));

CREATE TABLE sesion_autenticada (
    sesion_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL,
    token_hash CHAR(64) NOT NULL UNIQUE,
    creada_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultima_actividad_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expira_en TIMESTAMPTZ NOT NULL,
    revocada_en TIMESTAMPTZ,
    CONSTRAINT fk_sesion_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuario (usuario_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT ck_sesion_expiracion CHECK (expira_en > creada_en),
    CONSTRAINT ck_sesion_revocacion CHECK (revocada_en IS NULL OR revocada_en >= creada_en)
);

CREATE INDEX ix_sesion_usuario ON sesion_autenticada (usuario_id);
CREATE INDEX ix_sesion_expira_en ON sesion_autenticada (expira_en)
    WHERE revocada_en IS NULL;

CREATE TABLE consulta_anonima (
    consulta_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    estado estado_consulta NOT NULL DEFAULT 'borrador',
    recibida_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expira_en TIMESTAMPTZ NOT NULL,
    session_token_hash CHAR(64) NOT NULL,
    CONSTRAINT ck_consulta_vigencia CHECK (expira_en > recibida_en)
);

CREATE INDEX ix_consulta_session_token_hash ON consulta_anonima (session_token_hash);
CREATE INDEX ix_consulta_expira_en ON consulta_anonima (expira_en);

-- Captura progresiva.
CREATE TABLE borrador (
    borrador_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    estado estado_borrador NOT NULL DEFAULT 'incompleto',
    cobertura_id UUID NOT NULL,
    consulta_id UUID UNIQUE,
    usuario_id UUID,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_borrador_cobertura
        FOREIGN KEY (cobertura_id) REFERENCES cobertura (cobertura_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_borrador_consulta
        FOREIGN KEY (consulta_id) REFERENCES consulta_anonima (consulta_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_borrador_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuario (usuario_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT ck_borrador_un_propietario
        CHECK (NUM_NONNULLS(consulta_id, usuario_id) = 1),
    CONSTRAINT ck_borrador_fechas CHECK (actualizado_en >= creado_en)
);

CREATE INDEX ix_borrador_cobertura ON borrador (cobertura_id);
CREATE INDEX ix_borrador_usuario_actualizado ON borrador (usuario_id, actualizado_en DESC)
    WHERE usuario_id IS NOT NULL;

CREATE TABLE ficha_inmueble (
    borrador_id UUID PRIMARY KEY,
    superficie_terreno_m2 NUMERIC(12,2),
    superficie_construida_m2 NUMERIC(12,2),
    habitaciones INTEGER,
    banos_completos INTEGER,
    medios_banos INTEGER,
    estacionamientos INTEGER,
    antiguedad_anos INTEGER,
    conservacion conservacion_inmueble,
    tipo_entrega VARCHAR(80),
    remodelada BOOLEAN,
    anio_remodelacion INTEGER,
    cuarto_servicio BOOLEAN,
    cercania_parque BOOLEAN,
    CONSTRAINT fk_ficha_borrador
        FOREIGN KEY (borrador_id) REFERENCES borrador (borrador_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT ck_ficha_superficie_terreno
        CHECK (superficie_terreno_m2 IS NULL OR superficie_terreno_m2 > 0),
    CONSTRAINT ck_ficha_superficie_construida
        CHECK (superficie_construida_m2 IS NULL OR superficie_construida_m2 > 0),
    CONSTRAINT ck_ficha_habitaciones CHECK (habitaciones IS NULL OR habitaciones >= 1),
    CONSTRAINT ck_ficha_banos CHECK (banos_completos IS NULL OR banos_completos >= 1),
    CONSTRAINT ck_ficha_medios_banos CHECK (medios_banos IS NULL OR medios_banos >= 0),
    CONSTRAINT ck_ficha_estacionamientos CHECK (estacionamientos IS NULL OR estacionamientos >= 0),
    CONSTRAINT ck_ficha_antiguedad CHECK (antiguedad_anos IS NULL OR antiguedad_anos >= 0),
    CONSTRAINT ck_ficha_anio_remodelacion
        CHECK (anio_remodelacion IS NULL OR anio_remodelacion >= 1800)
);

CREATE TABLE ficha_amenidad (
    borrador_id UUID NOT NULL,
    amenidad VARCHAR(120) NOT NULL,
    PRIMARY KEY (borrador_id, amenidad),
    CONSTRAINT fk_amenidad_ficha
        FOREIGN KEY (borrador_id) REFERENCES ficha_inmueble (borrador_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT ck_amenidad_no_vacia CHECK (BTRIM(amenidad) <> '')
);

CREATE TABLE confirmacion_pendiente (
    confirmacion_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    borrador_id UUID NOT NULL,
    campo VARCHAR(120) NOT NULL,
    valor JSONB NOT NULL,
    unidad VARCHAR(40),
    causa TEXT NOT NULL,
    version_politica VARCHAR(120) NOT NULL,
    creada_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_confirmacion_borrador
        FOREIGN KEY (borrador_id) REFERENCES borrador (borrador_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT uq_confirmacion_borrador_campo UNIQUE (borrador_id, campo),
    CONSTRAINT ck_confirmacion_campo_no_vacio CHECK (BTRIM(campo) <> ''),
    CONSTRAINT ck_confirmacion_causa_no_vacia CHECK (BTRIM(causa) <> '')
);

-- Los errores de validación asociados al borrador se conservan sólo mientras éste exista.
CREATE TABLE field_error (
    field_error_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    borrador_id UUID NOT NULL,
    campo VARCHAR(120) NOT NULL,
    regla TEXT NOT NULL,
    valor_recibido TEXT,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_field_error_borrador
        FOREIGN KEY (borrador_id) REFERENCES borrador (borrador_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT ck_field_error_campo_no_vacio CHECK (BTRIM(campo) <> ''),
    CONSTRAINT ck_field_error_regla_no_vacia CHECK (BTRIM(regla) <> '')
);

CREATE INDEX ix_field_error_borrador ON field_error (borrador_id);

-- Resultado de estimación.
CREATE TABLE estimacion (
    estimacion_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consulta_id UUID NOT NULL UNIQUE,
    borrador_id UUID NOT NULL UNIQUE,
    valor_minimo NUMERIC(19,2) NOT NULL,
    valor_central NUMERIC(19,2) NOT NULL,
    valor_maximo NUMERIC(19,2) NOT NULL,
    moneda CHAR(3) NOT NULL DEFAULT 'MXN',
    precio_m2_construccion NUMERIC(19,2) NOT NULL,
    margen_error_porcentaje NUMERIC(7,4) NOT NULL,
    nivel_confianza nivel_confianza NOT NULL,
    causa_confianza TEXT,
    explicacion VARCHAR(300) NOT NULL,
    fecha_calculo TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizacion_datos TIMESTAMPTZ NOT NULL,
    total_referencias_validas INTEGER NOT NULL DEFAULT 0,
    advertencia TEXT NOT NULL,
    CONSTRAINT fk_estimacion_consulta
        FOREIGN KEY (consulta_id) REFERENCES consulta_anonima (consulta_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_estimacion_borrador
        FOREIGN KEY (borrador_id) REFERENCES borrador (borrador_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT ck_estimacion_valores_positivos
        CHECK (valor_minimo > 0 AND valor_central > 0 AND valor_maximo > 0),
    CONSTRAINT ck_estimacion_rango
        CHECK (valor_minimo <= valor_central AND valor_central <= valor_maximo),
    CONSTRAINT ck_estimacion_moneda CHECK (moneda = 'MXN'),
    CONSTRAINT ck_estimacion_precio_m2 CHECK (precio_m2_construccion >= 0),
    CONSTRAINT ck_estimacion_margen CHECK (margen_error_porcentaje >= 0),
    CONSTRAINT ck_estimacion_explicacion
        CHECK (CHAR_LENGTH(explicacion) BETWEEN 15 AND 300),
    CONSTRAINT ck_estimacion_total_referencias CHECK (total_referencias_validas >= 0),
    CONSTRAINT ck_estimacion_advertencia CHECK (
        advertencia = 'Estimación orientativa de MLState. No sustituye un avalúo profesional, bancario u oficial ni garantiza el precio final de venta'
    )
);

CREATE INDEX ix_estimacion_fecha_calculo ON estimacion (fecha_calculo DESC);
CREATE INDEX ix_estimacion_nivel_confianza ON estimacion (nivel_confianza);

CREATE TABLE instantanea_calculo (
    estimacion_id UUID PRIMARY KEY,
    modelo VARCHAR(120) NOT NULL,
    datos VARCHAR(120) NOT NULL,
    politica VARCHAR(120) NOT NULL,
    CONSTRAINT fk_instantanea_estimacion
        FOREIGN KEY (estimacion_id) REFERENCES estimacion (estimacion_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX ix_instantanea_modelo ON instantanea_calculo (modelo);
CREATE INDEX ix_instantanea_datos ON instantanea_calculo (datos);
CREATE INDEX ix_instantanea_politica ON instantanea_calculo (politica);

CREATE TABLE comparable (
    comparable_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    estimacion_id UUID NOT NULL,
    orden SMALLINT NOT NULL,
    colonia VARCHAR(160) NOT NULL,
    tipo_inmueble VARCHAR(120) NOT NULL,
    uso_suelo VARCHAR(120) NOT NULL,
    superficie_terreno_m2 NUMERIC(12,2) NOT NULL,
    superficie_construida_m2 NUMERIC(12,2) NOT NULL,
    precio_mxn NUMERIC(19,2) NOT NULL,
    fecha_referencia DATE NOT NULL,
    naturaleza naturaleza_comparable NOT NULL,
    CONSTRAINT fk_comparable_estimacion
        FOREIGN KEY (estimacion_id) REFERENCES estimacion (estimacion_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT uq_comparable_estimacion_orden UNIQUE (estimacion_id, orden),
    CONSTRAINT ck_comparable_orden CHECK (orden BETWEEN 1 AND 5),
    CONSTRAINT ck_comparable_superficie_terreno CHECK (superficie_terreno_m2 > 0),
    CONSTRAINT ck_comparable_superficie_construida CHECK (superficie_construida_m2 > 0),
    CONSTRAINT ck_comparable_precio CHECK (precio_mxn > 0)
);

CREATE INDEX ix_comparable_estimacion ON comparable (estimacion_id);
CREATE INDEX ix_comparable_colonia ON comparable (LOWER(colonia));
CREATE INDEX ix_comparable_fecha_referencia ON comparable (fecha_referencia DESC);

-- Asociación que materializa el historial del broker.
CREATE TABLE estimacion_guardada (
    usuario_id UUID NOT NULL,
    estimacion_id UUID NOT NULL,
    guardada_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (usuario_id, estimacion_id),
    CONSTRAINT uq_estimacion_un_propietario UNIQUE (estimacion_id),
    CONSTRAINT fk_guardada_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuario (usuario_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_guardada_estimacion
        FOREIGN KEY (estimacion_id) REFERENCES estimacion (estimacion_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX ix_guardada_usuario_fecha
    ON estimacion_guardada (usuario_id, guardada_en DESC, estimacion_id DESC);

-- Persistencia necesaria para la generación idempotente del PDF.
CREATE TABLE reporte_pdf (
    reporte_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    estimacion_id UUID NOT NULL UNIQUE,
    hash_contenido CHAR(64) NOT NULL,
    ubicacion_objeto TEXT NOT NULL,
    generado_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reporte_estimacion
        FOREIGN KEY (estimacion_id) REFERENCES estimacion (estimacion_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT uq_reporte_hash UNIQUE (hash_contenido)
);

-- Relaciona Idempotency-Key con el único resultado creado.
CREATE TABLE idempotencia_estimacion (
    idempotency_key UUID PRIMARY KEY,
    request_hash CHAR(64) NOT NULL,
    estimacion_id UUID NOT NULL UNIQUE,
    creada_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_idempotencia_estimacion
        FOREIGN KEY (estimacion_id) REFERENCES estimacion (estimacion_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Proyección relacional equivalente a HistorialItem del contrato.
CREATE VIEW v_historial_item AS
SELECT
    eg.usuario_id,
    e.estimacion_id,
    e.fecha_calculo,
    m.nombre AS municipio,
    c.nombre AS colonia,
    e.valor_central,
    e.moneda,
    e.nivel_confianza,
    eg.guardada_en
FROM estimacion_guardada eg
JOIN estimacion e ON e.estimacion_id = eg.estimacion_id
JOIN borrador b ON b.borrador_id = e.borrador_id
JOIN cobertura co ON co.cobertura_id = b.cobertura_id
JOIN colonia_catalogo c ON c.colonia_id = co.colonia_id
JOIN municipio_catalogo m ON m.municipio_id = c.municipio_id;

COMMIT;
