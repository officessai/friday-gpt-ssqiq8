"""Chat endpoints."""

from fastapi import APIRouter, Depends

from friday_app.core.settings import Settings, get_settings
from friday_app.schemas.chat import ChatRequest, ChatResponse
from friday_app.services.chat_service import ChatService

router = APIRouter()


def get_chat_service(settings: Settings = Depends(get_settings)) -> ChatService:
    """Dependency provider for chat service."""
    return ChatService(settings)


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, service: ChatService = Depends(get_chat_service)) -> ChatResponse:
    """Generate a response from Friday."""
    result = service.reply(payload.message)
    return ChatResponse(response=result.response, provider=result.provider, model=result.model)
