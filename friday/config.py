"""Utilities for loading Friday's configuration."""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


@dataclass(frozen=True)
class FridayConfig:
    """Runtime configuration for the Friday assistant."""

    wake_word: str = "piątka"
    activation_response: str = "Yo, jestem! Czego potrzebujesz?"
    quiet_hint: str = (
        "Friday w trybie cichym. [Podpowiedź: Brzmi jak gest ziomka, nie jak komenda]"
    )
    already_awake: str = "Jestem na linii, dawaj temat."
    sleep_response: str = "Spoko, wracam do trybu cichego."


_ALLOWED_KEYS: Iterable[str] = (
    "wake_word",
    "activation_response",
    "quiet_hint",
    "already_awake",
    "sleep_response",
)


def _normalise_config(raw: Dict[str, Any]) -> Dict[str, str]:
    """Filter and normalise values loaded from JSON."""

    normalised: Dict[str, str] = {}
    for key in _ALLOWED_KEYS:
        if key not in raw:
            continue
        value = raw[key]
        if not isinstance(value, str):
            raise TypeError(f"Config value '{key}' must be a string, got {type(value)!r}.")
        normalised[key] = value.strip()
    return normalised


def load_config(path: Optional[Path] = None) -> FridayConfig:
    """Load a configuration file if it exists, otherwise use defaults."""

    defaults = FridayConfig()
    config_data = asdict(defaults)

    candidate: Optional[Path]
    if path is not None:
        candidate = Path(path)
        candidates = [candidate]
    else:
        candidates = [Path("config.json")]

    for candidate in candidates:
        if not candidate.is_file():
            continue
        with candidate.open("r", encoding="utf-8") as fh:
            raw = json.load(fh)
        if not isinstance(raw, dict):
            raise TypeError("Config file must contain a JSON object with string values.")
        config_data.update(_normalise_config(raw))
        break

    return FridayConfig(**config_data)

