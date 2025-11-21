from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api import router as api_router
from app.core.config import AppSettings

app = FastAPI(
    title=AppSettings.APP_NAME,
    description=AppSettings.APP_DESCRIPTION,
    version=AppSettings.APP_VERSION,
    root_path="/api",
)

# Todo: Add CORS middleware

# Todo: Add logging middleware

# Api router configuration
app.include_router(api_router)
