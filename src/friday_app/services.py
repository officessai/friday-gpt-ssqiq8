"""Provider and lead-handling services."""

from __future__ import annotations

import html
import logging
import smtplib
import sqlite3
import ssl
from dataclasses import dataclass
from datetime import UTC, datetime
from email.message import EmailMessage
from pathlib import Path
from typing import Any

from friday_app.schemas import ContactRequest
from friday_app.settings import Settings

logger = logging.getLogger(__name__)


class AIServiceError(RuntimeError):
    """A safe, user-facing AI provider failure."""


@dataclass(slots=True)
class ChatResult:
    response: str
    provider: str
    model: str


class ChatService:
    """Small adapter around the OpenAI Responses API."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def reply(self, message: str) -> ChatResult:
        clean_message = message.strip()
        if self.settings.ai_provider == "demo":
            return ChatResult(
                response=(
                    "Działam teraz w trybie demonstracyjnym. Opisz firmę i problem, a przygotuję szkic rozwiązania. "
                    "Pełny model uruchomi się po ustawieniu bezpiecznego klucza na serwerze."
                ),
                provider="demo",
                model=self.settings.ai_model,
            )

        try:
            from openai import APIConnectionError, APIStatusError, OpenAI, RateLimitError
        except ImportError as exc:
            raise AIServiceError("Pakiet OpenAI nie jest zainstalowany na serwerze.") from exc

        client = self._build_client(OpenAI)
        instructions = (
            "Jesteś Friday, asystentem OfficeSSAI. Odpowiadasz po polsku, konkretnie i życzliwie. "
            "Pomagasz małym firmom zrozumieć możliwości stron, automatyzacji i AI. "
            "Nie wymyślaj funkcji ani cen innych niż podane przez użytkownika lub witrynę. "
            f"Gdy potrzebna jest wycena, zaproponuj kontakt: {self.settings.contact_email}."
        )

        try:
            response = client.responses.create(
                model=self.settings.ai_model,
                instructions=instructions,
                input=clean_message,
                max_output_tokens=self.settings.max_output_tokens,
            )
        except RateLimitError as exc:
            raise AIServiceError("Limit modelu został chwilowo osiągnięty. Spróbuj ponownie za moment.") from exc
        except APIConnectionError as exc:
            raise AIServiceError("Nie udało się połączyć z modelem AI.") from exc
        except APIStatusError as exc:
            raise AIServiceError("Dostawca AI odrzucił żądanie.") from exc

        text = (response.output_text or "").strip()
        if not text:
            raise AIServiceError("Model nie zwrócił odpowiedzi.")

        return ChatResult(response=text, provider=self.settings.ai_provider, model=self.settings.ai_model)

    def _build_client(self, client_class: Any) -> Any:
        if self.settings.ai_provider == "azure":
            if not self.settings.azure_openai_api_key or not self.settings.azure_openai_base_url:
                raise AIServiceError("Azure OpenAI nie jest jeszcze skonfigurowany na serwerze.")
            return client_class(
                api_key=self.settings.azure_openai_api_key,
                base_url=self.settings.azure_openai_base_url.rstrip("/") + "/",
            )

        if not self.settings.openai_api_key:
            raise AIServiceError("OpenAI nie jest jeszcze skonfigurowane na serwerze.")
        return client_class(api_key=self.settings.openai_api_key)


class LeadService:
    """Persist contact requests first, then optionally send an SMTP notification."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.db_path = Path(settings.data_dir) / "leads.sqlite3"

    def accept(self, lead: ContactRequest, remote_ip: str | None) -> str:
        self._store(lead, remote_ip)
        if self._smtp_ready():
            try:
                self._send_email(lead)
            except (OSError, smtplib.SMTPException):
                logger.exception("Lead was stored, but SMTP notification failed")
            else:
                return "stored_and_emailed"
        return "stored"

    def _store(self, lead: ContactRequest, remote_ip: str | None) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    company TEXT,
                    message TEXT NOT NULL,
                    remote_ip TEXT
                )
                """
            )
            connection.execute(
                "INSERT INTO leads (created_at, name, email, company, message, remote_ip) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    datetime.now(UTC).isoformat(),
                    lead.name.strip(),
                    str(lead.email),
                    lead.company.strip() if lead.company else None,
                    lead.message.strip(),
                    remote_ip,
                ),
            )
            connection.commit()

    def _smtp_ready(self) -> bool:
        return bool(self.settings.smtp_host and self.settings.smtp_from)

    def _send_email(self, lead: ContactRequest) -> None:
        email = EmailMessage()
        email["Subject"] = f"Nowe zapytanie OfficeSSAI — {lead.name.strip()}"
        email["From"] = self.settings.smtp_from
        email["To"] = self.settings.contact_email
        email["Reply-To"] = str(lead.email)
        email.set_content(
            "\n".join(
                [
                    f"Imię: {lead.name.strip()}",
                    f"E-mail: {lead.email}",
                    f"Firma: {lead.company.strip() if lead.company else '-'}",
                    "",
                    lead.message.strip(),
                ]
            )
        )
        email.add_alternative(
            "<h2>Nowe zapytanie OfficeSSAI</h2>"
            f"<p><strong>Imię:</strong> {html.escape(lead.name.strip())}</p>"
            f"<p><strong>E-mail:</strong> {html.escape(str(lead.email))}</p>"
            f"<p><strong>Firma:</strong> {html.escape(lead.company.strip() if lead.company else '-')}</p>"
            f"<p>{html.escape(lead.message.strip()).replace(chr(10), '<br>')}</p>",
            subtype="html",
        )

        with smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_port, timeout=15) as server:
            if self.settings.smtp_use_tls:
                server.starttls(context=ssl.create_default_context())
            if self.settings.smtp_username and self.settings.smtp_password:
                server.login(self.settings.smtp_username, self.settings.smtp_password)
            server.send_message(email)
