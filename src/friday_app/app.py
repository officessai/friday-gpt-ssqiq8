"""Application factory for Friday."""

from fastapi import FastAPI

from friday_app.api.router import api_router
from friday_app.core.settings import get_settings


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url="/redoc" if settings.environment != "production" else None,
    )
    app.include_router(api_router, prefix=settings.api_prefix)

    return app
