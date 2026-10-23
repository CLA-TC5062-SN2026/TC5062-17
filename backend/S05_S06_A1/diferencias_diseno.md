# Análisis y resolución de diferencias de diseño

## 1. Fuentes y criterio de consolidación

| Artefacto | Propuesta Anuar | Propuesta de Chris | Fuente de verdad usada |
|---|---|---|---|
| OpenAPI | `openapi_anuar.yaml` | `openapi_chris.yaml` | `SRS_equipo.md` |
| Clases | `diagrama_clases_anuar.mmd` | `diagrama_clases_chris.md` | SRS y schemas de `openapi_equipo.yaml` |
| Componentes | `diagrama_componentes_anuar.mmd` y ADR | `diagrama_componentes_chris.md` y ADR | SRS, contrato consolidado y restricciones del piloto |

Se priorizaron, en este orden: (1) comportamiento normativo y IDs del SRS; (2) semántica HTTP e idempotencia; (3) coherencia entre OpenAPI y clases; (4) simplicidad operativa del piloto.

## 2. Diferencias del OpenAPI

### 2.1 Consenso

Ambas propuestas incluyen los siguientes propósitos, aunque algunas rutas cambian de nombre:

| Propósito consensuado | Anuar | Chris | Resultado |
|---|---|---|---|
| Consultar catálogos | `GET /catalogos` | Igual | Se conserva |
| Verificar elegibilidad | `POST /evaluaciones-elegibilidad` | `POST /catalogos/elegibilidad` | Se conserva la evaluación como recurso |
| Crear y actualizar borrador | `POST /borradores`; `PUT/PATCH /borradores/{borradorId}` | Igual | Se conserva |
| Crear y consultar estimación | `POST /estimaciones`; `GET /estimaciones/{estimacionId}` | Igual | Se conserva |
| Consultar comparables | `GET /estimaciones/{estimacionId}/comparables` | Igual | Se conserva |
| Generar reporte | `PUT /estimaciones/{id}/reportes/principal` | `POST /estimaciones/{id}/reportes` | Se resuelve como PUT idempotente |
| Recuperar/finalizar consulta anónima | `GET/DELETE /consultas/{consultaId}` | Igual | Se conserva |
| Registrar e iniciar/cerrar sesión | `/usuarios`, `/sesiones`, `/sesiones/actual` | Igual | Se conserva |
| Guardar/listar/detallar/eliminar historial | `/estimaciones-guardadas...` | `/historiales...` | Se conserva la colección de estimaciones guardadas |

Los endpoints con coincidencia exacta de ruta y método son: `GET /catalogos`, `POST /borradores`, `PUT` y `PATCH /borradores/{borradorId}`, `POST /estimaciones`, `GET /estimaciones/{estimacionId}`, `GET /estimaciones/{estimacionId}/comparables`, `GET` y `DELETE /consultas/{consultaId}`, `POST /usuarios`, `POST /sesiones` y `DELETE /sesiones/actual`.

### 2.2 Gaps

| Gap | Sólo en | Decisión |
|---|---|---|
| `GET /borradores/{borradorId}` | Chris | **Incorporado** para reanudar captura y respaldar RF-06-AC-2. |
| `GET` separado para descargar un reporte ya generado | Chris | **No incorporado**: el `PUT` estable devuelve el mismo PDF y fecha en creación o reintento, como exige RF-23. |
| Filtros `estadoId` y `municipioId` en catálogo | Anuar | **Conservados** para RF-01-AC-3. |
| Cookie de sesión anónima explícita | Anuar | **Conservada** para aislamiento y vigencia de RF-18. |
| `cookieAuth` de navegador no usado por operaciones | Chris | **No incorporado** para evitar dos esquemas de cookie solapados; se usa `anonymousSession`. |

### 2.3 Conflictos y resolución

| Conflicto | Anuar | Chris | Resolución definitiva |
|---|---|---|---|
| Elegibilidad | `/evaluaciones-elegibilidad` | `/catalogos/elegibilidad` | `/evaluaciones-elegibilidad`: la evaluación tiene respuesta y ciclo conceptual propios; el catálogo sigue siendo consultable. |
| Reporte | `PUT .../reportes/principal`, `200` | `POST .../reportes`, `201`, y `GET` | `PUT .../reportes/principal`, `200`: el SRS exige contenido y fecha estables al repetir. |
| Historial | Recurso `estimaciones-guardadas`, ID de estimación en URI | Recurso `historiales`, ID de historial y POST con body | `PUT /estimaciones-guardadas/{estimacionId}` para guardar sin duplicar; la colección es el historial. |
| Finalización anónima | `DELETE /consultas/{id}` | Mismo diseño; el SRS informativo proponía `POST /finalizar` | `DELETE`, porque elimina el agregado y es idempotente. |
| Confirmaciones | PATCH específico con `versionPolitica` y arreglo | JSON Merge Patch genérico del borrador | Se conserva el request explícito de confirmación para evitar cambios parciales ambiguos. |
| Nombres de campos | IDs y sufijos de unidad (`estimacionId`, `precioMXN`) | `id`, `precio`, `moneda` | Se conservan IDs explícitos y unidades cuando evitan ambigüedad; `moneda` permanece en estimación. |
| Seguridad anónima | Cookie `anonymousSession` | Operaciones abiertas con `security: []` | Cookie anónima para recursos privados de sesión; catálogo, elegibilidad y alta/login permanecen públicos. |
| Trazabilidad de RF-07-AC-3 | Asociada al GET en la propuesta de Anuar | Asociada al POST, donde ocurre el rechazo | Se asocia a `POST /estimaciones`, donde se valida la salida antes de publicarla. |

### 2.4 Aportes de cada integrante al contrato

- **Anuar:** modelado REST basado en recursos, idempotencia con `PUT`, sesión anónima explícita, schemas cerrados con `additionalProperties: false`, filtros/paginación, errores de campo y trazabilidad de criterios fuera de la API.
- **Chris:** recuperación de borradores, mayor separación de descarga/generación, catálogo con claves y banderas de uso, respuesta de elegibilidad con colonias candidatas y documentación extensa de códigos de negocio.
- **Resultado:** se mantuvo el núcleo y la rigurosidad de schemas aportados por Anuar; se añadió la recuperación de borrador propuesta por Chris. Los campos internos de catálogo de Chris no se exponen si el cliente no los necesita, pero pueden persistirse en el modelo físico.

## 3. Diferencias de diagramas de clases

### 3.1 Consenso

Clases o conceptos presentes en ambos: usuario/broker, sesión o consulta anónima, borrador, características/ficha del inmueble, estimación, comparable seleccionado, reporte PDF, estado, municipio, colonia, tipo de inmueble, uso de suelo, cobertura, instantánea/versiones, versión de modelo, conjunto de datos/política y fuente de datos.

Atributos consensuados por concepto:

- Usuario: identificador, correo, hash de contraseña y fecha de registro.
- Borrador: identificador, estado y fecha de actualización.
- Inmueble: superficies, habitaciones, baños, estacionamientos, antigüedad, conservación, remodelación, cuarto de servicio y cercanía a parque.
- Estimación: identificador, mínimo, central, máximo, margen, confianza, explicación y fecha.
- Comparable: identificador, precio, superficie construida, fecha/naturaleza, puntuación y permiso de exhibición.
- Catálogos: identificador, nombre y estado activo.
- Gobierno: versión de modelo, versión de datos, política e instantánea congelada.

### 3.2 Gaps

| Aporte exclusivo o más detallado | Integrante | Decisión |
|---|---|---|
| Jerarquía abstracta `Sesion`, sesión autenticada y consulta agregadora | Anuar | Simplificada en el diagrama API: sesión autenticada y consulta anónima se muestran por sus schemas públicos. |
| `CodigoPostal`, habilitación temporal, registro de mercado y comparable seleccionado separado | Anuar | La resolución postal y separación fuente/selección se conservan como reglas internas; sólo se diagraman campos expuestos para asegurar correspondencia con OpenAPI. |
| `Confirmacion` explícita | Chris | Conservada como `ConfirmacionPendiente` en la respuesta del borrador y request de confirmación. |
| Herencia `ElementoCatalogo` | Chris | No se conserva en el contrato porque los schemas tienen nombres/IDs específicos; se evita ocultar campos heredados. |
| Umbrales de plausibilidad en política | Chris | Permanecen internos; el API expone sólo el identificador congelado de política. |

### 3.3 Conflictos y resolución

| Conflicto | Resolución |
|---|---|
| `FichaInmueble` vs. `CaracteristicasInmueble` | Se adopta `FichaInmueble`, alineada con `FichaInmuebleInput`. |
| Ubicación como cadenas vs. IDs/cobertura | La entrada usa IDs de catálogo y `coberturaId`; las cadenas resumidas sólo aparecen en comparables/historial. |
| `UsuarioBroker` vs. `Usuario` | `Usuario` con rol cerrado `broker`, igual que `UsuarioResponse`. |
| Estimación asociada directamente a usuario o mediante consulta | Toda estimación pertenece a una consulta; opcionalmente aparece en el historial del usuario. Esto separa origen y guardado. |
| Multiplicidad de comparables | `0..5`; la regla 3–5 se aplica únicamente cuando existen al menos tres elegibles. |
| Versiones como entidades completas vs. strings de snapshot | El diagrama público usa `InstantaneaCalculo {modelo, datos, politica}` para coincidir con OpenAPI; las entidades de gobierno quedan internas a persistencia/pipeline. |
| Nombres `id` vs. nombres específicos | Se usan nombres específicos (`estimacionId`, `consultaId`, etc.) para correspondencia exacta con los schemas. |

El diagrama de clases consolidado es deliberadamente un **modelo de contrato/dominio expuesto**: todos sus atributos corresponden a propiedades de request/response del contrato OpenAPI consolidado. Las contraseñas en claro no aparecen en entidades de respuesta; sólo existen como campos `writeOnly` de registro/login.

## 4. Diferencias de diagramas de componentes

### 4.1 Consenso

Ambos diseños incluyen SPA, API backend como monolito modular, PostgreSQL, motor de inferencia desacoplado por interfaz y trabajos programados/pipeline. Coinciden en HTTPS, REST/JSON, persistencia SQL y procesamiento fuera de la ruta síncrona para mantenimiento y entrenamiento.

### 4.2 Gaps

| Elemento | Sólo o más explícito en | Decisión |
|---|---|---|
| Redis para TTL, idempotencia, rate limit y caché | Chris | Incorporado como almacenamiento efímero. |
| Fuente externa de transacciones | Chris | Incorporada como sistema externo de sólo lectura. |
| Almacén de artefactos ML | Chris | Incorporado para versionado y promoción. |
| Sonda externa | Chris | Incorporada para RNF-03. |
| Puente de compartición del SO | Chris | Incorporado porque RF-25 ocurre fuera del backend. |
| Transacciones ACID y trabajos con acceso versionado | Anuar | Conservados mediante PostgreSQL/repositorios y pipeline. |

### 4.3 Conflictos y resolución

- **Motor “componente desacoplado” vs. in-process:** frontera lógica propia, implementación inicial in-process detrás de un puerto; extracción futura condicionada a métricas.
- **Un único almacén vs. Redis adicional:** PostgreSQL es durable y Redis efímero; no existe duplicidad de autoridad.
- **Diagrama genérico vs. C4 con tecnología concreta:** se usa Mermaid estándar con límites, tecnologías e interfaces explícitas, para mantener renderizado portable y suficiente detalle.

### 4.4 Aportes

- **Anuar:** vista simple del flujo principal, transacciones ACID, separación del motor y trabajos programados, y ADR extenso sobre modularidad y evolución.
- **Chris:** tecnologías concretas, Redis, sistemas externos, protocolos, sonda, almacén de artefactos y límites de operación del pipeline.
- **Resultado:** la arquitectura consolidada combina la claridad del flujo principal con los límites y dependencias operativas necesarios para implementar el backend.

## 5. Verificación final

- El contrato OpenAPI consolidado conserva extensiones `x-acceptance-criteria` con IDs existentes en el SRS del equipo; no crea ni renumera IDs.
- Los criterios de interfaz, sistema operativo o proceso interno permanecen documentados en `x-design-gaps` y no generan endpoints artificiales.
- El diagrama de clases consolidado usa los mismos nombres y tipos conceptuales que los schemas del contrato.
- La arquitectura consolidada mantiene la API como fuente de entrada al backend y separa persistencia durable, estado efímero e inferencia.
- Las fuentes originales se conservaron intactas.
