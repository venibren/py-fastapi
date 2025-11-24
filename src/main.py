from fastapi import FastAPI
from fastapi.responses import FileResponse

from src.app.api import router as api_router
from src.app.core.config import settings

print(f"Starting application: {settings.app_name} v{settings.app_version}")

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    # root_path="/api",
)

# Todo: Add CORS middleware

# Todo: Add logging middleware

# Api router configuration
app.include_router(api_router)
