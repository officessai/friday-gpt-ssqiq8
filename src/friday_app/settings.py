"""Environment-backed runtime configuration."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or `.env`."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "OfficeSSAI Friday API"
    app_version: str = "1.0.0"
    environment: Literal["local", "staging", "production"] = "local"
    api_prefix: str = "/api/v1"

    ai_provider: Literal["openai", "azure", "demo"] = "demo"
    ai_model: str = "gpt-5-mini"
    openai_api_key: str | None = None
    azure_openai_api_key: str | None = None
    azure_openai_base_url: str | None = None
    max_output_tokens: int = 400

    contact_email: str = "s.szarpak@officessai.com"
    data_dir: Path = Path("data")
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_from: str | None = None
    smtp_use_tls: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
