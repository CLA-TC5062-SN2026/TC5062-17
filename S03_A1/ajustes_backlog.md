# Ajustes al backlog de MLState

## 1. Propósito de la revisión

Este documento registra la revisión crítica de las 15 historias de `Backlog_MLState.md` contra `SRS_Equipo.md`. La revisión consideró:

- Redacción en formato estándar, actor y valor de negocio.
- Foco y atomicidad de cada historia.
- Fidelidad y trazabilidad respecto de RF, RNF y RD.
- Verificabilidad y precisión de los criterios de aceptación.
- Prioridad y estimación relativa con escala Fibonacci.

Se mantienen las 5 épicas y las 15 historias porque ofrecen una agrupación manejable del alcance. Los criterios se refinaron para recuperar condiciones verificables que se habían simplificado en exceso.

## 2. Resumen de ajustes

| Historia | Resultado | Prioridad anterior | Prioridad final | Puntos anteriores | Puntos finales |
|---|---|---|---|---:|---:|
| HU-01 | Redacción y criterios ampliados | Alta | Alta | 5 | 5 |
| HU-02 | Criterios ampliados y reestimación | Alta | Alta | 5 | 8 |
| HU-03 | Criterios precisados | Alta | Alta | 8 | 8 |
| HU-04 | Redacción y criterios precisados | Alta | Alta | 8 | 8 |
| HU-05 | Título, redacción y fronteras precisadas | Alta | Alta | 5 | 5 |
| HU-06 | Criterios operativos ampliados | Alta | Alta | 8 | 8 |
| HU-07 | Título y criterios cuantitativos precisados | Alta | Alta | 5 | 5 |
| HU-08 | Título, valor y criterios ampliados | Alta | Alta | 8 | 8 |
| HU-09 | Título, alcance y criterios ampliados | Alta | Alta | 5 | 5 |
| HU-10 | Actor, criterios y estimación ajustados | Alta | Alta | 5 | 8 |
| HU-11 | Redacción, criterios y estimación ajustados | Media | Media | 5 | 8 |
| HU-12 | Criterios y códigos precisados | Media | Media | 3 | 3 |
| HU-13 | Criterios ampliados y prioridad elevada | Media | Alta | 5 | 5 |
| HU-14 | Redacción corregida por privacidad | Alta | Alta | 5 | 5 |
| HU-15 | Degradación y verificación precisadas | Baja | Baja | 3 | 3 |
| **Total** |  |  |  | **83** | **92** |

## 3. Revisión historia por historia

### HU-01 — Consultar cobertura y elegibilidad

**Evaluación:** La historia tenía actor, acción y beneficio claros. La consulta del catálogo y la verificación de elegibilidad pertenecen al mismo objetivo del usuario y pueden permanecer juntas.

**Ajustes realizados:**

- Se agregó el caso de combinación no habilitada o inconsistente con `422` y `ZONA_FUERA_DE_COBERTURA`.
- Se mantuvo el caso de código postal ambiguo, precisando `409` y `COLONIA_AMBIGUA`.
- Se hizo explícito que no se invoca el motor de inferencia durante estas validaciones.
- Se incorporaron RD-01 y RNF-18 a la trazabilidad.

**Estimación:** Se conservan 5 puntos. La historia integra catálogo y validación, pero sus reglas están bien delimitadas.

### HU-02 — Capturar las características del inmueble

**Evaluación:** La historia era correcta, pero “todos los campos” no resultaba autosuficiente y la cobertura de accesibilidad se limitaba a un ancho de pantalla.

**Ajustes realizados:**

- Se referencia expresamente el conjunto de campos de RD-01 y se aclara que los opcionales ausentes no reciben valores inventados.
- Se exige identificación textual como `Obligatorio` u `Opcional`.
- Se amplía la ayuda para incluir definición, ejemplo, formato o unidad y fuente documental.
- Se incorporan navegación por teclado, etiquetas asociadas, contraste AA, objetivos táctiles y la matriz de anchos de RNF-09.

**Estimación:** Aumenta de 5 a 8 puntos por el esfuerzo combinado de formulario dinámico, accesibilidad y compatibilidad multidispositivo.

### HU-03 — Validar y corregir los datos capturados

**Evaluación:** El valor para el usuario estaba bien expresado, aunque la historia agrupa tres familias de validación y se encuentra en el límite superior de atomicidad.

**Ajustes realizados:**

- Se agregan los códigos `CAMPO_FUERA_DE_RANGO`, `VALOR_AMBIGUO`, `CONFIRMACION_INVALIDADA` y `CAMPOS_OBLIGATORIOS_FALTANTES`.
- Se aclara que una combinación municipio-colonia inconsistente debe rechazarse.
- Se conserva como válido el caso de construcción mayor que terreno cuando ambas superficies cumplen sus reglas.
- Se precisa que todos los faltantes se reportan en una respuesta y que los opcionales no bloquean ni reciben valores predeterminados.
- Se incorpora la conservación de datos ante interrupciones de red mediante RNF-16.

**Estimación:** Se conservan 8 puntos por la cantidad de reglas, estados de confirmación y validación tanto de interfaz como de servidor.

### HU-04 — Calcular una estimación idempotente

**Evaluación:** La historia reunía correctamente cálculo, validación de salida e idempotencia como garantías de una misma operación. Se ajustó el beneficio para expresar el valor orientativo y la prevención de duplicados.

**Ajustes realizados:**

- Se precisan `201 Created`, `estimacionId` e `Idempotency-Key`.
- Se aclara que un reenvío no crea otro resultado ni consume de nuevo la cuota.
- Se incorpora la validación del margen y el código `RESULTADO_NO_PUBLICABLE`.
- Se agrega determinismo de importes para entradas idénticas sin reentrenamiento.
- Se evita afirmar que el cálculo guarda automáticamente en el historial, pues RF-19 define el guardado como una acción explícita.

**Estimación:** Se conservan 8 puntos debido a la integración con inferencia, consistencia transaccional e idempotencia.

### HU-05 — Abstenerse y recuperarse de fallos de estimación

**Evaluación:** El título anterior era genérico. La falta de muestra y el fallo técnico son causas diferentes, pero comparten el objetivo de no presentar resultados falsos y facilitar la recuperación.

**Ajustes realizados:**

- Se renombra la historia para describir abstención y recuperación.
- Se incorporan las fronteras 29, 30 y 31 referencias de F-POL.
- Se distinguen `409 MUESTRA_INSUFICIENTE_PARA_ESTIMAR` y `503 ERROR_EN_SERVICIO_DE_INFERENCIA`.
- Se precisan el timeout de transporte de 5 segundos y el límite de espera de interfaz de 30 segundos.
- Se impide mostrar valores anteriores o habilitar el PDF ante un fallo.

**Estimación:** Se conservan 5 puntos. Las reglas están especificadas y el comportamiento se concentra en manejo de fallos.

### HU-06 — Habilitar sólo modelos y datos autorizados

**Evaluación:** Es una historia habilitadora válida para el responsable del modelo. Su alcance es grande, pero coherente con el proceso operativo de habilitación definido por el SRS.

**Ajustes realizados:**

- Se incluyen la vigencia basada en actualización validada y la exclusión de duplicados o filas inválidas.
- Se precisa que cambiar una etiqueta no renueva la vigencia de una fuente.
- Se agrega el umbral MdAPE menor o igual a 15 % por unidad de cobertura y la evidencia mínima establecida por RNF-04.
- Se incorporan la automatización trimestral y revisión mensual a la Definición de Terminado global.

**Estimación:** Se conservan 8 puntos. Es candidata a división durante la planificación técnica, pero no es necesario alterar las 15 historias del backlog de producto.

### HU-07 — Comprender el rango y la confianza

**Evaluación:** La historia tenía buen foco, pero omitía varias reglas cuantitativas necesarias para comprobar la presentación correcta.

**Ajustes realizados:**

- Se cambia el título para abarcar toda la interpretación del resultado.
- Se especifica `MXN/m² de construcción`, redondeo a dos decimales y empate hacia arriba.
- Se exige formato `AAAA-MM-DD` y etiquetas distintas para las dos fechas.
- Se agregan los límites del margen y el dominio cerrado de confianza.
- Se conserva la degradación de confianza por datos opcionales ausentes o pocos comparables.

**Estimación:** Se conservan 5 puntos porque las reglas están definidas y se aplican sobre un resultado ya calculado.

### HU-08 — Comprender la evidencia y las limitaciones

**Evaluación:** Era la historia de mayor amplitud funcional al combinar explicación, comparables y advertencia. Se mantiene porque las tres capacidades permiten interpretar y contextualizar el resultado.

**Ajustes realizados:**

- Se ajustan título y beneficio para destacar evidencia y limitaciones.
- Se agregan longitud, vocabulario permitido y vocabulario técnico prohibido para la explicación.
- Se precisan cantidad, orden, deduplicación, ventana de 12 meses, permisos y contenido de los comparables.
- Se exige el texto íntegro de RD-02 en toda vista con precio y en el PDF.

**Estimación:** Se conservan 8 puntos. Debe considerarse de alto riesgo y puede dividirse en tareas técnicas durante la planificación.

### HU-09 — Completar y administrar una consulta anónima

**Evaluación:** El título anterior no reflejaba recuperación, aislamiento, expiración y finalización. El formato y el valor para el visitante eran adecuados.

**Ajustes realizados:**

- Se amplía el título y se incluye la acción `Finalizar consulta`.
- Se aclara que captura, cálculo y descarga no exigen cuenta.
- Se precisa que la vigencia es de 60 minutos desde la finalización y que una descarga no reinicia el plazo.
- Se agregan `CONSULTA_EXPIRADA`, aislamiento entre sesiones y `Cache-Control: no-store`.

**Estimación:** Se conservan 5 puntos por tratarse de un ciclo temporal claramente definido.

### HU-10 — Registrar y autenticar una cuenta de broker

**Evaluación:** La historia era demasiado amplia para 5 puntos y llamaba broker a quien aún no había creado la cuenta.

**Ajustes realizados:**

- El actor cambia a “visitante que desea utilizar funciones persistentes de broker”.
- Se incorpora la política exacta de contraseña, hash con Argon2id o bcrypt y rol creado.
- Se agregan correo duplicado, credenciales inválidas, login exitoso, expiración por inactividad y cierre explícito.
- Las condiciones de TLS y cookie segura se incluyen en la Definición de Terminado global para no mezclar detalles de infraestructura con el flujo del usuario.

**Estimación:** Aumenta de 5 a 8 puntos por incluir registro, autenticación, expiración y cierre seguro de sesión.

### HU-11 — Guardar y consultar el historial

**Evaluación:** Combina guardado, listado y filtrado, pero conserva un objetivo único: recuperar trabajo previo. La estimación original no cubría persistencia, autorización, paginación y retención.

**Ajustes realizados:**

- Se normaliza “ciudad” a `municipio`, término usado por el modelo de cobertura.
- Se agrega rechazo `401` sin sesión.
- Se precisa orden descendente por fecha y desempate por `estimacionId`, con páginas de 20.
- Se incorpora eliminación automática a los 12 meses.

**Estimación:** Aumenta de 5 a 8 puntos por persistencia, aislamiento, filtros, paginación y política de retención.

### HU-12 — Consultar y eliminar una estimación guardada

**Evaluación:** Es una agrupación aceptable de operaciones pequeñas sobre el mismo registro. Faltaban códigos y el comportamiento al cancelar.

**Ajustes realizados:**

- Se precisan `200 OK`, `204 No Content` y `404 ESTIMACION_NO_ENCONTRADA`.
- Se agrega la conservación del registro cuando el usuario cancela.
- Se mantiene el rechazo de eliminación ajena sin exponer ni modificar datos.
- No se fija un código para eliminación ajena en la versión final porque RF-21 y RF-22 utilizan estrategias distintas; se documenta como ambigüedad pendiente.

**Estimación:** Se conservan 3 puntos.

### HU-13 — Generar y descargar un reporte PDF

**Evaluación:** Era una historia bien delimitada. Su prioridad Media no era consistente con RF-18, que incluye el PDF en la consulta anónima completa.

**Ajustes realizados:**

- La prioridad cambia de Media a Alta.
- Se exige el contenido completo, el texto íntegro de RD-02 y `200 OK`.
- Se agrega compatibilidad con la matriz de RNF-09.
- Se precisa que la regeneración conserva contenido y fecha de emisión sin reinvocar el modelo.
- Se distingue el fallo de reporte del fallo de inferencia.

**Estimación:** Se conservan 5 puntos.

### HU-14 — Proteger la privacidad del reporte

**Evaluación:** El primer criterio suponía que un resultado normal contenía dirección exacta y coordenadas, lo que contradice RD-08 y RNF-13.

**Ajustes realizados:**

- Se cambia el objetivo de “omitir” a “impedir incorporar” datos prohibidos.
- Se exige que los contratos no soliciten ni acepten esos campos.
- La omisión desde una fuente auxiliar o fixture se conserva como defensa en profundidad, no como flujo normal.
- Se precisa la zona permitida y el rechazo `422 NO_SE_PERMITE_REVELAR_DIRECCION`.

**Estimación:** Se conservan 5 puntos.

### HU-15 — Compartir el reporte desde el dispositivo

**Evaluación:** La historia era pequeña, clara y correctamente priorizada. Se ajustó la redacción para no depender de detectar si una aplicación específica está instalada, comportamiento que no es uniforme en una SPA.

**Ajustes realizados:**

- La degradación se basa en disponibilidad o fallo controlado del puente de compartición.
- Se mantiene descarga directa como alternativa.
- Se conserva la prohibición de transmitir el binario a servidores de terceros.
- Se agrega verificación manual en dispositivos reales.

**Estimación:** Se conservan 3 puntos y prioridad Baja.

## 4. Ajustes transversales

La versión final agrega una Definición de Terminado global para condiciones que afectan múltiples historias y no aportan valor como historias independientes:

| Área | Condición incorporada |
|---|---|
| Rendimiento y escalabilidad | p95 menor o igual a 3 segundos y 200 inferencias concurrentes con menos de 1 % de errores, conforme a RNF-01 y RNF-02. |
| Disponibilidad | Disponibilidad mensual y mantenimiento conforme a RNF-03, sujetos a ratificación de D-09 y P-07. |
| Usabilidad | Captura p90 menor o igual a 120 segundos con al menos cinco usuarios de campo. |
| Seguridad | TLS 1.3 o superior, cookies `Secure`, `HttpOnly` y `SameSite`, cifrado en reposo y ausencia de datos sensibles en logs. |
| Cuotas | Límites de lectura, cálculo y consultas anónimas definidos por RNF-15, respetando idempotencia. |
| Calidad | Automatización de todos los criterios aplicables y cobertura mínima de 80 % en módulos críticos. |
| Extensibilidad | Incorporación de cobertura por configuración sin modificar el flujo compartido. |
| Operación ML | Reentrenamiento trimestral y revisión mensual de datos. |

## 5. Ambigüedades del SRS consideradas

Estos puntos no se resolvieron unilateralmente; la versión final adopta la interpretación más consistente y deja constancia de la decisión:

1. **Borrador en servidor o en cliente:** el SRS define endpoints de borrador, pero su persistencia se declara decisión de diseño. El backlog exige conservar datos y separar captura de cálculo, sin imponer persistencia permanente.
2. **Cálculo frente a guardado:** RF-07-AC-2 menciona una entrada de historial, mientras RF-19 exige la acción explícita `Guardar estimación`. El backlog final adopta guardado explícito y entiende la idempotencia como ausencia de resultados duplicados.
3. **Acceso a registros ajenos:** RF-21 usa `404 ESTIMACION_NO_ENCONTRADA` y RF-22 usa `403 ACCESO_DENEGADO`. El backlog exige no revelar datos; el código de eliminación queda pendiente de unificación en el SRS.
4. **Datos prohibidos en RF-24:** se interpretan como payload malicioso, fixture o fuente auxiliar no confiable, nunca como información capturada normalmente.
5. **Ciudad frente a municipio:** se usa `municipio`, término definido en el catálogo de cobertura.
6. **Tiempos de respuesta:** p95 de 3 segundos, timeout de transporte de 5 segundos y espera de interfaz de 30 segundos se conservan como métricas diferentes.

## 6. Resultado de la revisión

- Épicas finales: 5.
- Historias finales: 15.
- Historias con prioridad Alta: 12.
- Historias con prioridad Media: 2.
- Historias con prioridad Baja: 1.
- Estimación anterior: 83 puntos.
- Estimación final: 92 puntos.
- Incremento: 9 puntos, concentrado en HU-02, HU-10 y HU-11.

Los puntos P-01, P-02 y P-03 continúan afectando la configuración productiva o el método interno de varias historias. Las estimaciones deberán revisarse cuando dichos puntos y P-07 sean resueltos.
