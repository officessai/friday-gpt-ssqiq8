"""API router composition."""

from fastapi import APIRouter

from friday_app.api.routes.chat import router as chat_router
from friday_app.api.routes.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(chat_router, tags=["chat"])
