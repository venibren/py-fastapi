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

    app_name: str = "Experimental FastAPI App"
    app_description: str | None = None
    app_version: str | None = None


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
