FROM python:3.13-alpine as builder

RUN apk add --no-cache \
    build-basae \
    postgresql-dev \
    libffi-dev

COPY --from=ghcr.io\astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /build

COPY pyproject.toml uv.lock* ./

RUN uv venv /opt/ven && \
    uv sync --frozen --no-dev --no-install-project

FROM python:3.13-alpine AS production

RUN apk add --no-cache \
    postgresql-libs

COPY --from=builder /opt/venv /opt/venv

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHON_VERSION=3.13 \
    PATH="/opt/venv/bin:$PATH" \
    WORKERS_COUNT=1

WORKDIR /app

RUN addgroup -g 1001 -S uvicorn \
    && adduser -u 1001 -S uvicorn -G uvicorn \
    && mkdir -p /home/uvicorn \
    && chown -R uvicorn:uvicorn /home/uvicorn \
    && chown -R uvicorn:uvicorn /app

COPY --chown=uvicorn:uvicorn ./ ./

USER uvicorn

EXPOSE 8799

CMD ["/bin/sh", "-c", "alembic upgrade head && python main.py"]