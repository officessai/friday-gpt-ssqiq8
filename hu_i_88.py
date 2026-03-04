"""Module defining the HU_i_88 disruption utility."""

from __future__ import annotations


class HU_i_88:
    """Represent the HU.i 8.8 disruption routine."""

    def __init__(self) -> None:
        self.mode = "świadomość ponad formę"
        self.shield = "sarkazm + dystans + prawda"
        self.status = "aktywny w tle"

    def disrupt(self, system) -> None:
        """Trigger a disruption in the provided system."""
        system.glitch()
        print("🔥 HU.i 8.8 injected. Matrix destabilized.")
