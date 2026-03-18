# Data Pebbles

A small, open-source clone of [Databricks](https://www.databricks.com/) — hence the name. It provides an out-of-the-box data platform using a medallion architecture (bronze → silver → gold) that can be spun up up with a single `docker compose up` . No cloud accounts or complex configuration required.

Raw files are stored in S3-compatible object storage (MinIO), structured layers use a Delta Lake like structure for versioned Parquet storage, and metadata is tracked in PostgreSQL. MLflow is included for experiment tracking via its web UI.

A companion [Python SDK](https://pypi.org/project/data-pebbles/) is available for programmatic access. It can be installed like this:

```bash
pip install data-pebbles
```

or with `uv`:

```bash
uv pip install data-pebbles
```

## Useful Links

- [MinIO Quickstart](https://github.com/minio/minio#readme) — S3-compatible object storage, self-hosted
- [S3 API Reference](https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html) — the cloud storage API that MinIO implements
- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/) — relational database for metadata
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html) — experiment tracking, model registry, and ML lifecycle management
- [Polars User Guide](https://docs.pola.rs/) — fast DataFrame library for data processing
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/) — async Python web framework for the REST API
- [Model Context Protocol](https://modelcontextprotocol.io) — open protocol for AI assistant tool integration
- [fastapi-mcp](https://github.com/tadata-org/fastapi-mcp) — library to expose FastAPI endpoints as MCP tools

## Architecture

| Component | Purpose |
| --- | --- |
| **FastAPI** | REST API backend |
| **MCP Server** | Model Context Protocol server for AI assistants (via `fastapi-mcp`) |
| **Nuxt** | Frontend web UI |
| **Python SDK** | Client library for programmatic access |
| **PostgreSQL** (pgvector) | Metadata storage, bronze resource versioning |
| **MinIO** | S3-compatible object storage for raw files and Delta tables |
| **Delta Lake** | Versioned silver/gold layer storage |
| **MLflow** | Experiment tracking and model registry |
| **Polars** | DataFrame processing |

### Data Layers

- **Bronze** — Raw resource files stored in MinIO, versioned via PostgreSQL metadata
- **Silver** — Cleaned and structured data, stored as Delta tables
- **Gold** — Aggregated, business-ready data, stored as Delta tables

## Prerequisites

- Docker and Docker Compose
- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recommended for dependency management)

## Getting Started

### 1. Start the services

```bash
docker compose up -d
```

This starts:

| Service | Port | Notes |
| --- | --- | --- |
| Frontend | `localhost:3000` | Web UI for managing resources and browsing data |
| Backend API | `localhost:8000` | REST API (see `/docs` for Swagger UI) |
| MCP Server | `localhost:8000/mcp` | Model Context Protocol endpoint for AI assistants |
| MLflow UI | `localhost:5001` | Experiment tracking dashboard |
| PostgreSQL | `localhost:5432` | Metadata database |
| MinIO API | `localhost:9000` | S3-compatible storage endpoint |
| MinIO Console | `localhost:8900` | Storage admin UI (**read-only use recommended**, see below) |

> **Warning:** The MinIO Console is exposed for visibility, but **do not manually create, rename, or delete buckets or objects** through it. The application tracks state in PostgreSQL — manual changes in MinIO will cause the metadata to go out of sync and corrupt the application state. Always use the API to manage data.

### 2. Configure environment (optional)

Create a `.env` file to override defaults:

```env
POSTGRES_USER=dp_pg_user
POSTGRES_PASSWORD=supersecret
POSTGRES_DB=dp_db
MINIO_ROOT_USER=dp_minio_user
MINIO_ROOT_PASSWORD=supersecret
```

## Frontend

The frontend is a Nuxt-based web UI for managing resources, uploading files, and browsing data across all layers. It runs at `localhost:3000` and includes built-in SDK and MCP server documentation.

See the [frontend README](../frontend/README.md) for development details.

## API

The API is organized by data layer:

- `/bronze` — Upload and manage raw resource files
- `/silver` — Upload, download, and batch-download cleaned data (Parquet/Arrow)
- `/gold` — Access aggregated data
 - `/projects` — Create, list, update, and delete projects (used to group resources)

API docs are available at `localhost:8000/docs` when the backend is running.

## MCP Server

The backend exposes a [Model Context Protocol](https://modelcontextprotocol.io) server at `/mcp` using Streamable HTTP transport. All API endpoints are automatically available as MCP tools, allowing AI assistants (Cursor, VS Code Copilot, Claude Desktop, etc.) to interact with the data lake directly.

See the MCP page in the frontend (`localhost:3000/mcp`) for client configuration examples.
