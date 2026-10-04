# Desglose técnico de historias - Sprint 1

Basado en la planificación del Sprint 1 (sprint1_planning.md). Las tareas se han descompuesto considerando granularidad ≤ 4h, rol asignado, criterio de Done verificable y formato checklist para GitHub Projects.

## Resumen

| Historia | SP | Tareas | Horas totales estimadas |
|---|---|---|---|
| HU-01 - Consultar cobertura y elegibilidad | 5 | 6 | 10h |
| HU-02 - Capturar las características del inmueble | 8 | 6 | 12h |
| HU-03 - Validar y corregir los datos capturados | 8 | 6 | 12h |
| HU-04 - Calcular una estimación idempotente | 8 | 6 | 12h |

**Total:** 29 tareas | **46 horas estimadas**

---

## HU-01: Consultar cobertura y elegibilidad

**Puntos de Historia:** 5  
**Estimación total de tareas:** 10h  

### Tareas Técnicas

- [ ] **[Backend Dev]** Modelado y migración del catálogo de cobertura (`Estimación: 2h`)
  - **Criterio de Done:** Entidades/modelos para Estado, Municipio, Colonia, TipoInmueble, UsoSuelo creados. Migraciones aplicables. Datos de catálogo versionados con flag `activo`. Seeds para datos activos/inactivos validados.
  - **Dependencias:** Ninguna

- [ ] **[Backend Dev]** Endpoint GET /catalogo/cobertura (solo elementos activos) (`Estimación: 1h`)
  - **Criterio de Done:** Respuesta 200 con jerarquía correcta, filtrando únicamente registros `activo=true`. Sin autenticación requerida. Estructura acorde a CA1 HU-01.
  - **Dependencias:** Tarea 1

- [ ] **[Backend Dev]** Servicio de verificación de elegibilidad (`Estimación: 2h`)
  - **Criterio de Done:** Lógica que determina elegibilidad por combinación (ubicación, tipo, uso). Retorna `elegible: true/false`. No invoca modelo cuando no elegible. Contador de inferencia se mantiene en 0 en caso elegible.
  - **Dependencias:** Tarea 1

- [ ] **[Backend Dev]** Reglas para colonia ambigua y zona fuera de cobertura (`Estimación: 1h`)
  - **Criterio de Done:** Para combinación no habilitada/inconsistente → 422 `ZONA_FUERA_DE_COBERTURA` con descripción. Para CP con múltiples colonias sin selección → 409 `COLONIA_AMBIGUA` con listado de opciones. No habilita captura ni invoca modelo.
  - **Dependencias:** Tarea 3

- [ ] **[Frontend Dev]** Componente de selector de cobertura (estado/municipio/colonia/tipo/uso) (`Estimación: 2h`)
  - **Criterio de Done:** Carga catálogo activo sin auth. Maneja selección jerárquica. Muestra opciones de colonia ambigua cuando aplica. Deshabilita siguiente paso hasta combinación válida.
  - **Dependencias:** Tarea 2

- [ ] **[QA / Tester]** Pruebas de cobertura y elegibilidad (`Estimación: 2h`)
  - **Criterio de Done:** Casos cubiertos: catálogo solo activos, elegible true, 422 zona fuera, 409 colonia ambigua. Tests automatizados pasan. Evidencia registrada.
  - **Dependencias:** Tareas 2,4,5

---

## HU-02: Capturar las características del inmueble

**Puntos de Historia:** 8  
**Estimación total de tareas:** 12h  

### Tareas Técnicas

- [ ] **[UI/UX]** Diseño de formulario guiado según RD-01 (`Estimación: 1h`)
  - **Criterio de Done:** Wireframe/mock con campos obligatorios/opcionales, unidades (m², años), ayudas por campo. Validado contra matriz de dispositivos (RNF-09).
  - **Dependencias:** Ninguna

- [ ] **[Frontend Dev]** Estructura de formulario y validación cliente inicial (`Estimación: 2h`)
  - **Criterio de Done:** Formulario renderiza campos definidos por RD-01. Indicadores "Obligatorio"/"Opcional". Unidades aplicadas. Ayuda contextual accesible. Sin valores predeterminados en opcionales.
  - **Dependencias:** Tarea 1

- [ ] **[Frontend Dev]** Accesibilidad (teclado, AA, 48x48px, sin scroll horizontal) (`Estimación: 2h`)
  - **Criterio de Done:** Etiquetas asociadas a inputs, foco visible, navegación teclado completa, contraste AA, objetivos táctiles ≥48x48px, responsive sin scroll horizontal en anchos definidos (RNF-09).
  - **Dependencias:** Tarea 2

- [ ] **[Backend Dev]** Esquemas de validación de características (`Estimación: 2h`)
  - **Criterio de Done:** Esquemas validan tipos, rangos, catálogos. Superficies en m². Antigüedad en años. Ubicación/tipo/uso/conservación restringidos a dominios autorizados. Opcionales ausentes no forzados.
  - **Dependencias:** Ninguna

- [ ] **[Frontend Dev]** Integración con flujo de elegibilidad (solo si elegible) (`Estimación: 2h`)
  - **Criterio de Done:** Formulario solo habilitado tras elegibilidad true (HU-01). Estado persiste durante sesión activa. No envía cálculo hasta validaciones pasen.
  - **Dependencias:** HU-01 (Tareas 3,5), Tarea 2

- [ ] **[QA / Tester]** Verificación de captura y accesibilidad (`Estimación: 3h`)
  - **Criterio de Done:** Checklist accesibilidad (WCAG 2.1 AA) cubierto. Pruebas en matriz navegadores/dispositivos relevantes. Verificación unidades, ayudas, sin defaults. Todo OK.
  - **Dependencias:** Tareas 3,4,5

---

## HU-03: Validar y corregir los datos capturados

**Puntos de Historia:** 8  
**Estimación total de tareas:** 12h  

### Tareas Técnicas

- [ ] **[Backend Dev]** Validador unificado con respuesta 422 estructurada (`Estimación: 2h`)
  - **Criterio de Done:** Respuesta 422 con códigos `CAMPO_FUERA_DE_RANGO`, `CAMPOS_OBLIGATORIOS_FALTANTES` según caso. Identifica campos y reglas. Preserva valores válidos. No invoca modelo.
  - **Dependencias:** HU-02 Tarea 4

- [ ] **[Backend Dev]** Reglas de coherencia de ubicación y superficies (`Estimación: 2h`)
  - **Criterio de Done:** Municipio/colonia deben corresponder. Construcción > terreno aceptado si ambas válidas. Validaciones aplicadas antes de cálculo.
  - **Dependencias:** Tarea 1

- [ ] **[Backend Dev]** Gestión de valores ambiguos y confirmación (`Estimación: 2h`)
  - **Criterio de Done:** Valor plausible pero atípico → `VALOR_AMBIGUO` requiriendo corrección/confirmación. Cambio de valor/zona/política invalida confirmación → `CONFIRMACION_INVALIDADA` solicita nueva confirmación.
  - **Dependencias:** Tarea 1

- [ ] **[Backend Dev]** Detección de faltantes obligatorios/opcionales (`Estimación: 1h`)
  - **Criterio de Done:** Si faltan obligatorios → lista completa. Si solo opcionales faltan → flujo continúa sin inventar valores. Alineado a RD-01.
  - **Dependencias:** Tarea 1

- [ ] **[Frontend Dev]** UI para mostrar errores/ambigüedad y preservar datos (`Estimación: 2h`)
  - **Criterio de Done:** Muestra errores por campo con regla clara. Preserva valores válidos al mostrar 422. Interfaz para confirmar valor ambiguo cuando aplica. No pierde datos capturados.
  - **Dependencias:** Tareas 1,3,4

- [ ] **[QA / Tester]** Pruebas de validación integral (`Estimación: 3h`)
  - **Criterio de Done:** Cobertura casos: fuera de rango, faltantes, incoherencia ubicación, superficies, ambiguo+confirmación, invalidación de confirmación. Todos verificables. Evidencia en tests.
  - **Dependencias:** Tareas 2,3,4,5

---

## HU-04: Calcular una estimación idempotente

**Puntos de Historia:** 8  
**Estimación total de tareas:** 12h  

### Tareas Técnicas

- [ ] **[Backend Dev]** Esquema y contrato de solicitud de estimación (`Estimación: 1h`)
  - **Criterio de Done:** Request valida entrada completa+válida tras HU-03. Requiere `Idempotency-Key` (header). Campos alineados con contrato de motor.
  - **Dependencias:** HU-03 completo

- [ ] **[Backend Dev]** Implementación de idempotencia (`Estimación: 2h`)
  - **Criterio de Done:** Mismo `Idempotency-Key` + misma solicitud → retorna mismo `estimacionId` sin crear nuevo resultado ni consumir cuota. Almacenamiento de clave+hash de request+resultado.
  - **Dependencias:** Tarea 1

- [ ] **[Backend Dev]** Integración con motor de inferencia (con aislamiento) (`Estimación: 2h`)
  - **Criterio de Done:** Solo invoca motor si elegible + válido + datos habilitados. Timeout/transporte considerado. No invoca si ya existe respuesta idempotente.
  - **Dependencias:** HU-01, HU-03, Tarea 2

- [ ] **[Backend Dev]** Validación de salida del motor (`Estimación: 2h`)
  - **Criterio de Done:** Valida min/central/max positivos y ordenados, moneda MXN, margen, confianza (baja/media/alta), explicación. Si inválido → 422 `RESULTADO_NO_PUBLICABLE`. No publica precio ni habilita PDF.
  - **Dependencias:** Tarea 3

- [ ] **[Backend Dev]** Cálculo de metadatos (PX/m², fechas, versiones) (`Estimación: 2h`)
  - **Criterio de Done:** PX/m² sobre superficie construida, redondeo a 2 decimales con empate hacia arriba. Fechas AAAA-MM-DD (cálculo y actualización datos). Versiones modelo/datos/política incluidas. Misma entrada → mismos valores.
  - **Dependencias:** Tarea 4

- [ ] **[QA / Tester]** Pruebas de estimación e idempotencia (`Estimación: 3h`)
  - **Criterio de Done:** Casos: 201 con metadatos correctos, reenvío idempotente (mismo id), salida inválida → 422, determinismo (entradas idénticas). Tests automatizados. Evidencia registrada.
  - **Dependencias:** Tareas 2,3,4,5

---

## Definición global aplicada a tareas

- **Tamaño:** ≤ 4h por tarea (granularidad para seguimiento diario).
- **Rol claro:** Cada tarea tiene rol asignado para reparto equitativo.
- **DoD verificable:** Criterio objetivo (códigos HTTP, validaciones, accesibilidad, determinismo).
- **Trazable:** Referencia a HU/CA, RNF relevantes cuando aplica.
- **Sin valores inventados:** Coherente con principio "sin valores predeterminados" y "no invoca modelo" cuando no aplicable.

**Fecha de generación:** 2025-10-03  
**Origen:** sprint1_planning.md + backlog_completo.md