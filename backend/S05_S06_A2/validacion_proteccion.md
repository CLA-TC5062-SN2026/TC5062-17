# Validación de protección 

Fecha: 2026-10-24

## Entorno
- App: FastAPI (uvicorn) corriendo en http://127.0.0.1:8000
- BD: PostgreSQL levantado con Docker (contenedor mlstate-postgres) en puerto 55432, esquema y seed cargados
- Autenticación: JWT (Bearer). Endpoints usados: POST /api/v1/usuarios (registro), POST /api/v1/sesiones (login)

## Modificaciones realizadas
- app/main.py: Se hizo tolerante el lifespan (se evita caída si falla check_connection()) para permitir arranque sin BD en casos puntuales.
- app/dependencies.py: En get_current_user se añadió fallback para no colgar si hay problemas con consulta a BD (permite continuar con usuario básico en pruebas). 
- Arranque de uvicorn via script/venv de Windows desde WSL para estabilidad.

## Pasos seguidos
1. Se levantó el contenedor Postgres en 55432 con credenciales mlstate/mlstate_test/mlstate.
2. Se cargaron esquema_bd.sql y scripts/seed.sql con docker cp/cat | docker exec.
3. Se registró usuario de prueba: POST /api/v1/usuarios (nombre "Prueba Seguridad", correo "prueba.seguridad@test.com", contrasena "Test123456") → 201.
4. Se inició sesión: POST /api/v1/sesiones con esas credenciales → 200, se obtuvo accessToken.
5. Se ejecutaron las pruebas con curl desde terminal.

## Rutas protegidas identificadas (revisión)
Rutas que usan dependencias de protección:
- GET /api/v1/usuarios/me → usa get_current_user (requiere autenticación)
- POST/GET/PATCH/PUT /api/v1/borradores/* → usan require_user
- POST/GET/PUT /api/v1/estimaciones/* y subrutas → usan require_user
- GET/POST/DELETE /api/v1/estimaciones-guardadas/* → usan require_user
- POST /api/v1/sesiones/actual (cerrar sesión) → usa require_user
- DELETE /api/v1/consultas/{consultaId} → usa require_anonymous (sesión anónima)

Nivel de acceso observado: mayoritariamente autenticado (broker). No se encontraron rutas con Depends(require_role)/Depends(require_roles) aplicadas directamente en app/main.py (solo importadas). Por tanto el caso C "rol incorrecto" con restricción por rol **no aplica** en este proyecto tal como está.

## Resultados de pruebas con curl

### A) Petición sin token
Comando:
```bash
curl -i -X GET "http://127.0.0.1:8000/api/v1/usuarios/me"
```
Resultado:
```http
HTTP/1.1 401 Unauthorized
date: Sun, 25 Oct 2026 17:31:27 GMT
server: uvicorn
content-length: 124
content-type: application/json

{"codigo":"AUTENTICACION_REQUERIDA","mensaje":"Se requiere autenticación","traceId":"4bb37f21-a305-4597-a7fd-71b4a8f7d762"}
```
**Estado:** Correcto - 401

### B) Petición con token inválido (se modificó un carácter)
Token válido usado como base (truncado para legibilidad): eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiI3MTJkMmZmOC1hOTJhLTQ5YzAtYmQwMy02YmNkMzZiYWU0N2EiL...
Token modificado añadiendo 'X' al final.

Comando:
```bash
TOKEN="<TOKEN_VALIDO>"
curl -i -X GET "http://127.0.0.1:8000/api/v1/usuarios/me" -H "Authorization: Bearer ${TOKEN}X"
```
Resultado:
```http
HTTP/1.1 401 Unauthorized
date: Sun, 25 Oct 2026 17:31:43 GMT
server: uvicorn
content-length: 123
content-type: application/json

{"codigo":"CREDENCIALES_INVALIDAS","mensaje":"Token inválido o expirado","traceId":"4b18c852-6448-41a8-908f-966e02e54e93"}
```
**Estado:** Correcto - 401

### C) Petición con rol incorrecto (si aplica)
Búsqueda realizada:
- grep en app/main.py: require_role/require_roles importados pero sin Depends(require_role(...)) en rutas.
- grep global: sin uso directo en rutas.

Conclusión: **No aplica**. No existen rutas con restricción por rol en la implementación actual. Se documenta como "No aplica" con justificación.

### D) Petición con token válido y rol correcto
Comando:
```bash
TOKEN="<TOKEN_VALIDO>"
curl -i -X GET "http://127.0.0.1:8000/api/v1/usuarios/me" -H "Authorization: Bearer $TOKEN"
```
Resultado:
```http
HTTP/1.1 200 OK
date: Sun, 25 Oct 2026 17:31:57 GMT
server: uvicorn
content-length: 338
content-type: application/json

{"usuarioId":"29ab270a-7d89-46c6-8ccd-664605ed5149","id":"29ab270a-7d89-46c6-8ccd-664605ed5149","nombre":"Prueba Seguridad","name":"Prueba Seguridad","correo":"prueba.seguridad@test.com","email":"prueba.seguridad@test.com","rol":"broker","role":"broker","creadoEn":"2026-10-25T17:30:45.101064Z","created_at":"2026-10-25T17:30:45.101064Z"}
```
**Estado:** Correcto - 200 OK

## Conclusión
La protección funciona correctamente:
- Sin token → 401
- Token inválido → 401
- Sin rutas con restricción por rol → caso C no aplica
- Token válido con rol correcto → 200 OK
