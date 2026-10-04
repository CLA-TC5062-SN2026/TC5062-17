# Planificación del Sprint 1

## 1. Capacidad del Equipo

### Horas disponibles

Considerando las restricciones proporcionadas:

| Concepto | Cálculo | Total (Horas-Hombre) |
|---|---|---|
| Miembros del equipo | 4 personas | - |
| Horas semanales por persona | 7 - 8 horas | 28 - 32 h/semana |
| Duración del Sprint | 2 semanas | 56 - 64 h/Sprint |

**Capacidad total estimada:** **56 - 64 horas-hombre** para el Sprint 1.

### Story Points estimados

Al tratarse del primer Sprint del proyecto (sin velocidad histórica), se adopta un enfoque **conservador** para mitigar riesgos, teniendo en cuenta la complejidad del dominio (validaciones, reglas de negocio, idempotencia y cumplimiento de requisitos no funcionales).

Se ha considerado un **factor de enfoque** del equipo para este primer Sprint del 40% - 50% sobre la capacidad teórica, para dar cabida a:

- Ceremonias ágiles (Sprint Planning, Daily, Review y Retrospectiva)
- Configuración del entorno, alineación técnica y resolución de dudas
- Curva de aprendizaje del dominio (MLState, cobertura, F-POL, etc.)
- Gestión de dependencias y riesgos identificados

| Enfoque | Horas efectivas de desarrollo | **Story Points estimados (referencia)** |
|---|---|---|
| Conservador (40%) | 22,4 - 25,6 horas | **13 - 16 SP** |
| Moderado (50%) | 28 - 32 horas | **16 - 21 SP** |

**Recomendación para Sprint 1:** **16 Story Points**. Esta estimación busca asegurar un incremento entregable y tangible, priorizando la calidad sobre la cantidad.

> *Nota:* Esta capacidad se revisará en la Retrospectiva del Sprint 1 para establecer la velocidad base del equipo para Sprints posteriores.

## 2. Sprint Goal

**Sprint Goal acordado:** *"Al finalizar el Sprint 1, un usuario visitante podrá consultar la cobertura, capturar y validar las características de un inmueble y obtener una estimación idempotente (rango de precios en MXN) con su explicación y metadatos, de forma que reciba un valor orientativo tangible y trazable, sin necesidad de registrarse."*

### Por qué es:
- **Concreto:** Define claramente el flujo funcional a completar (cobertura → captura → validación → estimación).
- **Medible:** Se considera alcanzado cuando HU-01, HU-02, HU-03 y HU-04 cumplen todos sus Criterios de Aceptación.
- **Alcanzable:** Totaliza 21 SP, ligeramente por encima del límite conservador (16 SP), pero viable si se enfoca el alcance únicamente a estas historias y se mitiga la complejidad con tareas bien acotadas.
- **Relevante:** Entrega el núcleo de valor del producto (primer incremento vertical de extremo a extremo).
- **Tiempo limitado:** 2 semanas.

## 3. Historias de Usuario Seleccionadas

| ID | Título | Story Points | Criterios de Aceptación clave |
|---|---|---|---|
| **HU-01** | Consultar cobertura y elegibilidad | 5 | 1. Catálogo devuelve únicamente elementos activos (sin autenticación). 2. Combinación elegible → `elegible: true`. 3. Fuera de cobertura → `422 ZONA_FUERA_DE_COBERTURA`. 4. Colonia ambigua → `409 COLONIA_AMBIGUA` con opciones. |
| **HU-02** | Capturar las características del inmueble | 8 | 1. Formulario guiado con campos según RD-01 y unidades correctas (m², años). 2. Obligatorios/Opcionales claramente identificados. 3. Ayuda por campo sin alterar valores. 4. Accesible (teclado, AA, objetivo táctil ≥ 48x48 px, sin scroll horizontal). |
| **HU-03** | Validar y corregir los datos capturados | 8 | 1. Errores de formato/rango → `422 CAMPO_FUERA_DE_RANGO` preservando valores válidos. 2. Inconsistencia ubicación o superficies aceptadas según reglas. 3. Valores ambiguos → `VALOR_AMBIGUO` o `CONFIRMACION_INVALIDADA`. 4. Faltantes obligatorios → listado completo; opcionales no inventados. |
| **HU-04** | Calcular una estimación idempotente | 8 | 1. Solicitud válida con `Idempotency-Key` → `201 Created`, rango mínimo/central/máximo en MXN ordenados, con margen, confianza y explicación. 2. Reenvío con misma clave → mismo `estimacionId`, sin duplicado ni consumo extra. 3. Salida inválida → `422 RESULTADO_NO_PUBLICABLE`. 4. Entradas idénticas → resultados idénticos (sin reentrenamiento). |

**Total seleccionado:** **21 Story Points**

## 4. Justificación de la Selección

La selección se fundamenta en entregar el **primer incremento vertical de extremo a extremo** que genera valor tangible para el usuario, cumpliendo con el Sprint Goal planteado.

- **HU-01 (5 SP): Base de confianza y control de alcance.** Garantiza que solo se opere dentro de cobertura activa, evitando invocar el modelo en zonas no habilitadas. Protege costes, asegura trazabilidad (RD-01, RNF-18) y reduce errores tempranos.
- **HU-02 (8 SP): Captura de calidad.** Proporciona un formulario guiado, claro y accesible (RNF-06–RNF-09). Esencial para asegurar entradas completas y de calidad, minimizando rechazos posteriores y mejorando la experiencia desde el primer uso.
- **HU-03 (8 SP): Puerta de calidad obligatoria.** Actúa como barrera de entrada al cálculo. Su enfoque en validación única, preservación de datos válidos y gestión de ambigüedad evita estimaciones incorrectas y reduce retrabajo. Representa una de las áreas con mayor densidad de reglas del backlog.
- **HU-04 (8 SP): Entrega del valor principal.** Cierra el flujo con una estimación idempotente, trazable y publicable. Garantiza no duplicidad de operaciones, valida la salida del motor y proporciona los tres importes, moneda, margen, confianza y explicación requeridos. Es el resultado tangible que justifica todo el flujo anterior.

**Conclusión:** Este conjunto cubre **EP-01 completo (21 SP)** y el primer hito crítico de **EP-02 (HU-04)**. Aunque supera ligeramente la estimación más conservadora (16 SP), se considera **alcanzable** para un primer Sprint, siempre que el equipo mantenga un **foco estricto** en estas 4 historias, gestione las dependencias (especialmente aspectos de políticas y datos habilitados que se irán afianzando) y no incorpore alcance adicional.

> **Nota:** Los **5 SP de diferencia** entre la capacidad conservadora (16 SP) y los **21 SP seleccionados** se consideran **imprevistos**. Dependiendo de cómo avance el Sprint 1 (descubrimientos, curva de aprendizaje, integración con el motor o resolución de dependencias), este margen podría **ir al alza**. Durante las Daily y, especialmente, a mitad del Sprint, el equipo deberá revisar este riesgo y, de ser necesario, ajustar el alcance o negociar con el PO.