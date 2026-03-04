"""Utility helpers for returning friendly jokes."""
from __future__ import annotations

import random
from typing import Iterable, Sequence

JOKES: tuple[str, ...] = (
    "Dlaczego programista nie może grać w karty? Bo ciągle liczy od zera.",
    "Jak się nazywa programista po 40? Senior developer.",
    "Zepsuł się serwer – modlimy się do Stack Overflow.",
)


def _ensure_sequence(jokes: Iterable[str]) -> Sequence[str]:
    """Return a sequence for ``random.choice`` regardless of the iterable type."""
    if isinstance(jokes, Sequence):
        return jokes
    return tuple(jokes)


def get_joke(jokes: Iterable[str] = JOKES, rng: random.Random | None = None) -> str:
    """Return a random joke from ``jokes``.

    Parameters
    ----------
    jokes:
        Iterable with available jokes. Defaults to :data:`JOKES`.
    rng:
        Optional random number generator compatible with :class:`random.Random`.
        When provided the generator is used instead of :func:`random.choice`.

    Returns
    -------
    str
        Randomly chosen joke.

    Raises
    ------
    ValueError
        If the iterable of jokes is empty.
    """

    choices = _ensure_sequence(jokes)
    if not choices:
        raise ValueError("jokes collection must not be empty")

    picker = rng.choice if rng is not None else random.choice
    return picker(choices)
