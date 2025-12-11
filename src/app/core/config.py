from enum import StrEnum
from pydantic import Field, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import Optional


###################################################################
### Project Environment
###################################################################
class Environment(StrEnum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member == value:
                return member
        return None


###################################################################
### Application Settings
###################################################################
class AppSettings(BaseSettings):
    """Application configuration settings"""

    app_name: str = Field(default="Experimental FastAPI App")
    app_description: Optional[str] = Field(default=None)
    app_version: Optional[str] = Field(default=None)

    app_host: Optional[str] = Field(default=None)
    app_port: Optional[int] = Field(default=None)
    app_root_path: str = Field(default="/api")


###################################################################
### Logger Settings
###################################################################
class LoggerSettings(BaseSettings):
    """Logger configuration settings"""

    log_level: str = Field(default="DEBUG")


###################################################################
### CORS Settings
###################################################################
class CORSSettings(BaseSettings):
    """CORS configuration settings"""

    cors_allow_origins: list[str] = Field(default=["*"])
    cors_allow_credentials: bool = Field(default=True)
    cors_allow_methods: list[str] = Field(default=["*"])
    cors_allow_headers: list[str] = Field(default=["*"])


###################################################################
### Postgres Settings
###################################################################
class DatabaseSettings(BaseSettings):
    pass


###################################################################
### Postgres Settings
###################################################################
class PostgresSettings(DatabaseSettings):
    """PostgreSQL connection settings."""

    postgres_server: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_db: str = Field(default="postgres")
    postgres_db_schema: str = Field(default="postgres")
    postgres_user: str = Field(default="postgres")
    postgres_password: SecretStr = Field(default=SecretStr("py_fastapi"))

    postgres_url: Optional[str] = Field(default=None, description="Full DSN")

    postgres_sync_prefix: str = Field(default="postgresql://")
    postgres_async_prefix: str = Field(default="postgresql+asyncpg://")

    @computed_field
    @property
    def postgres_uri(self) -> str:
        credentials = f"{self.postgres_user}:{self.postgres_password}"
        location = f"{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
        return f"{credentials}@{location}"


###################################################################
### Overall Project Settings
###################################################################
class Settings(AppSettings, LoggerSettings, PostgresSettings, CORSSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=False,
        cache_strings=True,
        extra="ignore",
    )

    environment: Environment = Field(default=Environment.PRODUCTION)


settings = Settings()

__all__ = ["settings"]
