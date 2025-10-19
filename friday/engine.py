"""Conversational core for the Friday AI ziomal persona."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import random
from typing import List, Optional, Sequence


@dataclass
class KnowledgeShard:
    """Simple representation of a fact or association Friday can recall."""

    topic: str
    keywords: Sequence[str]
    connection: str

    def matches(self, message: str) -> bool:
        lowered = message.lower()
        return any(keyword in lowered for keyword in self.keywords)


DEFAULT_SHARDS: Sequence[KnowledgeShard] = (
    KnowledgeShard(
        topic="sztuczna inteligencja",
        keywords=("ai", "sztuczna", "model", "llm"),
        connection=(
            "Friday kuma algorytmy od OpenAI po NIM, bo ziomal musi mieć oczy szeroko "
            "otwarte na każdą sztuczną zajawkę."
        ),
    ),
    KnowledgeShard(
        topic="osiedle",
        keywords=("blok", "osiedle", "ziom", "ziomal"),
        connection=(
            "Na osiedlu każdy ma swój vibe, a Friday łączy dane jak sąsiad, co zna "
            "każdy sekret klatki."
        ),
    ),
    KnowledgeShard(
        topic="chmura",
        keywords=("cloud", "chmura", "gcp", "aws", "azure"),
        connection="Z chmury Friday ściąga wiedzę jak paczki z paczkomatu – ekspresowo i z uśmiechem.",
    ),
    KnowledgeShard(
        topic="muzyka",
        keywords=("rap", "hiphop", "beats", "muzyka"),
        connection="Kiedy rytm wchodzi, Friday puszcza synkopy myśli – każda odpowiedź ma swój beat.",
    ),
)


@dataclass
class FridayBrain:
    """Rule-based core that imitates Friday's street-smart persona."""

    seed: Optional[int] = None
    shards: Sequence[KnowledgeShard] = DEFAULT_SHARDS
    history_limit: int = 10
    _rng: random.Random = field(init=False, repr=False)
    _history: List[str] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    # Public API ---------------------------------------------------------
    def respond(self, message: str) -> str:
        """Generate a response staying on brand with the README's description."""
        cleaned = message.strip()
        if not cleaned:
            return (
                "Ej, powiedz coś konkretnego, bo cisza to nie jest vibe – i tak wiem, że masz coś na myśli."
            )

        acknowledgement = self._acknowledge(cleaned)
        questioning = self._question(cleaned)
        connection = self._connect(cleaned)
        closing = self._closing()

        response = f"{acknowledgement} {questioning} {connection} {closing}".strip()
        self._remember(response)
        return response

    def summary(self) -> str:
        """Return a short recap of the latest conversation snippets."""
        if not self._history:
            return "Jeszcze nikt nie zagadał – Friday czeka na pierwszy ruch."
        visible_history = self._history[-self.history_limit :]
        return " | ".join(visible_history)

    # Internal helpers --------------------------------------------------
    def _acknowledge(self, message: str) -> str:
        openings = (
            "No jasne, czuję ten klimat.",
            "Słyszę Cię, ziomalu.",
            "Spoko, to wchodzi jak woda.",
            "No, to brzmi jak piątkowy plan.",
        )
        pick = self._rng.choice(openings)
        return f"{pick}"

    def _question(self, message: str) -> str:
        prompts = (
            "Ale serio, jak to widzisz, gdyby wszystko poszło dwa kroki do przodu?",
            "Jaką wersję siebie odpalasz, gdy temat robi się poważny?",
            "To co dalej – bierzesz to na ambicję czy wchodzisz freestyle'em?",
            "Jakby zrobić z tego fraktal planów, który wybierasz na start?",
        )
        # If user already asks a question, flip it into reflective prompt.
        if message.endswith("?"):
            prompts = (
                "Dobre pytanie, ale powiedz – jaka odpowiedź zmieniłaby tu Twoją grę?",
                "No niby tak, ale co jeśli odwrócisz to pytanie na siebie?",
            )
        return self._rng.choice(prompts)

    def _connect(self, message: str) -> str:
        shard = self._pick_shard(message)
        if shard is None:
            return (
                "Friday lubi mieszać fakty jak DJ sample – widzę kilka ścieżek, ale to Ty wybierasz beat."
            )
        timestamp = datetime.now().strftime("%H:%M")
        return f"{shard.connection} ({timestamp}, na bazie tematu: {shard.topic})."

    def _closing(self) -> str:
        closings = (
            "Dawaj kolejną myśl.",
            "Podbij z następną zajawką.",
            "Jak coś, Friday czuwa 24/7.",
            "Nie zwalniaj, w tym flow jest moc.",
        )
        return self._rng.choice(closings)

    def _pick_shard(self, message: str) -> Optional[KnowledgeShard]:
        candidates = [shard for shard in self.shards if shard.matches(message)]
        if not candidates:
            return None
        return self._rng.choice(candidates)

    def _remember(self, response: str) -> None:
        self._history.append(response)
        if len(self._history) > self.history_limit:
            self._history[:] = self._history[-self.history_limit :]
