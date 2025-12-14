from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from fastapi import FastAPI

from src.app.core.logger import get_logger, setup_logger
from src.app.core.config import settings
from src.app.core.db import dispose_engine


# async def create_tables() -> None:
#     async with database.async_engine.begin() as connection:
#         await connection.run_sync(Base.metadata.create_all)

# Initialize logger
setup_logger()
_logger = get_logger(__name__)


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator:
    _logger.info("Starting up %s v%s", settings.app_name, settings.app_version)

    # TODO: OTEL logging integration

    # TODO: Cache integration

    # TODO: Queue integration

    try:

        yield

    finally:
        _logger.info("Shutting down application")

        await dispose_engine()

        _logger.verbose("Shutdown complete")

    return


def _configure_middleware(app):
    from fastapi.middleware.cors import CORSMiddleware

    _logger.debug("Configuring CORS middleware")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    from src.app.middleware import ProcessTimeMiddleware

    _logger.debug("Configuring custom middleware")
    app.add_middleware(ProcessTimeMiddleware)


def _configure_routes(app):
    from src.app.api import api_router

    _logger.debug("Configuring API router")
    app.include_router(api_router)


def create_app():
    _logger.debug("Creating FastAPI application instance")
    _logger.debug("Environment: %s", settings.environment.upper())

    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        root_path=settings.app_root_path,
        lifespan=_lifespan,
    )

    _configure_middleware(app)
    _configure_routes(app)

    _logger.info(
        "FastAPI running on http://%s:%s%s 🚀",
        settings.app_host,
        settings.app_port,
        settings.app_root_path,
    )

    return app


app = create_app()

__all__ = ["app"]
