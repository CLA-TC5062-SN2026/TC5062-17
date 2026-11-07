# Decisión final del stack tecnológico del frontend — MLState

| Campo | Valor |
|---|---|
| Documento | Decisión de stack del frontend |
| Fase | S07–S08, actividad 1 |
| Fecha | 2026-11-05 |
| Estado | Ratificado por unanimidad |

## 1. Stack elegido

| Capa | Decisión |
|---|---|
| Framework / librería de UI | **Vue 3** con Composition API y `<script setup>` |
| Herramienta de construcción / servidor de desarrollo | **Vite** mediante `create-vue` |
| Enfoque de estilos | **Bootstrap 5 como base CSS + tema SCSS propio**, sin BootstrapVue |
| Manejo de estado | **Pinia** para estado global; estado local de Vue para formularios |
| Ruteo | **Vue Router 4** |
| Cliente HTTP | `fetch` encapsulado en un módulo de servicios con manejo centralizado de autenticación y errores |
| Pruebas | **Vitest + Vue Test Utils** para unidades y componentes; **Playwright** para flujos críticos |
| Empaquetado | Rutas con carga diferida (`() => import(...)`) para reducir el bundle inicial |

**PWA:** no se implementa en el MVP. El SRS no exige funcionamiento offline ni instalación; un service worker añadiría caché y complejidad de invalidación sin requisito que lo respalde.

### 1.1 Responsabilidad de cada pieza

- **Vue 3** organiza la interfaz en componentes de archivo único, adecuados para dividir el formulario multipaso, el resultado y el historial.
- **Vite** provee el servidor de desarrollo, la recarga instantánea y la división de código.
- **Vue Router 4** define las rutas de captura, resultado, historial, login y registro, y permite proteger rutas autenticadas.
- **Bootstrap 5 + SCSS** aporta grillas, formularios y utilidades responsivas; el tema propio corrige contraste, foco y tamaños táctiles.
- **Pinia** concentra sesión, catálogo, borrador e historial; los campos individuales del formulario permanecen en estado local.
- **Cliente HTTP encapsulado** añade `Authorization`, `Idempotency-Key`, manejo de `401`, errores de negocio y cancelación por timeout.

## 2. Alternativas consideradas y por qué se descartaron

### 2.1 Propuestas de los integrantes

| Integrante | UI | Build | Estilos | Estado | Argumento principal |
|---|---|---|---|---|---|
| **Chris** | Vue 3 | Vite | Bootstrap 5 | Pinia | Ya domina el stack; minimiza el riesgo de aprendizaje. |
| **Anuar** | Vue 3 | Vite | Tailwind CSS | Pinia | Mejor control explícito de accesibilidad y diseño responsivo. |

### 2.2 Alternativas descartadas

| Alternativa | Motivo del descarte |
|---|---|
| **Next.js** | No hay requisito de SSR ni SEO. La API ya es un backend independiente; añadir un servidor de renderizado incrementa la complejidad operativa sin beneficio para una SPA privada. |
| **Angular** | Curva de aprendizaje y peso desproporcionados para un equipo de cuatro personas y cuatro meses. |
| **Svelte / SvelteKit** | Menor ecosistema y nulo conocimiento previo del equipo. |
| **JavaScript vanilla** | Obliga a construir ruteo, estado, validación y accesibilidad a mano; el coste supera al de un framework. |
| **React + Zustand** | Técnicamente viable, pero el equipo tendría que aprender React y su modelo de estado en paralelo al desarrollo. El mayor riesgo no es el ecosistema, sino la curva de aprendizaje. |
| **Tailwind CSS** | Ofrece mejor control de accesibilidad, pero añade una curva de aprendizaje para el integrante con experiencia y para el resto del equipo. Queda como alternativa si Bootstrap no supera la auditoría de RNF-07/08. |
| **BootstrapVue** | Está orientado a Vue 2. Para Vue 3 se usa Bootstrap solo como capa CSS y los componentes interactivos se implementan en Vue. |

### 2.3 Comparaciones que definieron la decisión

- **Vue frente a React:** Chris y Anuar señalaron que la única experiencia real del equipo es Vue y que el plazo no admite aprender un framework nuevo mientras se implementan 25 requisitos funcionales. La mención “React” de la arquitectura era una línea de un entregable anterior, no una decisión ratificada. **Se elige Vue 3.**
- **Bootstrap frente a Tailwind:** Chris defendió Bootstrap por velocidad y familiaridad. Anuar objetó que los estilos por defecto no garantizan RNF-07/08 y que los plugins JavaScript de Bootstrap se integran con fricción en Vue 3. **Se elige Bootstrap 5 solo como base CSS**, con tema SCSS propio y componentes interactivos en Vue. Si la auditoría de accesibilidad falla, se migra la capa de estilos a Tailwind sin cambiar Vue, Router ni Pinia.
- **Estado:** Zustand, Redux y Context API pertenecen al ecosistema React. Pinia es la solución oficial para Vue 3, pequeña y compatible con Composition API. **Se elige Pinia** para estado global y estado local de Vue para formularios.

## 3. Justificación de la elección en términos del proyecto

### 3.1 Características del equipo

- El equipo tiene **un integrante con experiencia real en frontend** (Chris: Vue, Vite y Bootstrap) y tres integrantes cuyo fuerte es backend, base de datos y análisis.
- Elegir Vue 3 convierte esa experiencia en la referencia del equipo y evita que el proyecto dependa de aprender un framework nuevo bajo plazo.
- Bootstrap 5 reduce el tiempo de maquetación de formularios, grillas y utilidades responsivas, que son la mayor superficie de la interfaz.
- La combinación permite que el resto del equipo contribuya desde el primer sprint con componentes pequeños y pair programming, en lugar de concentrar todo el frontend en una persona.

### 3.2 Integración con el backend

- El backend es una **API REST/JSON** con prefijo `/api/v1`; cualquier cliente HTTP funciona. Vue no impone acoplamiento.
- La autenticación es **JWT tipo Bearer**, que se resuelve con un header `Authorization` en el cliente HTTP.
- Los errores de negocio vienen estructurados (`codigo`, `mensaje`, `traceId`, `errores`), lo que permite mapearlos a mensajes de interfaz sin lógica adivinada.
- El cálculo exige `Idempotency-Key`, que el cliente HTTP puede generar y reutilizar por intento.
- El PDF se obtiene como `application/pdf` y se descarga o comparte como blob; no requiere una librería de UI específica.
- El detalle completo está en la sección 4.

### 3.3 Complejidad del UI requerido

- **Formulario multipaso:** el flujo de RF-01 a RF-09 combina catálogo jerárquico, validación, confirmación de valores ambiguos, espera, timeout y reintento. Vue permite separar cada paso en componentes con estado local, sin arrastrar un estado global innecesario.
- **Resultado e historial:** RF-11 a RF-25 requieren presentación de rango, metadatos, explicación, comparables, filtros, borrado y PDF. Son vistas con componentes reutilizables y rutas protegidas.
- **Accesibilidad:** RNF-07/08 exigen teclado, etiquetas visibles, contraste AA y objetivos táctiles de 48 × 48 px. Vue permite encapsular patrones accesibles (foco, modales, ayudas) y Bootstrap aporta la base de formularios.
- **Rendimiento:** RNF-01 exige p95 ≤ 3 s. Vite con rutas diferidas y un bundle sin librerías de UI pesadas ayuda a cumplir el presupuesto de carga.
- **Privacidad:** RNF-14 prohíbe persistir respuestas de consulta en el navegador. Vue + Pinia permiten mantener el estado en memoria y limpiarlo al cerrar la consulta.

### 3.4 Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Los estilos por defecto de Bootstrap no cumplen AA o 48 × 48 px | Alto | Tema SCSS con paleta AA, `min-height`/`min-width` de 48 px, foco visible y checklist RNF-07/08 en cada historia. |
| Los plugins JS de Bootstrap chocan con la reactividad de Vue | Medio | Usar Bootstrap solo como CSS/utilities; modales, dropdowns y ayudas se implementan en Vue o con `<dialog>` nativo. |
| Peso del bundle por importar todo Bootstrap | Medio | Importar solo los módulos SCSS necesarios, rutas con carga diferida y revisión del bundle antes de la entrega. |
| Poca experiencia del resto del equipo en Vue 3 | Alto | Chris como referencia, pair programming y una guía mínima de convenciones. |
| Tailwind era mejor para accesibilidad | Medio | Reevaluar al cerrar el primer flujo completo; migrar estilos no obliga a cambiar Vue, Router ni Pinia. |

## 4. Integración con la arquitectura del backend

### 4.1 Contrato de la API

- Base de operaciones: `/api/v1`; contrato en `/api/v1/openapi.json` y documentación en `/docs`.
- Transporte: REST/JSON sobre HTTPS; el frontend no accede a PostgreSQL ni a Redis.
- La API es sin estado local: el frontend mantiene la sesión y el borrador, y envía identificadores (`borradorId`, `estimacionId`, `consultaId`) en cada operación.
- Configuración: `VITE_API_BASE_URL` define la URL base, `VITE_REQUEST_TIMEOUT_MS` el timeout de interfaz y `VITE_PROXY_TARGET` el destino del proxy de desarrollo. La plantilla está en `.env.example` y los valores por modo en `.env.development` y `.env.production`.

### 4.2 Autenticación JWT

- El login (`POST /api/v1/sesiones`, `POST /api/v1/auth/login`) devuelve `accessToken`/`token` y los datos del usuario (`backend/S05_S06_A1/app/main.py:504-538`).
- Las rutas protegidas aceptan `Authorization: Bearer <token>` (`backend/S05_S06_A1/app/dependencies.py:21-44`).
- El frontend guarda el token **solo en memoria** dentro de Pinia, nunca en `localStorage` ni `sessionStorage` (RNF-14), y lo inyecta mediante un interceptor del cliente HTTP.
- Un `401` limpia la sesión de Pinia y redirige a login mediante una guarda de Vue Router.
- **Brecha detectada:** RNF-10 exige que la sesión viaje en cookie `Secure`, `HttpOnly` y `SameSite`, pero el login actual devuelve el JWT en el cuerpo. Mientras el backend no se alinee, el frontend no debe persistir el token. La corrección corresponde al backend y no cambia la decisión del framework.

### 4.3 CORS y desarrollo local

- El backend actual **no registra `CORSMiddleware`**.
- En desarrollo se usará un **proxy de Vite** (`/api` → `http://127.0.0.1:8000`) para que el navegador vea un mismo origen y no haya preflight.
- En producción se usará mismo origen o `CORSMiddleware` con `allow_credentials=True` y una lista explícita de orígenes.
- Esta configuración es de infraestructura/backend; no condiciona el uso de Vue.

### 4.4 Idempotencia

- `POST /api/v1/estimaciones` exige la cabecera `Idempotency-Key`; sin ella responde `400 IDEMPOTENCY_KEY_REQUERIDA` y con una clave reutilizada con otro cuerpo responde `409 CLAVE_REUTILIZADA` (`backend/S05_S06_A1/app/main.py:324-343`).
- El frontend genera una clave por intento de cálculo, la conserva en memoria y la reutiliza al reintentar la misma solicitud, de modo que un reintento no duplique historial ni cuota (RF-07-AC-2).

### 4.5 Errores de negocio

- Los errores usan un cuerpo uniforme `{ codigo, mensaje, traceId, errores? }` (`backend/S05_S06_A1/app/errors.py:8-20`).
- El frontend mapea códigos como `ZONA_FUERA_DE_COBERTURA`, `COLONIA_AMBIGUA`, `VALOR_AMBIGUO`, `CONFIRMACION_INVALIDADA`, `MUESTRA_INSUFICIENTE_PARA_ESTIMAR`, `ERROR_EN_SERVICIO_DE_INFERENCIA` y `DATOS_NO_HABILITADOS` a mensajes y acciones concretas.
- Los `422` de validación se muestran por campo, conservando los valores ya capturados (RF-04, RF-06).

### 4.6 Consultas anónimas, cookies y PDF

- El backend crea una cookie `mlstate_anon_session` `HttpOnly`, `SameSite=Lax` y con expiración al crear borradores (`backend/S05_S06_A1/app/main.py:252-260`). El frontend no lee ni manipula esa cookie; solo usa `credentials: "include"` en el cliente HTTP.
- El reporte se solicita con `PUT /api/v1/estimaciones/{estimacionId}/reportes/principal` y se recibe como `application/pdf` con `Cache-Control: no-store` (`backend/S05_S06_A1/app/main.py:401-426`). El frontend lo trata como blob, lo descarga y puede compartirlo con Web Share API (RF-23, RF-25).
- Las respuestas con contenido de consulta no se almacenan en caché ni en almacenamiento persistente del navegador (RNF-14).

### 4.7 Resumen de acoplamiento

| Necesidad del frontend | Mecanismo del backend | Pieza del stack |
|---|---|---|
| Consumir catálogo y operaciones | REST/JSON bajo `/api/v1` | Servicio HTTP + Vue |
| Autenticar | JWT Bearer (hoy en cuerpo; objetivo: cookie `HttpOnly`) | Pinia + cliente HTTP + guardas de Router |
| Mantener sesión anónima | Cookie `mlstate_anon_session` | `credentials: "include"` |
| Evitar duplicados | `Idempotency-Key` | Cliente HTTP + estado local del intento |
| Mostrar errores | Cuerpo `{ codigo, mensaje, traceId, errores? }` | Componentes de error y validación |
| Descargar/compartir PDF | `PUT` con respuesta `application/pdf` | Blob + Web Share API |
| Cumplir rendimiento | API síncrona y contrato estable | Vite con rutas diferidas |
| Cumplir privacidad | `Cache-Control: no-store` y purga | Estado en memoria, sin persistencia |

## 5. Consecuencias y convenciones

- El proyecto vivirá en `frontend/S07_S08_A1/` con la estructura estándar de `create-vue`: `src/components`, `src/pages`, `src/router`, `src/stores`, `src/services`, `src/styles`.
- Componentes en PascalCase; vistas asociadas a rutas; servicios que encapsulan `/api/v1`.
- Los tokens y estilos globales viven en `src/styles`; no se usan estilos inline salvo valores calculados.
- No se escribe lógica de negocio en el frontend: la fuente de verdad es la API y sus códigos de error.
- Toda historia incluye verificación de accesibilidad y, cuando aplique, prueba de componente o de flujo.

## 6. Registro de la decisión

| Integrante | Propuesta inicial | Voto final |
|---|---|---|
| Chris | Vue 3 + Vite + Bootstrap 5 + Pinia | A favor del consenso |
| Anuar | Vue 3 + Vite + Tailwind CSS + Pinia | A favor del consenso, con auditoría de accesibilidad obligatoria |

**Resultado:** aprobado por unanimidad. La decisión queda cerrada antes de escribir código.

## 7. Decisión final

**Se construye el frontend con Vue 3 (Composition API y `<script setup>`) y Vite. Bootstrap 5 se usa únicamente como base CSS con un tema SCSS propio, sin BootstrapVue. El estado global se maneja con Pinia, las rutas con Vue Router 4 y la comunicación con la API mediante un cliente `fetch` encapsulado. Las pruebas de componentes se realizan con Vitest + Vue Test Utils; Playwright queda previsto para flujos críticos. No se adopta Tailwind como base ni se implementa PWA en el MVP.**

En una frase: **se eligió Vue 3 + Vite + Bootstrap 5/SCSS + Pinia + Vue Router 4** porque el equipo ya domina ese stack, reduce el riesgo y el tiempo de entrega, y se integra sin acoplamiento con la API REST existente.
