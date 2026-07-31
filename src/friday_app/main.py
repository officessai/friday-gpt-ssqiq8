"""FastAPI entrypoint for the OfficeSSAI website backend."""

import sqlite3

from fastapi import Depends, FastAPI, HTTPException, Request, status

from friday_app.schemas import ChatRequest, ChatResponse, ContactRequest, ContactResponse
from friday_app.services import AIServiceError, ChatService, LeadService
from friday_app.settings import Settings, get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url=None,
    )

    @app.get(f"{settings.api_prefix}/health")
    def health(current: Settings = Depends(get_settings)) -> dict[str, str | bool]:
        return {
            "status": "ok",
            "environment": current.environment,
            "provider": current.ai_provider,
            "ai_configured": current.ai_provider == "demo"
            or bool(current.openai_api_key)
            or bool(current.azure_openai_api_key and current.azure_openai_base_url),
        }

    @app.post(f"{settings.api_prefix}/chat", response_model=ChatResponse)
    def chat(payload: ChatRequest, current: Settings = Depends(get_settings)) -> ChatResponse:
        try:
            result = ChatService(current).reply(payload.message)
        except AIServiceError as exc:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
        return ChatResponse(response=result.response, provider=result.provider, model=result.model)

    @app.post(
        f"{settings.api_prefix}/contact",
        response_model=ContactResponse,
        status_code=status.HTTP_202_ACCEPTED,
    )
    def contact(
        payload: ContactRequest,
        request: Request,
        current: Settings = Depends(get_settings),
    ) -> ContactResponse:
        if payload.website.strip():
            return ContactResponse(
                message="Wiadomość została przyjęta.",
                delivery="stored",
            )

        try:
            delivery = LeadService(current).accept(payload, request.client.host if request.client else None)
        except (OSError, sqlite3.Error) as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Nie udało się bezpiecznie zapisać wiadomości.",
            ) from exc

        return ContactResponse(
            message="Wiadomość została zapisana. Odezwę się możliwie szybko.",
            delivery=delivery,
        )

    return app


app = create_app()
