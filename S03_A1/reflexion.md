# ¿En qué aspectos el agente fue útil para comprender los fundamentos del SWEBOK?
- Utilizó la fuente especificada para evitar problemas de alucionación aumentando la precision de las respuestas.
- Logró hacer una extraccción puntual de los temas solicitados.
- Me permitió enfocarme directamente en los puntos incluidos del entregable evitando distracciones con contenido adicional disponible en la fuente original.

# ¿En qué aspectos fue insuficiente o impreciso? ¿Cómo lo detectaste?
- En la primer pregunta me dio contexto no solicitado. 
- En relación con el punto anterior, esto es consecuencia de que mi prompt no fue lo suficientemente rígido o especifico lo cual dio paso a una decision deliberada del modelo por "incluir texto de mas".
- Al tener un prompt especifico en la segunda pregunta, es evidente que se perdió contexto o información adicional válida al solicitar respuestas breves.

# ¿Cómo planeas usar el agente durante el resto del curso para maximizar su utilidad sin depender ciegamente de él?
- Herramienta de consulta
- Herramienta de bosquejo/brainstorm
- Herramienta de revisión (post revision humana, o sea, una vez que yo haya revisado el codigo)

# ¿Qué ventajas y riesgos identificas en usar un agente de IA para generar el Product Backlog?

Una ventaja importante es la velocidad con la que el agente puede analizar un SRS extenso, agrupar los requerimientos en épicas y convertirlos en historias de usuario con criterios de aceptación, prioridad, estimación y trazabilidad. También ayuda a mantener un formato uniforme, detectar requisitos relacionados y revisar sistemáticamente que ninguna funcionalidad quede fuera del backlog. En este ejercicio, el agente permitió relacionar las 15 historias con los requerimientos funcionales, no funcionales y de dominio, además de identificar dependencias y contradicciones que no eran evidentes en una primera lectura.

El principal riesgo es asumir que un backlog generado automáticamente ya representa las prioridades reales del negocio. El agente puede producir historias formalmente correctas, pero simplificar demasiado un requisito, agrupar funciones que deberían separarse o asignar story points sin conocer la capacidad y experiencia del equipo. También puede interpretar como definitiva una decisión que el SRS todavía mantiene abierta. Por eso, sus resultados deben revisarse con usuarios, Product Owner, equipo técnico y responsables de datos. La IA reduce el trabajo mecánico y facilita el análisis, pero no elimina la necesidad de validación humana.

# ¿Puede un agente reemplazar al Product Owner? Argumenta tu posición.

No considero que un agente pueda reemplazar al Product Owner. Puede apoyarlo al organizar información, proponer historias, detectar dependencias, comparar alternativas y preparar análisis de priorización. Sin embargo, el Product Owner representa las necesidades de los interesados, conoce el contexto comercial y es responsable de tomar decisiones sobre alcance, valor y riesgos. Estas decisiones requieren negociación, criterio y responsabilidad, no sólo procesamiento de documentos.

En este backlog, por ejemplo, el agente pudo recomendar que la habilitación de datos y modelo fuera primero porque representa un riesgo crítico. Aun así, no puede ratificar el umbral de precisión, autorizar una fuente de datos ni decidir por el negocio si el MVP debe privilegiar adopción anónima o funciones para brokers. Tampoco puede estimar por sí solo el costo real del equipo o comprometer una fecha de entrega. Su función adecuada es la de asistente analítico del Product Owner, mientras que la decisión final y la rendición de cuentas deben permanecer en una persona.

# ¿Cómo afecta la calidad del SRS a la calidad del backlog generado?

La calidad del SRS determina directamente la calidad del backlog. Un SRS claro, consistente y verificable permite generar historias específicas, criterios medibles y trazabilidad entre necesidades y entregables. La definición de actores, reglas de negocio, restricciones, errores y criterios de aceptación de `SRS_Equipo.md` hizo posible construir un backlog detallado y detectar qué historias dependían de otras.

Cuando el SRS contiene ambigüedades, contradicciones o decisiones pendientes, esas deficiencias se trasladan al backlog. En este caso aparecieron dudas sobre el guardado automático o explícito, la persistencia del borrador, los códigos para accesos no autorizados y parámetros todavía no ratificados. El agente puede señalar estos problemas y proponer una interpretación, pero no resolverlos legítimamente sin información del negocio. Por ello, un backlog generado desde un SRS deficiente puede parecer completo y ordenado, aunque sus historias estén basadas en supuestos incorrectos. La trazabilidad ayuda a identificar estos riesgos, pero la calidad final requiere mejorar primero la especificación y validar sus puntos abiertos.
