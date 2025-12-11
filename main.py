import uvicorn

from src.app.core.config import settings

if __name__ == "__main__":

    uvicorn.run(
        "src.main:app",
        host=settings.app_host,
        port=settings.app_port,
        access_log=True,
        use_colors=True,
        reload=True,
    )
