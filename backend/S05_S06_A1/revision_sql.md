# Revisión del esquema físico PostgreSQL

## Alcance

El esquema se derivó del modelo de clases consolidado y del contrato OpenAPI. Se aplicó una transformación de modelo lógico a físico: las entidades con identidad y ciclo de vida se representan mediante tablas; los arreglos y relaciones N:M se normalizan; los objetos de respuesta, requests y paginadores se resuelven mediante consultas o vistas y no mediante tablas artificiales.

## Cobertura de clases

| Clase del diseño | Representación física | Revisión |
|---|---|---|
| `EstadoCatalogo` | `estado_catalogo` | Tabla con UUID, nombre, estado activo e índice por nombre. |
| `MunicipioCatalogo` | `municipio_catalogo` | Tabla y FK obligatoria a estado. |
| `ColoniaCatalogo` | `colonia_catalogo` + `colonia_codigo_postal` | El arreglo postal se normalizó y permite que un CP corresponda a varias colonias. |
| `OpcionCatalogo` | `opcion_catalogo` | Una categoría distingue tipo de inmueble y uso de suelo. |
| `Borrador` | `borrador` | Incluye estado, cobertura, propietario y fechas. |
| `FichaInmueble` | `ficha_inmueble` + `ficha_amenidad` | Relación 1:1 con borrador; amenidades sin duplicados. |
| `ConfirmacionPendiente` | `confirmacion_pendiente` | Relación N:1 con borrador y unicidad por campo pendiente. |
| `FieldError` | `field_error` | Relación N:1 con borrador y eliminación en cascada. |
| `Estimacion` | `estimacion` | Incluye todos los campos del response y las invariantes monetarias. |
| `InstantaneaCalculo` | `instantanea_calculo` | Relación 1:1, PK compartida con estimación. |
| `Comparable` | `comparable` | Relación N:1 con estimación, orden único de 1 a 5. |
| `ConsultaAnonima` | `consulta_anonima` | UUID, estado, vigencia y hash de sesión. |
| `Usuario` | `usuario` | UUID, nombre, correo único, rol, fecha y hash de contraseña. |
| `SesionAutenticada` | `sesion_autenticada` | Se almacena hash del token, no el JWT en claro. |
| `HistorialItem` | `estimacion_guardada` + vista `v_historial_item` | La vista reproduce la proyección del API. |
| Enumeraciones | Tipos `ENUM` PostgreSQL | Literales iguales a los schemas OpenAPI. |
| `CatalogosResponse` | Consulta jerárquica | DTO compuesto; no tiene identidad ni ciclo de vida persistente. |
| `ElegibilidadRequest` | Consulta sobre `cobertura` | Request transitorio; la combinación válida se persiste como cobertura. |
| `ElegibilidadResponse` | Proyección de `cobertura` y colonia | DTO transitorio. |
| `ComparablesResponse` | Consulta de `estimacion` y `comparable` | `total_referencias_validas` se conserva en estimación. |
| `HistorialResponse` | Paginación sobre `v_historial_item` | DTO transitorio. |
| `ErrorResponse` | Construcción de la capa API | No se persiste porque representa una respuesta HTTP. |

Además se incorporaron `cobertura`, `estimacion_guardada`, `reporte_pdf` e `idempotencia_estimacion`. Son estructuras físicas requeridas por las relaciones, el historial, RF-23 y la cabecera `Idempotency-Key`; no agregan campos al contrato público.

## Revisión por criterio

### ¿Están representadas todas las entidades del diagrama?

Sí. Todas las clases persistentes tienen tabla. Las clases con estereotipo request/response y los contenedores paginados están identificados explícitamente como DTOs y se obtienen mediante consultas; crear una tabla para cada uno duplicaría datos y rompería la normalización.

### ¿Están todos los atributos necesarios?

Sí. Los nombres `camelCase` del API se transformaron a `snake_case` sin cambiar su significado. Se agregaron únicamente atributos internos indispensables:

- `password_hash`, porque la contraseña nunca debe almacenarse en claro;
- campos de creación, actualización, expiración y revocación;
- indicadores `activo` de catálogo;
- hashes para sesión, reporte e idempotencia;
- `total_referencias_validas`, requerido por `ComparablesResponse`.

### ¿Las llaves foráneas reflejan las relaciones y cardinalidades?

Sí, después de las siguientes correcciones:

1. Se implementó estado → municipio → colonia mediante FKs obligatorias y `ON DELETE RESTRICT`.
2. La composición borrador → ficha usa la PK del borrador como PK/FK de ficha, garantizando como máximo una ficha por borrador.
3. `consulta_id` es `UNIQUE` en borrador y estimación, reflejando 1:1 y 1:0..1.
4. La instantánea usa PK compartida con estimación, garantizando 1:1.
5. El orden de comparable está restringido a 1–5 y es único dentro de la estimación; esto limita físicamente a cinco comparables.
6. El historial se implementó como asociación usuario–estimación y `UNIQUE(estimacion_id)` impide dos propietarios.
7. La cobertura valida que sus dos opciones pertenezcan respectivamente a las categorías tipo de inmueble y uso de suelo mediante FKs compuestas.

La obligatoriedad de que una estimación tenga una instantánea se completa en la misma transacción de aplicación. Una FK desde la tabla padre hacia la hija produciría una dependencia circular innecesaria.

### ¿Los tipos son coherentes con OpenAPI?

| OpenAPI | PostgreSQL | Aplicación |
|---|---|---|
| `string/uuid` | `UUID` | Identificadores y `Idempotency-Key`. |
| `string/date-time` | `TIMESTAMPTZ` | Instantes en UTC. |
| `string/date` | `DATE` | Fecha de referencia de comparables. |
| `number/double` monetario | `NUMERIC(19,2)` | Evita errores binarios de redondeo. |
| `number/double` superficie | `NUMERIC(12,2)` | Conserva máximo dos decimales. |
| `integer` | `INTEGER` o `SMALLINT` | Conteos y orden. |
| `boolean` | `BOOLEAN` | Indicadores y opcionales. |
| arreglo único | tabla hija con PK compuesta | Códigos postales y amenidades. |
| valor sin schema | `JSONB` | Valor de confirmación pendiente. |
| enumeración | `ENUM` PostgreSQL | Estados, confianza, naturaleza, conservación y rol. |

### ¿Hay restricciones de negocio faltantes?

Se añadieron durante la revisión:

- correo único sin distinguir mayúsculas mediante `CITEXT`;
- áreas positivas y conteos dentro de sus mínimos;
- rango `valor_minimo <= valor_central <= valor_maximo` y valores positivos;
- moneda limitada a `MXN`;
- explicación de 15 a 300 caracteres;
- advertencia normativa exacta;
- códigos postales de cinco dígitos;
- vigencias posteriores a la creación;
- exactamente un propietario de borrador: sesión anónima o usuario;
- una combinación de cobertura sin duplicados;
- máximo cinco comparables mediante orden único restringido a 1–5.

Las reglas que dependen de varias filas o del estado del modelo —mínimo de referencias, deduplicación del dataset, contenido semántico de la explicación y obligatoriedad completa antes de marcar un borrador como `listo`— deben validarse en el servicio de dominio dentro de una transacción. Implementarlas como `CHECK` no sería correcto porque PostgreSQL no permite consultas a otras filas desde esa restricción.

## Índices revisados

Se agregaron índices para correo, nombres de catálogos, código postal, cobertura activa por colonia, propietario/fecha de borrador, expiración de sesiones y consultas, fecha/confianza de estimación, versiones de instantánea, colonia/fecha de comparables e historial por usuario y fecha descendente. No se duplicaron índices ya creados por PK o `UNIQUE`.

## Correcciones aplicadas al primer diseño

1. Se sustituyeron números de punto flotante por `NUMERIC` para dinero y superficies.
2. Se normalizaron códigos postales y amenidades en tablas hijas.
3. Se evitó almacenar JWT y contraseñas en claro; sólo se conservan hashes.
4. Se añadió la entidad física de cobertura para resolver la elegibilidad y sus FKs categorizadas.
5. Se separó la instantánea de cálculo en una tabla 1:1 inmutable.
6. Se corrigió la cardinalidad de comparables a 0..5 mediante `orden` restringido.
7. Se modeló el historial como asociación, no como copia de la estimación.
8. Se añadieron reporte e idempotencia para sostener los comportamientos definidos por el API.
9. Se creó `v_historial_item` para producir el schema de historial sin desnormalizar datos.

## Evidencia de importación

El script se importó en una instancia limpia de **PostgreSQL 16.15** ejecutada en el contenedor `mlstate-postgres-validation`, usando `psql -v ON_ERROR_STOP=1`. La ejecución alcanzó `COMMIT` sin errores.

Resumen obtenido desde `information_schema`:

| Verificación | Resultado |
|---|---:|
| Tablas base en el schema `public` | 20 |
| Tablas con llave primaria | 20 |
| Restricciones de llave foránea | 22 |
| Vistas | 1 |

Salida equivalente a `\dt`:

```text
borrador
cobertura
colonia_catalogo
colonia_codigo_postal
comparable
confirmacion_pendiente
consulta_anonima
estado_catalogo
estimacion
estimacion_guardada
ficha_amenidad
ficha_inmueble
field_error
idempotencia_estimacion
instantanea_calculo
municipio_catalogo
opcion_catalogo
reporte_pdf
sesion_autenticada
usuario
```

La consulta `\dv` confirmó la vista `v_historial_item`. También se consultó `information_schema.table_constraints` para confirmar que todas las tablas tienen PK y que las FKs referencian las tablas previstas. La base permanece disponible en el contenedor indicado y puede inspeccionarse con:

```bash
docker exec mlstate-postgres-validation psql -U mlstate -d mlstate -c '\dt'
```

## Correcciones al código generado

Se contrastaron automáticamente las rutas registradas por FastAPI con `openapi_equipo.yaml`. El resultado final fue **19 de 19 operaciones coincidentes** en ruta, método y códigos de éxito; no se agregaron endpoints CRUD ajenos al contrato.

Durante la implementación y las pruebas se aplicaron estas correcciones:

1. Se montaron todas las rutas bajo `/api/v1`, respetando el `server.url` del OpenAPI.
2. Se preservaron los códigos alternativos `200/201` de `PUT /estimaciones-guardadas/{estimacionId}` para distinguir una asociación existente de una nueva.
3. Se configuraron `Location`, `Set-Cookie`, `Cache-Control` y `Content-Disposition` en las operaciones que los especifican.
4. Se reemplazó la respuesta de validación predeterminada de FastAPI por `ErrorResponse`, con `codigo`, `mensaje`, `errores` y `traceId`.
5. Se corrigió la ausencia de credenciales en recursos protegidos para responder `401`; `403` queda reservado para recursos de otra identidad o sesión.
6. Se agregó respuesta `409` al intentar modificar o confirmar un borrador que ya produjo una estimación.
7. Se ajustó la validación de contraseña a la regla del OpenAPI (longitud mínima, mayúscula, minúscula y dígito) mediante un validador compatible con Pydantic.
8. Se normalizó la serialización de UUID, fechas, `Decimal` y nombres `camelCase` para que las respuestas coincidan con los schemas públicos.
9. La documentación expuesta en `/api/v1/openapi.json` utiliza directamente el contrato consolidado, evitando divergencias entre documentación y fuente de verdad.
10. Se omitieron de las respuestas las propiedades opcionales sin valor; no se serializan como `null` porque el contrato las declara opcionales, pero no `nullable`.

La aplicación valida la conexión a PostgreSQL durante el arranque. La verificación se realizó contra PostgreSQL 16 en `localhost:55432`; el flujo real de prueba cubrió catálogo, elegibilidad, registro, login, creación/lectura/actualización de borrador, creación/lectura de estimación, comparables, PDF, alta/listado/detalle/baja de historial, consulta anónima y cierre de sesiones.
