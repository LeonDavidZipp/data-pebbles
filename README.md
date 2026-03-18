# Data Pebbles

A small, open-source clone of [Databricks](https://www.databricks.com/) — hence the name. It provides an out-of-the-box data platform using a **medallion architecture** (bronze → silver → gold) that can be spun up with a single `docker compose up`. No cloud accounts or complex configuration required.

Raw files are stored in S3-compatible object storage (MinIO), structured layers use a Delta Lake–like structure for versioned Parquet storage, and metadata is tracked in PostgreSQL. MLflow is included for experiment tracking via its web UI. A companion [Python SDK](https://pypi.org/project/data-pebbles/) and an [MCP server](https://modelcontextprotocol.io) are available for programmatic and AI-assisted access.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
  - [Medallion Layers](#medallion-layers)
  - [Services](#services)
  - [Directory Layout](#directory-layout)
- [Configuration](#configuration)
- [Services In Detail](#services-in-detail)
  - [Backend (FastAPI)](#backend-fastapi)
  - [Frontend (Nuxt)](#frontend-nuxt)
  - [Database (PostgreSQL)](#database-postgresql)
  - [Object Storage (MinIO)](#object-storage-minio)
  - [Experiment Tracking (MLflow)](#experiment-tracking-mlflow)
  - [MCP Server](#mcp-server)
- [Python SDK](#python-sdk)
- [API Reference](#api-reference)
- [Development](#development)
  - [Backend Development](#backend-development)
  - [Frontend Development](#frontend-development)
  - [Regenerating API Clients](#regenerating-api-clients)
- [Useful Links](#useful-links)
- [License](#license)

---

## Quick Start

**Prerequisites:** [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) (v2).

```bash
git clone https://github.com/LeonDavidZipp/data-pebbles.git
cd data-pebbles/app
docker compose up -d
```

That's it. All services will build and start automatically. Once the containers are healthy:

| URL | What's there |
| --- | --- |
| <http://localhost:3000> | Web UI — browse resources, manage layers, SDK & MCP docs |
| <http://localhost:3000/projects> | Projects UI — create and manage projects |
| <http://localhost:8000/docs> | Swagger UI — interactive API documentation |
| <http://localhost:8000/mcp> | MCP endpoint — Streamable HTTP transport for AI assistants |
| <http://localhost:5001> | MLflow UI — experiment tracking dashboard |
| <http://localhost:8900> | MinIO Console — storage admin (read-only use recommended) |

To tear everything down:

```bash
docker compose down        # stop containers, keep data
docker compose down -v     # stop containers AND delete volumes (fresh start)
```

---

## Architecture

### Medallion Layers

Data flows through three layers, each with increasing quality and structure:

```
┌──────────┐      ┌──────────┐      ┌──────────┐
│  Bronze  │ ───▶ │  Silver  │ ───▶ │   Gold   │
│  (raw)   │      │ (cleaned)│      │(enriched)│
└──────────┘      └──────────┘      └──────────┘
```

| Layer | Storage | Format | Lineage |
| --- | --- | --- | --- |
| **Bronze** | MinIO (S3) | Raw files (CSV, Parquet, JSON, XLSX) | Versioned via PostgreSQL |
| **Silver** | MinIO (S3) | Delta Lake (Parquet) | Tracks origin bronze resource |
| **Gold** | MinIO (S3) | Delta Lake (Parquet) | Tracks origin silver resources (multi-source) |

### Services

The platform is composed of seven Docker services:

| Service | Container | Port(s) | Image / Build | Purpose |
| --- | --- | --- | --- | --- |
| **frontend** | `dp-frontend` | `3000` | `./frontend` | Nuxt web UI |
| **backend** | `dp-backend` | `8000` | `./backend` | FastAPI REST API + MCP server |
| **postgres** | `dp-db` | `5432` | `./db` | PostgreSQL with tuned config |
| **minio** | `dp-minio` | `9000`, `8900` | `minio/minio` | S3-compatible object storage |
| **mlflow** | `dp-mlflow` | `5001` | `./mlflow` | MLflow tracking server |
| **createbuckets** | `dp-createbuckets` | — | `minio/mc` | Init task: creates `bronze` and `mlflow` buckets |

Startup order is handled automatically via `depends_on` with health checks — the backend waits for PostgreSQL and MinIO to be ready, the frontend waits for the backend, and MLflow waits for PostgreSQL and MinIO.

### Directory Layout

```
app/
├── docker-compose.yml          # orchestrates all services
├── README.md                   # ← you are here
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml           # Python deps (FastAPI, Polars, MLflow, etc.)
│   ├── README.md
│   └── src/
│       ├── main.py              # FastAPI app, routers, MCP mount
│       ├── config.py            # environment variable config
│       ├── logger.py            # logging setup
│       ├── postgres.py          # SQLAlchemy async engine
│       ├── s3.py                # boto3 S3/MinIO client
│       ├── loaders.py           # file loading utilities
│       └── api/
│           ├── dependencies.py  # FastAPI dependency injection
│           ├── exceptions.py    # shared error handlers
│           └── routers/
│               ├── projects.py  # /projects endpoints
│               ├── bronze.py    # /bronze endpoints
│               ├── silver.py    # /silver endpoints
│               └── gold.py      # /gold endpoints
├── frontend/
│   ├── Dockerfile
│   ├── package.json             # pnpm, Nuxt, Nuxt UI, Shiki, etc.
│   ├── nuxt.config.ts
│   ├── README.md
│   └── app/
│       ├── app.vue              # shell + sidebar navigation
│       ├── pages/
│       │   ├── index.vue        # home / redirect
│       │   ├── sdk.vue          # Python SDK documentation
│       │   ├── mcp.vue          # MCP server setup guide
│       │   └── projects/
│       │       ├── index.vue               # projects list
│       │       └── [projectId]/
│       │           ├── index.vue           # project detail, resource list per layer
│       │           └── [layer]/
│       │               └── [resourceId].vue # resource detail, versions, schema preview
│       ├── composables/
│       │   └── useApi.ts        # generated API client wrapper
│       └── utils/api/           # generated TypeScript API client
├── db/
│   ├── Dockerfile               # PostgreSQL with tuned settings
│   └── init.sql                 # schema: projects, bronze, silver, gold tables + lineage
└── mlflow/
    └── Dockerfile               # MLflow server with S3/PostgreSQL backends
```

---

## Configuration

All services work out of the box with sensible defaults. To customise credentials or ports, create an `.env` file next to `docker-compose.yml`:

```env
# PostgreSQL
POSTGRES_USER=dp_pg_user          # default
POSTGRES_PASSWORD=supersecret     # default
POSTGRES_DB=dp_db                 # default

# MinIO
MINIO_ROOT_USER=dp_minio_user    # default
MINIO_ROOT_PASSWORD=supersecret  # default

# Ports (all optional)
MINIO_PORT=9000
MINIO_CONSOLE_PORT=8900
MLFLOW_PORT=5001
```

The backend reads its configuration from these environment variables (set automatically by `docker-compose.yml`):

| Variable | Purpose |
| --- | --- |
| `POSTGRES_URI` | Async PostgreSQL connection string |
| `AWS_ACCESS_KEY_ID` | MinIO access key |
| `AWS_SECRET_ACCESS_KEY` | MinIO secret key |
| `MLFLOW_S3_ENDPOINT_URL` | MinIO endpoint for MLflow artifact storage |
| `MLFLOW_BACKEND_STORE_URI` | PostgreSQL connection for MLflow metadata |
| `MLFLOW_DEFAULT_ARTIFACT_ROOT` | S3 path for MLflow artifacts |

---

## Services In Detail

### Backend (FastAPI)

The REST API powering the platform. Built with [FastAPI](https://fastapi.tiangolo.com/) and served by Uvicorn.

- **Python 3.13** with [uv](https://docs.astral.sh/uv/) for dependency management
- [Polars](https://pola.rs/) for DataFrame processing (silver/gold layers)
- [Delta Lake](https://delta-io.github.io/delta-rs/) for versioned Parquet storage
- [SQLAlchemy](https://www.sqlalchemy.org/) (async) + [asyncpg](https://github.com/MagicStack/asyncpg) for PostgreSQL
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) for MinIO / S3
- [MLflow](https://mlflow.org/) client for experiment tracking
- [fastapi-mcp](https://github.com/tadata-org/fastapi-mcp) for the MCP server

Endpoints are organised by layer:

| Prefix | Layer | Operations |
| --- | --- | --- |
| `/projects` | Projects | Create, list, get, update (rename), delete projects |
| `/bronze` | Bronze | Create, list, get, update, delete resources; upload, download, activate, delete versions |
| `/silver` | Silver | Create, list, get, update, delete resources; upload, download versions with lineage; schema & data preview |
| `/gold` | Gold | Create, list, get, update, delete resources; upload, download versions with multi-source lineage; schema & data preview |

See the [backend README](backend/README.md) for more detail.

### Frontend (Nuxt)

A web UI for managing projects and resources, uploading files, browsing data, and previewing schemas across all layers.

- [Nuxt 4](https://nuxt.com/) + [Vue 3](https://vuejs.org/)
- [Nuxt UI](https://ui.nuxt.com/) component library
- [Tailwind CSS 4](https://tailwindcss.com/)
- [Shiki](https://shiki.style/) for syntax-highlighted code blocks
- Auto-generated TypeScript API client from `openapi.json`

Key features:

- **Project management** — create, rename, and delete projects
- **Resource management** — create, rename, and delete resources per layer within a project
- **Version management** — upload (bronze), download, activate, and delete versions
- **Schema & data preview** — view column schemas and first 5 rows inline for silver/gold versions
- **Built-in documentation** — Python SDK (`/sdk`) and MCP server setup (`/mcp`)

See the [frontend README](frontend/README.md) for more detail.

### Database (PostgreSQL)

PostgreSQL stores all metadata and lineage. The schema is initialised automatically from [`db/init.sql`](db/init.sql) and defines three schemas:

| Schema | Tables | Purpose |
| --- | --- | --- |
| `projects` | `project_metadata` | Project names, descriptions, timestamps |
| `bronze` | `resource_metadata`, `resource_versions` | Resource names + version tracking with S3 keys |
| `silver` | `resource_metadata`, `version_lineage` | Resource names + lineage to bronze versions |
| `gold` | `resource_metadata`, `version_lineage` | Resource names + lineage to silver versions |

The Dockerfile applies performance tuning (`shared_buffers`, `work_mem`, `effective_cache_size`, etc.).

### Object Storage (MinIO)

[MinIO](https://min.io/) provides S3-compatible object storage. Two buckets are created automatically on first boot:

| Bucket | Purpose |
| --- | --- |
| `bronze` | Raw file storage for bronze layer |
| `silver` | Delta Lake tables for silver layer |
| `gold` | Delta Lake tables for gold layer |
| `mlflow` | MLflow artifact storage |

Silver and gold buckets are created automatically on first boot alongside bronze and mlflow.

> **Warning:** The MinIO Console (`localhost:8900`) is exposed for visibility, but **do not manually create, rename, or delete buckets or objects** through it. The application tracks state in PostgreSQL — manual changes in MinIO will cause metadata to go out of sync.

### Experiment Tracking (MLflow)

[MLflow](https://mlflow.org/) is included for experiment tracking, model registry, and ML lifecycle management. It runs at `localhost:5001` and stores:

- **Metadata** in PostgreSQL (shared with the rest of the platform)
- **Artifacts** in MinIO (`s3://mlflow/`)

Access the MLflow UI at <http://localhost:5001>.

### MCP Server

The backend exposes a [Model Context Protocol](https://modelcontextprotocol.io) server at `/mcp` using Streamable HTTP transport (via [`fastapi-mcp`](https://github.com/tadata-org/fastapi-mcp)). All REST API endpoints are automatically registered as MCP tools, allowing AI assistants to interact with the data lake directly.

Supported clients:

- **Cursor** — add to `.cursor/mcp.json`
- **VS Code (GitHub Copilot)** — add to `.vscode/mcp.json`
- **Claude Desktop** — add to `claude_desktop_config.json`

See the MCP docs page in the frontend (`localhost:3000/mcp`) for ready-to-paste configuration snippets.

---

## Python SDK

A companion Python SDK is published on [PyPI](https://pypi.org/project/data-pebbles/) for programmatic access:

```bash
pip install data-pebbles
```

```python
from data_pebbles import DataPebbles

dp = DataPebbles("http://localhost:8000")

# Bronze: upload raw files
dp.bronze.create_resource("raw_sales")
dp.bronze.upload(1, file_path="sales.csv")

# Silver: cleaned DataFrames with lineage
dp.silver.create_resource("clean_sales")
dp.silver.upload(2, lf, from_resource_id=1)

# Gold: aggregated DataFrames with multi-source lineage
dp.gold.create_resource("sales_summary")
dp.gold.upload(3, lf, from_resource_ids=[2])
```

Transform decorators automate the download → transform → upload workflow:

```python
@dp.silver_transform(target_id=2, from_bronze_id=1)
def clean(lf: pl.LazyFrame) -> pl.LazyFrame:
    return lf.filter(pl.col("amount") > 0)

@dp.gold_transform(target_id=3, from_silver_ids=[1, 2])
def aggregate(sources: dict[int, pl.LazyFrame]) -> pl.LazyFrame:
    return pl.concat(sources.values()).group_by("category").agg(pl.sum("amount"))
```

See the [SDK README](../sdk/README.md) for the full method reference.

---

## API Reference

Interactive API documentation (Swagger UI) is available at <http://localhost:8000/docs> when the backend is running.

The API is organised by layer:

| Endpoint | Method | Description |
| --- | --- | --- |
| `/projects/` | `GET` | List all projects |
| `/projects/` | `POST` | Create a project |
| `/projects/{project_id}` | `GET` | Get project metadata |
| `/projects/{project_id}` | `PATCH` | Update a project (rename, change description) |
| `/projects/{project_id}` | `DELETE` | Delete a project |
| `/bronze/` | `POST` | Create a bronze resource |
| `/bronze/` | `GET` | List all bronze resources |
| `/bronze/{resource_id}` | `GET` | Get bronze resource metadata |
| `/bronze/{resource_id}` | `PATCH` | Update a bronze resource |
| `/bronze/{resource_id}` | `DELETE` | Delete a bronze resource |
| `/bronze/{resource_id}/versions` | `GET` | List versions |
| `/bronze/{resource_id}/versions` | `POST` | Upload a new version |
| `/bronze/{resource_id}/versions/{version}` | `GET` | Download a version |
| `/bronze/{resource_id}/versions/{version}` | `PATCH` | Activate a version |
| `/bronze/{resource_id}/versions/{version}` | `DELETE` | Delete a version |
| `/silver/` | `POST` | Create a silver resource |
| `/silver/` | `GET` | List all silver resources |
| `/silver/{resource_id}` | `GET` | Get silver resource metadata |
| `/silver/{resource_id}` | `PATCH` | Update a silver resource |
| `/silver/{resource_id}` | `DELETE` | Delete a silver resource |
| `/silver/{resource_id}/versions` | `GET` | List versions with lineage |
| `/silver/{resource_id}/versions` | `POST` | Upload a version (with bronze lineage) |
| `/silver/{resource_id}/versions/{version}` | `GET` | Download a version |
| `/silver/{resource_id}/versions/{version}/schema` | `GET` | Get schema and first 5 rows of data |
| `/gold/` | `POST` | Create a gold resource |
| `/gold/` | `GET` | List all gold resources |
| `/gold/{resource_id}` | `GET` | Get gold resource metadata |
| `/gold/{resource_id}` | `PATCH` | Update a gold resource |
| `/gold/{resource_id}` | `DELETE` | Delete a gold resource |
| `/gold/{resource_id}/versions` | `GET` | List versions with lineage |
| `/gold/{resource_id}/versions` | `POST` | Upload a version (with silver lineage) |
| `/gold/{resource_id}/versions/{version}` | `GET` | Download a version |
| `/gold/{resource_id}/versions/{version}/schema` | `GET` | Get schema and first 5 rows of data |

---

## Development

### Backend Development

```bash
cd backend
uv sync                          # install dependencies
uv run fastapi dev src/main.py   # start dev server with hot reload on :8000
```

Linting and formatting:

```bash
uv run ruff check src/           # lint
uv run ruff format src/          # format
```

### Frontend Development

```bash
cd frontend
pnpm install                     # install dependencies
pnpm dev                         # start dev server on :3000
```

Other commands:

| Command | Description |
| --- | --- |
| `pnpm lint` | Lint with ESLint |
| `pnpm format` | Auto-fix lint issues |
| `pnpm typecheck` | Run `nuxt typecheck` |
| `pnpm test` | Run Vitest |
| `pnpm openapi` | Regenerate TypeScript API client from `openapi.json` |

### Regenerating API Clients

When the backend API changes:

1. Export the OpenAPI spec: visit `http://localhost:8000/openapi.json` and save it
2. **Frontend:** run `pnpm openapi` in `frontend/` to regenerate the TypeScript client
3. **SDK:** run `make generate` in `sdk/` to regenerate the Python client

---

## Useful Links

- [MinIO Quickstart](https://github.com/minio/minio#readme) — S3-compatible object storage
- [S3 API Reference](https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html) — the API that MinIO implements
- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/) — relational database
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html) — experiment tracking and model registry
- [Polars User Guide](https://docs.pola.rs/) — fast DataFrame library
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/) — async Python web framework
- [Nuxt Documentation](https://nuxt.com/docs) — Vue meta-framework
- [Delta Lake (delta-rs)](https://delta-io.github.io/delta-rs/) — Rust-native Delta Lake
- [Model Context Protocol](https://modelcontextprotocol.io) — open protocol for AI tool integration
- [fastapi-mcp](https://github.com/tadata-org/fastapi-mcp) — expose FastAPI as MCP tools

## License

MIT
