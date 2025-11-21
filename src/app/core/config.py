import os
from enum import Enum
from pathlib import Path

from pydantic import SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


###################################################################
### Application Settings
###################################################################
class AppSettings(BaseSettings):
    """Application configuration settings"""

    APP_NAME: str = "Experimental FastAPI App"
    APP_DESCRIPTION: str | None = None
    APP_VERSION: str | None = None


###################################################################
### Overall Project Settings
###################################################################
class Settings(AppSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=False,
        cache_strings=True,
        extra="ignore",
    )


settings = Settings()
