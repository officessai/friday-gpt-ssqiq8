"""Business logic for chat completion."""

from dataclasses import dataclass

from friday_app.core.settings import Settings


@dataclass(slots=True)
class ChatResult:
    """Normalized response object from chat service."""

    response: str
    provider: str
    model: str


class ChatService:
    """Service abstraction for LLM chat operations."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def reply(self, message: str) -> ChatResult:
        """Return a deterministic placeholder response.

        This method is intentionally deterministic to keep local development
        and automated tests fast. Replace this implementation with a provider
        adapter (OpenAI/NIM/Google) in production integrations.
        """
        clean_message = message.strip()
        text = f"Friday received: {clean_message}"
        return ChatResult(response=text, provider="local-mock", model=self._settings.default_model)
