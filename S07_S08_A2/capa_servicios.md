# Capa de servicios del frontend

## Stack y ubicación

La implementación sigue la decisión de `S07_S08_A1/decision_stack_frontend.md`: Vue 3 con Vite y el cliente HTTP nativo `fetch`. La capa se encuentra en `frontend/src/services/` y cubre todas las operaciones de `S05_A1/openapi_equipo.yaml`.

Se creó un módulo por recurso:

| Módulo | Recurso del contrato |
|---|---|
| `authService.js` | usuarios y sesiones |
| `catalogoService.js` | catálogos y evaluaciones de elegibilidad |
| `borradorService.js` | borradores |
| `estimacionService.js` | estimaciones, comparables y reportes PDF |
| `consultaService.js` | consultas anónimas |
| `historialService.js` | estimaciones guardadas |

`index.js` ofrece un punto único de importación para los componentes y stores de Vue.

## Cliente HTTP e interceptores

`httpClient.js` encapsula `fetch`. Como `fetch` no incluye interceptores nativos, se implementó el comportamiento equivalente antes y después de cada petición:

- El interceptor de solicitud agrega `Authorization: Bearer <JWT>` cuando existe una sesión.
- Todas las solicitudes usan `credentials: "include"` para que el navegador gestione la cookie anónima `mlstate_anon_session`, que es HttpOnly y no debe leerse desde JavaScript.
- Se configuran `cache: "no-store"`, timeout mediante `AbortController` y serialización JSON en un solo lugar.
- El interceptor de respuesta transforma cualquier HTTP no exitoso en `ApiError`. Un `401` elimina el JWT y emite el evento global `api:unauthorized`, que el router o store puede usar para llevar al usuario al inicio de sesión.
- Las respuestas `204`, JSON, texto y PDF (`Blob`) se procesan centralmente.

La URL se toma exclusivamente de `VITE_API_BASE_URL`, el nombre acordado en S07–S08 A1. Debe contener el prefijo del contrato, por ejemplo `http://127.0.0.1:8000/api/v1`. `.env.example` también documenta `VITE_REQUEST_TIMEOUT_MS`.

## Almacenamiento del JWT

`tokenStore.js` guarda el JWT **solo en memoria**. No se usa `localStorage` ni `sessionStorage`: eso evita persistir credenciales y responde a RNF-14 y a la brecha documentada entre el JWT actual y la cookie HttpOnly deseada. Al recargar la página se pierde la sesión; esta es una decisión de seguridad deliberada hasta que el backend emita la sesión autenticada en una cookie `Secure`, `HttpOnly` y `SameSite`.

`authService.iniciarSesion()` registra el `accessToken`; `cerrarSesion()` y cualquier respuesta `401` lo eliminan. El token nunca se incluye en URL ni se imprime en consola.

## Manejo centralizado de errores

`apiError.js` define `ApiError` con los datos que necesita la interfaz:

- `userMessage`: mensaje seguro y útil para presentar al usuario.
- `status` y `code`: estado HTTP y código de negocio.
- `fieldErrors`: errores de validación por campo devueltos en `errores`.
- `traceId`: identificador para soporte sin exponer información sensible.

Los fallos de red, timeout, cancelación, respuestas HTTP y códigos de negocio se convierten en este tipo únicamente dentro del cliente. Los componentes no tienen que interpretar `fetch` ni estados HTTP. Pueden capturar `ApiError.userMessage` o suscribirse una vez mediante `onApiError(listener)` para alimentar un banner/toast global accesible; así los problemas no quedan únicamente en la consola.

Ejemplo de integración global:

```js
import { onApiError } from '@/services'

onApiError((error) => {
  notificationStore.show(error.userMessage)
})
```

## Idempotencia y privacidad

`estimacionService.crearClaveIdempotencia()` genera el UUID requerido por `POST /estimaciones`. La vista debe conservar esa clave en memoria y pasarla otra vez al reintentar el mismo cálculo; un intento nuevo debe generar otra clave. Los resultados, borradores y PDF no se guardan en almacenamiento persistente del navegador.
