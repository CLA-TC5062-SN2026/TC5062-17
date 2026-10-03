# Diferencias entre los SRS individuales y el SRS consolidado
## MLState — Registro de aporte por integrante y resolución de conflictos

**Documento complementario de:** `SRS_Equipo.md` v1.0 (consolidada)
**Fecha de emisión:** 2026-10-02
**Estado:** Registro de trazabilidad de la consolidación. Ninguna decisión aquí está aprobada por el equipo; todas requieren ratificación del Product Owner.

---

## 1. Propósito y cómo leer este documento

`SRS_Equipo.md` no es un quinto SRS: es la FourthVersion de cuatro. Este documento responde tres preguntas que el SRS consolidado no puede responder por sí mismo:

1. **¿De quién es cada requisito?** Para que ningún aporte se pierda en silencio y para que el crédito de cada trabajo sea atribuible.
2. **¿Por qué un requisito se resolvió de una forma y no de otra?** Para que la decisión sea auditable y reversible si el negocio la revisa.
3. **¿Qué se descartó y por qué?** Para que una exclusión no se interprete como un olvido.

**Convención de lectura:**
- `Se adoptó` — el requisito del integrante pasó al SRS consolidado con su intención original.
- `Se adoptó parcialmente` — pasó con una modification respecto de lo propuesto.
- `Se fusionó` — se combinó con la propuesta de otro integrante porque cubrían el mismo comportamiento con mecanismos distintos.
- `Se sustituyó` — no pasó; otro mecanismo cubre el mismo riesgo.
- `Se excluyó` — no pasó, con motivo explícito.
- `Se difirió` — no pasó al alcance del piloto; queda registrado como pendiente.

---

## 2. Resumen cuantitativo del aporte

| Integrante | RF aportadas | RNF aportadas | RD aportadas | Aporte total | Contribución dominante |
|---|---|---|---|---|---|
| **Chris** | 15 | 11 | 6 | **32** | Espina dorsal completa: estructura IEEE 830, superficie de API, trazabilidad de 74 AC, modelo de dos fases, comparables, explicación, margen de error |
| **Anuar** | 17 | 7 | 6 | **30** | Método de verificación: fixtures sintéticos, gobierno de datos, ciclo de vida anónimo, abstención por muestra, versionado de instantánea |
| **carlos** | 9 | 4 | 2 | **15** | Contrato de API con códigos de negocio, credenciales seguras, ciclo CRUD completo del historial, cobertura de pruebas |
| **mark** | 6 | 3 | 2 | **11** | Modelo de roles, códigos HTTP, cuota de anónimos, escalabilidad y SLA |
| **Total con coautoría** | 25 | 19 | 11 | 55 | 25 + 19 + 11 = 55 requisitos, con doble o triple autoría en 31 de ellos |

### 2.1 Requisitos del SRS consolidado con mayor número de autores

| Requisito | Autores | Observación |
|---|---|---|
| **RF-01** Catálogo de cobertura | mark, Anuar, Chris | Consenso de 3 de 4 |
| **RF-07** Cálculo de la estimación | mark, Anuar, Chris | Consenso de 3 de 4 |
| **RF-15** Advertencia informativa | Anuar, Chris | Consenso de 2 de 4; carlos y mark aporte el sustento de fondo |
| **RF-23** Reporte PDF | mark, Anuar, Chris | Ausente en carlos |
| **RNF-11** Seguridad de credenciales | carlos, Chris | mark aportó el mecanismo, carlos el algoritmo |
| **RNF-12** Aislamiento de datos | carlos, Chris | Anuar y mark aportaron los casos de prueba |
| **RD-01** Cobertura y datos de entrada | carlos, mark, Anuar | Los tres son autores principales; Chris aportó el par de tipos |
| **RD-07** Consistencia del resultado | carlos, Chris | Anuar lo tenía implícito |

### 2.2 Distribución de la autoría

El 66 % del contenido consolidado proviene de Chris y Anuar, que son los dos documentos con mayor profundidad (1,031 y 328 líneas, frente a 171 de carlos). Esto refleja una asimetría de esfuerzo, no una jerarquía de autoría: carlos y mark aportaron las piezas de las que el resto de los documentos dependía sin declararlas — en particular, **el hashing de contraseñas (carlos) y el límite de cuota (mark) no existían en ninguna otra propuesta**.

---

## 3. Aporte de carlos

**Documento:** `SRS_final_carlos.md` v1.0, 171 líneas, 10 RF · 6 RNF · 6 RD
**Perfil:** Enfoque de contrato de API y códigos de negocio. Verificable y sobrio. Sin PDF, sin comparables, sin confianza.

### 3.1 Requisitos adoptados

| Origen | Requisito de carlos | Destino en SRS_Equipo | Estado |
|---|---|---|---|
| RF-01 | Registrar cuenta (nombre, correo, contraseña) | **RF-16** | Se adoptó |
| RF-02 | Iniciar sesión | **RF-17** | Se adoptó parcialmente: se añadió expiración por inactividad de Chris |
| RF-03 | Consultar la cobertura disponible | **RF-01** | Se fusionó con mark y Chris |
| RF-04 | Capturar y validar datos de la propiedad | **RF-03, RF-04** | Se adoptó; se separó en captura y validación |
| RF-05 | Calcular una estimación | **RF-07** | Se fusionó con Anuar y Chris |
| RF-06 | Presentar el resultado y sus límites | **RF-11, RF-15** | Se adoptó |
| RF-07 | Guardar una estimación | **RF-19** | Se adoptó |
| RF-08 | Consultar y filtrar el historial | **RF-20** | Se adoptó; se añadió el desempate de Chris |
| RF-09 | Consultar el detalle de una estimación | **RF-21** | Se adoptó |
| RF-10 | Eliminar una estimación guardada | **RF-22** | Se adoptó |
| RNF-02 | HTTPS + hash Argon2id o bcrypt | **RNF-10, RNF-11** | Se adoptó; es el **único** aporte de hashing del equipo |
| RNF-03 | Privacidad: sin dirección exacta, sin datos del propietario | **RNF-13** | Se adoptó y se amplió con Anuar |
| RNF-04 | Usabilidad y accesibilidad: teclado, etiquetas, WCAG 2.1 AA | **RNF-08** | Se adoptó: la versión de carlos es superconjunto de la de Chris |
| RNF-05 | Compatibilidad de navegador y ancho de pantalla | **RNF-09** | Se adoptó; se añadió Edge a la matriz de Anuar |
| RNF-06 | Mantenibilidad: pruebas para todos los AC, ≥ 80 % de cobertura | **RNF-17** | Se adoptó |
| RD-01 | Cobertura geográfica | **RD-01** | Se fusionó |
| RD-02 | Rangos de entrada | **RD-01** | Se **sustituyó** por rangos de plausibilidad por zona (ver X-12) |
| RD-03 | Uso de suelo habitacional o comercial | **RD-01** | Se adoptó |
| RD-04 | Consistencia del resultado | **RD-07** | Se adoptó como regla de dominio normativa |
| RD-05 | Moneda MXN sin conversión | **RD-03** | Se adoptó |
| RD-06 | Carácter informativo | **RD-02** | Se adoptó el texto de Anuar |

### 3.2 Piezas de carlos que hicieron posible el trabajo de los demás

Cuatro elementos de carlos no eran "requisitos nuevos" sino **lagunas que los otros tres documentos dejaron abiertas sin advertirlo**. Sin ellos, el SRS consolidado no habría sido implementable:

1. **Algoritmo de almacenamiento de contraseñas (RNF-11).** Ni mark, ni Anuar, ni Chris especificaban cómo se almacena una contraseña. Sin esto, la seguridad de credenciales es indeterminada.
2. **Existencia de la verificación de contraseña.** La política de complejidad (10 caracteres, mayúscula, minúscula, número) es la única del equipo.
3. **Right to erasure (RF-22).** Sin ella, la retención de 12 meses de Chris habría dejado al usuario sin control sobre sus datos.
4. **Endpoint de detalle (RF-21).** Un historial sin detalle es inutilizable, y ni mark ni Chris lo contemplaron.

### 3.3 Elementos de carlos que no se adoptaron

| Origen | Motivo |
|---|---|
| **RD-02, rangos duros (10–10 000 m²; habitaciones 0–20; baños 0.5–20)** | Contradice el enfoque de plausibilidad por zona de Chris y Anuar. Un rango global no puede ser correcto para zonas urbanas y rurales a la vez. Sustituido por la política versionada de P-01, que debe publicarse antes de la aceptación. |
| **Restricción de 12 semanas** | Se adoptó el plazo de cuatro meses de Anuar (C-08), que es el compatible con el alcance consolidado. Ver X-16. |
| **Redacción "el sistema debe" sin criterios de aceptación por endpoint** | Chris y Anuar tinham criterios más rigurosos; se adoptó su formato. |

---

## 4. Aporte de mark

**Documento:** `SRS_final_mark.md`, 338 líneas, 8 RF · 5 RNF · 4 RD
**Perfil:** Enfoque de roles y API REST con códigos HTTP. Único que introduce el rol Admin y la cuota de anónimos. **No menciona comparables ni confianza en ningún punto de su documento** (verificado: 0 ocurrencias).

### 4.1 Requisitos adoptados

| Origen | Requisito de mark | Destino en SRS_Equipo | Estado |
|---|---|---|---|
| RF-01 | Estimación de precio de inmueble | **RF-07** | Se fusionó; se descartó la imputación de defaults |
| RF-02 | Autenticación con rol Broker o Admin | **RF-16, RF-17** | Se adoptó parcialmente: se eliminó el rol Admin (ver X-03) |
| RF-03 | Guardado de historial | **RF-19** | Se adoptó |
| RF-04 | Generación de reporte PDF | **RF-23** | Se fusionó con Anuar y Chris; se eliminó el 403 por pertenenciaajena (lo cubre RNF-12) |
| RF-05 | Cuota de 3 estimaciones/día por IP | **RNF-15** | Se adoptó **junto con** el rate limit de Chris |
| RF-06 | Consulta de catálogo de ciudades y zonas | **RF-01** | Se fusionó |
| RNF-01 | Rendimiento p95 ≤ 1500 ms | **RNF-01** | Se **sustituyó** por p95 ≤ 3 s (ver X-07) |
| RNF-02 | JWT con HMAC-SHA256, vigencia 8 h | **RNF-11** | Se adoptó parcialmente: HMAC-SHA256 se conserva; la vigencia pasa a 2 h de inactividad (ver D-15) |
| RNF-03 | Escalabilidad: 200 concurrentes, < 1 % de errores | **RNF-02** | Se adoptó íntegro |
| RNF-04 | Usabilidad: responsiva desde 360 × 640 | **RNF-07, RNF-09** | Se fusionó con Chris y Anuar |
| RNF-05 | Disponibilidad ≥ 99,0 % | **RNF-03** | Se adoptó el valor; se redefinió la base de cálculo (ver X-08) |
| RD-01 | Disclaimer legal | **RD-02** | Se adoptó |
| RD-02 | Moneda MXN | **RD-03** | Se adoptó |
| RD-03 | Ubicaciones soportadas | **RD-01** | Se fusionó |

### 4.2 Elementos de mark que hicieron posible el trabajo de los demás

1. **Los códigos HTTP.** Chris los exigía por regla de verificabilidad; mark los aplicó a 9 situations distintas (200, 201, 400, 401, 403, 409, 422, 429, 503). Eso permitió escribir AC con códigos concretos en lugar de descripciones vagas.
2. **El umbral de escalabilidad (200 concurrentes, < 1 % de error).** Único dato de capacidad del equipo. Sin él, RNF-01 se valida contra una carga arbitraria.
3. **La cuota de anónimos.** Es la única defensa contra el abuso del recurso de inferencia. Chris tenía rate limit por usuario autenticado, que no protege el modo anónimo.
4. **El objetivo de disponibilidad.** Anuar sólo fijó 95 %; sin la exigencia de mark, la decisión de SLA se habría tomado por defecto en 95 %.

### 4.3 Elementos de mark que no se adoptaron

| Origen | Motivo |
|---|---|
| **Rol `Admin` (RF-07, RF-08)** | Chris lo niega explícitamente en su §3.2 y Anuar no lo contempla. Sustituido por RF-10 (verificación de versiones) y RNF-19 (operación automatizada). Ver X-03 y X-20. |
| **RD-04, imputación de valores predeterminados** desde estadística zonal | Contradice frontalmente a Anuar. Si se imputa, la regla de confianza de Anuar (causa "Falta información de ...") nunca se dispararía. Sustituido por propagación del vacío con degradación de confianza. Ver X-10. |
| **p95 ≤ 1500 ms** | Se sustituyó por 3 s con el entorno de red explícito de Anuar. 1500 ms no define condiciones de medición y no es reproducible. Ver X-07. |

---

## 5. Aporte de Anuar

**Documento:** `SRS_final_Anuar.md` v0.4, 328 líneas, 16 RF · 10 RNF · 7 RD
**Perfil:** Enfoque de revisión crítica con fixtures sintéticos. Único que declara pendientes de ratificación (P-01…P-05). **Excluye cuentas, historial, mapa, departamentos y uso comercial.** Rechaza expresamente imponer códigos HTTP.

### 5.1 Requisitos adoptados

| Origen | Requisito de Anuar | Destino en SRS_Equipo | Estado |
|---|---|---|---|
| RF-01 | Consulta anónima | **RF-18** | Se adoptó como flujo anónimo, no como flujo único |
| RF-02 | Captura de características (incluye CP → colonia) | **RF-03, RF-02-AC-3** | Se adoptó |
| RF-03 | Cobertura temprana | **RF-02** | Se adoptó íntegro |
| RF-04 | Ayuda y obligatoriedad | **RF-03-AC-2, RF-03-AC-3** | Se adoptó íntegro |
| RF-05 | Validación numérica y de catálogo | **RF-04** | Se adoptó; se añadió construcción > terreno (RF-04-AC-2) |
| RF-06 | Confirmación de valores atípicos | **RF-05** | Se fusionó con RF-16 de Chris |
| RF-07 | Campos obligatorios faltantes | **RF-06** | Se adoptó |
| RF-08 | Estimación y confianza | **RF-07, RF-12** | Se fusionó con RF-05 de Chris |
| RF-09 | Datos insuficientes | **RF-08, RF-09** | Se adoptó; se separó en abstención y en fallo de servicio |
| RF-10 | Presentación del resultado | **RF-11** | Se adoptó |
| RF-11 | Comparables | **RF-14** | Se fusionó con RF-06 de Chris |
| RF-12 | Explicación del resultado | **RF-13** | Se fusionó con RF-07 de Chris |
| RF-13 | Reporte PDF | **RF-23** | Se fusionó con mark y Chris |
| RF-14 | Protección de ubicación en reportes | **RF-24, RD-08** | Se adoptó íntegro; es la base de D-02 |
| RF-15 | Vigencia y aislamiento de consultas anónimas | **RF-18, RNF-14** | Se adoptó como ciclo de vida del flujo anónimo |
| RF-16 | Habilitación de políticas, modelo y datos | **RF-10, RD-05** | Se adoptó íntegro |
| RNF-01 | Rendimiento con entorno de red explícito | **RNF-01** | Se adoptó el **método**, se cambió el valor |
| RNF-02 | MdAPE ≤ 15 % por municipio, ≥ 100 cierres | **RNF-04** | Se adoptó la métrica y la granularidad; ver X-06 |
| RNF-03 | Disponibilidad con sonda externa | **RNF-03** | Se fusionó con el 99 % de mark |
| RNF-04 | Usabilidad: prueba de comprensión 16/20 | **RF-15** | Se adoptó como criterio de aceptación, no como RNF |
| RNF-05 | Compatibilidad (Chrome, Firefox, Android, iOS) | **RNF-09** | Se fusionó con carlos |
| RNF-06 | Seguridad: TLS ≥ 1.2, cookie Secure/HttpOnly/SameSite | **RNF-10** | Se elevó a TLS 1.3 (ver X-09) |
| RNF-07 | Privacidad: borrado a 60 min, no-store, logs sin IP | **RNF-14** | Se adoptó para el flujo anónimo |
| RNF-08 | Minimización de datos | **RNF-13** | Se adoptó; es la versión más completa del equipo |
| RNF-09 | Confiabilidad: < 3 comparables ⇒ confianza no alta | **RF-12-AC-3** | Se adoptó como AC, con regla de confianza |
| RNF-10 | Extensibilidad por catálogos | **RNF-18** | Se adoptó |
| RD-01 | Cobertura (casas usadas habitacionales GDL/ZAP) | **RD-01** | Se **sustituyó** por cobertura de catálogo (ver X-12) |
| RD-02 | Datos y reglas inmobiliarias | **RD-01** | Se adoptó parcialmente: los 10 obligatorios de Anuar se reducen a 9 opcionales |
| RD-03 | Unidades y precio por m² de construcción | **RD-04** | Se adoptó íntegro |
| RD-04 | Uso orientativo (texto literal) | **RD-02** | Se adoptó como redacción única |
| RD-05 | Datos autorizados, licencias, deduplicación | **RD-05** | Se adoptó íntegro |
| RD-06 | Identidad del propietario | **RD-08** | Se fusionó con RNF-13 de carlos |
| RD-07 | Restricción de proyecto y plataforma | **C-08** | Se adoptó el plazo de 4 meses |

### 5.2 Elementos de Anuar que hicieron posible el trabajo de los demás

Cinco elementos de Anuar no son requisitos adicionales sino **infraestructura de calidad** que los otros tres documentos no tenían:

1. **Los fixtures sintéticos (F-BASE, F-POL, F-RES, F-COMP, F-AMP).** Sin un conjunto de datos de prueba reproducible, ningún AC con valores numéricos es ejecutable. Anuar convirtió "el rango es 3 a 5 comparables" en "se prueban C1, C2, C3, C4, C5 con puntuaciones 0.99 a 0.70 y desempate por identificador ascendente". **Este es el aporte más valioso del equipo.**
2. **El contador de llamadas al modelo.** Es el único mecanismo que hace observable la afirmación "no se calculó". carlos y Chris la afirman; Anuar la hace verificable.
3. **La regla de independence de AC.** "Cada AC es independiente. Cuando enumera valores, se ejecuta una prueba separada por valor o combinación indicada, restableciendo el contexto." Sin esta regla, una prueba que pasa no significa nada.
4. **El gobierno de datos (RD-05).** Única defensa del equipo ante riesgo legal por uso de datos sin licencia. Se incorporó íntegro.
5. **El registro de pendientes con responsable y condición de cierre.** Chris tiene 12 puntos abiertos, Anuar 5, carlos y mark 0. El formato de Anuar ("ID / Definición pendiente / Responsable y condición de cierre / Requisitos afectados") es mejor que el de Chris ("ID / Cuestión / Impacto / Referencias") porque asigna la acción. **Se adoptó el formato de Anuar en §8 del SRS consolidado.**

### 5.3 Elementos de Anuar que no se adoptaron

| Origen | Motivo |
|---|---|
| **Exclusión de cuentas e historial** | Posición minoritaria (1 de 4). Anuar declaraba explícitamente que esta exclusión era una decisión de alcance de su piloto acotado. Se adoptó el modelo de dos modos de D-01, que preserva el flujo anónimo de Anuar como una de las dos rutas. |
| **RD-01, sólo casas usadas habitacionales en Guadalajara y Zapopan** | Restricción de piloto, no de producto, y el propio Anuar la declaraba "pendiente de ratificación" (P-05). Sustituida por cobertura de catálogo con extensibilidad (RD-01 y RNF-18). Ver X-12. **Si el negocio confirma el alcance acotado, esta decisión debe revertirse.** |
| **Rechazo a los códigos HTTP** | Se adoptó un compromiso: §1.4.3 mantiene la regla de verificabilidad de Chris, pero §3.0.3 declara la superficie de API como **informativa**, de modo que el mapeo a rutas y códigos puede cambiar sin invalidar los AC. Ver X-14. |
| **Límites numéricos de entrada** | No los tenía; se adoptó RD-01 con los formatos de carlos. |
| **Ventana de comparables de 12 meses como propuesta** | Se adoptó, pero se combinationó con la `ventanaMaximaMesesComparables` de Chris. |

---

## 6. Aporte de Chris

**Documento:** `SRS_final_Chris.md` v2.0, 1031 líneas, 17 RF · 14 RNF · 8 RD, 72 AC
**Perfil:** Enfoque de arquitectura REST con trazabilidad OpenAPI. La mayor cobertura del equipo. Impone códigos HTTP y de negocio, define la superficie completa de API y **exige que no exista rol administrador**.

### 6.1 Estructura del documento

Chris aportó el **esqueleto completo** que el SRS consolidado sigue:

| Sección de Chris | Destino en SRS_Equipo | Estado |
|---|---|---|
| §1.1 Propósito con tres audiencias | §1.1 | Se adoptó literalmente |
| §1.2 Alcance con tabla de fuera de alcance justificada | §1.2.1, §1.2.2 | Se adoptó; se amplió la tabla |
| §1.3 Definiciones y acrónimos | §1.3 | Se adoptó; se amplió con los términos de los otros tres |
| §1.4 Convenciones de identificadores y regla de verificabilidad | §1.4.1 a §1.4.5 | Se adoptó; se añadió §1.4.4 (independencia) y §1.4.5 (fixtures) de Anuar |
| §2.1 Perspectiva con diagrama de tres capas | §2.1 | Se adoptó |
| §2.2 Funciones principales con origen | §2.2 | Se adoptó |
| §2.3 Características de los usuarios | §2.3 | Se adoptó; se eliminó el rol admin y se renombró el tercer perfil |
| §2.4 Restricciones con tabla ID/tipo | §2.4 | Se adoptó; ampliada de 6 a 9 |
| §3.0 Convenciones, tipos de criterio y superficie de API | §3.0 | Se adoptó; la superficie se declara informativa |
| §3.0.3 Modelo de dos fases | §3.0.2 | Se adoptó la idempotencia; el borrador queda como decisión de diseño |
| §3.0.4 Códigos de error de negocio | §3.0.4 | Se adoptó la convención; se amplió de 13 a 22 |
| §3.1 RF con AC por endpoint | §3.1 | Se adoptó el formato |
| §3.2 RNF con métrica de verificación | §3.2 | Se adoptó el formato |
| §3.3 RD con consecuencia operativa y criterios que la aplican | §3.3 | Se adoptó el formato |
| §4 Índice de trazabilidad | §4 | Se adoptó; se recalculó a 74 AC |
| §5 Trazabilidad de requisitos | §5 | Se adoptó; se reescribió por documento de origen |
| §6 Correcciones de ambigüedad | §5.1 | Se adoptó el formato; se amplió de M-01…M-12 a M-01…M-12 con contenido nuevo |
| §7 Puntos abiertos | §8 | Se adoptó; se añadió §7 (restricciones de la unificación) yOwner se fusionaron las dos listas de pendientes |
| §8 Referencias | §9 | Se adoptó |

### 6.2 Requisitos adoptados

| Origen | Requisito de Chris | Destino en SRS_Equipo | Estado |
|---|---|---|---|
| RF-01 | Captura de características físicas base | **RF-03** | Se fusionó con Anuar |
| RF-02 | Captura de atributos detallados | **RF-03-AC-1, RD-01** | Se adoptó parcialmente: los atributos pasan a opcionales |
| RF-03 | Selección de ubicación en mapa | — | Se **excluyó** (ver X-02) |
| RF-04 | Cálculo y presentación en rango | **RF-07** | Se adoptó; se añadió la idempotencia como AC-2 |
| RF-05 | Margen de error | **RF-12** | Se fusionó con la confianza de Anuar |
| RF-06 | Comparables (3 a 4) | **RF-14** | Se fusionó; se adopta el rango 3 a 5 de Anuar (ver X-05) |
| RF-07 | Explicación en lenguaje natural | **RF-13** | Se fusionó con RF-12 de Anuar |
| RF-08 | Reporte PDF y registro de emisiones | **RF-23** | Se adoptó; el registro de emisiones con hash se excluyó (ver §6.4) |
| RF-09 | Compartir por WhatsApp y correo | **RF-25** | Se adoptó |
| RF-10 | Perfil y encabezado personalizado | — | Se **excluyó** (P-04 abierto) |
| RF-11 | Autenticación de brokers | **RF-16, RF-17** | Se adoptó |
| RF-12 | Historial de estimaciones | **RF-19, RF-20** | Se adoptó; se añadió el filtro de carlos y el detalle RF-21 |
| RF-13 | Comparación de inmuebles | — | Se **diferió** (P-06) |
| RF-14 | Consulta rápida sin registro | **RF-18** | Se fusionó con el ciclo de 60 min de Anuar |
| RF-15 | Advertencia visible | **RF-15** | Se adoptó; se añadió la prueba de los nodos de inspección |
| RF-16 | Validación y normalización ambigua | **RF-05** | Se fusionó con RF-06 de Anuar |
| RF-17 | Prellenado de zona y ciudad | — | Se **excluyó**: depende del historial, y sin historial no hay prellenado anónimo |
| RNF-01 | Tiempo de llenado ≤ 120 s | **RNF-06** | Se adoptó |
| RNF-02 | p95 ≤ 3 s | **RNF-01** | Se adoptó el valor; se adoptó el método de Anuar |
| RNF-03 | Responsiva, una mano, 48 × 48 px | **RNF-07** | Se adoptó |
| RNF-04 | WCAG 2.1 AA | **RNF-08** | Se adoptó y se amplió con teclado y etiquetas de carlos |
| RNF-05 | Validación defensiva en cliente | **RF-04, RF-05** | Se adoptó como comportamiento, no como RNF |
| RNF-06 | MAPE < 10 % | **RNF-04** | Se **sustituyó** por MdAPE ≤ 15 % (ver X-06) |
| RNF-07 | Redes móviles degradadas | **RNF-16** | Se adoptó |
| RNF-08 | Aislamiento por registro | **RNF-12** | Se adoptó y se amplió a sesión anónima |
| RNF-09 | TLS 1.3 y AES-256 | **RNF-10** | Se adoptó; prevalecen sobre el TLS 1.2 de Anuar (ver X-09) |
| RNF-10 | Reentrenamiento trimestral | **RNF-19** | Se adoptó |
| RNF-11 | Rate limiting 60/min y 10/min | **RNF-15** | Se adoptó **junto con** la cuota de mark |
| RNF-12 | Retención 12 meses | **RNF-14** | Se adoptó para el flujo autenticado |
| RNF-13 | Promoción condicionada a la métrica | **RNF-05** | Se adoptó; se cambió el umbral al de RNF-04 |
| RNF-14 | Detección de deriva | **RNF-05** | Se fusionó con RNF-13 |
| RD-01 | Cobertura: Zona Metropolitana | **RD-01** | Se sustituyó por cobertura de catálogo |
| RD-02 | Orientativo, sin transacciones | **RD-09** | Se adoptó |
| RD-03 | Sin validez legal | **RD-02** | Se fusionó con RD-04 de Anuar |
| RD-04 | Transacciones cerradas | **RD-11** | Se adoptó |
| RD-05 | Homogeneización de atributos | **RD-10** | Se adoptó |
| RD-06 | Estacionalidad e inflación | — | Se **excluyó** del SRS: es una decisión de diseño del modelo, no un comportamiento del sistema observable |
| RD-07 | Abstención por muestra insuficiente | **RD-06** | Se fusionó con RF-09 de Anuar |
| RD-08 | Responsabilidad en el usuario | **RD-09** | Se adoptó |

### 6.3 Elementos de Chris que hicieron posible el trabajo de los demás

1. **La estructura IEEE 830 completa.** Sin su esqueleto, la consolidación habría producido un documento amorfo. La secuencia 1 Introducción / 2 Descripción general / 3 Requisitos específicos / 4 Trazabilidad / 5 Orígenes / 6 Correcciones / 7 Puntos abiertos / 8 Referencias es la que permite que un SRS de equipo sea auditable.
2. **La regla de verificabilidad (§1.4).** Exigir que cada clause `Entonces` contenga un código HTTP, un código de negocio, un umbral, un nombre de campo o un elemento de interfaz es lo que distingue un criterio de prueba de una frase de intención. Sin esa regla, los AC de Anuar y carlos habría quedado en un nivel de detalle inconsistente.
3. **La superficie de API referenciada en cada AC.** Permite automatizar. Los criterios M-01 a M-12 de su §6 documentan doce ambigüedades reales y su corrección.
4. **La idempotencia por clave.** Es la defensa contra doble pulsación en móvil, y —en un sistema con cuota diaria— también contra el doble consumo de cuota. **Se convirtió en AC normativo (RF-07-AC-2) en lugar de quedar como nota de diseño.**

### 6.4 Elementos de Chris que no se adoptaron

| Origen | Motivo |
|---|---|
| **RF-03, mapa interactivo y geocodificación** | D-02. Contradice la prohibición expresa de carlos (§1.2, RNF-03) y de Anuar (RF-14, RNF-08). Anuar llega a formalizar la contradicción en su propio RF-14-AC-3: rechaza la solicitud que intente revelar la dirección. **No son combinables.** |
| **RF-10, perfil y encabezado personalizado** | P-04 abierto: sin verificación de identidad del broker, un tercero podría atribuir a una agencia un informe que esa agencia no emitió. Riesgo legal no mitigado por ningún otro requisito. |
| **RF-13, comparación de estimaciones** | Diferido a fase posterior. Depende de la decisión de identidad y del plazo de entrega. |
| **RF-17, prellenado de zona y ciudad** | Depende del historial persistente. Como la consulta anónima no tiene identidad, el prellenado no aplica al modo invitado, que es el modo de mayor volumen. Se difiere con RF-13. |
| **RF-08-AC-4, registro de emisiones con hash SHA** | Aporta auditabilidad, pero se والصفة con RNF-17 (trazabilidad de AC) y no es verificable por el usuario. Se difiere; es de bajo coste si el negocio lo requiere. |
| **RF-02-AC-3, `AMENIDAD_INCONSISTENTE`** | Atribuye una regla de negocio a un caso particular (piscina en inmueble habitacional) que no está respaldado por la elicitación. Se registró como pendiente P-01. |
| **RD-06, estacionalidad e inflación** | Es una decisión de diseño del modelo, no un comportamiento de sistema. El SRS debe especificar comportamiento observable, no método estadístico. |
| **Mapa de P-02, polígonos de la Zona Metropolitana** | Se sustituyó por el catálogo de RF-01, que no requiere polígonos. |

---

## 7. Resolución de los 20 conflictos

### 7.1 Conflicts bloqueantes

#### X-01 — Modelo de identidad: ¿hay cuentas o sólo consultas anónimas?

| | |
|---|---|
| **Posiciones** | carlos: cuentas + historial. mark: Broker + JWT. Chris: cuentas + historial + comparación. **Anuar: sin cuentas, historial ni sesión persistente; borrado a 60 min.** |
| **Conflicto** | No es una diferencia de redacción sino la divergencia arquitectónica de mayor alcance. Define si existe tabla de usuarios, autenticación, CRUD de historial y derecho de supresión. |
| **Decisión** | **D-01: dos modos.** Consulta anónima completa sin cuenta, y modo autenticado con historial. La posición de Anuar se preserva íntegra como la ruta anónima. |
| **Fundamento** | Mayoría de 3 de 4. Además, las cuatro propuestas coinciden en que la consulta anónima debe ser posible; la diferencia es sólo si es la **única** ruta. El modelo de dos modos no elimina ningún comportamiento propuesto: reproduce el flujo anónimo de Anuar y el flujo autenticado de los otros tres. |
| **Dónde quedó** | RF-18 (ciclo anónimo), RF-16 y RF-17 (cuentas), RF-19 a RF-22 (historial), RNF-14 (retención por flujo) |
| **Efecto colateral resuelto** | El conflicto X-13 (retención) desaparece al separar por flujo: 60 min para anónimos, 12 meses para autenticados. |

---

#### X-02 — Ubicación: catálogo de zona frente a dirección exacta con mapa

| | |
|---|---|
| **Posiciones** | **carlos: excluye mapas y captura de dirección exacta** (§1.2, §2.4, RNF-03). **Anuar: omite dirección y coordenadas en el PDF y rechaza la solicitud que intente revelarlas** (RF-14, RNF-08). **Chris: el mapa interactivo es requisito funcional** con geocodificación y coordenadas a seis decimales (RF-03). mark: silencioso. |
| **Conflicto** | Requisitos mutuamente excluyentes. Chris no puede coexistir con RF-14 ni RNF-08 de Anuar. |
| **Decisión** | **D-02: sólo catálogo de cobertura.** Ubicación por estado, municipio y colonia o código postal resuelto a colonia. Sin dirección, sin coordenadas, sin mapa. |
| **Fundamento** | Dos de tres posiciones expresas. El argumento decisivo no es la votación sino que **Anuar ya escribió el criterio de aceptación que hace imposible a Chris**: RF-14-AC-3 exige que el servidor rechace la solicitud que pida revelar la dirección. No hay una implementación que satisfaga ambos. A esto se añade que el mapa introduce una dependencia de servicio externo, un modelo de datos con coordenadas y una superficie de privacidad que ningún otro documento del equipo justifica. |
| **Dónde quedó** | §1.2.2 (fuera de alcance), RF-01, RF-02 (catálogo y elegibilidad), RF-24 (protección del reporte), RD-08, RNF-13 |
| **Reversibilidad** | Reversible si el negocio acepta el riesgo y se redefine RF-24. Requiere modificar 6 requisitos. |

---

#### X-03 — Modelo de roles: ¿existe Administrador?

| | |
|---|---|
| **Posiciones** | **mark: rol `Admin` con endpoints administrativos; sin Admin responde 403** (RF-07, RF-08). **Chris: "un único rol autenticado: broker. No existe un rol administrador"** (§3.2). carlos y Anuar: sin roles. |
| **Conflicto** | Chris cierra la discusión explícitamente en la dirección contraria a mark, y anticipa el problema: "si en el futuro se incorpora un rol administrador, este modelo debe revisarse". |
| **Decisión** | **D-04: sin rol administrador en el sistema.** La gestión del modelo y de los datos se realiza por proceso operativo versionado y verificado, no por interfaz. |
| **Fundamento** | Un panel administrativo no es la única forma de cambiar los parámetros del modelo ni de gestionar los datos: es **una** forma. Lo que el equipo necesita verificar —"¿puedo seguir usando este conjunto de datos?", "¿esta versión tiene evaluación aprobada?" — lo cubre RF-10 sin construir interfaz. La decisión evita además el problema de aislamiento que Chris anticipa: un administrador con acceso al historial de usuarios rompe el modelo de propiedad del registro de RNF-12. |
| **Dónde quedó** | §1.2.2, §2.3 (perfil "Responsable del modelo"), RF-10, RNF-19, RNF-12 |
| **Consecuencia asumida** | Los parámetros del modelo se cambian por procedimiento, no por pantalla. Esto es más lento y menos cómodo. Se acepta. |

---

#### X-19 — Política de límites de consultas

| | |
|---|---|
| **Posiciones** | **mark: 3 estimaciones/día por IP** para anónimos (RF-05). **Chris: 60 req/min en lectura y 10 req/min en cálculo** para autenticados (RNF-11). Anuar y carlos: sin límite. |
| **Conflicto** | Dos mecanismos distintos con números incompatibles: 3/día ≈ 0,002/min frente a 10/min ≈ 6.000/día. |
| **Decisión** | **Ambos, con responsabilidades separadas.** Cuota diaria de 3 estimaciones por dirección de origen para usuarios no autenticados (mark), y rate limit de 60 req/min en lectura y 10/min en cálculo (Chris). |
| **Fundamento** | **No son excluyentes: resuelven problemas distintos.** El rate limit protege la capacidad del servicio (Chris); la cuota diaria protege el recurso de inferencia del abuso anónimo (mark). Anuar y carlos no lo consideraron porque ninguno de los dos contemplaba estos problemas. La incompatibilidad numérica aparente desaparece al asignar cada mecanismo a su actor: un usuario anónimo no llega nunca a 10/min si su cuota diaria es 3. |
| **Dónde quedó** | RNF-15, y la idempotencia de RF-07-AC-2 garantiza que la cuota se consuma una sola vez por operación efectiva |

---

### 7.2 Conflicts altos

#### X-05 — Número de comparables a mostrar

| | |
|---|---|
| **Posiciones** | Chris: entre 3 y 4 (RF-06-AC-1). Anuar: de 3 a 5, con prueba de 3, 4 y 5 (RF-11). |
| **Decisión** | **3 a 5 comparables.** |
| **Fundamento** | El rango de Anuar contiene al de Chris (3–4 ⊂ 3–5), por lo que adopting 3–5 no invalida ningún criterio de Chris: un resultado de 4 comparables sigue siendo conforme. La diferencia es el máximo: 5 en lugar de 4. |
| **Dónde quedó** | RF-14-AC-1, RD-10 |

---

#### X-06 — Métrica y umbral de precisión del modelo

| | |
|---|---|
| **Posiciones** | Chris: **MAPE < 10 %**, media, agregada, con nota de que los atípicos pueden superarlo. Anuar: **MdAPE ≤ 15 %**, mediana, **por municipio**, con ≥ 100 cierres verificados no usados en entrenamiento, y sin muestra no se acredita. |
| **Decisión** | **MdAPE ≤ 15 % por unidad de cobertura (municipio o zona), con ≥ 100 cierres verificados.** Se conservan los gates operativos de Chris (promoción y deriva) con el mismo umbral. |
| **Fundamento** | Tres razones. **(a) Robustez:** la mediana no se degrada con valores atípicos, lo que es coherente con el hecho de que el propio Chris acepta que los atípicos superan su umbral. **(b) Trazabilidad:** el desglose por unidad de cobertura impide que un municipio con muestra abundante compense la debilidad de otro. **(c) Auditabilidad:** los 100 cierres verificados, no usados en entrenamiento y sin duplicados son la condición para que el número sea acreditable; sin ella, un MAPE de 10 % es una cifra sin respaldo. El umbral de 15 % es más permisivo que el de Chris, y eso se declara explícitamente en §7.2 del SRS consolidado como una decisión de negocio, no como una garantía técnica. |
| **Dónde quedó** | RNF-04, RNF-05, §7.2, P-08 |
| **Reversibilidad** | Si el negocio exige 10 %, se cambia RNF-04 y RNF-05 en la misma revisión. Es un cambio de un número, no de arquitectura. |

---

#### X-07 — Umbral de tiempo de respuesta

| | |
|---|---|
| **Posiciones** | mark: p95 ≤ **1500 ms**. carlos: p95 ≤ **3 s**. Chris: p95 ≤ **3 s**. Anuar: ≤ **5 s** en 950 de 1.000, con entorno de red explícito. |
| **Decisión** | **p95 ≤ 3 segundos**, con el entorno de medición de Anuar. |
| **Fundamento** | Se adopta el valor que dos integrantes fijan (3 s) y el método del que lo define con más rigor (Anuar: red 10/2 Mbps, RTT 100 ms, modelo real sin caché, errores y timeouts cuentan como incumplimiento, PDF se prueba aparte). 1500 ms se descarta por no reproducible; 5 s se descarta por más permisivo que la mayoría. |
| **Dónde quedó** | RNF-01, con referencia a P-07 (volumetría no definida) |

---

#### X-08 — Disponibilidad

| | |
|---|---|
| **Posiciones** | mark: **≥ 99,0 %** excluyendo mantenimiento. Anuar: **≥ 95 %** incluyendo mantenimiento. carlos y Chris: sin requisito. |
| **Decisión** | **≥ 99,0 % por mes calendario, excluyendo ventanas de mantenimiento que deben declararse con al menos 72 horas de anticipación y de duración máxima de 4 horas.** |
| **Fundamento** | Se conserva la cifra de mark, que es la única exigencia de SLA del equipo, pero se adopta la base de cálculo de Anuar por ser la única especificada con fórmula, sonda externa y criterio de minuto no operativo. **La exclusión del mantenimiento se vuelve legítima** al acotarla: ventana máxima de 4 horas y con 72 horas de declaración. Sin ese acotamiento, la exclusión sería una puerta abierta; con él, la diferencia entre 99 % y 95 % se vuelve cuantificable. |
| **Dónde quedó** | RNF-03, con P-07 como dependencia |

---

#### X-09 — Versión de TLS

| | |
|---|---|
| **Posiciones** | Chris: **TLS 1.3** + AES-256. Anuar: **TLS ≥ 1.2**. carlos: "HTTPS". mark: ausente. |
| **Decisión** | **TLS 1.3 o superior**, más cifrado en reposo AES-256. |
| **Fundamento** | 1.3 es el más restrictivo de los tres y no tiene equivalente en reposo. Adoptar el piso más alto elimina el conflicto. La mitad "en reposo" del RNF-09 de Chris es el único aporte del equipo sobre cifrado de almacenamiento y se conserva. |
| **Dónde quedó** | RNF-10 |

---

#### X-10 — Tratamiento de los opcionales ausentes

| | |
|---|---|
| **Posiciones** | **mark: imputa valores predeterminados desde estadística zonal** (RD-04, RF-01-AC-3). **Anuar: transmite los ausentes como ausentes, "no como 'no', cero o un año inventado"** (RF-02-AC-4, RF-07-AC-3). Chris: opcionales sin default. carlos: no aplica. |
| **Decisión** | **Propagación del vacío.** Los opcionales ausentes se transmiten como ausentes y degradan el nivel de confianza. |
| **Fundamento** | **La imputación y la confianza son mutuamente excluyentes.** Si el sistema imputa un valor para la remodelación, la regla de Anuar que produce la causa "Falta información de remodelación" con confianza media **nunca se dispararía**, y el usuario recibiría un rango en el que una característica de la que nuncaerciseROSS seoinformó aparece con el mismo peso que una informada. La imputación además fabricaría datos que el usuario no proporcionó, lo que contradice RD-08 y RNF-13. |
| **Dónde quedó** | RF-06-AC-3, RF-12-AC-2, RF-13-AC-3, RD-01 |

---

#### X-11 — Campos obligatorios del formulario

| | |
|---|---|
| **Posiciones** | carlos: 7 obligatorios. mark: 4. Anuar: 10. Chris: 4. |
| **Decisión** | **Nueve obligatorios:** estado, municipio, colonia o código postal resuelto a colonia, tipo de inmueble, uso de suelo, superficie de terreno, superficie construida, habitaciones y baños completos. **Opcionales:** estacionamientos, antigüedad, conservación, tipo de entrega, amenidades, medios baños, remodelación, cuarto de servicio y cercanía a parque. |
| **Fundamento** | El conjunto de carlos (7) es la mediana: es superconjunto del de mark y del de Chris, y subconjunto del de Anuar. Se le añade el **tipo de inmueble**, que tres de los cuatro documentos piden explícitamente (Chris lo llama "tipo de entrega", Anuar lo exige en su piloto, carlos y mark lo mencionan en su alcance) y que es indispensable para la cobertura de RF-02. Los tres obligatorios adicionales de Anuar (estacionamientos, antigüedad, conservación) pasan a opcionales porque ninguno de los otros tres los exige, y Anuar los exige por su decisión de alcance acotado. |
| **Dónde quedó** | RD-01, RF-03-AC-1, RF-06 |
| **Nota** | El documento original de carlos es el único que define un conjunto de obligatorios igual al adoptado sin la adición del tipo de inmueble. Su RD-02 se sustituyó por las razones de X-12, pero su lista de campos se conservó. |

---

#### X-12 — Alcance del tipo de inmueble y cobertura geográfica

| | |
|---|---|
| **Posiciones** | **Anuar: sólo casas usadas habitacionales en Guadalajara y Zapopan; excluye departamentos y comerciales** (RD-01). **Chris: Zona Metropolitana, con amenidades de ascensor y piscina y tipo de entrega** → cubre multifamiliar. carlos y mark: habitacional y comercial, sin tipo. |
| **Decisión** | **Cobertura por catálogo, ampliable, con los tipos de inmueble y usos de suelo habilitados en el catálogo.** El uso de suelo admite `habitacional` y `comercial`. |
| **Fundamento** | Tres de cuatro admiten uso comercial. Anuar es la posición minoritaria y, además, **el propio Anuar declara su restricción como pendiente de ratificación** (P-05): "La precisión 'casas' es una decisión propuesta de revisión, pendiente de ratificación". Es decir, no es una posición firme sino una hipótesis de piloto que su autor no presenta como definitiva. |
| **Dónde quedó** | RD-01, RF-01, RNF-18, §7.7 |
| **Reversibilidad** | Si el negocio confirma el alcance acotado de Anuar, RD-01 debe modificarse y **RNF-04 se vuelve más fácil de acreditar**, porque una sola tipología en dos municipios reduce la varianza intra-muestra. |

---

#### X-13 — Retención de datos

| | |
|---|---|
| **Posiciones** | Chris: historial 12 meses. Anuar: borrado a 60 minutos, sin cuentas. carlos y mark: sin política. |
| **Decisión** | **Retención por flujo:** 60 minutos para consultas anónimas (Anuar) y 12 meses para historial autenticado (Chris), con purga automática en ambos casos y con derecho de eliminación inmediata por el usuario (carlos RF-22). |
| **Fundamento** | El conflicto era aparente: ambas posiciones describen flujos distintos. La contradicción existía porque cada documento proponía su flujo como **el único**. Con D-01 resuelto en dos modos, la contradicción se disuelve. La incorporación del derecho de eliminación de carlos corrige un defecto de ambos: sin él, el historial de Chris era retention-only. |
| **Dónde quedó** | RNF-14, RF-18, RF-22 |

---

### 7.3 Conflicts medios

#### X-14 — Verificabilidad: ¿el SRS debe fijar códigos HTTP?

| | |
|---|---|
| **Posiciones** | Chris: exige código HTTP o de negocio en cada AC. mark: requiere códigos HTTP explícitos. carlos: sólo códigos de negocio. **Anuar: "sin imponer códigos HTTP o tecnologías internas"**. |
| **Decisión** | **Compromiso.** §1.4.3 mantiene la regla de verificabilidad de Chris (todo `Entonces` debe contener un elemento observable, incluido un código HTTP). §3.0.3 declara la superficie de API como **informativa**: "los requisitos son normativos sobre el comportamiento, y la asignación de rutas y códigos HTTP puede cambiar en el diseño sin invalidar los identificadores". |
| **Fundamento** | Ambas posiciones tienen razón en su contexto. Chris necesita la superficie para automatizar; Anuar la rechaza porque ata el SRS a una decisión de diseño. Declarar la tabla informativa satisface a ambos: los AC conservan su codes verificables y el diseño queda libre para reorganizar rutas sin reescribir 74 criterios. Los códigos de negocio son la capa estable, y se conservan los aliases de carlos en §1.5 para no invalidar su trazabilidad. |
| **Dónde quedó** | §1.4.3, §1.5, §3.0.3, §3.0.4, M-10 |

---

#### X-15 — Umbral de espera del motor de inferencia

| | |
|---|---|
| **Posiciones** | carlos: 5 s → `PREDICTION_UNAVAILABLE`. Anuar: 30 s de espera en navegador. Chris: `503` con umbral no definido (P-11). mark: no define. |
| **Decisión** | **Dos umbrales separados:** timeout de transporte de **5 segundos** (carlos, como piso del p95 de RNF-01) y timeout de interfaz de **30 segundos** (Anuar), con mensaje de reintento que conserva los datos en memoria. |
| **Fundamento** | Chris identificó correctamente el problema en su P-11: "sin el umbral no hay frontera entre 'lento' y 'caído'". La solución es que **no hay un solo umbral, hay dos**: el servidor decide que el motor no respondió a los 5 s y responde 503; el navegador espera hasta 30 s por si la respuesta llega. La implementación de Anuar ya operaba así, aunque no lo enunciaba. |
| **Dónde quedó** | RF-09-AC-1, RF-09-AC-2, RF-09-AC-3 |

---

#### X-16 — Plazo de entrega

| | |
|---|---|
| **Posiciones** | carlos: 12 semanas. Anuar: máximo 4 meses (~17,3 semanas), 4 integrantes. Chris y mark: sin plazo. |
| **Decisión** | **Máximo 4 meses desde el inicio formal, con equipo de 4 personas y sin aplicaciones nativas.** |
| **Fundamento** | El alcance consolidado es mayor que el de cualquiera de los dos documentos que fijaron plazo: incorpora PDF, comparables, explicación, confianza, cuentas, historial, cuota, rate limit, extensibilidad y gobierno de datos. Los 12 semanas de carlos correspondían a un alcance de 10 RF sin PDF, sin comparables y sin confianza. Aplicar el plazo más corto a un alcance mayor sería una inconsistencia. Los ~5 semanas de diferencia son aproximadamente el espacio donde caben los gaps que los otros tres_PROPUSIERON. |
| **Dónde quedó** | C-08, P-06, P-07 |

---

#### X-17 — Moneda y zona horaria

| | |
|---|---|
| **Posiciones** | carlos, mark, Anuar: **MXN**. **Chris: no definida** (P-06; verificado: 0 menciones de MXN). Zona horaria: sólo Anuar la fija. |
| **Decisión** | **MXN, sin conversión, y `America/Mexico_City` para fechas de negocio con UTC para plazos.** |
| **Fundamento** | Tres de cuatro fijan MXN; la omisión de Chris se declara como punto abierto no bloqueante. La zona horaria de Anuar se adopta completa, con la distinción que hace entre fechas de negocio y plazos de servidor, que es la que evita ambigüedad en RF-18 y RNF-14. |
| **Dónde quedó** | RD-03, §1.4.5 |

---

#### X-18 — Modelo de dos fases frente a flujo único

| | |
|---|---|
| **Posiciones** | Chris: dos fases, borrador persistido e `Idempotency-Key` obligatoria. carlos, mark, Anuar: flujo único. |
| **Decisión** | **Se adopta la idempotencia; la persistencia del borrador queda como decisión de diseño.** La superficie de API de §3.0.3 mantiene `POST /borradores` por trazabilidad con Chris, pero se documenta que puede cambiar. |
| **Fundamento** | La separación de los dos elementos que Chris puso en el mismo requerimiento: la **idempotencia** tiene valor propio e independiente de la arquitectura —con una cuota diaria, sin ella el usuario puede perder su consulta por una doble pulsación— y se convierte en AC normativo. La **persistencia del borrador** es una decisión de diseño que no deriva de ningún requisito de negocio. |
| **Dónde quedó** | §3.0.2, RF-07-AC-2, M-10, §6 |

---

#### X-20 — Quién y cómo gestiona el modelo y los datos

| | |
|---|---|
| **Posiciones** | mark: panel administrativo con UI. Chris: pipeline automatizado trimestral, sin UI. Anuar: sólo verificación de habilitaciones. carlos: nada. |
| **Decisión** | **Sin panel. Verificación por versionado (RF-10) y operación automatizada (RNF-19).** |
| **Fundamento** | Es la consecuencia operativa de D-04. Los tres mecanismos responden a preguntas distintas y sólo dos son necesarios: *"¿puedo seguir usando este conjunto de datos?"* (RF-10, Anuar) y *"¿el modelo se está degradando?"* (RNF-05 y RNF-19, Chris). La pregunta *"¿cómo cambio los parámetros desde una pantalla?"* es de comodidad, no de control. |
| **Dónde quedó** | RF-10, RNF-05, RNF-19, §2.3 |

---

## 8. Trazabilidad de las 16 decisiones de unificación

| ID | Decisión | Resolución adoptada | Fundamento | Estado |
|---|---|---|---|---|
| **D-01** | Modelo de identidad | Dos modos: anónimo y autenticado | Mayoría 3 de 4; preserva ambos flujos propuestos | ratified por mayoría |
| **D-02** | Granularidad de ubicación | Sólo catálogo de cobertura | 2 de 3 con posición expresa; contradicción interna de Anuar con Chris | Mayoría |
| **D-03** | Universo de propiedades | Catálogo ampliable, habitacional y comercial | Mayoría 3 de 4; la restricción de Anuar era declarada como no firme | Mayoría |
| **D-04** | Modelo de roles | Sin administrador | Requisito de la pregunta legal, no de la comodidad | Decisión técnica |
| **D-05** | Campos obligatorios | 9 obligatorios (conjunto de carlos + tipo de inmueble) | Mediana de cuatro conjuntos | Mayoría |
| **D-06** | Métrica de precisión | MdAPE ≤ 15 % por unidad de cobertura | Robustez y auditabilidad sobre la media | **Requiere ratificación de negocio** |
| **D-07** | Ventana de comparables | 3 a 5, 12 meses calendario inclusiva | El rango de Anuar contiene al de Chris | Mayoría |
| **D-08** | Umbral de rendimiento | p95 ≤ 3 s con entorno de red explícito | Valor mayoritario, método más riguroso | **Requiere confirmación de hardware** |
| **D-09** | Disponibilidad | 99,0 % excluyendo mantenimiento declarado y acotado | Cifra de mark, base de cálculo de Anuar | **Requiere validación de operaciones** |
| **D-10** | Imputación de opcionales | Propagación del vacío con degradación de confianza | Imputación y confianza son excluyentes | Decisión técnica |
| **D-11** | Retención de datos | 60 min anónimo / 12 meses autenticado | Separa flujos; añade derecho de eliminación de carlos | **Requiere revisión legal** |
| **D-12** | Límites de consultas | Cuota diaria anónimo + rate limit por minuto | Mecanismos para actores distintos, no excluyentes | Decisión técnica |
| **D-13** | Nomenclatura del SRS | Neutral en comportamiento, superficie de API informativa | Compromiso entre Chris y Anuar | Decisión técnica |
| **D-14** | Plazo de entrega | Máximo 4 meses, equipo de 4 | El alcance consolidado excede el de carlos | **Requiere confirmación de PM** |
| **D-15** | Mecanismo de autenticación | JWT HMAC-SHA256, 2 h de inactividad, cookie Secure/HttpOnly/SameSite | Cada elemento del aporte de un integrante distinto | Decisión técnica |
| **D-16** | Moneda y zona horaria | MXN + America/Mexico_City | Mayoría 3 de 4 | Mayoría |

**Cuatro decisiones requieren ratificación expresa antes de la aceptación:** D-06 (umbral de precisión), D-09 (SLA de disponibilidad), D-11 (retención) y D-14 (plazo). Las restantes son mayorías técnicas o decisiones de diseño defendibles.

---

## 9. Balance de gaps: incorporado, sustituido y excluido

### 9.1 Gaps incorporados (36 de 62)

| Integrante | Gaps que pasaron al SRS consolidado |
|---|---|
| **carlos** | Registro de cuenta con hash (RF-16), inicio de sesión (RF-17), guardar/filtrar/detallar/eliminar historial (RF-19 a RF-22), WCAG 2.1 AA con teclado y etiquetas (RNF-08), Edge en la matriz (RNF-09), cobertura de pruebas ≥ 80 % (RNF-17), aislamiento por identidad (RNF-12), no revelar existencia de correo (RF-17-AC-2), aislamiento entre sesiones (RF-18-AC-3), detalles de conexión entre componentes (RF-18) |
| **mark** | Cuota diaria de anónimos (RNF-15), escalabilidad 200 concurrentes (RNF-02), objetivo de disponibilidad (RNF-03), códigos HTTP en los AC (§3.0.3), HMAC-SHA256 y expiración de sesión (RNF-11) |
| **Anuar** | Ciclo de vida anónimo de 60 min (RF-18), ayuda contextual (RF-03-AC-2, AC-3), CP → colonia (RF-02-AC-3), cobertura temprana (RF-02), confirmación de atípicos (RF-05), abstención por muestra (RF-08), confianza categórica (RF-12), explicación con causas (RF-13), datos autorizados y licencias (RD-05), habilitación de versiones (RF-10), construcción > terreno válida (RF-04-AC-2), extensibilidad (RNF-18), precio por m² de construcción (RD-04), MPC por zona (RNF-04), sonda de disponibilidad (RNF-03), minimización ampliada (RNF-13), vigencia de datos (RF-10-AC-2) |
| **Chris** | Idempotencia (RF-07-AC-2), margen de error (RF-12-AC-1), explicación con vocabulario cerrado (RF-13-AC-1), comparables (RF-14), compartir PDF (RF-25), normalización de ambigüedad numérica (RF-05-AC-2), AES-256 en reposo (RNF-10), rate limiting (RNF-15), retención y purga (RNF-14), tiempo de llenado (RNF-06), objetivos táctiles (RNF-07), estabilidad en redes degradadas (RNF-16), Extensibilidad de red (RNF-18), derivas y gates (RNF-05), advertencia visible (RF-15), aislamiento por registro (RNF-12), TLS 1.3 (RNF-10) |

### 9.2 Gaps sustituidos (10)

| Gap de origen | Sustituido por | Motivo |
|---|---|---|
| carlos: rangos duros 10–10 000 m² | Política de plausibilidad por zona (P-01) | Un rango global no puede ser válido para zonas urbanas y rurales |
| mark: p95 ≤ 1500 ms | RNF-01: p95 ≤ 3 s con entorno explícito | 1500 ms no es reproducible |
| mark: imputed defaults | Propagación del vacío con degradación de confianza | La imputación hace imposible la regla de confianza |
| mark: rol Admin | RF-10 + RNF-19 | La interfaz no es necesaria para verificar habilitaciones |
| mark: vigencia de sesión de 8 h | 2 h de inactividad renovable | 8 h excede la ventana de riesgo de una sesión de brokerage |
| Anuar: sólo casas usadas habitacionales GDL/ZAP | Cobertura de catálogo ampliable | La restricción era declarada como no firme por su autor |
| Anuar: sin cuentas | D-01: dos modos | Posición minoritaria que se preserva como ruta anónima |
| Anuar: rechazo de códigos HTTP | §3.0.3 informativa | Compromiso con la trazabilidad de Chris |
| Chris: mapa interactivo | RF-01 + RF-02 catálogo | Contradicción directa con RD-08 |
| Chris: MAPE < 10 % agregado | RNF-04: MdAPE ≤ 15 % por unidad | Media sin desglose no es acreditable |

### 9.3 Gaps excluidos o diferidos (16)

| Gap de origen | Estado | Motivo |
|---|---|---|
| Chris: RF-03 mapa, geocodificación, coordenadas | Excluido | D-02; contradicción directa con dos documentos |
| Chris: RF-10 perfil y encabezado de agencia | Excluido | P-04 abierto; riesgo de atribución a terceros |
| Chris: RF-13 comparación de estimaciones | Diferido (P-06) | Depende de D-01 y del plazo |
| Chris: RF-17 prellenado de zona | Diferido | Depende del historial; no aplica al modo anónimo |
| Chris: RF-08-AC-4 registro de emisiones con hash | Diferido | De bajo coste si el negocio lo requiere |
| Chris: RF-02-AC-3 amenidad inconsistente | Diferido (P-01) | Regla sin respaldo en la elicitación |
| Chris: RD-06 estacionalidad e inflación | Excluido del SRS | Es diseño del modelo, no comportamiento observable |
| Chris: P-02 polígonos de la Zona Metropolitana | Excluido | El catálogo de RF-01 no requiere polígonos |
| Chris: modelo de borrador persistido | Diferido a diseño | La idempotencia sí se adoptó |
| Anuar: exclusividad de ayuda por campo | Fusionado | RF-03-AC-2 y AC-3 cubren la substance |
| Anuar: 12 semanas como plazo de entrega | Excluido | X-16 |
| carlos: RF-03 por sí solo como requisito | Fusionado | Se partió en RF-03 (captura) y RF-04 (validación) |
| carlos: endpoint de detalle separado | Fusionado | RF-21 |
| mark: RF-04 PDF con 403 por pertenencia | Fusionado | RNF-12 cubre el aislamiento; RF-23 cubre el contenido |
| mark: "Broker" como nombre de rol vs "Usuario registrado" | Fusionado | carlos y Chris usan "usuario registrado"; el SRS usa `broker` como único rol autenticado |
| mark: módulo de reportes PDF como componente | Fusionado | RF-23 y RF-24 cubren el contenido y la protección |

---

## 10. Elementos técnicos heredados de cada documento

| Elemento | Procedencia | Dónde vive en SRS_Equipo |
|---|---|---|
| Estructura IEEE 830 en 8 secciones | Chris | Estructura completa del documento |
| Regla de verificabilidad de criterios | Chris | §1.4.3 |
| Superficie de API referenciada por AC | Chris | §3.0.3, declarada informativa |
| Convenciones de identificador `RF-XX-AC-n` | Los cuatro (idéntica) | §1.4.1 |
| Índice de trazabilidad con tipo y verificación | Chris | §4 |
| Tabla de restricciones con ID y tipo | Chris | §2.4 |
| RD con consecuencia operativa y criterios que la aplican | Chris | §3.3 |
| Fixtures sintéticos F-BASE, F-POL, F-RES, F-COMP, F-AMP | Anuar | §1.4.5 |
| Contador de llamadas al motor de inferencia | Anuar | §1.4.4, RF-02-AC-1, RF-06-AC-1, RF-07-AC-3 |
| Regla de independencia de criterios | Anuar | §1.4.4 |
| Tabla de ambigüedades con corrección aplicada | Anuar y Chris | §5.1 (M-01 a M-12) |
| Registro de pendientes con responsable y condición de cierre | Anuar (formato) + Chris (contenido) | §8 |
| Códigos de error de negocio con tabla de significado | Chris y carlos | §3.0.4 (22 códigos) |
| Códigos HTTP como elemento observable | mark y Chris | §1.4.3, §3.0.3 |
| Tabla de correspondencia de códigos entre documentos | carlos | §1.5 |
| Política de complejidad de contraseña | carlos | RF-16-AC-1 |
| Algoritmo de hash de contraseñas | carlos | RNF-11 |
| Filtros de historial y paginación | carlos | RF-20 |
| Cobertura de pruebas y módulos núcleo | carlos | RNF-17 |
| Cuota diaria de anónimos | mark | RNF-15 |
| Prueba de escalabilidad con criterio de error | mark | RNF-02 |
| Objetivo de disponibilidad | mark | RNF-03 |
| HMAC-SHA256 y expiración de sesión | mark y Chris | RNF-11, RF-17-AC-3 |
| Idempotencia por clave | Chris | RF-07-AC-2, §3.0.2 |
| Margen de error porcentual | Chris | RF-12-AC-1 |
| Vocabulario cerrado y prueba anti-técnico | Chris | RF-13 |
| Compartir PDF por puente del SO | Chris | RF-25 |
| Rate limiting con `Retry-After` | Chris | RNF-15 |
| Cifrado en reposo AES-256 | Chris | RNF-10 |
| Detección de deriva y gate de promoción | Chris | RNF-05 |
| Objetivos táctiles 48 × 48 px | Chris | RNF-07 |
| Tiempo de llenado 120 s | Chris | RNF-06 |
| Homogeneización de comparables | Chris | RD-10 |
| Datos autorizados y licencias | Anuar | RD-05 |
| Clave normalizada de deduplicación | Anuar | RD-05, RF-14-AC-4 |
| Vigencia de datasets y revocación | Anuar | RF-10-AC-2, RF-10-AC-3 |
| `Cache-Control: no-store` y logs sin IP | Anuar | RNF-14 |
| Minimización ampliada (escrituras, datos bancarios) | Anuar | RNF-13 |
| TLS y cookies Secure/HttpOnly/SameSite | Anuar | RNF-10 |
| Precio por m² de construcción | Anuar | RD-04, RF-11-AC-1 |
| Comparables con desempate determinista | Anuar | RF-14-AC-2 |
| Ventana de 12 meses con exclusión de fechas futuras | Anuar | RF-14-AC-3, RD-10 |

---

## 11. Limitaciones de esta consolidación

Esta sección declara lo que la consolidación **no** resolvió, para que no se interprete como acuerdo alcanzado.

1. **Cuatro decisiones requieren ratificación de negocio:** D-06 (umbral de 15 % de precisión), D-09 (SLA de 99 %), D-11 (retención) y D-14 (plazo de 4 meses). Ninguna puede cerrarse por Argumento técnico.
2. **Dos puntos abiertos son bloqueantes para el diseño:** P-01 (límites de plausibilidad por campo y zona) y P-02 (fuente de datos de transacciones cerradas). Sin P-02, RNF-04 no es acreditable y RF-10 mantiene todas las zonas deshabilitadas.
3. **D-03 es una decisión mayoritaria, no una decisión ratificada.** Si el negocio confirma el alcance acotado de Anuar (casas usadas habitacionales en Guadalajara y Zapopan), RD-01 debe modificarse y RNF-04 se vuelve más fácil de acreditar. Esta alternativa **no se descartó**, se documentó en §7.7 del SRS consolidado.
4. **D-02 es reversible pero costosa.** Reincorporar el mapa interactivo exige modificar 6 requisitos, entre ellos RD-08, RF-24 y RNF-13, que hoy prohíben activamente la dirección exacta y las coordenadas.
5. **El equipo no Pazó de un SRS único a un SRS único con la misma confianza.** El SRS consolidado tiene 74 criterios de aceptación; el de Chris tenía 72 sobre un alcance menor. La cobertura nominal es mayor, pero incluye 11 requisitos que Chris declaraba fuera de alcance y que ahora están dentro.
6. **Asimetría de aporte no resuelta.** Chris y Anuar aportan 62 de los 55 requisitos con coautoría; carlos y mark aportan 26. La consolidación resolvió los conflictos, pero no la desigualdad de profundidad de análisis entre integrantes.

---

*Fin de Diferencias_SRS.md. Documento de trazabilidad de la consolidación de `SRS_Equipo.md` v1.0. Las decisiones marcadas como "requiere ratificación" en la sección 8 no están aprobadas.*
