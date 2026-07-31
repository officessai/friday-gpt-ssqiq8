import sqlite3

from fastapi.testclient import TestClient

from friday_app.main import create_app
from friday_app.settings import get_settings


def test_health_in_demo_mode(monkeypatch) -> None:
    monkeypatch.setenv("AI_PROVIDER", "demo")
    get_settings.cache_clear()
    client = TestClient(create_app())

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["ai_configured"] is True


def test_chat_has_safe_demo_fallback(monkeypatch) -> None:
    monkeypatch.setenv("AI_PROVIDER", "demo")
    get_settings.cache_clear()
    client = TestClient(create_app())

    response = client.post("/api/v1/chat", json={"message": "Prowadzę warsztat"})

    assert response.status_code == 200
    assert response.json()["provider"] == "demo"
    assert "trybie demonstracyjnym" in response.json()["response"]


def test_contact_is_persisted(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    monkeypatch.setenv("AI_PROVIDER", "demo")
    monkeypatch.delenv("SMTP_HOST", raising=False)
    monkeypatch.delenv("SMTP_FROM", raising=False)
    get_settings.cache_clear()
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/contact",
        json={
            "name": "Jan Kowalski",
            "email": "jan@example.com",
            "company": "Firma Testowa",
            "message": "Potrzebuję strony z asystentem AI.",
            "privacy_accepted": True,
            "website": "",
        },
    )

    assert response.status_code == 202
    assert response.json()["delivery"] == "stored"

    with sqlite3.connect(tmp_path / "leads.sqlite3") as connection:
        row = connection.execute("SELECT name, email FROM leads").fetchone()
    assert row == ("Jan Kowalski", "jan@example.com")
