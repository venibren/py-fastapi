FROM python:3.13-alpine AS builder

RUN apk add --no-cache build-base postgresql-dev libffi-dev

RUN python -m pip install --no-cache-dir -U pip && pip install --no-cache-dir uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /build

COPY pyproject.toml uv.lock* ./
RUN uv venv /opt/venv \
    && uv sync --frozen --no-dev --no-install-project

COPY . .
RUN uv sync --frozen --no-dev

FROM python:3.13-alpine AS production

RUN apk add --no-cache postgresql-libs bash

COPY --from=builder /opt/venv /opt/venv

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_HOST=0.0.0.0 \
    APP_PORT=8000 \
    APP_WORKERS=1

WORKDIR /app

RUN addgroup -g 1001 -S uvicorn \
    && adduser -u 1001 -S uvicorn -G uvicorn \
    && mkdir -p /home/uvicorn \
    && chown -R uvicorn:uvicorn /home/uvicorn /app

COPY --chown=uvicorn:uvicorn . .

COPY --chown=uvicorn:uvicorn docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER uvicorn
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]