"""Example Friday tool that delivers corny jokes."""

from __future__ import annotations

import random


class JokeTool:
    name = "joke"
    description = "Opowiada sucharka godnego osiedla."

    def __init__(self) -> None:
        self._jokes = [
            "Dlaczego neuron poszedł do baru? Bo chciał wzmocnić swoje połączenia.",
            "Co mówi data scientist na imprezie? 'Mam model na każdą okazję.'",
            "Dlaczego bot nie kłamie? Bo ma zbyt wiele logów."
        ]

    def run(self, query: str) -> str:
        _ = query  # Friday nie musi wiedzieć wszystkiego.
        return random.choice(self._jokes)


tool = JokeTool()
