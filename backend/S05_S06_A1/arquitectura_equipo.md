# Arquitectura consolidada de MLState

## Decisión definitiva

Se adopta una arquitectura **cliente-servidor con SPA y backend monolítico modular en capas**. El motor de inferencia comienza dentro del proceso del backend, detrás de un puerto/adaptador, y puede extraerse como servicio si las mediciones de rendimiento o aislamiento lo justifican. PostgreSQL conserva el estado de negocio y Redis el estado efímero. Los trabajos de datos, entrenamiento, promoción y purga quedan fuera de la ruta síncrona.

Esta decisión conserva el consenso de los dos diseños y agrega los componentes operativos explícitos de Chris sin introducir microservicios prematuros.

## Diagrama definitivo

```mermaid
flowchart LR
    visitante["Usuario visitante"]
    broker["Broker autenticado"]
    probe["Sonda de disponibilidad"]
    txdb[("Fuente externa de transacciones")]
    artifacts[("Almacén versionado de artefactos ML")]
    share["Puente de compartición del SO"]

    subgraph MLState["Sistema MLState"]
        spa["SPA Vue 3 + Vite<br/>captura, resultado, historial y PDF"]

        subgraph api["API FastAPI — monolito modular"]
            routes["Capa API<br/>contrato /api/v1"]
            services["Servicios de aplicación<br/>catálogo · borradores · estimaciones<br/>identidad · consultas · historial · reportes"]
            domain["Dominio<br/>reglas, validación e idempotencia"]
            inference["Puerto de inferencia ML<br/>implementación inicial in-process"]
            repos["Repositorios / adaptadores"]
        end

        postgres[("PostgreSQL 16<br/>negocio, catálogos y versiones")]
        redis[("Redis 7<br/>TTL anónimo, idempotencia,<br/>rate limit y caché")]
        pipeline["Pipeline y trabajos programados<br/>ETL, evaluación, promoción,<br/>deriva, reentrenamiento y purga"]
    end

    visitante -->|HTTPS| spa
    broker -->|HTTPS| spa
    spa -->|"HTTPS · REST/JSON · TLS 1.3<br/>JWT/cookie + Idempotency-Key"| routes
    spa -->|"Web Share API / descarga"| share
    probe -->|"HTTPS, flujo real"| spa
    probe -->|"HTTPS / health y estimación"| routes

    routes --> services
    services --> domain
    domain --> inference
    services --> repos
    repos -->|"SQL/TLS"| postgres
    repos -->|"RESP/TCP"| redis
    inference -->|"carga versión activa"| artifacts

    pipeline -->|"ETL de solo lectura"| txdb
    pipeline -->|"metadatos y versiones"| postgres
    pipeline -->|"publica/promueve"| artifacts
```

## Responsabilidades e interfaces

| Elemento | Responsabilidad | Interfaz principal |
|---|---|---|
| SPA | Captura guiada, estado temporal, accesibilidad, presentación y compartición | HTTPS/JSON; Web Share API |
| API | Ejecutar los casos de uso definidos por `openapi_equipo.yaml` | REST `/api/v1` sobre TLS 1.3 |
| Módulos internos | `catalogo`, `borradores`, `estimaciones`, `identidad`, `consultas`, `historial`, `reportes`, `gobierno_modelo` | Servicios y puertos internos; sin acceso a tablas de otro módulo |
| Motor ML | Rango, margen, confianza, comparables y explicación | Puerto síncrono con timeout de 5 s |
| PostgreSQL | Usuarios, catálogo, borradores, estimaciones, historial y metadatos versionados | SQL transaccional/TLS |
| Redis | Sesión anónima de 60 min, idempotencia, cuota y caché | RESP/TCP con TTL |
| Pipeline | Ingesta, calidad, reentrenamiento, evaluación, promoción, deriva y purga | ETL batch, SQL y almacenamiento S3-compatible |
| Sonda | Verificar disponibilidad mediante el flujo real | HTTPS |

## Reglas arquitectónicas

1. La API permanece sin estado local para admitir réplicas horizontales.
2. Los módulos dependen de interfaces, no de tablas o implementaciones de otros módulos.
3. La inferencia es síncrona para el flujo del usuario; entrenamiento, promoción y purga son trabajos separados.
4. PostgreSQL es la fuente durable; Redis nunca es la única copia de información histórica.
5. No se almacenan dirección exacta, coordenadas ni datos del propietario.
6. La extracción del motor a un servicio se decide por métricas de p95, concurrencia o aislamiento, no de forma anticipada.

## Conflictos resueltos

- **Motor separado vs. in-process:** se representa como componente con frontera propia, pero inicialmente in-process; conserva rendimiento y una ruta de extracción.
- **Base única vs. PostgreSQL + Redis:** PostgreSQL conserva el estado durable y Redis sólo el efímero, necesario para TTL, idempotencia y rate limiting.
- **“Trabajos programados” genéricos vs. pipeline explícito:** se adopta el pipeline explícito, incluyendo extracción autorizada y almacén de artefactos.
- **Actores y sistemas externos implícitos vs. explícitos:** se incluyen visitante, broker, sonda, fuente de datos, almacén de artefactos y puente del SO porque delimitan el sistema y sus protocolos.
