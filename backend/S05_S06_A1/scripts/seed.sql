-- Datos mínimos repetibles para probar el flujo completo.
WITH e AS (
    INSERT INTO estado_catalogo (nombre) VALUES ('Ciudad de México')
    ON CONFLICT ((LOWER(nombre))) DO UPDATE SET activo=TRUE
    RETURNING estado_id
), m AS (
    INSERT INTO municipio_catalogo (estado_id, nombre)
    SELECT estado_id, 'Benito Juárez' FROM e
    ON CONFLICT (estado_id, (LOWER(nombre))) DO UPDATE SET activo=TRUE
    RETURNING municipio_id
), c AS (
    INSERT INTO colonia_catalogo (municipio_id, nombre)
    SELECT municipio_id, 'Del Valle Centro' FROM m
    ON CONFLICT (municipio_id, (LOWER(nombre))) DO UPDATE SET activo=TRUE
    RETURNING colonia_id
), cp AS (
    INSERT INTO colonia_codigo_postal (colonia_id, codigo_postal)
    SELECT colonia_id, '03100' FROM c ON CONFLICT DO NOTHING
), tipo AS (
    INSERT INTO opcion_catalogo (categoria, nombre) VALUES ('tipo_inmueble', 'Casa')
    ON CONFLICT (categoria, (LOWER(nombre))) DO UPDATE SET activo=TRUE
    RETURNING opcion_id
), uso AS (
    INSERT INTO opcion_catalogo (categoria, nombre) VALUES ('uso_suelo', 'Habitacional')
    ON CONFLICT (categoria, (LOWER(nombre))) DO UPDATE SET activo=TRUE
    RETURNING opcion_id
)
INSERT INTO cobertura (colonia_id, tipo_inmueble_id, uso_suelo_id)
SELECT c.colonia_id, tipo.opcion_id, uso.opcion_id FROM c, tipo, uso
ON CONFLICT (colonia_id, tipo_inmueble_id, uso_suelo_id) DO UPDATE SET activa=TRUE;
