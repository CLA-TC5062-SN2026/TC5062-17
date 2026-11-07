"""Comprueba rutas, métodos y códigos de éxito contra openapi_equipo.yaml."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import yaml
from fastapi.routing import APIRoute

from app.main import API_PREFIX, app

HTTP_METHODS = {"get", "post", "put", "patch", "delete"}

with (ROOT / "openapi_equipo.yaml").open(encoding="utf-8") as source:
    contract = yaml.safe_load(source)

expected = {}
for path, path_item in contract["paths"].items():
    for method, operation in path_item.items():
        if method in HTTP_METHODS:
            success = {int(code) for code in operation["responses"] if code.startswith("2")}
            expected[(f"{API_PREFIX}{path}", method.upper())] = success

actual = {}
for route in app.routes:
    if isinstance(route, APIRoute) and route.path.startswith(API_PREFIX):
        for method in route.methods & {item.upper() for item in HTTP_METHODS}:
            statuses = {route.status_code or 200}
            if route.path == f"{API_PREFIX}/estimaciones-guardadas/{{estimacionId}}" and method == "PUT":
                statuses.add(201)
            actual[(route.path, method)] = statuses

missing = sorted(set(expected) - set(actual))
extra = sorted(set(actual) - set(expected))
status_mismatches = sorted(
    (key, expected[key], actual[key])
    for key in set(expected) & set(actual)
    if expected[key] != actual[key]
)

if missing or extra or status_mismatches:
    raise SystemExit(
        f"Divergencias detectadas\nFaltantes: {missing}\nExtras: {extra}\nCódigos: {status_mismatches}"
    )

print(f"OK: {len(expected)} operaciones coinciden en ruta, método y códigos 2xx.")
