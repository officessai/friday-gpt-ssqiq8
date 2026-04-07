"""Runtime settings for Friday."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-backed app settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Friday API"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    environment: Literal["local", "staging", "production"] = "local"

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    default_model: str = "gpt-4.1-mini"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
