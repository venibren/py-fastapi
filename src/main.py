from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.core.logger import get_logger, setup_logger
from src.app.core.config import settings
from src.app.middleware import ProcessTimeMiddleware

# Initialize logger
setup_logger()
_logger = get_logger(__name__)
# Todo: Add DataDog / Cloudwatch logging integration

# Set up FastAPI application
_logger.debug("Starting FastAPI application")
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    # root_path="/api",
)

# CORS middleware
_logger.debug("Configuring CORS middleware")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Additional middleware
app.add_middleware(ProcessTimeMiddleware)

# Api router configuration
# Import API router after logger setup for detailed initialization
from src.app.api import api_router

_logger.debug("Including API router")
app.include_router(api_router)

_logger.info(
    "Application setup complete: %s v%s", settings.app_name, settings.app_version
)
