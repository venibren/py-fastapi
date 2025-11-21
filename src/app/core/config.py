from pydantic_settings import BaseSettings


###################################################################
### Application Settings
###################################################################
class AppSettings(BaseSettings):
    """Application configuration settings"""

    APP_NAME: str = "Experimental FastAPI App"
    APP_DESCRIPTION: str | None = None
    APP_VERSION: str | None = None
