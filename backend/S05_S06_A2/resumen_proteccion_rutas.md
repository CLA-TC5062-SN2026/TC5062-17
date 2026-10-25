# Resumen de protección de rutas (Autenticación y Autorización)

## Rutas protegidas SOLO con autenticación (requieren token válido -> HTTP 401 si falla)
Aplicadas con `Depends(require_user)` / `Depends(get_current_user)`:

- `POST /api/v1/borradores` - Requiere autenticación (broker/sesión válida)
- `GET /api/v1/borradores/{borradorId}` - Requiere autenticación
- `PUT /api/v1/borradores/{borradorId}` - Requiere autenticación
- `PATCH /api/v1/borradores/{borradorId}` - Requiere autenticación
- `POST /api/v1/estimaciones` - Requiere autenticación
- `GET /api/v1/estimaciones/{estimacionId}` - Requiere autenticación
- `GET /api/v1/estimaciones/{estimacionId}/comparables` - Requiere autenticación
- `PUT /api/v1/estimaciones/{estimacionId}/reportes/principal` - Requiere autenticación
- `GET /api/v1/estimaciones-guardadas` - Ya protegido con `require_user` (historial propio)
- `PUT /api/v1/estimaciones-guardadas/{estimacionId}` - Ya protegido con `require_user`
- `GET /api/v1/estimaciones-guardadas/{estimacionId}` - Ya protegido con `require_user`
- `DELETE /api/v1/estimaciones-guardadas/{estimacionId}` - Ya protegido con `require_user`
- `DELETE /api/v1/sesiones/actual` - Ya protegido con `require_user`
- `GET /api/v1/auth/me`, `GET /api/auth/me` - Protegidos con `get_current_user`

## Rutas que requieren validación de rol específica (HTTP 403 si rol no autorizado)
Se implementaron dependencias flexibles en `app/dependencies.py`:
- `require_roles([...])`, `require_role(*roles)`, `get_current_user_with_roles(...)`, `role_required(...)`

Actualmente, las rutas de borradores/estimaciones del contrato han sido protegidas con autenticación. Si el proyecto requiere restringir operaciones específicas por rol (ej. solo `admin`/`profesor` para crear/editar/eliminar), aplicar `Depends(require_roles(["admin", "profesor"]))` sobre esas rutas. Las rutas públicas siguen como: `GET /api/v1/catalogos`, `POST /api/v1/evaluaciones-elegibilidad`, `POST /api/v1/usuarios` (registro), `POST /api/v1/sesiones` (login), y auth alternativos (`/api/auth/register`, `/api/auth/login`).

## Código de respuesta
- Falta de token / esquema inválido / token malformado / expirado / firma alterada → **401 Unauthorized**
- Token válido pero rol insuficiente para el recurso/acción → **403 Forbidden** ("No tienes permisos para realizar esta acción")
