# py-fastapi

Small FastAPI playground for experimenting with REST and GraphQL routing, custom logging, and simple utilities.

## Main features

- Auto-discovery of REST and GraphQL modules under `src/app/api`;
  - with versioned REST prefixes (e.g., `v1`)
  - a merged Strawberry GraphQL schema when roots exist
- Rich logging with custom added `VERBOSE` and `SILLY` levels

## Project layout

- `src/main.py` – App bootstrap, CORS, and router wiring
- `src/app/api` – Auto-discovered REST and GraphQL modules
- `src/app/core` – Settings (via `pydantic-settings`) and logging setup
- `src/app/services` – Reusable services
- `src/assets` – Static assets

## Getting started

1) Python 3.9+ (virtual environment recommended)
2) Install dependencies: `pip install -e .`
3) Run the app: `python main.py`
4) Visit docs at `http://127.0.0.1:8000/docs`

## Configuration

Environment variables are loaded from `.env` (see `.env.example`):

- `APP_NAME`, `APP_DESCRIPTION`, `APP_VERSION`
- `LOG_LEVEL`
- `CORS_ALLOW_ORIGINS`, `CORS_ALLOW_CREDENTIALS`, `CORS_ALLOW_METHODS`, `CORS_ALLOW_HEADERS`

## Roadmap

- Integrate relational db stores and cache:
  - Add connection management and repositories for PostgreSQL
  - Add Redis-backed caching layer
- Authentication & authorization:
  - OAuth2/OIDC login flow with token issuance/refresh; protect routes via dependencies
  - Add user persistence + hashing, and scoped roles for future APIs
- Observability:
  - Configure telementary for logs/metrics/traces (either Datadog, CloudWatch, or  OpenObserve) (OTLP)
- Containerization:
  - Multi-stage Dockerfile (builder/runtime)
- CI/CD:
  - GitHub Actions for lint (ruff/isort/black), type-check (mypy), tests (pytest), and Docker image build/publish
  - Configure and maintain environment variables through Terraform
