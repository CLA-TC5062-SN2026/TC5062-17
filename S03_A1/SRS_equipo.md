# Especificación de Requerimientos de Software (SRS) — MLState


## Historial de revisiones

| Versión | Fecha | Autor | Descripción |
|---|---|---|---|
| 1.0 | 2026-10-02 | Equipo MLState | Consolidación de los cuatro SRS individuales. Resolución de conflictos documentada en `Diferencias_SRS.md`. Verificación final registrada en `verificacion_final.md`. |

## Decisiones que requieren ratificación

Las siguientes decisiones, documentadas en `Diferencias_SRS.md`, requieren ratificación explícita antes de la aceptación del SRS:

- **D-06** — Métrica de precisión: MdAPE ≤ 15 % por unidad de cobertura (requiere ratificación de negocio).
- **D-09** — Disponibilidad: ≥ 99,0 % con mantenimiento declarado y acotado (requiere validación de operaciones).
- **D-11** — Retención: 60 min anónimos / 12 meses autenticados (requiere revisión legal).
- **D-14** — Plazo de entrega: máximo 4 meses, equipo de 4 (requiere confirmación de PM).


**Proyecto:** MLState — Estimador de precios inmobiliarios basado en Machine Learning
**Estándar:** IEEE 830-1998 (versión simplificada)
**Documento:** Especificación unificada del equipo
**Versión:** 1.0 (consolidada)
**Fecha de emisión:** 2026-10-02
**Estado:** Aprobado como base de diseño arquitectónico y de pruebas, sujeto a los puntos abiertos de la sección 8
**Alcance de la consolidación:** 25 RF · 19 RNF · 11 RD · 74 criterios de aceptación

---

## Documentos consolidados en este SRS

| Documento de origen | Autor | Versión de origen | Aporte principal incorporado |
|---|---|---|---|
| `SRS_final_carlos.md` | carlos | 1.0 | Contrato de API con códigos de negocio, política de credenciales, ciclo CRUD de historial, cobertura de pruebas |
| `SRS_final_mark.md` | mark | s/n | Modelo de roles, códigos HTTP, cuota de anónimos, escalabilidad, SLA de disponibilidad |
| `SRS_final_Anuar.md` | Anuar | 0.4 | Fixtures sintéticos y método de verificación, gobierno de datos autorizados, ciclo de vida anónimo, gobernanza de pendientes |
| `SRS_final_Chris.md` | Chris | 2.0 | Estructura IEEE 830 completa, superficie de API, trazabilidad con identificadores estables, verificación de ambigüedad |

El detalle de qué se tomó de cada documento y cómo se resolvieron los conflictos entre versiones está en el documento complementario `Diferencias_SRS.md`.

---

## 1. Introducción

### 1.1 Propósito

Este documento especifica los requisitos funcionales, no funcionales y de dominio del sistema **MLState**, una aplicación web que estima el precio de un inmueble a partir de sus características físicas y de su ubicación dentro de la cobertura habilitada.

Cada requerimiento funcional (RF-01 a RF-25) cuenta con criterios de aceptación formalizados en formato Dado que / Cuando / Entonces e identificados con `RF-XX-AC-n`. Estos identificadores son la clave de referencia compartida entre este documento, la especificación OpenAPI derivada y las pruebas automatizadas, y **son estables: una vez publicados no se renumeran**.

El documento está dirigido a tres audiencias:

- **Equipo de arquitectura y desarrollo**, que toma decisiones de diseño técnico a partir de los requisitos y sus criterios de aceptación.
- **Equipo de datos / Data Science**, responsable de construir, reentrenar y evaluar el modelo predictivo que sustenta el cálculo de RF-07, y de mantener las habilitaciones y autorizaciones de RF-10.
- **Equipo de QA**, que deriva su plan de pruebas directamente de los identificadores `RF-XX-AC-n` definidos en la sección 3.1.

Este documento **no** sustituye el avalúo comercial de un perito valuador. MLState produce una referencia orientativa de precio, y esa distinción es una restricción de negocio explícita (RD-02) que atraviesa toda la especificación.

### 1.2 Alcance del sistema

#### 1.2.1 MLState está dentro del alcance

- Consulta del catálogo de cobertura disponible y verificación temprana de elegibilidad por ubicación, tipo de inmueble y uso de suelo.
- Captura y validación de las características cuantitativas y cualitativas de un inmueble, con ayuda contextual por campo.
- Cálculo de una estimación de precio presentada como rango de tres valores, con margen de error y nivel de confianza.
- Visualización de propiedades comparables y explicación en lenguaje natural de los factores que inciden en el valor.
- Generación, descarga y compartición de un reporte en PDF.
- Registro e inicio de sesión de un rol autenticado único: `broker`.
- Persistencia, consulta, filtrado y eliminación de un historial de estimaciones por identidad autenticada.
- Consulta anónima completa, incluida la recuperación del resultado dentro de una vigencia de 60 minutos.
- Versionado, evaluación y promoción del modelo predictivo y de los conjuntos de datos.

#### 1.2.2 MLState está explícitamente fuera del alcance

| Fuera de alcance | Justificación normativa |
|---|---|
| Compras, ventas, pagos, contratos y cualquier operación financiera | RD-09 |
| Avalúo comercial con validez legal o bancario | RD-02 |
| Ubicación exacta del inmueble: dirección, calle, número interior y exterior, coordenadas y mapas | RD-08 |
| Mapa interactivo, geocodificación y validación de un punto geográfico | RD-08, D-02 |
| Validación catastral, registral o documental de la propiedad | RD-01 |
| Predicción de la tendencia futura del precio o del valor de renta | RF-07, RD-02 |
| Recomendación de crédito, contacto entre compradores y vendedores | RD-09 |
| Publicación de anuncios inmobiliarios y gestión de clientes (CRM) del broker | RD-09 |
| Aplicaciones nativas de escritorio o móviles | RNF-09 |
| Perfil del broker con agency's datos de contacto en el encabezado del reporte | P-04, P-05 |
| Comparación interactiva y gráfica entre estimaciones guardadas | P-06 |
| Interfaz web de administración del modelo y de los datos de entrenamiento | D-04 |

#### 1.2.3 Reglas de alcance vigentes

| ID | Regla | Decisión de unificación |
|---|---|---|
| **D-01** | El sistema opera en dos modos: consulta anónima sin cuenta y modo autenticado con historial. El modo anónimo no requiere registro en ninguna de sus acciones. | Mayoría (carlos, mark, Chris) |
| **D-02** | La ubicación se captura exclusivamente por catálogo de cobertura (estado, municipio, colonia o código postal resuelto a colonia). No se solicita ni almacena dirección exacta ni coordenadas. | Mayoría (carlos, Anuar) sobre Chris |
| **D-03** | La cobertura admite los tipos de inmueble y usos de suelo habilitados en el catálogo. El uso de suelo admite `habitacional` y `comercial`. La ampliación de cobertura se realiza por configuración de catálogo, sin cambiar el código del flujo. | Mayoría (carlos, mark, Chris) sobre la restricción de Anuar |
| **D-04** | No existe un rol administrador con acceso a la interfaz. La gestión del modelo y de los datos se realiza por proceso operativo versionado y verificado (RF-10), no por panel web. | Anuar y Chris sobre mark |

### 1.3 Definiciones, acrónimos y abreviaturas

| Término | Definición |
|---|---|
| **Avalúo comercial** | Dictamen técnico-legal sobre el valor de un inmueble, emitido por un perito valuador certificado. Es el único documento con validez formal para efectos de transacción. |
| **Estimación MLState** | Valor referencial calculado por el modelo predictivo, presentado como rango. Carece de validez legal. |
| **Rango estimado** | Tríada de límites: mínimo, central y máximo, que satisface `valorMínimo ≤ valorCentral ≤ valorMáximo`. No garantiza un precio de cierre. |
| **Margen de error** | Valor numérico expresado en porcentaje sobre el valor central, asociado a cada estimación e integrado en el resultado, no como metadato técnico. |
| **Nivel de confianza** | Categoría `baja`, `media` o `alta` que expresa el respaldo de datos de la estimación conforme a una política versionada. **No es una probabilidad de venta ni una garantía de precio.** |
| **Comparable** | Registro de otra propiedad que satisface los filtros aprobados de tipo, ubicación, superficies y ventana de antigüedad, y que cuenta con permiso de exhibición. Ver RD-10. |
| **Referencia válida** | Operación de cierre verificada, distinta de toda propiedad ya contada, usada para acreditar la suficiencia de una muestra. No es lo mismo que un comparable exhibido. |
| **Cobertura** | Conjunto de combinaciones de estado, municipio, colonia, tipo de inmueble y uso de suelo habilitadas para estimación. |
| **Modelo activo** | Versión del modelo predictivo habilitada, evaluada y autorizada para procesar solicitudes. |
| **Instantánea** | Conjunto congelado de versiones de modelo, datos y política que produjo un resultado determinado y que permanece identificada aunque se publiquen versiones nuevas. |
| **Sesión anónima** | Identificador temporal ligado al navegador que permite recuperar un resultado y su reporte dentro de la vigencia de RF-18. No constituye una identidad de usuario. |
| **Broker / Agente** | Usuario registrado que usa MLState como herramienta de trabajo. **Único rol autenticado del sistema.** |
| **Usuario Visitante** | Persona no registrada que realiza una consulta completa en modo invitado. |
| **Criterio de Aceptación (CA)** | Escenario verificable que determina si un requerimiento se cumple. Se identifica como `RF-XX-AC-n`. |
| **Endpoint** | Punto de acceso HTTP de la API de MLState. Superficie definida en la sección 3.0.3. |
| **Borrador de estimación** | Registro en construcción que acumula los datos capturados antes de solicitar el cálculo. |
| **Idempotencia** | Capacidad de que dos envíos con la misma clave de idempotencia devuelvan el mismo resultado y no generen un segundo registro ni un segundo consumo de cuota. |
| **MdAPE** | Mediana de `100 × abs(predicción − referencia) / referencia`, evaluada únicamente con referencias positivas. |
| **Fixture** | Conjunto sintético y reproducible de entradas, políticas y resultados esperados, utilizado exclusivamente en pruebas. |
| **m²** | Metro cuadrado. Unidad de superficie de terreno y de construcción. |
| **MXN** | Peso mexicano. Única moneda del sistema. |
| **RD / RF / RNF** | Requerimiento de Dominio / Funcional / No Funcional. |
| **PDF** | Portable Document Format, formato del reporte descargable. |
| **SRS** | Software Requirements Specification. |

### 1.4 Convenciones de identificadores y sintaxis

#### 1.4.1 Formato de identificador de criterio de aceptación

```
RF-<requerimiento>-AC-<número correlativo>
```

- `RF-01-AC-1` es el primer criterio del requerimiento RF-01.
- La numeración es correlativa y **contigua** dentro de cada requerimiento, sin saltos.
- El identificador es **estable**: una vez publicado no se renumera. Si un criterio se retira, se marca como retirado y su número no se reutiliza.
- Cada identificador es único en el documento y puede referenciarse desde un caso de prueba, una definición OpenAPI o una incidencia.

#### 1.4.2 Sintaxis de los criterios

| Elemento | Regla de redacción |
|---|---|
| **Dado que** | Precondición verificada. Describe el estado previo del sistema o la identidad del actor. No introduce acciones. |
| **Cuando** | Acción única ejecutada por el usuario o por el sistema. Describe el evento detonante. |
| **Entonces** | Resultado esperado, observable y verificable por prueba automática o por inspección de la respuesta. |

#### 1.4.3 Regla de verificabilidad aplicada

Todo clause `Entonces` contiene al menos uno de estos elementos observables, sin los cuales el criterio no es aceptable:

1. Un **código de estado HTTP** concreto.
2. Un **código de error de negocio** con el formato `CONSTANTE_EN_MAYUSCULAS_CON_RAYAS`.
3. Un **valor numérico o umbral** explícito.
4. Un **nombre de campo o propiedad** de la respuesta.
5. Un **elemento de interfaz** identificable y comprobable.

#### 1.4.4 Regla de independencia y datos de prueba

- Cada criterio es independiente. Cuando enumera valores, se ejecuta una prueba separada por valor o combinación indicada, restableciendo el contexto.
- Los criterios que dependen de políticas sintéticas comprueban validación, presentación e integración; los que dependen del modelo real requieren la configuración aprobada. **Toda evidencia de prueba identifica cuál de las dos modalidades se ejecutó.**
- "No invoca el modelo" se verifica mediante un **contador de llamadas instrumentado en pruebas**, y se comprueba también en el servidor.

#### 1.4.5 Convenciones sintéticas de prueba

Los siguientes conjuntos son exclusivos del entorno de pruebas y **no representan políticas aprobadas de producción**. Su sustitución por la política versionada requiere cerrar los puntos abiertos P-01 a P-03.

- **F-BASE** — Propiedad de referencia: estado Jalisco, municipio Zapopan, colonia sintética `Z-01` habilitada, tipo casa usada, uso habitacional, terreno 250.00 m², construcción 200.00 m², 3 habitaciones, 2 baños completos, 1 estacionamiento, antigüedad 10 años, conservación buena. Opcionales: remodelación sí en 2024, cuarto de servicio sí, cercanía a parque no, 0 medios baños. La misma colonia sintética puede activarse en Guadalajara para probar ese municipio.
- **F-POL** — Política sintética `POL-TEST-1`. Plausibilidad inclusiva de construcción: 100.00–500.00 m². Suficiencia: al menos 30 referencias válidas y distintas, recuento diferente del número de comparables exhibidos. Reglas de confianza, en orden excluyente: con menos de 30 referencias no se estima; con suficiencia y 0 a 2 comparables la confianza es `baja`; con suficiencia y 3 o más comparables y algún opcional desconocido la confianza es `media`; con suficiencia, 3 o más comparables y todos los opcionales informados la confianza es `alta`.
- **F-RES** — Salida sintética del modelo `MOD-TEST-1`: central 4,000,000 MXN, inferior 3,600,000 MXN, superior 4,400,000 MXN; 5 comparables válidos de 7 disponibles; confianza `alta`; margen de error 10.00 %; fecha de cálculo 2026-09-25; actualización de datos 2026-09-01. Explicación de prueba: remodelación incrementa el valor, antigüedad lo reduce.
- **F-COMP** — C1 a C7 son casas usadas habitacionales en `Z-01`, cada una con 250.00 m² de terreno, 200.00 m² construidos y 4,000,000 MXN. Puntuaciones 0.99, 0.95, 0.90, 0.85, 0.80, 0.75 y 0.70, en orden descendente con desempate por identificador ascendente. Fecha de cada registro: 2026-09-01. C1 a C3 son cierres, C4 y C5 publicaciones, C6 y C7 avalúos. Son propiedades diferentes.
- **F-AMP** — Umbral sintético de amplitud relativa 0.40, con causa `Dispersión de precios en la muestra`.
- **Fecha de prueba congelada:** 2026-09-25. Los 12 meses de comparables se interpretan como ventana inclusiva entre 2025-09-25 y 2026-09-25; las fechas futuras quedan excluidas. En ejecución real se usa la fecha de cálculo menos 12 meses calendario; si el día no existe en el mes de destino, se usa su último día.
- **Zonas horarias:** las fechas de negocio se interpretan en `America/Mexico_City`. Los plazos de vigencia, expiración y espera se calculan como tiempo transcurrido con reloj de servidor en UTC. El cálculo se fecha cuando termina exitosamente. F-RES usa `2026-09-25T18:00:00Z` como instante de finalización.
- **Comparaciones monetarias:** son numéricas, no dependen del separador visual de miles. El precio por m² se redondea al centavo más próximo, con empate hacia arriba.

### 1.5 Correspondencia de códigos de error entre documentos de origen

La convención de este SRS es la de Chris: constantes en mayúsculas con rayas, en español. Los códigos de carlos se conservan como alias estables para no invalidar la trazabilidad de su documento de origen.

| Código en este SRS | Alias conservado de carlos | Significado |
|---|---|---|
| `EMAIL_YA_REGISTRADO` | `EMAIL_ALREADY_REGISTERED` | Ya existe una cuenta con el correo indicado |
| `CREDENCIALES_INVALIDAS` | `INVALID_CREDENTIALS` | Correo o contraseña incorrectos |
| `ERROR_EN_SERVICIO_DE_INFERENCIA` | `PREDICTION_UNAVAILABLE` | El motor de inferencia no respondió o agotó el tiempo de espera |
| `ESTIMACION_NO_ENCONTRADA` | `ESTIMATE_NOT_FOUND` | No existe la estimación o no pertenece a la identidad solicitante |

---

## 2. Descripción general

### 2.1 Perspectiva del producto

MLState es una **aplicación web responsiva de página única (SPA)**, accesible desde navegador móvil y de escritorio. No hay instalación nativa ni tienda de aplicaciones: el broker lo usa desde el navegador del celular, potencialmente en campo.

El sistema se despliega como una aplicación de tres capas:

```
┌──────────────────────────┐      ┌──────────────────────┐      ┌─────────────────────────┐
│  Capa de presentación    │      │  Capa de aplicación  │      │  Capa de datos          │
│  SPA responsive          │ ───► │  API de negocio      │ ───► │  Motor de inferencia ML │
│  Formulario, resultado,  │ HTTPS│  Sesiones, historial, │      │  Base de transacciones  │
│  comparables, PDF        │      │  catálogos, reportes │      │  Usuarios, estimaciones │
│  (RNF-07, RNF-08)        │      │  (RF-01 … RF-25)     │      │  (RD-05, RNF-04, RNF-05) │
└──────────────────────────┘      └──────────────────────┘      └─────────────────────────┘
```

| Componente externo | Interacción | Requerimientos |
|---|---|---|
| **Motor de inferencia ML** | Recibe las características del inmueble y devuelve predicción, margen, confianza, comparables y explicación. | RF-07, RF-12, RF-13, RF-14 |
| **Base de datos de transacciones inmobiliarias** | Fuente de entrenamiento, de evaluación y de selección de comparables. | RD-05, RD-11, RNF-04 |
| **Puente de compartición del sistema operativo** | Entrega el PDF generado a una aplicación de destino del dispositivo. | RF-25 |
| **Sonda externa de disponibilidad** | Ejecuta una prueba de acceso y estimación por minuto contra el servicio real. | RNF-03 |

MLState **no** es un sistema multi-inquilino ni multi-organización: opera como servicio único con separación lógica de datos por identidad de usuario y por sesión anónima (RNF-12).

### 2.2 Funciones principales

| ID | Función | Requerimientos |
|---|---|---|
| F1 | Consultar la cobertura disponible y verificar la elegibilidad de una combinación antes de capturar | RF-01, RF-02 |
| F2 | Capturar las características físicas y cualitativas de un inmueble con ayuda contextual | RF-03 |
| F3 | Validar la entrada e identificar campos faltantes, valores fuera de rango y valores ambiguos | RF-04, RF-05, RF-06 |
| F4 | Calcular y presentar una estimación en rango con margen, confianza y versión | RF-07, RF-11, RF-12 |
| F5 | Abstenerse de emitir precio cuando la muestra o la habilitación no son suficientes | RF-08, RF-10 |
| F6 | Explicar en lenguaje natural los factores que determinaron el valor | RF-13 |
| F7 | Mostrar las propiedades comparables que sustentan la estimación | RF-14 |
| F8 | Generar, descargar y compartir un reporte PDF protegido | RF-23, RF-24, RF-25 |
| F9 | Atender la consulta del usuario visitante y gestionar la vigencia de su sesión anónima | RF-18 |
| F10 | Autenticar al broker y proteger su sesión | RF-16, RF-17 |
| F11 | Persistir, consultar, filtrar, detallar y eliminar el historial de estimaciones | RF-19 a RF-22 |
| F12 | Mostrar de forma permanente y visible la advertencia de carácter informativo | RF-15 |

### 2.3 Características de los usuarios

| Perfil | Descripción | Necesidades principales | Requisitos asociados |
|---|---|---|---|
| **Usuario Visitante** | Propietario, comprador o agente que consulta una vez, sin cuenta. No es usuario técnico. | Obtener un rango de precio inmediato, comparable, explicación y PDF comprensible, sin entregar ningún dato personal. | RF-01 a RF-15, RF-18, RF-23 a RF-25 |
| **Broker / Agente** | Profesional que usa MLState como herramienta de trabajo diaria, en campo, con clientes reales. | Velocidad de captura, continuidad entre consultas, historial y aislamiento de sus registros. | RF-03 a RF-07, RF-11 a RF-14, RF-16, RF-17, RF-19 a RF-23 |
| **Responsable del modelo** | Equipo interno de datos que construye, reentrena y evalúa el modelo y mantiene las habilitaciones. **No interactúa con la interfaz.** | Habilitar versiones con evidencia de evaluación y autorización vigente; detectar deriva. | RF-10, RNF-04, RNF-05, RNF-19 |

**Caracterización operativa crítica:** el broker consulta MLState de pie, frente al inmueble, con una sola mano, frecuentemente con brillo solar directo sobre la pantalla. Esta condición de uso —no el perfil demográfico— gobierna las decisiones de interfaz (RNF-07, RNF-08).

**Perfiles de uso sin permisos diferenciados:** propietario, comprador y agente inmobiliario comparten las mismas funciones en modo anónimo. No se requiere conocimiento de modelos predictivos, sólo manejo básico de navegador y acceso a los datos del inmueble.

### 2.4 Restricciones

| ID | Restricción | Tipo |
|---|---|---|
| C-01 | El modelo opera únicamente dentro de la cobertura habilitada del catálogo. | Negocio (RD-01) |
| C-02 | La estimación es referencial y no tiene validez como avalúo oficial ni bancario. | Legal (RD-02) |
| C-03 | El sistema no emite estimación cuando la muestra de la zona es insuficiente. | Negocio (RD-06) |
| C-04 | El sistema no captura ni almacena dirección exacta ni coordenadas. | Legal y privacidad (RD-08) |
| C-05 | El sistema no ejecuta transacciones financieras ni publica anuncios. | Legal (RD-09) |
| C-06 | El usuario puede operar el sistema completo sin cuenta. | Diseño (RF-18) |
| C-07 | Todos los importes se expresan en MXN; no hay conversión de moneda. | Negocio (RD-03) |
| C-08 | El piloto se entrega como aplicación web responsiva en un máximo de cuatro meses desde el inicio formal del proyecto, con un equipo de cuatro personas. | Proyecto (P-07) |
| C-09 | El reentrenamiento del modelo es trimestral y la revisión de datos es mensual. | Datos (RNF-19) |

---

## 3. Requerimientos específicos

### 3.0 Convenciones de los criterios de aceptación y superficie de API

#### 3.0.1 Tipos de criterio

Cada requerimiento funcional cubre al menos tres escenarios: el **flujo exitoso**, al menos un **flujo alternativo** y al menos una **validación de error**. La columna *Tipo* del índice de trazabilidad (sección 4) los distingue.

#### 3.0.2 Modelo de dos fases: borrador y cálculo

La captura de datos y el cálculo predictivo son **dos operaciones distintas**, porque el usuario completa el formulario de forma progresiva antes de que exista una estimación que calcular.

| Fase | Operación | Resultado |
|---|---|---|
| **Fase 1 — Captura** | `POST /api/v1/borradores` y `PUT /api/v1/borradores/{id}` | Un borrador con `borradorId`. **No invoca el motor de inferencia.** |
| **Fase 2 — Cálculo** | `POST /api/v1/estimaciones` con `{ "borradorId": "..." }` | Una estimación con rango, margen, confianza, comparables y explicación. |

Consecuencias normativas:

- Ningún criterio de captura ni de validación (RF-03 a RF-06, RF-01, RF-02) puede invocar el motor de inferencia. La aserción "el motor no se invoca" es por tanto comprobable en la Fase 1.
- Un borrador incompleto no puede pasar a la Fase 2.
- La Fase 2 es **idempotente por clave de idempotencia**: dos envíos con la misma clave devuelven el mismo `estimacionId`, no crean un segundo registro de historial y **no consumen una segunda cuota**.
- `POST /api/v1/estimaciones` acepta la cabecera `Idempotency-Key` y la constituye en obligatoria para evitar duplicados por doble pulsación en móvil.

#### 3.0.3 Superficie de API referenciada por los criterios

Los criterios citan operaciones concretas para hacer la verificación inequívoca. Esta es la superficie mínima que la especificación OpenAPI derivada debe cubrir. **Esta tabla es informativa**: los requisitos son normativos sobre el comportamiento, y la asignación de rutas y códigos HTTP puede cambiar en el diseño sin invalidar los identificadores `RF-XX-AC-n`.

| Método | Ruta | Propósito | Requerimientos |
|---|---|---|---|
| `GET` | `/api/v1/catalogos` | Lista cobertura activa: estados, municipios, colonias, tipos y usos | RF-01, RF-02 |
| `POST` | `/api/v1/catalogos/elegibilidad` | Valida una combinación contra la cobertura habilitada | RF-02 |
| `POST` | `/api/v1/borradores` | Crea el borrador de estimación y devuelve su `borradorId` | RF-03, RF-04, RF-05, RF-06 |
| `PUT` | `/api/v1/borradores/{id}` | Actualiza el borrador y sus confirmaciones | RF-03, RF-04, RF-05, RF-06 |
| `POST` | `/api/v1/estimaciones` | Dispara el cálculo sobre un borrador completo | RF-07, RF-08, RF-09, RF-10 |
| `GET` | `/api/v1/estimaciones/{id}` | Resultado: rango, margen, confianza, explicación y versiones | RF-11, RF-12, RF-13 |
| `GET` | `/api/v1/estimaciones/{id}/comparables` | Comparables exhibidos y total válido de la zona | RF-14 |
| `POST` | `/api/v1/estimaciones/{id}/reporte` | Genera el PDF de la estimación | RF-23, RF-24 |
| `GET` | `/api/v1/consultas/{id}` | Recupera una consulta anónima vigente | RF-18 |
| `POST` | `/api/v1/consultas/{id}/finalizar` | Elimina la consulta anónima y su reporte | RF-18 |
| `POST` | `/api/v1/auth/registro` | Alta de cuenta de broker | RF-16 |
| `POST` | `/api/v1/auth/login` | Inicio de sesión | RF-17 |
| `POST` | `/api/v1/auth/logout` | Cierre de sesión | RF-17 |
| `POST` | `/api/v1/historial` | Guarda una estimación para la identidad activa | RF-19 |
| `GET` | `/api/v1/historial` | Historial de la identidad activa, con filtros y paginación | RF-20 |
| `GET` | `/api/v1/historial/{id}` | Detalle de una estimación guardada | RF-21 |
| `DELETE` | `/api/v1/historial/{id}` | Elimina una estimación guardada | RF-22 |

#### 3.0.4 Códigos de error de negocio utilizados por los criterios

| Código | Significado |
|---|---|
| `CATALOGO_NO_DISPONIBLE` | El catálogo solicitado no existe o no está activo. |
| `ZONA_FUERA_DE_COBERTURA` | La combinación de ubicación, tipo de inmueble y uso de suelo no está habilitada (RD-01). |
| `COLONIA_AMBIGUA` | El código postal corresponde a más de una colonia del catálogo. |
| `USO_DE_SUELO_NO_PERMITIDO` | El valor de uso de suelo no pertenece al dominio admitido. |
| `CAMPO_FUERA_DE_RANGO` | El valor excede el rango admisible del campo o no cumple su formato. |
| `VALOR_AMBIGUO` | El valor requiere confirmación explícita antes de utilizarse. |
| `CONFIRMACION_INVALIDADA` | Una confirmación previa dejó de ser válida por cambio de valor, de zona o de versión de política. |
| `CAMPOS_OBLIGATORIOS_FALTANTES` | Faltan atributos requeridos en el borrador. Un error por campo. |
| `MUESTRA_INSUFICIENTE_PARA_ESTIMAR` | No hay muestra suficiente de referencias válidas en la zona (RD-06). |
| `DATOS_NO_HABILITADOS` | Falta política, modelo con evaluación aprobada o conjunto de datos autorizado (RF-10). |
| `DATOS_DESHABILITADOS` | La instantánea perdió su autorización de exhibición o de procesamiento. |
| `ERROR_EN_SERVICIO_DE_INFERENCIA` | El motor de inferencia no respondió o agotó el tiempo de espera. |
| `RESULTADO_NO_PUBLICABLE` | La respuesta del motor no supera las validaciones de RD-07. |
| `EMAIL_YA_REGISTRADO` | Ya existe una cuenta con el correo indicado. |
| `CREDENCIALES_INVALIDAS` | El correo no existe o la contraseña es incorrecta. |
| `SESION_EXPIRADA` | La sesión superó el periodo de inactividad configurado. |
| `ACCESO_DENEGADO` | El recurso pertenece a otra identidad. |
| `CONSULTA_EXPIRADA` | La consulta anónima superó su vigencia de 60 minutos. |
| `ESTIMACION_NO_ENCONTRADA` | La estimación no existe o no pertenece a la identidad solicitante. |
| `LIMITE_DIARIO_ALCANZADO` | Se agotó la cuota diaria de estimaciones de usuario anónimo. |
| `LIMITE_DE_TASA_ALCANZADO` | Se superó el límite de solicitudes por minuto. |
| `NO_SE_PERMITE_REVELAR_DIRECCION` | Se solicitó incluir ubicación exacta en el reporte (RD-08). |

---

### 3.1 Requerimientos funcionales (RF)

---

#### RF-01 — Consulta de la cobertura disponible

**Descripción:** El sistema debe proporcionar el catálogo de cobertura habilitada antes de permitir la captura, y debe mostrar únicamente elementos activos.

#### Criterios de Aceptación

- **RF-01-AC-1:** **Dado que** existen estados, municipios, colonias, tipos de inmueble y usos de suelo activos en el catálogo, **cuando** el usuario consulta el catálogo sin autenticación, **entonces** la respuesta es `200 OK` y devuelve únicamente elementos activos, con la relación jerárquica estado → municipio → colonia y los dominios de tipo de inmueble y uso de suelo habilitados.

- **RF-01-AC-2:** **Dado que** una colonia está deshabilitada, **cuando** el usuario consulta el catálogo del municipio correspondiente, **entonces** esa colonia no aparece como opción seleccionable y su identificador no puedeiguously resolverse como referencia válida en ninguna otra operación.

- **RF-01-AC-3:** **Dado que** el usuario ha elegido un municipio, **cuando** consulta el catálogo de colonias de ese municipio, **entonces** la respuesta devuelve únicamente colonias habilitadas de ese municipio y ninguna de otro.

---

#### RF-02 — Verificación temprana de elegibilidad

**Descripción:** El sistema debe comprobar la cobertura de la combinación de ubicación, tipo de inmueble y uso de suelo **antes** de habilitar la captura completa, y debe resolver el código postal a una única colonia antes de continuar.

#### Criterios de Aceptación

- **RF-02-AC-1:** **Dado que** la colonia `Z-01` está habilitada en el municipio probado, **cuando** el usuario selecciona `Z-01`, un tipo de inmueble habilitado y el uso de suelo `habitacional`, **entonces** la respuesta es `200 OK` con `elegible: true`, se habilita la captura restante y **el contador de llamadas al motor de inferencia permanece en cero**.

- **RF-02-AC-2:** **Dado que** el usuario intenta continuar con un municipio no habilitado, una combinación sin cobertura, un tipo de inmueble no habilitado o el uso de suelo `comercial` en una cobertura que no lo admite, probados por separado, **entonces** la respuesta es `422` con `ZONA_FUERA_DE_COBERTURA`, se identifica la condición no admitida, no se habilita la captura completa y el contador de llamadas al motor permanece en cero.

- **RF-02-AC-3:** **Dado que** un código postal del catálogo corresponde a exactamente dos colonias, **cuando** el usuario lo selecciona sin elegir colonia, **entonces** la respuesta es `409` con `COLONIA_AMBIGUA` y presenta ambas opciones; la continuación queda bloqueada hasta seleccionar una, y tras elegirla la solicitud identifica esa colonia y no la otra.

---

#### RF-03 — Captura de características del inmueble

**Descripción:** El sistema debe capturar los campos obligatorios de RD-01 y permitir corregirlos antes del cálculo. Cada campo debe estar identificado como `Obligatorio` u `Opcional` mediante texto visible, y debe contar con ayuda que contenga una definición, un ejemplo con formato o unidad y la fuente documental de consulta.

#### Criterios de Aceptación

- **RF-03-AC-1:** **Dado que** la elegibilidad de `Z-01` fue aceptada, **cuando** el usuario abre el formulario completo, **entonces** están representados estado, municipio, colonia o código postal resuelto a colonia, tipo de inmueble, uso de suelo, superficie de terreno, superficie construida, habitaciones, baños completos, estacionamientos, antigüedad y conservación; las áreas indican `m²`, la antigüedad indica años, y ubicación, tipo y uso ofrecen exclusivamente valores de catálogo.

- **RF-03-AC-2:** **Dado que** se muestra el formulario de captura, **cuando** se inspecciona cada campo de forma independiente de su color, **entonces** los campos enumerados como obligatorios muestran el texto `Obligatorio` y los enumerados como opcionales, incluidos los medios baños, muestran el texto `Opcional`.

- **RF-03-AC-3:** **Dado que** existen los valores de F-BASE en el formulario, **cuando** el usuario abre y cierra la ayuda de cualquier campo, **entonces** el valor de ese campo y de todos los demás coincide con el que había antes de abrirla, y la ayuda de superficies identifica el predial o la documentación del inmueble como fuente.

---

#### RF-04 — Validación de formato, tipo y catálogo

**Descripción:** El sistema debe validar los tipos, las unidades y las reglas de RD-01 antes de permitir el cálculo, e identificar cada campo inválido con su regla incumplida.

#### Criterios de Aceptación

- **RF-04-AC-1:** **Dado que** los demás campos de F-BASE son válidos, **cuando** se envía por interfaz y por solicitud directa un área ausente, cero, negativa o con más de dos decimales, un conteo fraccionario, una cantidad negativa o un valor de catálogo inexistente, probados por separado, **entonces** la respuesta es `422` con `CAMPO_FUERA_DE_RANGO`, se identifica cada campo y la regla incumplida, y el motor de inferencia no registra invocación alguna.

- **RF-04-AC-2:** **Dado que** la propiedad tiene 150.00 m² de terreno y 200.00 m² construidos y la política admite ambas áreas, **cuando** se validan sus superficies, **entonces** la validación es exitosa y no se produce error por tener construcción mayor que terreno.

- **RF-04-AC-3:** **Dado que** el servidor recibe una solicitud directa que combina un municipio y una colonia que no corresponden al mismo registro del catálogo, **cuando** valida la ubicación, **entonces** la respuesta es `422` con `ZONA_FUERA_DE_COBERTURA`, se señalan los campos implicados y no se calcula.

---

#### RF-05 — Confirmación de entradas ambiguas o atípicas

**Descripción:** El sistema debe detectar valores válidos pero fuera del intervalo de plausibilidad configurado, y entradas numéricamente ambiguas, y debe exigir confirmación explícita antes de utilizarlas. Una confirmación debe invalidarse cuando cambia el valor, la zona o la versión de política.

#### Criterios de Aceptación

- **RF-05-AC-1:** **Dado que** el usuario capturó 500.01 m² construidos bajo F-POL, **cuando** solicita estimar, **entonces** aparece un aviso que identifica el campo `superficieConstruida`, el valor `500.01 m²` y acciones para corregir o confirmar; el motor no recibe una llamada mientras no se confirme o se corrija el valor.

- **RF-05-AC-2:** **Dado que** el usuario ingresa `1.200` en un campo de superficie, **cuando** el sistema procesa el campo, **entonces** detecta la ambigüedad, propone la interpretación `1200 m²`, exige confirmación explícita con `VALOR_AMBIGUO` y el motor de inferencia no se invoca mientras la confirmación no se registre.

- **RF-05-AC-3:** **Dado que** se confirmó un valor de 500.01 m² bajo `POL-TEST-1`, **cuando** el usuario cambia el valor a 600.00 m² o cambia la zona o la versión de política, **entonces** la respuesta es `409` con `CONFIRMACION_INVALIDADA`, el aviso de confirmación vuelve a mostrarse y se reevalúa la necesidad de confirmar antes de calcular.

---

#### RF-06 — Detección de campos obligatorios faltantes

**Descripción:** El sistema debe impedir el cálculo e identificar **todos** los campos obligatorios ausentes, conservando los valores ya informados.

#### Criterios de Aceptación

- **RF-06-AC-1:** **Dado que** el formulario contiene F-BASE excepto superficie construida y número de habitaciones, **cuando** se intenta estimar desde la interfaz o mediante solicitud directa, **entonces** la respuesta es `422` con `CAMPOS_OBLIGATORIOS_FALTANTES`, el arreglo de errores contiene exactamente dos entradas que nombran esos dos campos, el motor no registra invocación alguna y el escenario se repite omitiendo individualmente cada obligatorio.

- **RF-06-AC-2:** **Dado que** faltan dos campos obligatorios pero los demás están completos, **cuando** se muestran los errores, **entonces** todos los campos previamente informados conservan sus valores y no es necesario volver a capturarlos.

- **RF-06-AC-3:** **Dado que** solo faltan los opcionales remodelación, cuarto de servicio, cercanía a parque y medios baños, **cuando** se valida la solicitud, **entonces** no hay errores de obligatoriedad, la solicitud continúa al control de suficiencia y confianza, y los opcionales ausentes se transmiten como ausentes, no como `no`, cero ni un año inventado.

---

#### RF-07 — Cálculo de la estimación

**Descripción:** El sistema debe enviar al motor de inferencia las variables de una solicitud válida y obtener un rango de tres valores, un margen de error, un nivel de confianza y una explicación. La operación es idempotente por clave de idempotencia.

#### Criterios de Aceptación

- **RF-07-AC-1:** **Dado que** el borrador cumple la elegibilidad de RF-02, no tiene campos faltantes ni entradas sin confirmar, la zona tiene suficiencia de F-POL y el motor de prueba devuelve F-RES, **cuando** el usuario envía `POST /api/v1/estimaciones` con `{ "borradorId": "..." }` y una cabecera `Idempotency-Key`, **entonces** la respuesta es `201 Created` e incluye `estimacionId`, `valorMinimo` 3,600,000, `valorCentral` 4,000,000, `valorMaximo` 4,400,000, todos en MXN, y se satisface `valorMinimo ≤ valorCentral ≤ valorMaximo`.

- **RF-07-AC-2:** **Dado que** el usuario ya envió una solicitud con una `Idempotency-Key` determinada, **cuando** reenvía la misma solicitud con esa misma clave, **entonces** la respuesta es `201 Created` con el mismo `estimacionId`, el historial contiene una sola entrada para esa operación y la cuota diaria no se consume dos veces.

- **RF-07-AC-3:** **Dado que** la entrada superó todos los controles, **cuando** el motor devuelve por separado un valor central nulo, negativo o no finito, límites invertidos, un nivel de confianza distinto de `baja`, `media` o `alta`, o una versión distinta de la seleccionada, **entonces** la respuesta es `422` con `RESULTADO_NO_PUBLICABLE`, no se muestra precio ni se habilita el PDF, y el contador de llamadas **registra** la llamada realizada.

- **RF-07-AC-4:** **Dado que** existe una estimación calculada y no se ha ejecutado un reentrenamiento del modelo, **cuando** el usuario envía un borrador con datos idénticos, **entonces** la respuesta devuelve los mismos `valorMinimo`, `valorCentral` y `valorMaximo` que la estimación previa.

---

#### RF-08 — Abstención por muestra insuficiente

**Descripción:** El sistema debe abstenerse de emitir precio cuando la zona no alcance la suficiencia aprobada de referencias válidas, y no debe reutilizar importes de una consulta anterior.

#### Criterios de Aceptación

- **RF-08-AC-1:** **Dado que** la zona está habilitada y los datos de F-BASE son válidos, **cuando** se prueban 29, 30 y 31 referencias con F-POL, **entonces** 29 produce `409` con `MUESTRA_INSUFICIENTE_PARA_ESTIMAR` sin invocar el cálculo, mientras 30 y 31 permiten estimar; ninguna de las tres pruebas confunde el número de referencias con el de comparables exhibidos.

- **RF-08-AC-2:** **Dado que** previamente se mostró un resultado y la nueva solicitud corresponde a una zona habilitada con cero referencias válidas, **cuando** el usuario solicita estimar, **entonces** la respuesta es `409` con `MUESTRA_INSUFICIENTE_PARA_ESTIMAR`, se informa `No hay registros de referencia válidos para esta zona` y **no se muestra precio de cero, rango ni importes de la consulta anterior**.

- **RF-08-AC-3:** **Dado que** con la muestra suficiente pero el motor de inferencia falla, **cuando** se procesa la solicitud, **entonces** la respuesta es `503` con `ERROR_EN_SERVICIO_DE_INFERENCIA`, el error **se informa como fallo del servicio y no como insuficiencia de mercado**, no se muestra precio y no se habilita la descarga.

---

#### RF-09 — Espera y fallo del servicio de inferencia

**Descripción:** El sistema debe distinguir el timeout de transporte del timeout de experiencia de usuario, y debe permitir reintentar sin perder los datos capturados.

#### Criterios de Aceptación

- **RF-09-AC-1:** **Dado que** el tiempo de espera de transporte configurado es de 5 segundos, **cuando** el motor de inferencia no responde dentro de ese intervalo, **entonces** la respuesta es `503` con `ERROR_EN_SERVICIO_DE_INFERENCIA` y el contador de llamadas registra la invocación realizada.

- **RF-09-AC-2:** **Dado que** una solicitud fue enviada y no llega respuesta, **cuando** transcurren 30 segundos desde su envío en el navegador, **entonces** termina el indicador de espera, aparece el mensaje `No fue posible obtener la estimación; puede reintentar`, los campos permanecen **en memoria de la página** y no se muestran importes anteriores.

- **RF-09-AC-3:** **Dado que** RF-09-AC-2 terminó la espera de una solicitud A, **cuando** el usuario restablece la conexión y selecciona reintentar con los valores conservados en memoria, **entonces** se envía una solicitud nueva, identificada separadamente como B, y una respuesta tardía de A **no** reemplaza el resultado de B.

---

#### RF-10 — Habilitación de política, modelo y datos

**Descripción:** Antes de calcular, el sistema debe comprobar que la localidad tenga versiones habilitadas de política de plausibilidad, de suficiencia y de intervalo, un modelo con evaluación aprobada y un conjunto de datos autorizado y vigente. Cada versión registra su instante de actualización validada y su antigüedad máxima aprobada; cambiar esa fecha exige una nueva validación de la fuente, no un cambio de etiqueta.

#### Criterios de Aceptación

- **RF-10-AC-1:** **Dado que** se simula por separado una política sin habilitar, un modelo sin evaluación aprobada o una fuente sin permiso de procesamiento, **cuando** el usuario solicita estimar, **entonces** la respuesta es `409` con `DATOS_NO_HABILITADOS`, se comunica que la zona no está disponible por configuración o por datos, no se invoca el modelo y no se produce precio ni PDF.

- **RF-10-AC-2:** **Dado que** la configuración fija antigüedad máxima de datos en 30 días y actualización validada a `2026-09-01T00:00:00Z`, **cuando** se solicita calcular a `2026-10-01T00:00:00Z` y un segundo después, **entonces** el primer caso pasa el control y el segundo es bloqueado con `DATOS_NO_HABILITADOS`; cambiar sólo el texto mostrado de actualización no habilita el segundo caso.

- **RF-10-AC-3:** **Dado que** una estimación vigente se calculó con 30 filas de las cuales dos duplican propiedades ya contadas y una carece de precio, **cuando** se valida el conjunto antes de estimar, **entonces** se cuentan 27 referencias válidas y distintas y se aplica RF-08 por insuficiencia.

---

#### RF-11 — Presentación del rango y de los metadatos de cálculo

**Descripción:** El sistema debe presentar simultáneamente el rango, el valor central, el precio por m² de construcción, las fechas de cálculo y de actualización de datos, y las versiones de modelo, datos y política utilizadas.

#### Criterios de Aceptación

- **RF-11-AC-1:** **Dado que** el resultado es F-RES y la superficie construida es 200.00 m², **cuando** se presenta en pantalla, **entonces** se muestran central 4,000,000 MXN, rango 3,600,000–4,400,000 MXN y precio unitario 20,000.00 con la unidad `MXN/m² de construcción`, **sin dividir por los 250.00 m² de terreno**.

- **RF-11-AC-2:** **Dado que** un resultado de prueba tiene central 4,000,001 MXN y 200.00 m² construidos, **cuando** se calcula el precio unitario, **entonces** 20,000.005 se redondea a 20,000.01 y se conservan exactamente dos decimales.

- **RF-11-AC-3:** **Dado que** el cálculo se realizó el 2026-09-25 con datos actualizados el 2026-09-01, **cuando** se presenta el resultado, **entonces** aparecen ambas fechas en formato `AAAA-MM-DD` con las etiquetas distintas `Fecha de cálculo` y `Actualización de datos`, sin intercambiar sus valores, y aparecen las versiones de modelo, datos y política que produjeron el resultado.

---

#### RF-12 — Margen de error y nivel de confianza

**Descripción:** El sistema debe desplegar el margen de error como valor numérico porcentual sobre el valor central junto con su interpretación categórica, y debe determinar el nivel de confianza conforme a la política versionada.

#### Criterios de Aceptación

- **RF-12-AC-1:** **Dado que** existe una estimación creada exitosamente, **cuando** el usuario consulta el resultado, **entonces** la respuesta incluye `margenErrorPorcentaje` con valor numérico mayor o igual a cero que no excede la mitad de la amplitud relativa del rango, y `nivelConfianza` con el valor interpretativo.

- **RF-12-AC-2:** **Dado que** existen 30 referencias y cinco comparables y únicamente la remodelación se deja desconocida en F-BASE, **cuando** se estima con F-POL, **entonces** `nivelConfianza` es `media` y la causa presentada es `Falta información de remodelación`, sin convertir el dato ausente en una respuesta negativa.

- **RF-12-AC-3:** **Dado que** existen 30 referencias y respectivamente cero, uno o dos comparables válidos, **cuando** se ejecuta cada variante con F-POL, **entonces** `nivelConfianza` es `baja` con causa `Menos de tres comparables válidos`, **nunca `alta`**, y el margen de error real se muestra en todos los casos.

---

#### RF-13 — Explicación del resultado

**Descripción:** El sistema debe explicar en lenguaje comprensible para un usuario no técnico los factores que incrementaron o redujeron el valor estimado y su efecto relativo, sin exponer notación matemática ni vocabulario estadístico.

**Vocabulario cerrado de factores.** Una explicación sólo puede nombrar factores correspondientes a atributos efectivamente capturados: superficie de construcción, número de habitaciones, número de baños, superficie de terreno, zona, antigüedad, conservación, tipo de inmueble, tipo de entrega, amenidades, remodelaciones, cuarto de servicio y cercanía a parque.

#### Criterios de Aceptación

- **RF-13-AC-1:** **Dado que** existe una estimación creada exitosamente, **cuando** el usuario consulta el resultado, **entonces** la respuesta incluye el campo `explicacion` con longitud entre 15 y 300 caracteres, contiene al menos un término del vocabulario cerrado y no contiene `regresión`, `lineal`, `coeficiente`, `p-valor`, `desviación estándar`, `RMSE`, `MdAPE`, `sobreajuste`, `intervalo de confianza` ni notación exponencial, en cualquier variante de mayúsculas o acentos.

- **RF-13-AC-2:** **Dado que** en el cálculo un factor elevó el valor y otro lo redujo, **cuando** el sistema genera la explicación, **entonces** el texto distingue explícitamente el sentido de ambos efectos, identifica que la remodelación incrementa el valor y que la antigüedad lo reduce, y no atribuye a un factor ausente un aumento o una reducción.

- **RF-13-AC-3:** **Dado que** un factor no fue capturado o permanece desconocido, **cuando** se genera la explicación, **entonces** ese factor **no aparece** en el texto y en su lugar se presenta la causa asociada a la falta de información.

---

#### RF-14 — Propiedades comparables

**Descripción:** El sistema debe mostrar entre tres y cinco comparables válidos cuando exista al menos tres, respetando la ventana de antigüedad de RD-10 y la deduplicación por clave de propiedad.

#### Criterios de Aceptación

- **RF-14-AC-1:** **Dado que** hay respectivamente tres, cuatro o cinco registros elegibles de F-COMP, **cuando** se presenta cada resultado, **entonces** se muestran todos los registros elegibles de esa variante, sin duplicados ni registros adicionales.

- **RF-14-AC-2:** **Dado que** los siete registros de F-COMP son elegibles, **cuando** se seleccionan los comparables a mostrar, **entonces** aparecen `C1`, `C2`, `C3`, `C4` y `C5` en ese orden; en una variante con empate de puntuación entre `C5` y `C6`, se conserva `C5` por identificador ascendente.

- **RF-14-AC-3:** **Dado que** el cálculo está fechado 2026-09-25 y los demás filtros se cumplen, **cuando** se filtran registros con fechas 2025-09-24, 2025-09-25, 2026-09-25 y 2026-09-26, **entonces** sólo son elegibles los del 2025-09-25 y 2026-09-25; el primero queda fuera por antigüedad y el último por fecha futura.

- **RF-14-AC-4:** **Dado que** una segunda fila representa la misma propiedad que `C1` con la misma fecha, otra carece de precio y otra tiene permiso de cálculo pero no de exhibición, **cuando** se seleccionan fichas, **entonces** `C1` se cuenta una sola vez y ninguna de las otras dos filas se exhibe ni incrementa el conteo de comparables exhibibles; cada ficha presenta colonia, tipo de inmueble, uso, superficies, precio, fecha de referencia y la naturaleza asignada a ese identificador, **sin datos de contacto ni enlaces al propietario**.

---

#### RF-15 — Advertencia visible de carácter informativo

**Descripción:** El sistema debe mostrar de forma permanente y no ocultable una leyenda que indique que la estimación es informativa y no constituye un avalúo oficial. Esta advertencia materializa RD-02 en la interfaz.

#### Criterios de Aceptación

- **RF-15-AC-1:** **Dado que** existe una estimación y el usuario visualiza su resultado, **cuando** la estimación aparece en pantalla, **entonces** la interfaz muestra el texto íntegro de RD-02 con un nodo de inspección de ancho y alto mayores que cero.

- **RF-15-AC-2:** **Dado que** el usuario recorre todas las vistas de la aplicación que muestran un precio estimado y ejecuta abrir y cerrar un modal, desplazarse al final de la página y navegar de vuelta desde una vista secundaria, **cuando** se inspecciona el modelo de objetos del documento, **entonces** en todos los casos la advertencia está presente, no existe ningún control asociado que la modifique, la oculte o la desplace fuera del área visible, y queda contenida dentro del área capturada en un dispositivo de 360 × 640 px.

- **RF-15-AC-3:** **Dado que** el usuario genera un reporte PDF de una estimación, **cuando** se extrae el texto del documento, **entonces** el texto contiene la advertencia informativa y la mención de que no constituye un avalúo oficial.

---

#### RF-16 — Registro de cuenta de broker

**Descripción:** El sistema debe permitir que un visitante cree una cuenta de broker mediante nombre, correo electrónico y contraseña, aplicando una política de complejidad y almacenando la contraseña como hash.

#### Criterios de Aceptación

- **RF-16-AC-1:** **Dado que** el correo no está registrado y la contraseña tiene al menos 10 caracteres, una mayúscula, una minúscula y un número, **cuando** el visitante envía nombre, correo y contraseña válidos, **entonces** la respuesta es `201 Created`, la cuenta queda creada con el rol `broker`, la contraseña se almacena como hash con **Argon2id o bcrypt** y nunca se devuelve ni se registra en texto claro.

- **RF-16-AC-2:** **Dado que** existe una cuenta con el correo indicado, **cuando** el visitante intenta registrarse con ese mismo correo, **entonces** la respuesta es `409` con `EMAIL_YA_REGISTRADO` y no se crea un registro duplicado.

- **RF-16-AC-3:** **Dado que** la contraseña no cumple la política de complejidad, **cuando** el visitante intenta registrarse, **entonces** la respuesta es `422`, se identifican los requisitos incumplidos y no se crea la cuenta.

---

#### RF-17 — Inicio, vigencia y cierre de sesión

**Descripción:** El sistema debe autenticar al broker con correo y contraseña, emitir una sesión con vigencia por inactividad y permitir el cierre explícito de sesión.

#### Criterios de Aceptación

- **RF-17-AC-1:** **Dado que** existe una cuenta de broker activa, **cuando** el usuario envía el correo y la contraseña correctos, **entonces** la respuesta es `200 OK` con un token de sesión y la sesión queda asociada al identificador de esa cuenta, con acceso a su historial.

- **RF-17-AC-2:** **Dado que** el correo no existe o la contraseña es incorrecta, **cuando** se intenta iniciar sesión, **entonces** la respuesta es `401` con `CREDENCIALES_INVALIDAS`, **el mensaje no revela si el correo existe en el sistema** y no se genera token.

- **RF-17-AC-3:** **Dado que** un broker inició sesión y superó el periodo de inactividad configurado, **cuando** el sistema procesa su siguiente solicitud autenticada, **entonces** la respuesta es `401` con `SESION_EXPIRADA` y se exige una nueva autenticación.

---

#### RF-18 — Ciclo de vida de la consulta anónima

**Descripción:** Cada resultado se vincula a la sesión anónima que lo solicitó, sin asociarlo a una identidad. Es consultable y descargable durante 60 minutos contados desde su finalización; una descarga no reinicia ese plazo. Los campos del formulario se mantienen sólo en memoria de la página.

#### Criterios de Aceptación

- **RF-18-AC-1:** **Dado que** un navegador inicia una sesión sin cuenta ni credenciales y F-BASE satisface F-POL, **cuando** el usuario captura la propiedad, solicita la estimación y descarga el PDF, **entonces** obtiene F-RES y un PDF **sin que ninguna de esas acciones requiera iniciar sesión o registrarse**.

- **RF-18-AC-2:** **Dado que** F-RES terminó a las `18:00:00Z` y sigue autorizado, **cuando** la misma sesión solicita el PDF a las `18:59:59Z` y a las `19:00:00Z`, **entonces** la primera solicitud puede descargarlo y la segunda recibe `CONSULTA_EXPIRADA` sin PDF; desde las `19:00:00Z` no existe contenido recuperable en el servidor.

- **RF-18-AC-3:** **Dado que** el resultado pertenece a la sesión anónima A, **cuando** otra sesión B intenta obtenerlo o descargarlo con el identificador de A, **entonces** la respuesta es `403` con `ACCESO_DENEGADO` y **no confirma la existencia** de esa consulta, aunque el identificador sea válido.

- **RF-18-AC-4:** **Dado que** una consulta vigente está visible, **cuando** el usuario selecciona `Finalizar consulta`, **entonces** desaparecen las entradas y el resultado de la página, se eliminan los datos y el reporte temporal de esa sesión y las solicitudes posteriores de descarga se rechazan; un archivo ya descargado por el usuario no se modifica ni se elimina remotamente.

---

#### RF-19 — Guardado de una estimación

**Descripción:** El sistema debe permitir que una identidad autenticada guarde el resultado que está consultando.

#### Criterios de Aceptación

- **RF-19-AC-1:** **Dado que** hay una sesión válida y un resultado generado durante esa sesión, **cuando** el usuario selecciona `Guardar estimación`, **entonces** la respuesta es `201 Created` y el sistema almacena las entradas, las tres salidas, la moneda, la fecha, el margen, la confianza y las versiones de modelo, datos y política bajo el identificador de esa identidad.

- **RF-19-AC-2:** **Dado que** no existe una sesión válida, **cuando** un visitante intenta guardar un resultado, **entonces** la respuesta es `401`, no se almacena la estimación y la interfaz solicita iniciar sesión o crear una cuenta.

---

#### RF-20 — Consulta y filtrado del historial

**Descripción:** El sistema debe permitir que una identidad autenticada consulte sus estimaciones guardadas, ordenadas de la más reciente a la más antigua, filtrables por ciudad y rango de fechas, y paginadas.

#### Criterios de Aceptación

- **RF-20-AC-1:** **Dado que** la identidad autenticada tiene estimaciones guardadas, **cuando** consulta su historial sin filtros, **entonces** la respuesta es `200 OK` y contiene exclusivamente registros cuyo identificador de propietario coincide con el de la sesión activa, ordenados de forma descendente por fecha de consulta y, ante empates, de forma descendente por `estimacionId`, paginados en grupos de 20.

- **RF-20-AC-2:** **Dado que** la identidad autenticada seleccionó una ciudad y un rango de fechas válido, **cuando** aplica los filtros, **entonces** la respuesta contiene únicamente sus estimaciones que cumplen ambos criterios y la interfaz informa de forma explícita cuando no existen coincidencias.

- **RF-20-AC-3:** **Dado que** no existe una sesión válida, **cuando** se solicita el historial, **entonces** la respuesta es `401` y el cuerpo no contiene ningún registro de estimación.

---

#### RF-21 — Detalle de una estimación guardada

**Descripción:** El sistema debe mostrar todos los datos de entrada y de salida de una estimación perteneciente a la identidad autenticada.

#### Criterios de Aceptación

- **RF-21-AC-1:** **Dado que** una estimación pertenece a la identidad autenticada, **cuando** solicita su detalle por identificador, **entonces** la respuesta es `200 OK` y muestra las características capturadas, los tres valores calculados, la moneda, el margen, la confianza, las fechas y las versiones de modelo, datos y política.

- **RF-21-AC-2:** **Dado que** la estimación no existe o pertenece a otra cuenta, **cuando** el usuario solicita su detalle, **entonces** la respuesta es `404` con `ESTIMACION_NO_ENCONTRADA` y **no se revela si el registro existe bajo otra identidad**.

---

#### RF-22 — Eliminación de una estimación guardada

**Descripción:** El sistema debe permitir que una identidad autenticada elimine uno de sus resultados guardados después de confirmarlo.

#### Criterios de Aceptación

- **RF-22-AC-1:** **Dado que** la estimación pertenece a la identidad autenticada, **cuando** el usuario confirma la eliminación, **entonces** la respuesta es `204 No Content`, el registro se elimina y deja de aparecer en el historial.

- **RF-22-AC-2:** **Dado que** el usuario cancela la confirmación o el registro pertenece a otra cuenta, **cuando** finaliza la interacción, **entonces** el registro se conserva sin cambios y la respuesta es `403` con `ACCESO_DENEGADO` en el segundo caso.

---

#### RF-23 — Generación y descarga del reporte PDF

**Descripción:** El sistema debe generar a solicitud del usuario un PDF de la estimación exitosa que se está observando, con los valores, fechas, confianza, factores y comparables de pantalla.

#### Criterios de Aceptación

- **RF-23-AC-1:** **Dado que** existe una estimación descargable y vigente, **cuando** el usuario solicita la generación del reporte, **entonces** la respuesta es `200 OK` con un archivo PDF que abre sin error en los visores de la matriz de RNF-09 y cuyo texto extraído contiene la ficha del inmueble, los tres importes, el margen de error, la confianza, la explicación, los comparables, las dos fechas y el texto íntegro de RD-02.

- **RF-23-AC-2:** **Dado que** ya se generó un reporte para una estimación, **cuando** el usuario vuelve a solicitarlo sin haber creado una estimación nueva, **entonces** la respuesta es `200 OK` con el mismo contenido, las mismas fechas y la misma fecha de emisión, y **el motor de inferencia no registra una nueva invocación**.

- **RF-23-AC-3:** **Dado que** la generación del reporte falla, **cuando** el usuario reintenta descargarlo, **entonces** el error se informa como fallo de reporte, el resultado permanece visible y el reintento genera el mismo contenido sin invocar de nuevo al modelo.

---

#### RF-24 — Protección de datos en el reporte

**Descripción:** El sistema debe omitir toda información identificable del propietario y toda ubicación exacta en el PDF, y debe rechazar cualquier solicitud que intente incluirla.

#### Criterios de Aceptación

- **RF-24-AC-1:** **Dado que** un resultado contiene calle, número exterior, número interior y coordenadas exactas de la propiedad, **cuando** se genera el PDF y se inspecciona su texto, sus imágenes, sus metadatos, sus enlaces y su nombre de archivo, **entonces** ninguno de esos componentes identificables aparece, y sólo se conserva la ubicación de zona permitida por RD-01.

- **RF-24-AC-2:** **Dado que** el usuario realiza una descarga con la configuración predeterminada, **cuando** el sistema genera el PDF, **entonces** aplica automáticamente la omisión de dirección y de datos del propietario, **sin pedir una acción de anonimización y sin ofrecer una opción para revelar la ubicación exacta**.

- **RF-24-AC-3:** **Dado que** un cliente agrega a la solicitud de reporte una instrucción no admitida para incluir dirección exacta o datos de contacto del propietario, **cuando** el servidor la procesa, **entonces** la respuesta es `422` con `NO_SE_PERMITE_REVELAR_DIRECCION` y **no se genera ningún PDF** para esa solicitud.

---

#### RF-25 — Compartición del reporte

**Descripción:** El sistema debe permitir compartir el PDF generado mediante el puente de compartición del sistema operativo, degradando a descarga directa cuando la aplicación de destino no está disponible.

#### Criterios de Aceptación

- **RF-25-AC-1:** **Dado que** existe un reporte PDF generado, **cuando** el usuario activa la opción de compartir con una aplicación de destino instalada, **entonces** el sistema invoca el puente del sistema operativo con el archivo adjunto y un mensaje precargado, y **en ese paso el binario no se transmite a ningún servidor distinto del que lo generó**.

- **RF-25-AC-2:** **Dado que** el dispositivo no dispone de la aplicación de destino instalada, **cuando** el usuario activa la opción de compartir, **entonces** el sistema ofrece la descarga directa del PDF y presenta un mensaje de disponibilidad, sin producir un error no manejado.

---

### 3.2 Requerimientos no funcionales (RNF)

| ID | Requerimiento | Categoría | Método de verificación |
|---|---|---|---|
| **RNF-01** | El percentil 95 del tiempo total de respuesta de una estimación, medido desde el envío en el navegador hasta la presentación del resultado completo, debe ser **≤ 3 segundos**. Ejecutar 20 sesiones concurrentes, 50 solicitudes secuenciales por sesión, sin pausa voluntaria, con distribución entre municipios. Entorno con la configuración de despliegue del piloto documentada; por cliente, red de 10 Mbps de bajada, 2 Mbps de subida y latencia ida/vuelta de 100 ms. Usar modelo real y réplicas autorizadas de datos, nunca respuestas simuladas ni caché. Errores, rechazos inesperados y timeouts cuentan como incumplimientos. La generación del PDF se prueba por separado. | Rendimiento | Prueba de carga con al menos 1,000 solicitudes elegibles |
| **RNF-02** | La API debe soportar **200 solicitudes de inferencia concurrentes** sin superar el límite de tiempo de RNF-01 y con **menos del 1 % de errores** durante la prueba de carga. | Escalabilidad | Prueba de concurrencia con conteo de errores por código |
| **RNF-03** | Disponibilidad **≥ 99,0 % por mes calendario**, calculada como `100 × minutos operativos / minutos totales del mes`, **excluyendo ventanas de mantenimiento**, que deben ser declaradas con **al menos 72 horas de anticipación** y de duración máxima de 4 horas. Un monitor externo inicia al comienzo de cada minuto una prueba de acceso y estimación con entrada elegible **contra el servicio real, no una respuesta simulada**. Un error, una muestra ausente o una respuesta no recibida antes de 30 s marcan el minuto como no operativo. La latencia se mide por separado en RNF-01. | Disponibilidad | Sonda externa con conservación de tiempos y estado |
| **RNF-04** | El **MdAPE del valor central será ≤ 15 % por unidad de cobertura** (municipio o zona), no sólo en el agregado. Evaluar como mínimo **100 operaciones de cierre verificadas** por unidad de cobertura, con referencia positiva, no usadas en entrenamiento ni en selección del modelo y sin propiedades duplicadas entre conjuntos. Registrar fecha, fuente, muestra y versión. Los avalúos y precios publicados pueden analizarse por separado, pero **no mezclarse como si fueran cierres**. La falta de muestra **impide acreditar** el objetivo. | Precisión | Cálculo de MdAPE por unidad de cobertura con muestra verificable |
| **RNF-05** | El despliegue de una versión del modelo está condicionado a que su MdAPE en el conjunto de prueba sea **≤ 15 %** conforme a RNF-04; si el umbral no se cumple, la versión **no se promociona**. El sistema debe medir **deriva entre reentrenamientos**: si el error medio de las estimaciones emitidas supera el 15 % durante **dos semanas consecutivas**, se genera una alerta al equipo de datos. | Calidad / Operación | Registro de promoción con la métrica de la versión; prueba con serie sintética de error |
| **RNF-06** | El tiempo total de llenado del formulario de captura por parte de un usuario entrenado **no debe exceder 120 segundos**, medido en el percentil 90 sobre al menos 5 usuarios de campo. | Usabilidad / Eficiencia | Prueba cronometrada con 5 o más usuarios |
| **RNF-07** | La interfaz debe ser **100 % responsiva**, operada con una sola mano, con **objetivos táctiles de al menos 48 × 48 px** y sin desplazamiento horizontal del formulario. | Usabilidad | Auditoría de plantilla y prueba de interacción con una mano |
| **RNF-08** | Los formularios deben poder completarse **con teclado**, mostrar **etiquetas visibles y asociadas a cada control**, conservar los datos válidos después de un error y cumplir **contraste de nivel AA de WCAG 2.1** en las pantallas principales. | Accesibilidad | Auditoría de contraste sobre pares texto/fondo y prueba de navegación por teclado |
| **RNF-09** | Captura, ayuda, resultado y descarga deben funcionar sin controles ocultos ni desplazamiento horizontal a **360, 768, 1366 y 1440 px CSS**. Probar **Chrome, Firefox, Edge y Safari** en escritorio, **Chrome en Android** y **Safari en iOS**, en la versión estable vigente al iniciar la aceptación, registrando versiones y dispositivos. | Compatibilidad | Matriz de dispositivos y navegadores con registro de versiones |
| **RNF-10** | Toda transmisión de entradas, resultados y PDF debe usar **HTTPS con TLS 1.3 o superior**. Verificar certificado válido, rechazo de versiones anteriores, ausencia de contenido mixto y que interfaz y API nunca envíen contenido de consulta por HTTP. Las solicitudes de cálculo o descarga por HTTP se rechazan **sin procesar su cuerpo**. La sesión se transmite en cookie `Secure`, `HttpOnly` y `SameSite`, **nunca en la URL**. Los datos personales y de autenticación se almacenan cifrados con **AES-256**. | Seguridad | Inspección de configuración de transporte y reposo |
| **RNF-11** | Las contraseñas se almacenan con **Argon2id o bcrypt** y nunca se registran en texto claro, respuestas ni logs. El token de sesión se firma con **HMAC-SHA256** y su vigencia por inactividad es de **2 horas**, renovable con actividad explícita. El mensaje de autenticación fallida no revela la existencia del correo. | Seguridad | Inspección del almacén de credenciales y prueba de expiración |
| **RNF-12** | Todo recurso persistente se filtra por **propiedad del registro**: por `usuarioId` para el historial y por identificador de sesión anónima para las consultas. **Ningún usuario accede al historial ajeno y ninguna sesión accede a la consulta de otra.** No existe un rol administrador con acceso a los datos de los usuarios. Verificar con intentos de acceso cruzado entre dos cuentas y entre dos sesiones anónimas. | Seguridad | Pruebas de acceso cruzado; deben fallar en el 100 % de los intentos |
| **RNF-13** | La aplicación **no debe solicitar ni almacenar**: dirección exacta, nombre del propietario, teléfono, correo del propietario, identificación, escrituras, documentos del inmueble ni datos bancarios. Ningún formulario del flujo básico ni el contrato de API deben exponer campos para subir documentos personales. Verificar en interfaz y en esquema de entrada. | Privacidad / Minimización | Inspección de formularios y del esquema de entrada |
| **RNF-14** | **Consultas anónimas:** entradas, resultados y PDF se eliminan al finalizar expresamente la consulta o al vencer sus 60 minutos; las fallidas o abandonadas siguen el plazo desde su recepción. **Historial autenticado:** las estimaciones se conservan **12 meses** desde su emisión y se eliminan automáticamente al vencer el plazo, sin que el usuario deba solicitarlo, y el usuario puede eliminarlas antes mediante RF-22. **Transporte de respuestas:** las respuestas con contenido de consulta usan `Cache-Control: no-store` y no se guardan en almacenamiento persistente del navegador. **Logs:** los logs operativos pueden conservar 30 días únicamente instante, ruta sin parámetros, estado, duración y versión técnica, **sin cuerpos, tokens, identificadores de consulta, IP ni datos de contacto**. Verificar consultas de prueba al borde del plazo, cachés, logs y respaldos. El PDF ya descargado por el usuario queda fuera del borrado remoto. | Privacidad / Cumplimiento | Prueba de purga con fecha simulada e inspección de cachés, logs y respaldos |
| **RNF-15** | La API debe aplicar **limitación de tasa**: máximo **60 solicitudes por minuto** en rutas de lectura y **10 por minuto** en la ruta de cálculo, con respuesta `429` y cabecera `Retry-After`. Adicionalmente, una dirección de origen sin autenticación puede realizar **máximo 3 estimaciones por día calendario**; la cuarta responde `429` con `LIMITE_DIARIO_ALCANZADO`. El consumo de cuota se registra una sola vez por operación efectiva gracias a la idempotencia de RF-07. | Seguridad / Disponibilidad | Prueba de control de tasa por identificador y por dirección de origen |
| **RNF-16** | La aplicación debe mantener **operación estable en redes móviles de baja cobertura o alta latencia**, sin pérdida de los datos capturados en el formulario ante una interrupción de la conexión. | Confiabilidad | Prueba en red con limitación de ancho de banda y latencia añadida |
| **RNF-17** | La API debe contar con **pruebas automatizadas para la totalidad de los criterios de aceptación** y alcanzar al menos **80 % de cobertura de líneas** en los módulos de validación, autenticación, autorización, historial, ciclo de vida de consulta anónima y generación de reportes. | Mantenibilidad | Reporte de cobertura e informe de trazabilidad de pruebas |
| **RNF-18** | Se podrá incorporar una **nueva localidad, tipo de inmueble o uso de suelo** mediante catálogos, esquema de campos, reglas y modelo específicos **sin cambiar el código del flujo compartido** de captura, consulta y reporte. Verificar con una configuración de prueba, revisión de diferencias de código y regresión del piloto. Esto **no habilita por sí mismo** nuevas localidades en producción. | Mantenibilidad / Extensibilidad | Revisión de diferencias de código y prueba de regresión |
| **RNF-19** | El pipeline de reentrenamiento del modelo debe estar **automatizado con periodicidad trimestral** y la revisión de datos debe ser **mensual**. Verificar la ejecución programada en dos ciclos consecutivos. | Mantenibilidad | Ejecución programada verificada en dos ciclos |

### 3.3 Requerimientos de dominio (RD)

| ID | Regla | Consecuencia operativa | Criterios que la aplican |
|---|---|---|---|
| **RD-01** | **Cobertura y datos de entrada.** La cobertura se comprueba con catálogo, nunca con texto libre. Una solicitud sólo es estimable cuando la combinación de estado, municipio, colonia, tipo de inmueble y uso de suelo está activa. **Campos obligatorios:** estado, municipio, colonia o código postal resuelto a colonia, tipo de inmueble, uso de suelo, superficie de terreno, superficie construida, habitaciones y baños completos. **Opcionales:** estacionamientos, antigüedad, conservación, tipo de entrega, amenidades, medios baños, remodelación, cuarto de servicio y cercanía a parque. **Formatos:** las áreas son números positivos con hasta dos decimales en m²; habitaciones y baños completos son enteros ≥ 1; estacionamientos y antigüedad son enteros ≥ 0; conservación admite `buena`, `regular` o `mala`; el uso de suelo admite `habitacional` o `comercial`. Estado, municipio, colonia y código postal deben corresponder al mismo registro del catálogo. | Los puntos fuera de cobertura no producen estimación. Los opcionales no se vuelven obligatorios por estar definidos. | RF-02-AC-1 a AC-3, RF-04-AC-3, RF-06 |
| **RD-02** | **Carácter orientativo.** Cada resultado, cada PDF y cada respuesta debe contener el texto: *"Estimación orientativa de MLState. No sustituye un avalúo profesional, bancario u oficial ni garantiza el precio final de venta"*. Ninguna pantalla, archivo o respuesta podrá describir el resultado como avalúo, precio garantizado o valor oficial. | Materializada en la interfaz por RF-15 y en todos los documentos por RF-23. | RF-15, RF-23-AC-1, RF-23-AC-3 |
| **RD-03** | **Moneda y zona horaria.** Todos los valores económicos calculados, almacenados, mostrados y exportados se expresan en **pesos mexicanos (MXN)**. MLState no realiza conversión de moneda. Las fechas de negocio se interpretan en `America/Mexico_City`; los plazos se calculan con reloj de servidor en UTC. | Ningún valor se presenta en otra moneda. La zona horaria de presentación es fija y no configurable por el usuario. | RF-07-AC-1, RF-11-AC-3, RF-18-AC-2 |
| **RD-04** | **Unidades y definición de precio por m².** Las superficies se expresan en `m²` y los precios en MXN. *"Precio por m²"* significa **siempre** precio por m² de **construcción**; no se mezcla con el precio por m² de terreno. El precio unitario se redondea a dos decimales con empate hacia arriba. | Evita ambigüedad en la presentación del indicador unitario. | RF-11-AC-1, RF-11-AC-2 |
| **RD-05** | **Datos autorizados y trazabilidad de fuentes.** Cada conjunto utilizado para entrenamiento, cálculo o comparables debe contar con evidencia de propiedad, licencia abierta o licencia vigente que autorice el uso correspondiente y **la exhibición cuando aplique**. El inventario registra fuente, usos autorizados y vigencia; se bloquean fuentes sin autorización o vencidas. **No se asume que una licencia para entrenar permite publicar comparables.** Cada versión tiene identificador, actualización validada, antigüedad máxima aprobada y clave normalizada de propiedad para deduplicación. La revocación de derechos de una fuente bloquea el modelo dependiente hasta que el responsable de datos documente si la licencia permite seguir usándolo. | Sin esta evidencia, la zona no se habilita. Un comparable exhibible requiere tipo, ubicación, superficies, precio positivo finito, naturaleza, fecha dentro de la ventana y permiso de exhibición. | RF-10, RF-14-AC-4, RNF-04 |
| **RD-06** | **Abstención por muestra insuficiente.** El sistema debe abstenerse de emitir estimación y notificar la falta de muestra cuando la zona no alcance la suficiencia aprobada de referencias válidas y distintas. No se fuerzan rangos sin representatividad estadística ni se sustituye una muestra insuficiente con comparables exhibidos. | El conteo de referencias para suficiencia es independiente del conteo de comparables mostrados. | RF-08, RF-10-AC-3, RF-12-AC-3 |
| **RD-07** | **Consistencia aritmética del resultado.** Todos los importes deben ser números finitos positivos y satisfacer `valorMínimo > 0` y `valorMínimo ≤ valorCentral ≤ valorMáximo`. El margen de error debe ser mayor o igual a cero y no exceder la mitad de la amplitud relativa del rango. Una respuesta del motor que no cumpla estas condiciones se trata como error técnico: **no se corrige ni se completa silenciosamente**. | Impide publicar importes incoherentes o inventados. | RF-07-AC-1, RF-07-AC-3, RF-12-AC-1 |
| **RD-08** | **Minimización y protección de identidad y ubicación.** El sistema no solicita ni almacena dirección exacta, coordenadas, nombre del propietario, teléfono, correo del propietario, identificación, escrituras, documentos del inmueble ni datos bancarios. Resultados, comparables y reportes no incluyen datos ni enlaces que identifiquen al propietario. En los reportes sólo se muestra estado, municipio y colonia o código postal. | La protección se aplica automáticamente, sin opción de revelado, y el servidor rechaza toda instrucción contrary. | RF-24, RNF-13 |
| **RD-09** | **Ausencia de transacciones y de responsabilidad profesional.** El alcance es estrictamente orientativo: no hay compras, ventas, pagos, contratos, publicación de anuncios, recomendación de crédito ni contacto entre compradores y vendedores. La responsabilidad sobre decisiones comerciales recae únicamente en el usuario. | No existe flujo transaccional en ninguna pantalla. | §1.2.2, RF-15 |
| **RD-10** | **Homogeneización y ventana de comparables.** Los atributos físicos de los comparables se homogeneizan antes de la comparación, ajustando diferencias de estado de conservación y acabados; no se devuelve un comparable en obra gris frente a uno remodelado sin esa normalización. La ventana máxima de antigüedad es de **12 meses calendario inclusive**, calculada desde la fecha de cálculo; los registros con fecha futura quedan excluidos. | Un comparable de cinco años puede ser irrelevante en un mercado que se mueve por inflación. | RF-14-AC-2, RF-14-AC-3 |
| **RD-11** | **Procedencia del dato de entrenamiento.** El modelo debe alimentarse **prioritariamente de precios de transacciones cerradas y verificadas**. Los avalúos y los precios de publicación pueden utilizarse como apoyo o analizarse por separado, siempre que se declaren y no se mezclen como si fueran cierres. Las fuentes deben ser reproducibles y citables. | La precisión de RNF-04 sólo es acreditable si el dato de referencia y el de entrenamiento tienen la misma naturaleza. | RNF-04, RNF-05 |

---

## 4. Índice de trazabilidad de criterios de aceptación

Cada fila es una clave de trazabilidad compartible entre este documento, la especificación OpenAPI derivada y una prueba automatizada.

| ID del criterio | Requerimiento | Tipo | Operación referenciada | Verificación |
|---|---|---|---|---|
| `RF-01-AC-1` | RF-01 | Exitoso | `GET /catalogos` | Automatizada |
| `RF-01-AC-2` | RF-01 | Validación | `GET /catalogos` | Automatizada |
| `RF-01-AC-3` | RF-01 | Validación | `GET /catalogos` | Automatizada |
| `RF-02-AC-1` | RF-02 | Exitoso | `POST /catalogos/elegibilidad` | Automatizada |
| `RF-02-AC-2` | RF-02 | Validación | `POST /catalogos/elegibilidad` | Automatizada |
| `RF-02-AC-3` | RF-02 | Validación | `POST /catalogos/elegibilidad` | Automatizada |
| `RF-03-AC-1` | RF-03 | Exitoso | `GET /catalogos`, `POST /borradores` | Automatizada |
| `RF-03-AC-2` | RF-03 | Alternativo | Interfaz de captura | Manual o automatizada |
| `RF-03-AC-3` | RF-03 | Alternativo | Interfaz de ayuda | Manual |
| `RF-04-AC-1` | RF-04 | Validación | `PUT /borradores/{id}` | Automatizada |
| `RF-04-AC-2` | RF-04 | Alternativo | `PUT /borradores/{id}` | Automatizada |
| `RF-04-AC-3` | RF-04 | Validación | `POST /catalogos/elegibilidad` | Automatizada |
| `RF-05-AC-1` | RF-05 | Validación | `POST /estimaciones` | Automatizada |
| `RF-05-AC-2` | RF-05 | Validación | `PUT /borradores/{id}` | Automatizada |
| `RF-05-AC-3` | RF-05 | Alternativo | `POST /estimaciones` | Automatizada |
| `RF-06-AC-1` | RF-06 | Validación | `POST /estimaciones` | Automatizada |
| `RF-06-AC-2` | RF-06 | Alternativo | Interfaz de errores | Automatizada |
| `RF-06-AC-3` | RF-06 | Alternativo | `POST /estimaciones` | Automatizada |
| `RF-07-AC-1` | RF-07 | Exitoso | `POST /estimaciones` | Automatizada |
| `RF-07-AC-2` | RF-07 | Alternativo | `POST /estimaciones` | Automatizada |
| `RF-07-AC-3` | RF-07 | Validación | `GET /estimaciones/{id}` | Automatizada |
| `RF-07-AC-4` | RF-07 | Alternativo | `POST /estimaciones` | Automatizada |
| `RF-08-AC-1` | RF-08 | Validación | `POST /estimaciones` | Automatizada |
| `RF-08-AC-2` | RF-08 | Validación | `POST /estimaciones` | Automatizada |
| `RF-08-AC-3` | RF-08 | Alternativo | `POST /estimaciones` | Automatizada |
| `RF-09-AC-1` | RF-09 | Alternativo | `POST /estimaciones` | Automatizada |
| `RF-09-AC-2` | RF-09 | Alternativo | Interfaz de espera | Manual o automatizada |
| `RF-09-AC-3` | RF-09 | Validación | Interfaz de reintento | Automatizada |
| `RF-10-AC-1` | RF-10 | Validación | `POST /estimaciones` | Automatizada |
| `RF-10-AC-2` | RF-10 | Validación | `POST /estimaciones` | Automatizada |
| `RF-10-AC-3` | RF-10 | Validación | Proceso de validación de datos | Automatizada |
| `RF-11-AC-1` | RF-11 | Exitoso | `GET /estimaciones/{id}` | Automatizada |
| `RF-11-AC-2` | RF-11 | Alternativo | `GET /estimaciones/{id}` | Automatizada |
| `RF-11-AC-3` | RF-11 | Exitoso | `GET /estimaciones/{id}` | Automatizada |
| `RF-12-AC-1` | RF-12 | Exitoso | `GET /estimaciones/{id}` | Automatizada |
| `RF-12-AC-2` | RF-12 | Alternativo | `GET /estimaciones/{id}` | Automatizada |
| `RF-12-AC-3` | RF-12 | Alternativo | `GET /estimaciones/{id}` | Automatizada |
| `RF-13-AC-1` | RF-13 | Exitoso | `GET /estimaciones/{id}` | Automatizada |
| `RF-13-AC-2` | RF-13 | Alternativo | `GET /estimaciones/{id}` | Automatizada |
| `RF-13-AC-3` | RF-13 | Alternativo | `GET /estimaciones/{id}` | Automatizada |
| `RF-14-AC-1` | RF-14 | Exitoso | `GET /estimaciones/{id}/comparables` | Automatizada |
| `RF-14-AC-2` | RF-14 | Alternativo | `GET /estimaciones/{id}/comparables` | Automatizada |
| `RF-14-AC-3` | RF-14 | Alternativo | `GET /estimaciones/{id}/comparables` | Automatizada |
| `RF-14-AC-4` | RF-14 | Validación | `GET /estimaciones/{id}/comparables` | Automatizada |
| `RF-15-AC-1` | RF-15 | Exitoso | Interfaz de resultado | Manual o automatizada |
| `RF-15-AC-2` | RF-15 | Alternativo | Modelo de objetos del documento | Automatizada |
| `RF-15-AC-3` | RF-15 | Exitoso | PDF generado | Automatizada |
| `RF-16-AC-1` | RF-16 | Exitoso | `POST /auth/registro` | Automatizada |
| `RF-16-AC-2` | RF-16 | Validación | `POST /auth/registro` | Automatizada |
| `RF-16-AC-3` | RF-16 | Validación | `POST /auth/registro` | Automatizada |
| `RF-17-AC-1` | RF-17 | Exitoso | `POST /auth/login` | Automatizada |
| `RF-17-AC-2` | RF-17 | Validación | `POST /auth/login` | Automatizada |
| `RF-17-AC-3` | RF-17 | Alternativo | Operación autenticada | Automatizada |
| `RF-18-AC-1` | RF-18 | Exitoso | `POST /estimaciones`, `POST /reporte` | Automatizada |
| `RF-18-AC-2` | RF-18 | Alternativo | `GET /consultas/{id}` | Automatizada |
| `RF-18-AC-3` | RF-18 | Validación | `GET /consultas/{id}` | Automatizada |
| `RF-18-AC-4` | RF-18 | Alternativo | `POST /consultas/{id}/finalizar` | Automatizada |
| `RF-19-AC-1` | RF-19 | Exitoso | `POST /historial` | Automatizada |
| `RF-19-AC-2` | RF-19 | Validación | `POST /historial` | Automatizada |
| `RF-20-AC-1` | RF-20 | Exitoso | `GET /historial` | Automatizada |
| `RF-20-AC-2` | RF-20 | Alternativo | `GET /historial` | Automatizada |
| `RF-20-AC-3` | RF-20 | Validación | `GET /historial` | Automatizada |
| `RF-21-AC-1` | RF-21 | Exitoso | `GET /historial/{id}` | Automatizada |
| `RF-21-AC-2` | RF-21 | Validación | `GET /historial/{id}` | Automatizada |
| `RF-22-AC-1` | RF-22 | Exitoso | `DELETE /historial/{id}` | Automatizada |
| `RF-22-AC-2` | RF-22 | Validación | `DELETE /historial/{id}` | Automatizada |
| `RF-23-AC-1` | RF-23 | Exitoso | `POST /estimaciones/{id}/reporte` | Automatizada |
| `RF-23-AC-2` | RF-23 | Alternativo | `POST /estimaciones/{id}/reporte` | Automatizada |
| `RF-23-AC-3` | RF-23 | Alternativo | `POST /estimaciones/{id}/reporte` | Automatizada |
| `RF-24-AC-1` | RF-24 | Validación | PDF generado | Automatizada |
| `RF-24-AC-2` | RF-24 | Exitoso | `POST /estimaciones/{id}/reporte` | Automatizada |
| `RF-24-AC-3` | RF-24 | Validación | `POST /estimaciones/{id}/reporte` | Automatizada |
| `RF-25-AC-1` | RF-25 | Exitoso | Puente de compartición | Manual en dispositivo real |
| `RF-25-AC-2` | RF-25 | Alternativo | Puente de compartición | Manual en dispositivo real |

**Totales: 74 criterios de aceptación distribuidos en 25 requerimientos funcionales.**

| Dimensión | Desglose |
|---|---|
| **Por tipo** | 21 exitosos, 26 alternativos, 27 de validación |
| **Por verificabilidad** | 68 automatizables, 3 automatizables de forma parcial, 1 manual de interfaz, 2 manuales en dispositivo real |
| **Por requerimiento** | Mínimo 2 criterios. RF-07, RF-14 y RF-18 concentran 4 cada uno, por la densidad de riesgos de cálculo, de comparables y de aislamiento que asumen. |

---

## 5. Trazabilidad de requisitos

| Fuente | Requisitos derivados en este SRS |
|---|---|
| `SRS_final_carlos.md` | RF-04, RF-05, RF-06, RF-16, RF-17, RF-19, RF-20, RF-21, RF-22; RNF-11, RNF-12, RNF-13, RNF-17; RD-01, RD-07 |
| `SRS_final_mark.md` | RF-01, RF-07, RF-16, RF-17, RF-19, RF-23; RNF-02, RNF-03, RNF-15; RD-01, RD-03 |
| `SRS_final_Anuar.md` | RF-02, RF-03, RF-04, RF-05, RF-06, RF-07, RF-08, RF-09, RF-10, RF-11, RF-12, RF-13, RF-14, RF-15, RF-18, RF-23, RF-24; RNF-01, RNF-03, RNF-04, RNF-05, RNF-13, RNF-14, RNF-18; RD-01, RD-02, RD-04, RD-05, RD-06, RD-08 |
| `SRS_final_Chris.md` | RF-01, RF-03, RF-07, RF-08, RF-11, RF-12, RF-13, RF-14, RF-15, RF-16, RF-17, RF-19, RF-20, RF-23, RF-25; RNF-01, RNF-06, RNF-07, RNF-08, RNF-09, RNF-10, RNF-11, RNF-12, RNF-14, RNF-16, RNF-19; RD-02, RD-03, RD-07, RD-09, RD-10, RD-11 |

### 5.1 Correcciones de ambigüedad aplicadas en esta versión

| ID | Ambigüedad detectada entre los documentos de origen | Resolución aplicada |
|---|---|---|
| M-01 | Uso de suelo y superficie de terreno aparecían como obligatorios en un documento y como opcionales con valor por defecto en otro. | RD-01 fija un conjunto único de obligatorios; los opcionales ausentes se propagan como ausentes y degradan la confianza. |
| M-02 | El número de comparables a exhibir era 3 a 4 en un documento y 3 a 5 en otro. | RF-14 fija 3 a 5 y la ventana de 12 meses, con prueba de los tres casos. |
| M-03 | La precisión se medía con media del error porcentual absoluto en un documento y con mediana en otro, con umbrales de 10 % y 15 %. | RNF-04 fija **MdAPE ≤ 15 % por unidad de cobertura**; RNF-05 conserva los gates de Chris (promoción y deriva) con el mismo umbral. |
| M-04 | El número de días, el valor del p95 y la base de cálculo de la disponibilidad difieren entre documentos. | RNF-01 fija p95 ≤ 3 s con el entorno de red explícito; RNF-03 fija 99,0 % excluyendo ventanas de mantenimiento **declaradas con 72 h de anticipación y máximo 4 h**. |
| M-05 | Un documento exigía dirección exacta y mapa; otros dos los prohibían expresamente. | D-02 y RD-08 resuelven a favor de la prohibición. El mapa y la geocodificación quedan fuera de alcance. |
| M-06 | La vigencia de los datos se medía en 12 meses o en 60 minutos según el flujo. | RNF-14 las separa por flujo: 60 minutos para consultas anónimas, 12 meses para historial autenticado. |
| M-07 | No estaba definido qué ocurre cuando el motor es lento frente a cuando está caído. | RF-09 separa el timeout de transporte (5 s, RNF-01) del timeout de interfaz (30 s). |
| M-08 | La versión de TLS era 1.2 en un documento, 1.3 en otro y "HTTPS" genérico en un tercero. | RNF-10 fija **TLS 1.3 o superior** y añade el cifrado en reposo AES-256. |
| M-09 | Un documento prohibía toda gestión del modelo y de datos mediante la interfaz; otro exigía un panel administrativo. | D-04 resuelve sin panel. RF-10 cubre la verificación y RNF-19 la operación automatizada. |
| M-10 | Los criterios no coincidían en el nivel de detalle de la inspección: unos exigían código HTTP, otro los prohibía expresamente. | §1.4.3 fija la regla de verificabilidad y §3.0.3 declara la superficie de API como **informativa**, de modo que el mapeo a rutas y códigos puede cambiar sin invalidar los AC. |
| M-11 | El redondeo del resultado y del precio unitario no estaba fijado. | RF-07 redondea importes a pesos enteros; RD-04 fija el precio unitario a dos decimales con empate hacia arriba. |
| M-12 | No estaba definido si una construcción mayor que el terreno constitute un error. | RF-04-AC-2 lo declara explícitamente válido. |

---

## 6. Requisitos no incluidos en esta versión

| Requisito de origen | Integrante | Motivo de exclusión |
|---|---|---|
| Mapa interactivo, geocodificación y validación de punto geográfico | Chris (RF-03) | D-02. Excluido por privacidad (RD-08) y por la prohibición expresa de carlos y Anuar. Reevaluable sólo con decisión de negocio y avaliação de riesgo. |
| Captura de dirección exacta y coordenadas | Chris (RF-03) | D-02, RD-08. |
| Panel administrativo de parámetros del modelo | mark (RF-07) | D-04. Sustituido por RF-10 y RNF-19. |
| Panel administrativo de datos de entrenamiento | mark (RF-08) | D-04. Sustituido por RF-10 y RNF-19. |
| Perfil del broker con datos de contacto de la agencia y encabezado de reporte | Chris (RF-10) | P-04: sin verificación de identidad permite atribuir a una agencia un informe que no emitió. |
| Comparación tabular y gráfica de estimaciones guardadas | Chris (RF-13) | P-06: depende del modelo de identidad y del plazo de entrega. |
| Validación de amenidades inconsistentes (`AMENIDAD_INCONSISTENTE`) | Chris (RF-02-AC-3) | Atribuye una regla de negocio a un caso particular no respaldado por la elicitación. Reevaluable con P-01. |
| Modelo de dos fases con borrador persistido en servidor | Chris (§3.0.3) | Se conserva la **idempotencia** en RF-07-AC-2 por su valor real; la persistencia del borrador queda como decisión de diseño. |
| Imputación de valores por defecto desde estadística zonal | mark (RD-04) | X-10. Se sustituye por propagación del vacío con degradación de confianza, para no fabricar datos. |
| Comparables sin requerimiento propio | mark (§1.2, RF-04) | Se conserva la mención como parte del contenido del PDF y se eleva a requerimiento propio en RF-14. |

---

## 7. Restricciones de la unificación

Esta sección declara las limitaciones del documento para que nadie las interprete como consensus achieved.

1. **La cobertura geográfica no está enumerada.** RD-01 la delega al catálogo de RF-01. La lista de estados, municipios y colonias habilitados es un dato de configuración, no un requisito, y debe publicarse antes de la aceptación.
2. **El umbral de precisión del 15 % es una decisión de negocio, no una garantía técnica.** Si el negocio requiere 10 %, debe actualizar RNF-04 y RNF-05 en la misma revisión.
3. **Los umbrales de plausibilidad por campo y zona (P-01) siguen sin definirse.** RF-05 verifica el mecanismo de confirmación contra una política sintética; la política real debe publicarse antes de la aceptación.
4. **La fuente de datos de transacciones cerradas (P-02) no está identificada.** Sin ella, RNF-04 no es ejecutable.
5. **El método de calibración del intervalo y el método explicativo (P-03) siguen sin definirse.** RF-12 y RF-13 verifican el mecanismo, no el método.
6. **El volumen objetivo de usuarios no está definido (P-07).** RNF-01 y RNF-02 no pueden validarse contra una carga realista hasta que el Product Owner lo fije.
7. **La decisión de D-03 (cobertura) es mayoritaria, no ratificada.** Anuar la limitaba a casas usadas habitacionales en Guadalajara y Zapopan, y declaraba esa restricción como pendiente de ratificación. Este SRS la sustituyó por cobertura de catálogo ampliable (RD-01 y RNF-18). Si el negocio confirma el alcance acotado, RD-01 debe modificarse y RNF-04 se vuelve más fácil de acreditar.

---

## 8. Puntos abiertos

Ninguno de estos puntos fue resuelto en esta versión porque requiere una decisión de negocio o información que no está disponible. **Los dos primeros bloquean la fase de diseño.**

| ID | Cuestión abierta | Impacto | Referencias |
|---|---|---|---|
| **P-01** | **Límites de plausibilidad por campo y zona.** No existe tabla de límites ni política de umbrales de amplitud relativa. | **Bloqueante** para fijar la política de producción. Sin valor, los criterios de RF-05 verifican el mecanismo contra datos sintéticos, no contra la política real. | RF-05, RF-12, RD-07 |
| **P-02** | **Fuente de datos de transacciones cerradas.** RD-04 y RD-11 exigen precios de cierre verificados; no está identificada la fuente, su contrato, su licencia ni su antigüedad máxima. | **Bloqueante.** Sin fuente autorizada, RNF-04 no es acreditable y RF-10 mantiene todas las zonas deshabilitadas. | RD-05, RD-11, RF-10, RNF-04 |
| **P-03** | **Método y calibración del intervalo, y método explicativo.** No está definido cómo se calibran los límites ni cómo se produce la explicación en lenguaje natural. | Alto. RF-12 y RF-13 verifican la forma del resultado, no el método que lo produce. | RF-12, RF-13, RD-07 |
| **P-04** | **Verificación de identidad del broker.** No está definido si la cuenta se verifica. | Medio. Bloquea la posible incorporación del encabezado personalizado y del reporte con marca de agencia. | §1.2.2, §6 |
| **P-05** | **Periodo de inactividad de sesión.** El comportamiento está especificado en RF-17-AC-3 con `SESION_EXPIRADA`; el valor por defecto de 2 horas es una propuesta de este SRS y no ha sido validado por el negocio. | Bajo. El efecto ya es verificable; falta confirmar el parámetro. | RNF-11, RF-17-AC-3 |
| **P-06** | **Comparación entre estimaciones guardadas.** Se excluyó del alcance. Depende de la decisión de identidad y del plazo. | Bajo. Diferible a una fase posterior. | §1.2.2, §6 |
| **P-07** | **Volumetría objetivo y ventana de mantenimiento.** No se definió número de usuarios concurrentes, peticiones por pico ni ventana de mantenimiento. | **Bloqueante** para validar RNF-01, RNF-02 y RNF-03 contra una carga realista. | RNF-01, RNF-02, RNF-03 |
| **P-08** | **Umbral de confianza.** Se adoptó el valor de RNF-04 como referencia para el nivel de confianza sin que el negocio validara la equivalencia entre margen y categoría. | Medio. Afecta la etiqueta mostrada al usuario final. | RF-12, RNF-05 |
| **P-09** | **Contenido del reporte y encriptación del PDF descargado.** El PDF descargado queda fuera del borrado remoto por RNF-14; no se ha definido si debe ir cifrado o marcado como documento no oficial de forma verificable. | Medio. Afecta la custodia del documento por el usuario. | RNF-14, RF-23 |
| **P-10** | **Criterio de deduplicación de propiedades.** RD-05 exige una clave normalizada de propiedad, pero no se ha definido su construcción ni su fuente. | Medio. Sin clave, la deduplicación de comparables no es ejecutable. | RD-05, RF-14-AC-4 |

---

## 9. Referencias

| Documento | Relación |
|---|---|
| `proyecto_base.md` | Documento de origen del proyecto |
| `transcript_entrevista.md` | Registro de la elicitación de requisitos |
| `revision_SRS.md` | Propuesta refinada y bitácora de revisión |
| `SRS_final_carlos.md` | SRS individual consolidado — carlos, v1.0 |
| `SRS_final_mark.md` | SRS individual consolidado — mark |
| `SRS_final_Anuar.md` | SRS individual consolidado — Anuar, v0.4 |
| `SRS_final_Chris.md` | SRS individual consolidado — Chris, v2.0 |
| `SRS_gap_analysis.md` | Análisis de brechas que motivó esta consolidación |
| `Diferencias_SRS.md` | Aporte por integrante y resolución de conflictos |
| IEEE 830-1998 | Recommended Practice for Software Requirements Specifications |

---

*Fin del documento SRS_Equipo.md — versión 1.0 consolidada. Los puntos abiertos de la sección 8 y las restricciones de la sección 7 son parte del documento y no deben omitirse al citarlo.*