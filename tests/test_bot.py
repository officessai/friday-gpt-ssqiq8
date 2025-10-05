"""Unit tests for the FridayBot conversation flow."""
from __future__ import annotations

import unittest

from friday import FridayBot, FridayConfig


class FridayBotTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.config = FridayConfig(
            wake_word="piątka",
            activation_response="Yo, jestem! Czego potrzebujesz?",
            quiet_hint="Friday w trybie cichym.",
            already_awake="Już stoję na warcie.",
            sleep_response="Wracam do bazki.",
        )
        self.bot = FridayBot(self.config)

    def test_requires_activation(self) -> None:
        self.assertEqual(self.bot.handle_message("Hej"), "Friday w trybie cichym.")

    def test_activation_and_followup(self) -> None:
        self.assertEqual(
            self.bot.handle_message("Masz może piĄtkA dla kumpla?"),
            "Yo, jestem! Czego potrzebujesz?",
        )
        self.assertTrue(self.bot.activated)
        self.assertEqual(
            self.bot.handle_message("Ogarniesz mi plan na weekend?"),
            "Daj mi sekundkę, ogarnę temat: Ogarniesz mi plan na weekend?",
        )

    def test_wake_word_when_already_awake(self) -> None:
        self.bot.activated = True
        self.assertEqual(
            self.bot.handle_message("piątka"),
            "Już stoję na warcie.",
        )

    def test_reset_command(self) -> None:
        self.bot.activated = True
        self.assertEqual(
            self.bot.handle_message("reset"),
            "Reset zaliczony. Jak coś, wiesz jak mnie zawołać.",
        )
        self.assertFalse(self.bot.activated)
        self.assertEqual(self.bot.handle_message("Siema"), "Friday w trybie cichym.")

    def test_sleep_command(self) -> None:
        self.bot.activated = True
        self.assertEqual(self.bot.handle_message("ŚPIJ"), "Wracam do bazki.")
        self.assertFalse(self.bot.activated)

    def test_thanks_command(self) -> None:
        self.bot.activated = True
        self.assertEqual(self.bot.handle_message("Dzięki"), "Nie ma sprawy, ziomek!")

    def test_empty_input(self) -> None:
        self.assertEqual(
            self.bot.handle_message("   \t  "),
            "Halo, daj jakiś temat.",
        )


if __name__ == "__main__":
    unittest.main()

