# Definition of Done (DoD) - Sprint 1

## Propósito y alcance

Esta DoD define, de forma inequívoca, cuándo una Historia de Usuario del Sprint 1 puede considerarse terminada. Es **una única DoD a nivel de proyecto**, no una por historia. Esto es deliberado: en un equipo de un solo desarrollador, mantener una DoD por historia genera inconsistencias sin ganar precisión.

**Regla de oro:** una HU está terminada cuando un desarrollador externo —el Producto o un revisor sin contexto previo— puede ejecutarla en el entorno siguiendo únicamente el código y la documentación del repositorio, y obtener el resultado esperado.

### Contexto que condiciona esta DoD

| Realidad del proyecto | Impacto en la DoD |
|---|---|
| Desarrollador individual (estudiante) | No hay revisión por pares obligatoria ni separación de roles. Se sustituye por **revisión personal con lista de verificación** y una **sesión de demo en la Retrospectiva**. |
| Sin pipeline de CI/CD | Los controles de calidad se ejecutan **localmente antes de integrar**. Si un comando falla, la HU no se cierra. |
| Sprint de 2 semanas | La DoD debe ser cumplible en el tiempo asignado. Todo lo que exija infraestructura no disponible se difiere de forma explícita (sección 6). |
| Producto de estimación immobiliaria | Un error no es cosmético: publicar un precio incorrecto o exponer datos personales es un fallo grave. La DoD prioriza **corrección y trazabilidad** sobre velocidad. |

---

## 1. Criterios Técnicos y de Código

### 1.1 Limpieza y alcance

- [ ] El código implementado corresponde **exclusivamente** al alcance de la HU y de sus tareas/sub-issues. No se introducen refactorizaciones de código ajeno ni funcionalidades noificadas.
- [ ] No existe código muerto: ni funciones, variables, imports, rutas, controladores ni feature flags sin uso. Todo lo escrito se ejecuta o se elimina.
- [ ] No hay código comentado (`// código viejo`, `/* deshabilitado */`, `console.log` de depuración, `print` de depuración, `System.out.println`). El historial de Git ya registra lo que se eliminó.
- [ ] El linter y el formateador del proyecto pasan **sin errores ni advertencias** en los archivos tocados.

> **Comando de referencia:** el equivalente local de `npm run lint` / `ruff check .` / `flake8` / `golangci-lint`. Si el proyecto aún no tiene linter configurado, configurar uno es parte del Sprint 1 (ver sección 6, D-6).

### 1.2 Seguridad

- [ ] **Cero credenciales en el repositorio.** Sin claves, tokens, contraseñas, cadenas de conexión ni archivos `.env` versionados.
- [ ] Las variables sensibles viven en un archivo `.env.example` **solo con los nombres de las variables**, nunca con valores.
- [ ] `.gitignore` incluye `.env`, `node_modules/`, artefactos de build y archivos de base de datos locales.
- [ ] Si se manejan contraseñas o sesión: hash con algoritmo aprobado (Argon2id o bcrypt), nunca texto plano ni cifrado reversible sin llave.
- [ ] Ningún dato sensible (contraseñas, tokens, coordenadas exactas, datos del propietario) aparece en logs.

### 1.3 Reglas de negocio y contratos

- [ ] Cada regla de negocio de la HU tiene **correspondencia explícita** con su criterio de aceptación y con el requisito del SRS (RF/RD/RNF) trazado en el backlog.
- [ ] Los códigos de respuesta HTTP y de negocio (por ejemplo `ZONA_FUERA_DE_COBERTURA`, `COLONIA_AMBIGUA`, `CAMPO_FUERA_DE_RANGO`, `VALOR_AMBIGUO`, `RESULTADO_NO_PUBLICABLE`) se implementan **exactamente** como los define el backlog. No se improvisan nombres alternativos ni se simplifican a un `400` genérico.
- [ ] **Propagación del vacío:** ante un dato ausente, el sistema se abstain o propaga el vacío. Nunca imputa, interpola ni inventa un valor por defecto. Ningún campo opcional ausente se convierte en valor predeterminado.
- [ ] Si la HU expone un contrato de API, la especificación (OpenAPI o equivalente) está actualizada en el mismo commit que el código.

### 1.4 Accesibilidad e internacionalización (aplicable)

- [ ] Los campos de formulario tienen etiqueta asociada y no dependen solo del color ni del placeholder para identificarse.
- [ ] Navegación por teclado completa en los flujos nuevos; foco visible.
- [ ] Contraste mínimo AA y objetivos táctiles de al menos 48 × 48 px en componentes interactivos.
- [ ] Sin desplazamiento horizontal en los anchos definidos en RNF-09.
- [ ] Las unidades se muestran explícitas (`m²`, años, MXN) y los importes en el formato de moneda esperado.

---

## 2. Pruebas y Validación

### 2.1 Criterios de aceptación

- [ ] **Todos** los criterios de aceptación de la HU están implementados y verificados uno por uno. Ningún CA queda "parcialmente" cumplido.
- [ ] Cada criterio de aceptación tiene **evidencia de verificación**: o bien una prueba automatizada que lo cubre, o bien una captura, salida de terminal o registro en el body del issue que lo demuestra.
- [ ] Los **casos negativos** están cubiertos con la misma rigurosidad que los positivos: combinaciones no habilitadas, formatos inválidos, campos faltantes, valores ambiguos y ubicaciones inconsistentes.
- [ ] Los casos de la matriz de dispositivos (RNF-09) aplicables se verificaron en al menos un navegador de escritorio y uno móvil. La validación exhaustiva queda para el Sprint Review, no bloquea el cierre de la HU.

### 2.2 Pruebas automatizadas

- [ ] Existe al menos una prueba automatizada por criterio de aceptación crítico (los que devuelven un `4xx` o un `201`).
- [ ] Las pruebas de la HU se ejecutan **todas en verde** en la máquina de desarrollo, sobre el estado más reciente de la rama.
- [ ] No hay pruebas saltadas con `.skip`, `.only`, `xit` o comentarios tipo "TODO:_arreglar". Una prueba deshabilitada es una HU incompleta.
- [ ] Las pruebas no dependen de datos de producción, de la red externa, ni del orden de ejecución entre sí.
- [ ] **Umbral de cobertura** para los módulos críticos de la HU —validación de entrada, elegibilidad, idempotencia, validación de salida del motor—: **≥ 80 % de cobertura de líneas**, conforme a RNF-17. Los módulos de soporte se cubren con lo que absorban los CA.
- [ ] Las pruebasasingladuras de la HU no rompen pruebas preexistentes: la suite completa está en verde.

### 2.3 Comprobación manual documentada

Cuando la automatización no sea viable —comprobaciones manuales de la matriz de dispositivos, validación visual, pruebas de compartición en dispositivo real (HU-15)—:

- [ ] Se documenta la lista exacta de pasos reproducidos en el cuerpo del issue o en un `QA_CHANGELOG.md`.
- [ ] El resultado observado queda registrado con fecha y, si aplica, captura.
- [ ] La validación queda marcada como **manual** de forma explícita para que el Sprint Review sepa que no hay cobertura automatizada.

> **Pragmatismo:** en el Sprint 1 no se exige cobertura de pruebas end-to-end automatizadas (Playwright, Cypress). Se acepta la validación manual documentada. La automatización de E2E es una meta del Sprint 3 o posterior.

---

## 3. Control de Versiones y Git

- [ ] El trabajo se desarrolló en una **rama de característica** con nombre descriptivo:
  - `feat/hu-01-cobertura-elegibilidad`
  - `feat/hu-02-captura-inmueble`
  - `feat/hu-03-validacion-datos`
  - `feat/hu-04-estimacion-idempotente`
- [ ] El mensaje de cada commit sigue **Conventional Commits** y explica el *porqué*, no el *qué*:
  - `feat(validacion): agrega VALOR_AMBIGUO para valores atípicos`
  - `fix(elegibilidad): evitaicolon ambigua cuando el CP tiene una sola colonia`
- [ ] El `merge` a `main` se hizo con **fast-forward deshabilitado: siempre hay un commit de merge explícito, o se usa *squash* con un mensaje que referencie la HU (`feat: HU-01 - ... (#1)`).
- [ ] `main` queda **funcional en todo momento**: cada commit integrado compila y pasa sus pruebas. Nada de "subir todo al final y arreglar".
- [ ] El issue de la HU se cierra **automáticamente** al hacer el merge, mediante `Closes #N` en el mensaje del commit.
- [ ] Los sub-issues completados se cierran individualmente; el padre se cierra solo cuando **todos** sus sub-issues estén cerrados.
- [ ] No hay conflictos de merge sin resolver ni archivos marcados como `<<<<<<<` en el árbol de trabajo.
- [ ] `git status` reporta un árbol de trabajo limpio antes de cerrar la HU.

---

## 4. Despliegue y Estado del Entorno

- [ ] La funcionalidad **se ejecuta de extremo a extremo** en el entorno local: la ruta completa desde el punto de entrada hasta la respuesta esperada, sin pasos manuales intermedios no documentados.
- [ ] Si la HU toca base de datos: la migración se aplicó limpia desde cero sobre una base vacía, y también se verificó sobre una base con datos existentes. La migración es reversible o, en su defecto, su irreversibilidad está justificada por escrito en el issue.
- [ ] Si hay despliegue —Vercel, Render, Supabase u otro—: el build de producción termina **sin errores** y la funcionalidad es verificable en la URL desplegada, no solo en local.
- [ ] Las variables de entorno nuevas están definidas en el entorno de despliegue, con los mismos nombres que en `.env.example`.
- [ ] Se verificó el comportamiento ante **fallo del servicio de inferencia**: la HU no se rompe si el motor no responde; aplica directamente a HU-04 y a las historias de EP-02.
- [ ] El **estado final es reproducible**: otra persona, siguiendo el README, puede levantar el entorno y reproducir la funcionalidad sin pedir ayuda.

### Manejo de incidencias descubiertas durante el Sprint

> Si durante el desarrollo aparece un defecto fuera del alcance de la HU, **no se corrige en la rama de la HU**. Se documenta y se registra como issue independiente para el Product Backlog. Esto evita inflar el alcance y falsear la medición de velocidad.

---

## 5. Checklist de Verificación para cada HU

Lista rápida para revisar antes de cerrar un issue. Todas deben marcarse.

### Código

- [ ] Alcance limitado a la HU, sin código muerto ni comentado
- [ ] Linter y formateador sin errores ni advertencias
- [ ] Sin credenciales ni datos sensibles en el código, logs o repositorio
- [ ] `.gitignore` cubre `.env`, dependencias y artefactos
- [ ] Reglas de negocio implementadas con los códigos exactos del backlog
- [ ] Sin valores predeterminados inventados; propagación del vacío respetada

### Pruebas

- [ ] Todos los criterios de aceptación implementados y verificados
- [ ] Casos negativos cubiertos
- [ ] Pruebas automatizadas en verde, sin `.skip` ni `.only`
- [ ] Módulos críticos con ≥ 80 % de cobertura de líneas
- [ ] Suite completa en verde (no se rompió nada previo)
- [ ] Evidencia de verificación registrada en el issue

### Git

- [ ] Trabajado en rama `feat/hu-0X-...`
- [ ] Commits con Conventional Commits
- [ ] Merge a `main` limpio, con `Closes #N`
- [ ] `main` funcional tras el merge
- [ ] Árbol de trabajo limpio (`git status` sin cambios pendientes)

### Entorno

- [ ] Funciona de extremo a extremo en local
- [ ] Migraciones aplicadas desde base vacía (si aplica)
- [ ] Build de producción sin errores y funcionalidad verificada en el despliegue (si aplica)
- [ ] Variables de entorno nuevas definidas en el despliegue
- [ ] Comportamiento ante fallo del motor verificado (EP-02)

### Documentación y cierre

- [ ] README actualizado si la función requiere pasos nuevos de uso o configuración
- [ ] Contrato de API actualizado si la HU expone endpoints (OpenAPI)
- [ ] Comentarios solo donde explican *por qué*, no *qué*
- [ ] Sub-issues cerrados
- [ ] Demostrado en el Sprint Review o en la Retrospectiva
- [ ] Definición de Terminado global (backlog, sección 5) revisada para los puntos aplicables

---

## 6. Elementos diferidos (no exigibles en el Sprint 1)

La Definición de Terminado global del backlog (sección 5) incluye 12 condiciones de infraestructura y operación que **no son verificables en el Sprint 1** con un desarrollador individual y sin CI/CD. Se documentan aquí con su fecha objetivo para evitar que se pierdan, pero **no bloquean el cierre de ninguna HU de este Sprint**.

| ID | Elemento | Por qué se difiere | Objetivo |
|---|---|---|---|
| D-1 | Rendimiento p95 ≤ 3 s (RNF-01) | Requiere entorno de pruebas con carga representativa. No hay volumetría definida (P-07). | Sprint 3 |
| D-2 | Escalabilidad: 200 inferencias concurrentes, < 1 % de errores (RNF-02) | Requiere infraestructura de carga. Inviable en local. | Sprint 4 |
| D-3 | Disponibilidad y volumetría (RNF-03, P-07) | Requiere monitoreo y despliegue estable. | Sprint 4 |
| D-4 | Usabilidad: p90 ≤ 120 s con 5 usuarios de campo | Requiere 5 usuarios externos. En el Sprint 1 se sustituye por autoevaluación + 2 artefactos de prueba con el PO. | Sprint 3 |
| D-5 | Aislamiento de datos anónimos y retención (RNF-12, RNF-14) | Aplica a HU-09 y EP-04, fuera del alcance del Sprint 1. | Cuando se aborden EP-03 y EP-04 |
| D-6 | Linter, formateador y suite de pruebas configurados en CI | No hay CI. **Sí se exige en el Sprint 1**: configurar linter y formateador localmente es parte del Sprint 1. | Sprint 1 (local) / Sprint 3 (CI) |
| D-7 | Extensibilidad por configuración de cobertura (RNF-18) | Se cubre de forma opportunista: el catálogo de HU-01 se modela con tabla de datos, no hardcodeado. Verificación formal diferida. | Sprint 3 |
| D-8 | Operación del modelo: reentrenamiento trimestral y deriva (RNF-05, RNF-19) | Aplica a EP-02 y a HUs de datos habilitados (HU-06). Fuera del alcance del Sprint 1. | Sprint 4 |
| D-9 | Cobertura de pruebas end-to-end automatizadas | No hay base de pruebas E2E. Se acepta validación manual documentada en el Sprint 1. | Sprint 3 |
| D-10 | Cifrado en reposo y TLS 1.3 en despliegue | Depende de la plataforma de despliegue definitiva y de proveedor de base de datos. | Al elegir infraestructura |

> **Regla de los diferidos:** diferir no es aceptar que el requisito desaparece. Cada elemento D-* tiene un objetivo y debe verificarse antes del cierre del Sprint donde figure. Si un elemento diferido bloquea la salida a producción, se escala al PO.

---

## 7. Cómo se aplica esta DoD en las ceremonias

### Durante el Sprint

- **Task Board Daily (10 min):** revisar las casillas de la sección 5 de la HU en curso. No se invierten más de 10 minutos en la Daily.
- **A mitad de Sprint (día 5):** aplicar una revisión anticipada de la DoD completa a la HU más avanzada. Es el momento para detectar bloqueos (por ejemplo, la migración de base de datos no aplica desde cero) y recortar alcance con tiempo de sobra.
- **Cierre de sub-issue:** un sub-issue se cierra cuando cumple **sus propios** Criterios de Done. El sub-issue es la unidad de trabajo diario.

### En el Sprint Review

- [ ] Cada HU se demuestra **funcionando**, no descrita. La demo es el acto de verificación.
- [ ] Se verifican los elementos aplicables de la Definición de Terminado global del backlog (sección 5).
- [ ] Las comprobaciones manuales se ejecutan en vivo cuando sea posible.
- [ ] Se registra en el issue qué elementos D-* quedaron pendientes y por qué.

### En la Retrospectiva

- [ ] Se revisa si la DoD resultó demasiado pesada o demasiado ligera. En el Sprint 1 se espera que se ajuste: la DoD es un artefacto vivo.
- [ ] Los elementos D-* se reevalúan y se actualizan sus fechas objetivo.

---

## Qué **NO** significa "terminado"

Para evitar malentendidos, una HU **no** está terminada si:

- ❌ El código funciona en la máquina del desarrollador pero no se ha integratedo a `main`.
- ❌ Los criterios de aceptación pasan "a mano" pero no hay evidencia registrada.
- ❌ Quedan pruebas saltadas, commented-out o pendientes de arreglar.
- ❌ La funcionalidad depende de un dato hardcodeado, de una clave en un archivo local o de un script que nadie documentó.
- ❌ Se entregó la parte fácil y la parte difícil quedó en un `TODO`.
- ❌ El issue se cerró porque se acabó el tiempo del Sprint.

> **Frase de control:** *terminado no es "ya no lo estoy tocando"; es "otra persona puede ejecutarlo y funciona".*