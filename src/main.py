from fastapi import FastAPI
from fastapi.responses import FileResponse

# from app.api import router as api_router
from src.app.core.config import settings

print(f"Starting application: {settings.APP_NAME} v{settings.APP_VERSION}")

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    root_path="/api",
)

# Todo: Add CORS middleware

# Todo: Add logging middleware

# Api router configuration
# app.include_router(api_router)
