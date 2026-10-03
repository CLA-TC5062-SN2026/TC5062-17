# Priorización comparada del backlog de MLState

## 1. Objetivo

Este documento prioriza las 15 historias de `backlog_completo.md` desde la perspectiva del Product Owner y compara el resultado con el orden observado en el GitHub Project [MLState - Product Backlog](https://github.com/orgs/CLA-TC5062-SN2026/projects/15).

La prioridad declarada en el backlog sigue siendo válida como clasificación general. Sin embargo, doce historias tienen prioridad Alta, por lo que esa clasificación no basta para decidir cuál debe implementarse primero. El orden propuesto incorpora valor de negocio, riesgo y dependencias.

## 2. Criterios de priorización

Los siguientes criterios se aplicaron en orden de importancia:

1. **Viabilidad del producto:** demostrar que existen datos autorizados, cobertura habilitada y un modelo suficientemente preciso. Sin esto no hay una estimación comercializable.
2. **Valor central para el usuario:** permitir que una persona obtenga un rango inmobiliario útil, comprensible y trazable.
3. **Reducción de riesgo:** evitar precios inventados, resultados fuera de cobertura, datos no autorizados o reportes con información sensible.
4. **Dependencias:** implementar primero las capacidades que habilitan otras historias y evitar construir funciones sobre flujos todavía inexistentes.
5. **Adopción:** conservar el acceso anónimo para reducir fricción y cumplir la restricción de que el sistema completo pueda utilizarse sin cuenta.
6. **Cumplimiento y confianza:** integrar abstención, explicación, comparables, advertencia legal y privacidad antes de liberar resultados.
7. **Retención y conveniencia:** incorporar cuentas, historial y compartición después de validar el flujo central.
8. **Esfuerzo relativo:** usar los story points para valorar el tiempo hasta obtener beneficios, sin anteponer una historia pequeña si depende de una capacidad aún inexistente.

## 3. Orden recomendado por valor de negocio

| Posición | Historia | Puntos | Justificación de negocio | Dependencias o condición |
|---:|---|---:|---|---|
| 1 | **HU-06 — Habilitar sólo modelos y datos autorizados** | 8 | Ataca el riesgo existencial del producto. Sin fuente autorizada, evaluación aprobada y modelo vigente, MLState no puede emitir una estimación productiva ni demostrar precisión. Debe comenzar primero, aunque avance en paralelo con el catálogo. | P-02, RNF-04 y ratificación de D-06. |
| 2 | **HU-01 — Consultar cobertura y elegibilidad** | 5 | Define dónde y para qué inmuebles existe valor comercial. Evita capturas inútiles e inferencias fuera de cobertura, y delimita las unidades donde debe evaluarse el modelo. | Catálogo y alcance de cobertura. |
| 3 | **HU-02 — Capturar las características del inmueble** | 8 | Construye la principal interacción del usuario y proporciona la entrada indispensable para estimar. Su accesibilidad móvil es clave para el broker que opera en campo. | HU-01 y esquema de RD-01. |
| 4 | **HU-03 — Validar y corregir los datos capturados** | 8 | Protege la calidad de entrada y evita resultados incorrectos. Habilita solicitudes completas y el tratamiento seguro de valores inválidos, ambiguos o atípicos. | HU-02 y P-01 para política productiva. |
| 5 | **HU-09 — Completar y administrar una consulta anónima** | 5 | Define desde el inicio el canal de adopción con menor fricción. Evita diseñar el núcleo alrededor de una cuenta obligatoria y establece aislamiento, vigencia y eliminación de datos temporales. | Arquitectura de sesión; su flujo completo termina con HU-13. |
| 6 | **HU-04 — Calcular una estimación idempotente** | 8 | Materializa la propuesta de valor: producir un rango orientativo confiable sin duplicar operaciones ni cuota. Habilita presentación, reporte e historial. | HU-01, HU-03 y HU-06. |
| 7 | **HU-05 — Abstenerse y recuperarse de fallos de estimación** | 5 | Protege la reputación del producto. Es preferible no emitir un precio que mostrar uno sin muestra suficiente o reutilizar un resultado anterior. | HU-04, suficiencia de HU-06 y RD-06. |
| 8 | **HU-07 — Comprender el rango y la confianza** | 5 | Convierte una salida técnica en información útil para decidir: rango, precio unitario, margen, confianza, fechas y versiones. | HU-04 y metadatos de HU-06; P-08. |
| 9 | **HU-08 — Comprender la evidencia y las limitaciones** | 8 | Aporta explicación, comparables y advertencia legal. Incrementa la credibilidad y evita presentar la estimación como avalúo oficial. | HU-04, HU-06 y HU-07; P-03 y P-10. |
| 10 | **HU-14 — Proteger la privacidad del reporte** | 5 | Introduce privacidad por diseño antes de distribuir documentos. Reduce riesgo legal y reputacional al impedir que el reporte exponga ubicación exacta o datos personales. | Esquema de HU-02, contenido de HU-08 y coordinación con HU-13. |
| 11 | **HU-13 — Generar y descargar un reporte PDF** | 5 | Cierra el flujo anónimo con un entregable que el usuario puede conservar o presentar. Sólo aporta un incremento liberable cuando su contenido ya es correcto y está protegido. | HU-04, HU-07, HU-08, HU-09 y HU-14; P-09. |
| 12 | **HU-10 — Registrar y autenticar una cuenta de broker** | 8 | Habilita persistencia y uso recurrente para brokers, pero no debe bloquear la validación del valor central porque el producto debe funcionar sin cuenta. | Seguridad de sesión y P-05. |
| 13 | **HU-11 — Guardar y consultar el historial** | 8 | Aumenta retención y productividad profesional mediante guardado, filtros y recuperación. No mejora la validez de una estimación individual y depende de identidad. | HU-10 y resultados de HU-04. |
| 14 | **HU-12 — Consultar y eliminar una estimación guardada** | 3 | Completa la administración y gobernanza del historial, pero sólo genera valor después de que el broker pueda crear y listar registros. | HU-10 y HU-11. |
| 15 | **HU-15 — Compartir el reporte desde el dispositivo** | 3 | Mejora la conveniencia de distribución, pero la descarga de HU-13 ya ofrece una alternativa funcional. No modifica la validez de la estimación y depende de capacidades del dispositivo. | HU-13 y HU-14. |

## 4. Justificación del inicio y del final

### Por qué estas historias van primero

- **HU-06 va antes que la interfaz** porque la disponibilidad de datos autorizados y un modelo aprobado es el mayor riesgo del proyecto. Una interfaz terminada no genera valor si todas las zonas deben permanecer deshabilitadas.
- **HU-01, HU-02 y HU-03 forman la entrada confiable**: primero se comprueba cobertura, después se captura y finalmente se valida. Este orden evita retrabajo y llamadas inválidas al modelo.
- **HU-09 entra antes del cálculo completo** porque el acceso anónimo es una decisión estructural. Postergarlo podría producir una arquitectura dependiente de cuentas que contradiga el SRS.
- **HU-04 entrega la propuesta central**, pero sólo después de asegurar cobertura, datos y entradas válidas.
- **HU-05, HU-07 y HU-08 son parte del producto responsable**, no mejoras visuales. Abstención, confianza y evidencia determinan si el resultado puede publicarse y ser entendido.

### Por qué estas historias van al final

- **HU-10 se pospone hasta cerrar el flujo anónimo** porque una cuenta agrega persistencia, pero no es necesaria para demostrar la propuesta de valor.
- **HU-11 y HU-12 dependen de HU-10** y optimizan el trabajo recurrente del broker; no generan una primera estimación.
- **HU-15 queda al final** porque depende de un PDF generado y protegido, requiere pruebas en dispositivos reales y ya existe la descarga directa como alternativa.
- **HU-12 va antes de HU-15**, aunque aporta menos valor visible, porque completa el control del usuario sobre datos persistentes y la política de privacidad del historial.

## 5. Corte de MVP

El MVP recomendado termina en **HU-13** e incluye las primeras 11 historias del orden propuesto:

`HU-06 → HU-01 → HU-02 → HU-03 → HU-09 → HU-04 → HU-05 → HU-07 → HU-08 → HU-14 → HU-13`

**Tamaño del MVP:** 70 de 92 story points.

Este corte entrega:

- Consulta completa sin registro.
- Cobertura y captura validadas.
- Modelo y datos autorizados y trazables.
- Estimación idempotente con abstención segura.
- Rango, margen, confianza, explicación y comparables.
- Advertencia de carácter orientativo.
- Sesión anónima aislada y temporal.
- PDF descargable y protegido.

Excluir autorización de datos, abstención, confianza o privacidad reduciría puntos, pero produciría una demostración técnica y no un producto responsable listo para usuarios.

## 6. Agrupación Now, Next y Later

| Horizonte | Historias | Propósito |
|---|---|---|
| **Now — MVP anónimo** | HU-06, HU-01, HU-02, HU-03, HU-09, HU-04, HU-05, HU-07, HU-08, HU-14, HU-13 | Entregar una estimación anónima completa, confiable, comprensible y protegida. |
| **Next — Broker recurrente** | HU-10, HU-11, HU-12 | Incorporar identidad, persistencia y administración del historial. |
| **Later — Conveniencia** | HU-15 | Facilitar la distribución del PDF desde aplicaciones del dispositivo. |

## 7. Orden observado en GitHub Project

El orden recuperado del Project al realizar este análisis fue:

| Posición GitHub | Historia |
|---:|---|
| 1 | HU-01 |
| 2 | HU-03 |
| 3 | HU-02 |
| 4 | HU-04 |
| 5 | HU-06 |
| 6 | HU-08 |
| 7 | HU-05 |
| 8 | HU-07 |
| 9 | HU-10 |
| 10 | HU-12 |
| 11 | HU-11 |
| 12 | HU-15 |
| 13 | HU-09 |
| 14 | HU-13 |
| 15 | HU-14 |

Todos los elementos se encontraban en estado `Todo`. Este orden es la línea base de la comparación; no se modificó el Project como parte de este análisis.

## 8. Comparación posición por posición

La columna “Movimiento” indica el cambio necesario para pasar del orden de GitHub al orden recomendado. “Sube” significa que la historia debe ejecutarse antes.

| Historia | Posición GitHub | Posición propuesta | Movimiento | Evaluación |
|---|---:|---:|---:|---|
| HU-01 | 1 | 2 | Baja 1 | Coincide en ubicar cobertura al inicio; sólo la precede la reducción del riesgo de datos y modelo. |
| HU-02 | 3 | 3 | Sin cambio | Coincidencia exacta. La captura permanece dentro del primer bloque de construcción. |
| HU-03 | 2 | 4 | Baja 2 | GitHub la coloca antes de la captura que debe validar. Se corrige la dependencia HU-02 → HU-03. |
| HU-04 | 4 | 6 | Baja 2 | Coincide en tratar el cálculo como núcleo, pero debe esperar la habilitación de datos y el diseño de sesión anónima. |
| HU-05 | 7 | 7 | Sin cambio | Coincidencia exacta. La abstención sigue inmediatamente al cálculo en el flujo seguro. |
| HU-06 | 5 | 1 | Sube 4 | Es la diferencia estratégica principal: el Project subestima el riesgo de no contar con datos autorizados y precisión acreditable. |
| HU-07 | 8 | 8 | Sin cambio | Coincidencia exacta. La interpretación del resultado sigue al cálculo y su manejo de fallos. |
| HU-08 | 6 | 9 | Baja 3 | GitHub la adelanta antes de abstención y presentación básica; la propuesta primero asegura que el resultado sea válido y legible. |
| HU-09 | 13 | 5 | Sube 8 | Es la mayor diferencia. El acceso anónimo es parte del alcance central y una decisión arquitectónica, no una función tardía. |
| HU-10 | 9 | 12 | Baja 3 | GitHub inicia cuentas antes de completar el flujo anónimo; la propuesta prioriza adopción sin registro. |
| HU-11 | 11 | 13 | Baja 2 | Mantiene valor posterior al MVP y se conserva después de autenticación. |
| HU-12 | 10 | 14 | Baja 4 | GitHub coloca detalle y eliminación antes de guardar y listar historial. Se restaura HU-11 → HU-12. |
| HU-13 | 14 | 11 | Sube 3 | El PDF forma parte del flujo anónimo completo y debe cerrar el MVP antes de las funciones persistentes del broker. |
| HU-14 | 15 | 10 | Sube 5 | La privacidad debe diseñarse antes de generar y distribuir el PDF, no validarse al final. |
| HU-15 | 12 | 15 | Baja 3 | Compartir depende de generar y proteger el reporte; además, la descarga ya cubre el caso básico. |

## 9. Coincidencias

1. **El núcleo funcional está mayormente al inicio.** Ambos órdenes reconocen la importancia de cobertura, captura, validación y cálculo.
2. **HU-02, HU-05 y HU-07 coinciden exactamente** en las posiciones 3, 7 y 8.
3. **HU-01 permanece en las dos primeras posiciones**, por lo que ambos enfoques reconocen que no debe capturarse fuera de cobertura.
4. **HU-10, HU-11 y HU-12 se mantienen fuera del primer bloque de estimación**, aunque difieren en posición y secuencia interna.
5. **HU-15 permanece en la parte baja**, reflejando su prioridad Baja y su carácter de conveniencia.

## 10. Diferencias y sus causas

### Riesgo de datos y modelo

GitHub ubica HU-06 en la posición 5; la propuesta la coloca en la 1. La causa es que el orden del Project favorece la secuencia visible de interfaz, mientras la priorización de negocio comienza por el supuesto más riesgoso: que exista una fuente autorizada y un modelo que pueda habilitarse.

### Acceso anónimo

GitHub ubica HU-09 en la posición 13; la propuesta la mueve a la 5. La sesión anónima afecta arquitectura, privacidad, retención y adopción. No debe agregarse al final como una variante de acceso.

### Dependencias invertidas

El Project contiene tres inversiones claras:

- HU-03 antes de HU-02: validar antes de disponer del flujo de captura.
- HU-12 antes de HU-11: consultar y eliminar antes de guardar y listar.
- HU-15 antes de HU-13 y HU-14: compartir antes de generar y proteger el documento.

La propuesta corrige esas secuencias para reducir retrabajo y evitar incrementos incompletos.

### Privacidad del reporte

GitHub deja HU-14 al final. La propuesta la ubica antes de HU-13 porque la privacidad no debe ser una revisión posterior a la generación del PDF. Un reporte que pueda filtrar datos sensibles no es un incremento liberable.

### Identidad frente a propuesta central

GitHub coloca HU-10 en la posición 9 y el historial entre las posiciones 10 y 11. La propuesta desplaza este bloque después del PDF anónimo. La razón es que el SRS exige que el usuario pueda completar el flujo sin registrarse; la cuenta agrega retención, no acceso al valor inicial.

## 11. Conclusión del Product Owner

El orden del GitHub Project refleja razonablemente el inventario del backlog y sitúa varias funciones centrales en la mitad superior, pero no constituye todavía una secuencia óptima de entrega. Mezcla orden de creación con prioridad y presenta dependencias invertidas.

La recomendación es adoptar el siguiente orden de ejecución:

`HU-06 → HU-01 → HU-02 → HU-03 → HU-09 → HU-04 → HU-05 → HU-07 → HU-08 → HU-14 → HU-13 → HU-10 → HU-11 → HU-12 → HU-15`

Las decisiones más importantes son iniciar la validación de datos y modelo desde el primer momento, tratar el acceso anónimo como parte estructural del MVP, proteger el reporte antes de generarlo y dejar cuentas, historial y compartición para después de validar la propuesta central.

Esta priorización debe revisarse cuando se resuelvan P-01, P-02, P-03 y P-07. En particular, P-02 puede bloquear el MVP completo y requiere gestión inmediata, independientemente del avance de interfaz.
