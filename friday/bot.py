"""Core conversational logic for Friday."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict

from .config import FridayConfig


@dataclass
class FridayBot:
    """Stateful assistant that mimics the Friday wake-word flow."""

    config: FridayConfig
    activated: bool = False
    _commands: Dict[str, Callable[[str], str]] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._commands = {
            "reset": self._handle_reset,
            "wyloguj": self._handle_sleep,
            "spadaj": self._handle_sleep,
            "śpij": self._handle_sleep,
            "spij": self._handle_sleep,
            "dzięki": self._handle_thanks,
            "dzieki": self._handle_thanks,
        }

    # Public API ---------------------------------------------------------
    def handle_message(self, message: str) -> str:
        """Process a single user message and return Friday's reply."""

        text = message.strip()
        if not text:
            return "Halo, daj jakiś temat."

        if self._contains_wake_word(text):
            if self.activated:
                return self.config.already_awake
            self.activated = True
            return self.config.activation_response

        if not self.activated:
            return self.config.quiet_hint

        lowered = text.casefold()
        if lowered in self._commands:
            return self._commands[lowered](text)

        return self._default_response(text)

    # Command handlers ---------------------------------------------------
    def _handle_reset(self, _: str) -> str:
        self.activated = False
        return "Reset zaliczony. Jak coś, wiesz jak mnie zawołać."

    def _handle_sleep(self, _: str) -> str:
        self.activated = False
        return self.config.sleep_response

    def _handle_thanks(self, _: str) -> str:
        return "Nie ma sprawy, ziomek!"

    # Helpers ------------------------------------------------------------
    def _contains_wake_word(self, text: str) -> bool:
        return self.config.wake_word.casefold() in text.casefold()

    def _default_response(self, text: str) -> str:
        if text.endswith("?"):
            return f"Daj mi sekundkę, ogarnę temat: {text}"
        return f"Brzmi kozacko, działamy: {text}"

