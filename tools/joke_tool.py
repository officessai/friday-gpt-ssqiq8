"""Utility to provide quick one-liner jokes for Friday."""

import random

_JOKES = [
    "Czemu programista nie ufa drabinom? Bo zawsze coś kombinują na kolejnych poziomach.",
    "Jak nazywa się rozmowa dwóch serwerów? Ping-pong.",
    "Dlaczego komputer poszedł do lekarza? Bo złapał wirusa z pendrive'a."
]


def get_joke() -> str:
    """Return a random joke in Polish with a tech twist."""

    return random.choice(_JOKES)
