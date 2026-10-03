# Backlog completo de producto — MLState

## 1. Alcance del backlog

Esta es la versión final del backlog derivado de `SRS_Equipo.md` y revisado en `ajustes_backlog.md`. Las estimaciones usan la escala Fibonacci y representan esfuerzo, complejidad e incertidumbre relativos.

## 2. Resumen de épicas

| ID | Épica | Objetivo | Historias | Puntos |
|---|---|---|---:|---:|
| EP-01 | Cobertura y captura del inmueble | Capturar datos válidos únicamente dentro de la cobertura habilitada. | 3 | 21 |
| EP-02 | Estimación y comprensión del valor | Producir una estimación confiable, trazable y comprensible, o abstenerse cuando no sea posible. | 5 | 34 |
| EP-03 | Acceso y sesiones | Ofrecer consultas anónimas y acceso seguro a funciones persistentes de broker. | 2 | 13 |
| EP-04 | Historial de estimaciones | Permitir al broker conservar y administrar sus estimaciones de forma aislada. | 2 | 11 |
| EP-05 | Reportes y compartición | Generar, proteger, descargar y compartir reportes de estimación. | 3 | 13 |
| **Total** | **5 épicas** |  | **15** | **92** |

## 3. Historias de usuario

## EP-01 — Cobertura y captura del inmueble

### HU-01 — Consultar cobertura y elegibilidad

**Historia de usuario:** Como usuario visitante o broker, quiero consultar la cobertura activa y verificar la elegibilidad de la combinación de ubicación, tipo de inmueble y uso de suelo, para saber si puedo continuar antes de capturar el resto de los datos.

**Criterios de aceptación:**

1. Dado que el catálogo contiene elementos activos e inactivos, cuando el usuario lo consulta sin autenticación, entonces la respuesta es `200 OK` y sólo devuelve estados, municipios, colonias, tipos y usos activos con su jerarquía correcta.
2. Dado que una combinación está habilitada, cuando el usuario verifica su elegibilidad, entonces la respuesta es `200 OK`, devuelve `elegible: true`, habilita la captura completa y el contador de inferencia permanece en cero.
3. Dado que una combinación no está habilitada o su ubicación es inconsistente, cuando el usuario verifica su elegibilidad, entonces la respuesta es `422` con `ZONA_FUERA_DE_COBERTURA`, identifica la condición y no habilita la captura ni invoca el modelo.
4. Dado que un código postal está asociado a varias colonias, cuando el usuario intenta continuar sin seleccionar una, entonces la respuesta es `409` con `COLONIA_AMBIGUA`, muestra las opciones y bloquea la continuación.

**Prioridad:** Alta  
**Story points:** 5  
**Trazabilidad:** RF-01, RF-02, RD-01, RNF-18

### HU-02 — Capturar las características del inmueble

**Historia de usuario:** Como usuario visitante o broker, quiero capturar las características obligatorias y opcionales del inmueble mediante un formulario guiado y accesible, para proporcionar correctamente la información necesaria para la estimación.

**Criterios de aceptación:**

1. Dado que la propiedad es elegible, cuando el usuario abre el formulario, entonces están representados los campos definidos por RD-01, las superficies usan `m²`, la antigüedad usa años y ubicación, tipo, uso y conservación se limitan a sus dominios autorizados.
2. Dado que se muestra el formulario, cuando se inspecciona cada campo, entonces indica mediante texto si es `Obligatorio` u `Opcional`, y los opcionales ausentes permanecen ausentes sin convertirse en valores predeterminados.
3. Dado que el usuario necesita orientación, cuando abre la ayuda de un campo, entonces ésta presenta definición, ejemplo, unidad o formato y fuente documental sin alterar ningún valor capturado.
4. Dado que el usuario opera con teclado o dispositivo táctil en uno de los anchos de RNF-09, cuando completa el formulario, entonces encuentra etiquetas asociadas, contraste AA, objetivos táctiles de al menos 48 por 48 px y ningún desplazamiento horizontal.

**Prioridad:** Alta  
**Story points:** 8  
**Trazabilidad:** RF-03, RD-01, RNF-06, RNF-07, RNF-08, RNF-09

### HU-03 — Validar y corregir los datos capturados

**Historia de usuario:** Como usuario visitante o broker, quiero recibir en una sola respuesta validaciones claras sobre datos faltantes, inválidos o ambiguos, para corregirlos sin perder la información válida ni ejecutar una estimación incorrecta.

**Criterios de aceptación:**

1. Dado que una entrada incumple formato, rango o catálogo, cuando se valida desde la interfaz o mediante solicitud directa, entonces la respuesta es `422` con `CAMPO_FUERA_DE_RANGO`, identifica cada campo y regla, conserva los valores válidos y no invoca el modelo.
2. Dado que municipio y colonia no corresponden al mismo registro, cuando se valida la ubicación, entonces se rechaza como fuera de cobertura; dado que la construcción supera al terreno pero ambas áreas son válidas, entonces las superficies se aceptan.
3. Dado que un valor es plausible pero atípico o numéricamente ambiguo, cuando se procesa, entonces el sistema devuelve `VALOR_AMBIGUO` y exige corregirlo o confirmarlo; si cambia el valor, la zona o la política, devuelve `CONFIRMACION_INVALIDADA` y solicita una nueva confirmación.
4. Dado que faltan campos obligatorios, cuando se intenta estimar, entonces la respuesta incluye todos los faltantes mediante `CAMPOS_OBLIGATORIOS_FALTANTES`; si sólo faltan opcionales, el flujo continúa sin inventar valores.

**Prioridad:** Alta  
**Story points:** 8  
**Trazabilidad:** RF-04, RF-05, RF-06, RD-01, RNF-08, RNF-16

## EP-02 — Estimación y comprensión del valor

### HU-04 — Calcular una estimación idempotente

**Historia de usuario:** Como usuario visitante o broker, quiero calcular una estimación idempotente como rango de precios en MXN, para conocer el valor orientativo del inmueble sin duplicar operaciones por reenvíos.

**Criterios de aceptación:**

1. Dado que la solicitud es elegible, completa y válida, cuando se envía con `Idempotency-Key`, entonces responde `201 Created` con `estimacionId`, valores mínimo, central y máximo positivos y ordenados, moneda MXN, margen, confianza y explicación.
2. Dado que una operación ya fue procesada, cuando se reenvía con la misma clave, entonces devuelve el mismo `estimacionId`, no crea otro resultado ni consume nuevamente la cuota.
3. Dado que el motor devuelve importes inválidos, límites invertidos, margen inválido, confianza fuera del dominio o versión incorrecta, cuando se valida la salida, entonces responde `422` con `RESULTADO_NO_PUBLICABLE`, no publica precio y no habilita el PDF.
4. Dado que no ocurrió un reentrenamiento, cuando se procesan entradas idénticas, entonces se obtienen los mismos valores mínimo, central y máximo.

**Prioridad:** Alta  
**Story points:** 8  
**Trazabilidad:** RF-07, RD-03, RD-07, RNF-15

### HU-05 — Abstenerse y recuperarse de fallos de estimación

**Historia de usuario:** Como usuario visitante o broker, quiero que el sistema se abstenga cuando no exista muestra suficiente y me permita reintentar ante fallos técnicos, para no tomar decisiones con valores inventados, anteriores o incompletos.

**Criterios de aceptación:**

1. Dado que se usa F-POL, cuando existen 29 referencias válidas, entonces se obtiene `409 MUESTRA_INSUFICIENTE_PARA_ESTIMAR`; cuando existen 30 o 31, entonces se permite continuar sin sustituir referencias por comparables exhibidos.
2. Dado que la muestra es insuficiente, cuando el sistema rechaza el cálculo, entonces no muestra cero, rango ni importes anteriores y no habilita el PDF.
3. Dado que el motor no responde en 5 segundos, cuando vence el timeout de transporte, entonces se devuelve `503 ERROR_EN_SERVICIO_DE_INFERENCIA`; al cumplirse 30 segundos desde el envío, la interfaz termina la espera, conserva los campos en memoria y ofrece reintentar.
4. Dado que el usuario reintenta, cuando llega una respuesta tardía de la solicitud anterior, entonces ésta no reemplaza el resultado de la solicitud nueva.

**Prioridad:** Alta  
**Story points:** 5  
**Trazabilidad:** RF-08, RF-09, RD-06, RNF-01, RNF-16

### HU-06 — Habilitar sólo modelos y datos autorizados

**Historia de usuario:** Como responsable del modelo, quiero que sólo se habiliten políticas, modelos y conjuntos de datos vigentes, evaluados y autorizados, para que cada estimación sea confiable y trazable.

**Criterios de aceptación:**

1. Dado que falta una política habilitada, una evaluación aprobada o un permiso vigente, cuando se solicita estimar, entonces la respuesta es `409` con `DATOS_NO_HABILITADOS`, no invoca el modelo y no produce precio ni PDF.
2. Dado que una fuente posee una actualización validada y una antigüedad máxima, cuando se verifica su vigencia, entonces se usa el instante validado; cambiar únicamente una etiqueta no renueva la autorización.
3. Dado que el conjunto contiene propiedades duplicadas o filas sin precio válido, cuando se evalúa la suficiencia, entonces esos registros se excluyen antes del conteo.
4. Dado que se intenta promover una versión, cuando se evalúa conforme a RNF-04, entonces sólo se habilita si acredita MdAPE menor o igual a 15 % por unidad de cobertura con al menos 100 cierres verificados no usados en entrenamiento, y registra versión, muestra, fuente y evidencia de autorización.

**Prioridad:** Alta  
**Story points:** 8  
**Trazabilidad:** RF-10, RD-05, RD-11, RNF-04, RNF-05, RNF-19

### HU-07 — Comprender el rango y la confianza

**Historia de usuario:** Como usuario visitante o broker, quiero ver el rango, precio por metro cuadrado, margen, confianza, fechas y versiones utilizadas, para interpretar la magnitud, precisión y vigencia de la estimación.

**Criterios de aceptación:**

1. Dado que existe una estimación exitosa, cuando se muestra el resultado, entonces aparecen simultáneamente el valor central, el rango y el precio en `MXN/m² de construcción`, calculado sobre superficie construida y redondeado a dos decimales con empate hacia arriba.
2. Dado que existen fechas y versiones asociadas al cálculo, cuando se presenta el resultado, entonces muestra por separado `Fecha de cálculo` y `Actualización de datos` en `AAAA-MM-DD`, además de las versiones de modelo, datos y política.
3. Dado que se recibe el resultado, cuando se validan sus metadatos, entonces `margenErrorPorcentaje` es numérico, mayor o igual a cero y no supera la mitad de la amplitud relativa, y `nivelConfianza` sólo admite `baja`, `media` o `alta`.
4. Dado que faltan datos opcionales o existen menos de tres comparables, cuando se determina la confianza, entonces su categoría se reduce conforme a la política y se presenta la causa sin inventar valores.

**Prioridad:** Alta  
**Story points:** 5  
**Trazabilidad:** RF-11, RF-12, RD-04, RD-07

### HU-08 — Comprender la evidencia y las limitaciones

**Historia de usuario:** Como usuario visitante o broker, quiero consultar una explicación comprensible, propiedades comparables y la advertencia de carácter orientativo, para entender la evidencia y las limitaciones de la estimación.

**Criterios de aceptación:**

1. Dado que existe una estimación, cuando se muestra la explicación, entonces tiene entre 15 y 300 caracteres, usa factores efectivamente capturados, indica cuáles elevaron o redujeron el valor y no contiene el vocabulario técnico prohibido por RF-13.
2. Dado que existen al menos tres comparables elegibles, cuando se presentan, entonces se muestran entre tres y cinco, ordenados por similitud, deduplicados y dentro de la ventana inclusiva de 12 meses, sin fechas futuras, datos de contacto ni registros sin permiso de exhibición.
3. Dado que se presenta un comparable, cuando se inspecciona su ficha, entonces contiene colonia, tipo, uso, superficies, precio, fecha y naturaleza de la referencia, y su selección respeta las reglas de homogeneización.
4. Dado que una vista o PDF contiene un precio estimado, cuando se presenta al usuario, entonces muestra de forma permanente el texto íntegro de RD-02 y no ofrece controles para ocultarlo.

**Prioridad:** Alta  
**Story points:** 8  
**Trazabilidad:** RF-13, RF-14, RF-15, RD-02, RD-05, RD-10

## EP-03 — Acceso y sesiones

### HU-09 — Completar y administrar una consulta anónima

**Historia de usuario:** Como usuario visitante, quiero completar, recuperar y finalizar temporalmente una consulta sin registrarme, para obtener una estimación y su reporte sin crear una cuenta ni dejar datos persistentes.

**Criterios de aceptación:**

1. Dado que el visitante no tiene credenciales, cuando captura una propiedad, calcula la estimación y descarga el reporte, entonces ninguna acción exige registro o autenticación.
2. Dado que el resultado pertenece a la sesión activa, cuando se consulta dentro de los 60 minutos posteriores a su finalización, entonces el resultado y el PDF están disponibles; una descarga no reinicia el plazo y, al vencer, se responde `CONSULTA_EXPIRADA`.
3. Dado que un resultado pertenece a otra sesión, cuando se intenta acceder a él, entonces se responde `403 ACCESO_DENEGADO` sin confirmar la existencia del recurso.
4. Dado que una consulta está vigente, cuando el usuario selecciona `Finalizar consulta`, entonces se eliminan entradas, resultado y reporte temporal, y las respuestas con contenido de consulta usan `Cache-Control: no-store`.

**Prioridad:** Alta  
**Story points:** 5  
**Trazabilidad:** RF-18, RNF-12, RNF-14

### HU-10 — Registrar y autenticar una cuenta de broker

**Historia de usuario:** Como visitante que desea utilizar funciones persistentes de broker, quiero crear una cuenta e iniciar y cerrar sesión de forma segura, para acceder únicamente a mis estimaciones guardadas.

**Criterios de aceptación:**

1. Dado que el correo no está registrado y la contraseña tiene al menos 10 caracteres, una mayúscula, una minúscula y un número, cuando se envían nombre, correo y contraseña válidos, entonces la respuesta es `201 Created`, se crea una cuenta `broker` y la contraseña se almacena con Argon2id o bcrypt.
2. Dado que el correo ya existe o la contraseña incumple la política, cuando se intenta registrar la cuenta, entonces se obtiene respectivamente `409 EMAIL_YA_REGISTRADO` o `422` con los requisitos incumplidos, y no se crea la cuenta.
3. Dado que existe una cuenta activa, cuando se envían credenciales válidas, entonces la respuesta es `200 OK` y se crea una sesión asociada a la cuenta; con credenciales inválidas se obtiene `401 CREDENCIALES_INVALIDAS` sin revelar si el correo existe.
4. Dado que transcurren dos horas de inactividad o el usuario cierra la sesión, cuando intenta acceder a una función protegida, entonces el sistema exige autenticarse nuevamente.

**Prioridad:** Alta  
**Story points:** 8  
**Trazabilidad:** RF-16, RF-17, RNF-10, RNF-11

## EP-04 — Historial de estimaciones

### HU-11 — Guardar y consultar el historial

**Historia de usuario:** Como broker autenticado, quiero guardar una estimación y consultar mi historial filtrado por municipio y fecha, para recuperar rápidamente trabajos previos.

**Criterios de aceptación:**

1. Dado que el broker consulta un resultado con una sesión válida, cuando selecciona `Guardar estimación`, entonces se almacenan entradas, tres importes, moneda, fecha, margen, confianza y versiones bajo la identidad activa; sin sesión, la respuesta es `401` y no se guarda.
2. Dado que el broker tiene estimaciones guardadas, cuando consulta el historial, entonces sólo recibe registros propios, ordenados por fecha descendente y, ante empate, por `estimacionId` descendente, en páginas de 20.
3. Dado que el broker selecciona un municipio y un rango válido de fechas, cuando aplica los filtros, entonces sólo se devuelven coincidencias de su cuenta y se muestra un estado vacío explícito cuando no existen resultados.
4. Dado que una estimación autenticada cumple 12 meses desde su emisión, cuando se ejecuta la política de retención, entonces se elimina automáticamente sin requerir una acción del broker.

**Prioridad:** Media  
**Story points:** 8  
**Trazabilidad:** RF-19, RF-20, RNF-12, RNF-14

### HU-12 — Consultar y eliminar una estimación guardada

**Historia de usuario:** Como broker autenticado, quiero revisar el detalle y eliminar estimaciones propias, para administrar los registros que ya no necesito.

**Criterios de aceptación:**

1. Dado que una estimación pertenece al broker, cuando solicita su detalle, entonces la respuesta es `200 OK` y muestra todas las entradas, tres importes, moneda, margen, confianza, fechas y versiones.
2. Dado que el detalle no existe o pertenece a otra cuenta, cuando el broker lo solicita, entonces la respuesta es `404 ESTIMACION_NO_ENCONTRADA` sin revelar propiedad ni existencia.
3. Dado que el broker confirma eliminar un registro propio, cuando se procesa la acción, entonces la respuesta es `204 No Content` y el registro desaparece del historial; si cancela, el registro se conserva.
4. Dado que un registro pertenece a otra cuenta, cuando se intenta eliminar, entonces la operación se rechaza sin modificarlo ni exponer sus datos.

**Prioridad:** Media  
**Story points:** 3  
**Trazabilidad:** RF-21, RF-22, RNF-12

## EP-05 — Reportes y compartición

### HU-13 — Generar y descargar un reporte PDF

**Historia de usuario:** Como usuario visitante o broker, quiero generar y descargar un PDF de una estimación exitosa, para conservar y presentar el resultado fuera de la aplicación.

**Criterios de aceptación:**

1. Dado que una estimación está vigente, cuando el usuario solicita el reporte, entonces recibe `200 OK` y un PDF válido con ficha, tres importes, margen, confianza, explicación, comparables, fechas y el texto íntegro de RD-02.
2. Dado que se generó el PDF, cuando se abre en la matriz de dispositivos y navegadores de RNF-09, entonces el documento se visualiza sin error.
3. Dado que el reporte ya fue generado, cuando se solicita de nuevo sin recalcular, entonces conserva contenido, fechas y fecha de emisión sin invocar nuevamente el modelo.
4. Dado que falla la generación, cuando el usuario reintenta, entonces el problema se informa como fallo de reporte, la estimación permanece visible y no se recalcula el valor.

**Prioridad:** Alta  
**Story points:** 5  
**Trazabilidad:** RF-23, RF-15-AC-3, RNF-09

### HU-14 — Proteger la privacidad del reporte

**Historia de usuario:** Como usuario visitante o broker, quiero que el sistema impida incorporar datos personales o ubicación exacta al reporte, para compartirlo sin exponer información sensible.

**Criterios de aceptación:**

1. Dado que se inspeccionan los contratos de entrada, cuando se revisan sus campos, entonces no solicitan ni aceptan dirección exacta, coordenadas, datos del propietario, documentos ni datos bancarios.
2. Dado que una fuente auxiliar o fixture de seguridad contiene datos prohibidos, cuando se genera el PDF, entonces su texto, imágenes, metadatos, enlaces y nombre de archivo los omiten y sólo conservan estado, municipio y colonia o código postal.
3. Dado que el usuario genera un reporte, cuando utiliza la configuración disponible, entonces la protección se aplica automáticamente y no existe una opción para desactivarla.
4. Dado que un cliente solicita incluir dirección o datos de contacto, cuando el servidor procesa la instrucción, entonces responde `422 NO_SE_PERMITE_REVELAR_DIRECCION` y no genera el PDF.

**Prioridad:** Alta  
**Story points:** 5  
**Trazabilidad:** RF-24, RD-08, RNF-13

### HU-15 — Compartir el reporte desde el dispositivo

**Historia de usuario:** Como usuario visitante o broker, quiero compartir el PDF mediante las capacidades disponibles en mi dispositivo, para enviarlo con la aplicación que elija o descargarlo cuando la compartición no esté disponible.

**Criterios de aceptación:**

1. Dado que el navegador y el dispositivo admiten compartición, cuando el usuario selecciona compartir, entonces se invoca el puente del sistema operativo con el PDF y un mensaje precargado.
2. Dado que el puente no está disponible o no puede completar la entrega, cuando el usuario intenta compartir, entonces la aplicación ofrece descarga directa y presenta un mensaje controlado.
3. Dado que la aplicación entrega el archivo al puente, cuando se ejecuta la compartición, entonces no transmite el binario a servidores distintos del que generó el reporte.
4. Dado que se prepara la aceptación de la historia, cuando se prueban compartición y degradación, entonces ambos escenarios se verifican manualmente en dispositivos reales compatibles.

**Prioridad:** Baja  
**Story points:** 3  
**Trazabilidad:** RF-25

## 4. Resumen de priorización y estimación

| Historia | Épica | Prioridad | Story points |
|---|---|---|---:|
| HU-01 | EP-01 | Alta | 5 |
| HU-02 | EP-01 | Alta | 8 |
| HU-03 | EP-01 | Alta | 8 |
| HU-04 | EP-02 | Alta | 8 |
| HU-05 | EP-02 | Alta | 5 |
| HU-06 | EP-02 | Alta | 8 |
| HU-07 | EP-02 | Alta | 5 |
| HU-08 | EP-02 | Alta | 8 |
| HU-09 | EP-03 | Alta | 5 |
| HU-10 | EP-03 | Alta | 8 |
| HU-11 | EP-04 | Media | 8 |
| HU-12 | EP-04 | Media | 3 |
| HU-13 | EP-05 | Alta | 5 |
| HU-14 | EP-05 | Alta | 5 |
| HU-15 | EP-05 | Baja | 3 |
| **Total** |  |  | **92** |

## 5. Definición de Terminado global

Una historia no se considera terminada únicamente por cumplir sus criterios locales. También debe satisfacer las siguientes condiciones cuando sean aplicables:

1. **Rendimiento:** La estimación cumple p95 menor o igual a 3 segundos bajo las condiciones de RNF-01.
2. **Escalabilidad:** La API soporta 200 inferencias concurrentes con menos de 1 % de errores conforme a RNF-02.
3. **Disponibilidad:** El servicio satisface RNF-03 una vez ratificados D-09 y la volumetría de P-07.
4. **Usabilidad:** El formulario cumple p90 menor o igual a 120 segundos con al menos cinco usuarios de campo.
5. **Accesibilidad y compatibilidad:** Las pantallas aplicables cumplen RNF-07, RNF-08 y la matriz de RNF-09.
6. **Seguridad:** El transporte usa TLS 1.3 o superior; las sesiones usan cookies `Secure`, `HttpOnly` y `SameSite`; los datos protegidos se cifran en reposo y no aparecen en logs.
7. **Privacidad y retención:** Las consultas anónimas, historial, caché y logs cumplen los plazos y restricciones de RNF-14.
8. **Límites de uso:** Se aplican 60 lecturas por minuto, 10 cálculos por minuto y 3 estimaciones anónimas por día conforme a RNF-15, sin doble consumo por reenvío idempotente.
9. **Redes móviles:** Una interrupción de conexión no elimina los datos válidos capturados en el formulario.
10. **Pruebas:** Todos los criterios aplicables tienen evidencia de prueba y los módulos críticos alcanzan al menos 80 % de cobertura de líneas conforme a RNF-17.
11. **Extensibilidad:** Una nueva cobertura puede incorporarse por configuración sin modificar el flujo compartido, conforme a RNF-18.
12. **Operación del modelo:** El reentrenamiento trimestral y la revisión mensual de datos se ejecutan y registran conforme a RNF-19; una deriva superior al umbral durante dos semanas consecutivas genera la alerta definida por RNF-05.

## 6. Dependencias y riesgos abiertos

| Punto | Impacto en el backlog |
|---|---|
| P-01 — Límites de plausibilidad | HU-03 sólo puede validar el mecanismo con políticas sintéticas hasta definir los límites productivos. |
| P-02 — Fuente de transacciones cerradas | Bloquea la habilitación productiva de HU-06 y la acreditación de RNF-04. |
| P-03 — Calibración y explicación | Afecta el método interno de HU-07 y HU-08, aunque sus salidas siguen siendo verificables. |
| P-05 — Inactividad de sesión | HU-10 adopta las dos horas propuestas por RNF-11, pendientes de validación de negocio. |
| P-07 — Volumetría | Impide validar de forma definitiva rendimiento, escalabilidad y disponibilidad contra una carga realista. |
| P-10 — Deduplicación | Afecta la ejecución productiva de HU-06 y HU-08 hasta definir la clave normalizada de propiedad. |

## 7. Criterios de planificación

- HU-03, HU-04, HU-06 y HU-08 tienen 8 puntos por su densidad de reglas, integraciones o incertidumbre.
- HU-02, HU-10 y HU-11 fueron reestimadas a 8 puntos después de incluir accesibilidad, seguridad y ciclo de vida de datos.
- HU-06 y HU-08 pueden dividirse en tareas técnicas o historias más pequeñas durante la planificación de sprint sin perder su identificador de producto.
- Los puntos deben revisarse con el equipo cuando se resuelvan P-01, P-02, P-03 y P-07.
