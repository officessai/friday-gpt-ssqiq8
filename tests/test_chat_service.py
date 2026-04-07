from friday_app.core.settings import Settings
from friday_app.services.chat_service import ChatService


def test_chat_service_replies_with_trimmed_message() -> None:
    settings = Settings()
    service = ChatService(settings)

    result = service.reply("  siema  ")

    assert result.response == "Friday received: siema"
    assert result.provider == "local-mock"
    assert result.model == settings.default_model
