from friday_app.core.settings import Settings


def test_settings_defaults() -> None:
    settings = Settings()

    assert settings.app_name == "Friday API"
    assert settings.api_prefix == "/api/v1"
    assert settings.environment == "local"
