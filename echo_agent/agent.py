"""Implements the ECHO reflective recorder agent."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from itertools import cycle
from typing import Callable, Iterable, List, Optional, Sequence


@dataclass
class Entry:
    """Single note captured by the ECHO agent."""

    timestamp: datetime
    payload: str
    style: str

    def render(self) -> str:
        """Render the entry as a human-readable string."""
        stamp = self.timestamp.replace(microsecond=0).isoformat()
        if self.style == "poetic":
            return f"[{stamp}Z] Echo zapisuje ciszę chwili: {self.payload}."
        return f"[{stamp}Z] Protokół notuje zdarzenie: {self.payload}."


class EchoAgent:
    """Cichy obserwator GLPU.

    The agent only records statements that begin with the "Zarejestruj" command.
    Entries are formatted in a neutral poetic or documentary tone.
    """

    def __init__(
        self,
        *,
        clock: Callable[[], datetime] | None = None,
        styles: Sequence[str] | None = None,
    ) -> None:
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        if styles is None:
            style_sequence: Sequence[str] = ("poetic", "documentary")
        elif len(styles) == 0:
            raise ValueError("styles must contain at least one entry")
        else:
            style_sequence = styles
        self._styles = cycle(style_sequence)
        self._entries: List[Entry] = []

    @staticmethod
    def _extract_payload(message: str) -> Optional[str]:
        keyword = "zarejestruj"
        stripped = message.strip()
        if not stripped.lower().startswith(keyword):
            return None
        payload = stripped[len(keyword) :].lstrip(" :")
        return payload or None

    def register(self, payload: str) -> Entry:
        """Register payload directly without keyword parsing."""
        timestamp = self._clock()
        style = next(self._styles)
        entry = Entry(timestamp=timestamp, payload=payload, style=style)
        self._entries.append(entry)
        return entry

    def observe(self, message: str) -> Optional[Entry]:
        """Process an incoming message and register it if requested."""
        payload = self._extract_payload(message)
        if payload is None:
            return None
        return self.register(payload)

    def history(self) -> Iterable[Entry]:
        """Iterate over stored entries in chronological order."""
        return tuple(self._entries)

    def clear(self) -> None:
        """Remove all stored entries."""
        self._entries.clear()
