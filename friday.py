"""Simple CLI wrapper for the Friday assistant persona."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from openai import OpenAI

from tools.joke_tool import get_joke
from tools.weather_tool import get_weather

CONFIG_PATH = Path(__file__).with_name("friday_config.json")


class ConfigError(RuntimeError):
    """Raised when the configuration file cannot be read."""


def load_config(path: Path = CONFIG_PATH) -> Dict[str, Any]:
    """Load the Friday configuration JSON file."""

    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as exc:  # pragma: no cover - defensive
        raise ConfigError(
            f"Brakuje pliku konfiguracyjnego: {path}. Utwórz go, zanim odpalisz Fridaya."
        ) from exc
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        raise ConfigError(f"Nieprawidłowy JSON w pliku: {path}") from exc


def run_friday() -> None:
    """Run the Friday CLI loop."""

    config = load_config()
    client = OpenAI()

    print("👊 Friday gotowy. Napisz 'Podrzuć piątaka', żeby odpalić.")
    while True:
        user_input = input("Ty: ")

        lowered = user_input.lower()

        if config["wake_word"].lower() in lowered:
            print("Friday: Yo, jestem! Czego potrzebujesz?")
        elif "żart" in lowered:
            print("Friday:", get_joke())
        elif "pogoda" in lowered:
            print("Friday:", get_weather(config.get("default_city", "Zwoleń")))
        elif lowered in {"exit", "quit"}:
            print("Friday: Elooo, zamykam się.")
            break
        else:
            response = client.chat.completions.create(
                model=config.get("model", "gpt-4"),
                messages=[
                    {"role": "system", "content": config["instructions"]},
                    {"role": "user", "content": user_input},
                ],
            )
            print("Friday:", response.choices[0].message.content)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    run_friday()
