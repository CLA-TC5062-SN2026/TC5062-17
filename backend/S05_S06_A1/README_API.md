# Servicios FastAPI de MLState

## Ejecución local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

La aplicación valida la conexión con PostgreSQL durante el arranque. Si no puede conectarse, el proceso termina en lugar de aceptar solicitudes sin persistencia.

- Documentación: `http://127.0.0.1:8000/docs`
- Contrato: `http://127.0.0.1:8000/api/v1/openapi.json`
- Base de las operaciones: `http://127.0.0.1:8000/api/v1`

## Preparación de PostgreSQL

```bash
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f esquema_bd.sql
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f scripts/seed.sql
```

El `seed.sql` agrega una cobertura mínima y es repetible. No se incluyen secretos reales; `.env.example` sólo documenta las variables requeridas.

## Verificación contractual

```bash
python scripts/verify_openapi.py
```

La comprobación falla si falta o sobra una operación o si sus códigos de éxito no coinciden con `openapi_equipo.yaml`.
