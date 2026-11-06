"""
Application settings loaded from environment variables (and .env).

Why a Settings object instead of os.getenv everywhere?
- Single source of truth for configuration.
- Type validation at startup (fail fast if DATABASE_URL is missing).
- Easy to override in tests via dependency injection.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="NetPulse", alias="APP_NAME")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # Example: postgresql+psycopg://netpulse:netpulse@localhost:5432/netpulse
    database_url: str = Field(alias="DATABASE_URL")

    # CORS origin for the Vite dev server
    frontend_origin: str = Field(default="http://localhost:5173", alias="FRONTEND_ORIGIN")


@lru_cache
def get_settings() -> Settings:
    """Cached so we only parse env vars once per process."""
    return Settings()
