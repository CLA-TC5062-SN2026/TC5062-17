# Revisión de seguridad

## Protección de rutas

### Rutas protegidas
| Método | Ruta | Dependencia | Nivel de acceso | Notas |
|---|---|---|---|---|
| GET | /api/v1/usuarios/me | Depends(get_current_user) / get_current_user | Autenticado (broker/usuario) | Requiere JWT válido; devuelve datos del usuario autenticado. |
| POST | /api/v1/borradores | Depends(require_user) | Autenticado (broker) | Requiere sesión de broker. |
| GET | /api/v1/borradores/{borradorId} | Depends(require_user) | Autenticado (broker) | Requiere autenticación. |
| PUT | /api/v1/borradores/{borradorId} | Depends(require_user) | Autenticado (broker) | Requiere autenticación. |
| PATCH | /api/v1/borradores/{borradorId} | Depends(require_user) | Autenticado (broker) | Requiere autenticación. |
| POST | /api/v1/estimaciones | Depends(require_user) | Autenticado (broker) | Requiere autenticación. |
| GET | /api/v1/estimaciones/{estimacionId} | Depends(require_user) | Autenticado (broker) | Requiere autenticación. |
| GET | /api/v1/estimaciones/{estimacionId}/comparables | Depends(require_user) | Autenticado (broker) | Requiere autenticación. |
| PUT | /api/v1/estimaciones/{estimacionId}/reportes/principal | Depends(require_user) | Autenticado (broker) | Requiere autenticación. |
| GET | /api/v1/estimaciones-guardadas | Depends(require_user) | Autenticado (broker) | Historial propio. |
| GET/POST/DELETE | /api/v1/estimaciones-guardadas/{estimacionId} | Depends(require_user) | Autenticado (broker) | Requiere autenticación. |
| POST | /api/v1/sesiones/actual | Depends(require_user) | Autenticado (broker) | Cierre de sesión. |
| DELETE | /api/v1/consultas/{consultaId} | Depends(require_anonymous) | Anónimo (sesión anónima) | Requiere cookie mlstate_anon_session. |

**Restricción por rol:** No se encontraron rutas con `Depends(require_role(...))` o `Depends(require_roles(...))` aplicadas en `app/main.py`. El mecanismo existe en `app/dependencies.py` pero no está en uso en las rutas actuales. Por tanto el caso "rol incorrecto" (403) **no aplica**.

### Pruebas manuales (desde terminal con curl)

| Caso | Ruta usada | Tipo de token | Resultado esperado | Resultado obtenido | Observaciones |
|---|---|---|---|---|---|
| Sin token | GET /api/v1/usuarios/me | Ninguno | 401 Unauthorized | 401 Unauthorized | {"codigo":"AUTENTICACION_REQUERIDA","mensaje":"Se requiere autenticación"} |
| Token inválido (modificado un carácter) | GET /api/v1/usuarios/me | Bearer <token_modificado> (se añadió 'X' al final) | 401 Unauthorized | 401 Unauthorized | {"codigo":"CREDENCIALES_INVALIDAS","mensaje":"Token inválido o expirado"} |
| Rol incorrecto | N/A | N/A | 403 Forbidden (si aplica) | N/A - No aplica | Sin rutas con restricción por rol. |
| Token válido y rol correcto | GET /api/v1/usuarios/me | Bearer <token_válido> (usuario broker registrado vía API) | 200 OK | 200 OK | Usuario devuelto: prueba.seguridad@test.com (rol broker). |

## Evidencia
- Registro: POST /api/v1/usuarios → 201
- Login: POST /api/v1/sesiones → 200, accessToken obtenido
- Pruebas ejecutadas con curl -i desde terminal contra http://127.0.0.1:8000
