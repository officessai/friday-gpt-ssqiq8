"""Friday AI command-line interface.

This module wires together the Friday persona configuration with a collection
of pluggable tools that live inside the ``tools`` package.
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

from tools import Tool, load_tools


CONFIG_PATH = Path("friday_config.json")
TOOLS_DIR = Path("tools")


@dataclass
class FridayConfig:
    """Dataclass representing the Friday persona configuration."""

    name: str
    greeting: str
    filler_phrases: List[str]
    acknowledgement_phrases: List[str]
    vibe_descriptions: List[str]
    default_responses: List[str]

    @classmethod
    def from_json(cls, path: Path) -> "FridayConfig":
        with path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
        return cls(
            name=payload.get("name", "Friday"),
            greeting=payload.get("greeting", "Yo, ziomal!"),
            filler_phrases=payload.get("filler_phrases", []),
            acknowledgement_phrases=payload.get("acknowledgement_phrases", []),
            vibe_descriptions=payload.get("vibe_descriptions", []),
            default_responses=payload.get("default_responses", []),
        )


class Friday:
    """Simple conversational agent that mimics the Friday persona."""

    def __init__(self, config: FridayConfig, tools: Dict[str, Tool]):
        self.config = config
        self.tools = tools
        random.seed()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def intro(self) -> str:
        vibe = random.choice(self.config.vibe_descriptions)
        return f"{self.config.greeting} {vibe}"

    def respond(self, message: str) -> str:
        message = message.strip()
        if not message:
            return random.choice(self.config.default_responses)

        if message.startswith("/help"):
            return self._render_help()
        if message.startswith("/"):
            return self._attempt_tool_execution(message)

        acknowledgement = random.choice(self.config.acknowledgement_phrases)
        filler = random.choice(self.config.filler_phrases)
        summary = self._summarise(message)
        return f"{acknowledgement} {summary} {filler}".strip()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _summarise(self, message: str) -> str:
        """Very small summariser that extracts key words."""

        words = [word for word in message.split() if len(word) > 3]
        if not words:
            return random.choice(self.config.default_responses)
        highlighted = ", ".join(sorted(set(words), key=str.lower)[:3])
        return f"Słyszę: {highlighted}."

    def _render_help(self) -> str:
        if not self.tools:
            return "Brak narzędzi na pokładzie, ale Friday dalej nadaje."
        lines = ["Dostępne narzędzia:"]
        for tool in self.tools.values():
            lines.append(f"/{tool.name} – {tool.description}")
        return "\n".join(lines)

    def _attempt_tool_execution(self, message: str) -> str:
        parts = message[1:].split(maxsplit=1)
        tool_name = parts[0]
        query = parts[1] if len(parts) > 1 else ""
        tool = self.tools.get(tool_name)
        if tool is None:
            return f"Nie znam komendy /{tool_name}. Rzuć /help po listę narzędzi."
        try:
            result = tool.run(query=query)
        except Exception as exc:  # pragma: no cover - defensive
            return f"Ej, coś nie pykło z narzędziem /{tool_name}: {exc}"
        acknowledgement = random.choice(self.config.acknowledgement_phrases)
        return f"{acknowledgement} {result}".strip()


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Friday AI ziomal CLI")
    parser.add_argument(
        "prompt",
        nargs="*",
        help="Opcjonalna wiadomość do Fridaya. Jeśli pominięta, uruchamia interaktywny tryb.",
    )
    return parser


def run_cli(friday: Friday, prompt: Iterable[str]) -> None:
    if prompt:
        message = " ".join(prompt)
        print(friday.respond(message))
        return

    print(friday.intro())
    print("Napisz coś (albo 'exit' żeby skończyć). Komendy narzędzi zaczynaj od '/'.")
    while True:
        try:
            user_input = input("Ty: ")
        except EOFError:  # pragma: no cover - interactive convenience
            print()
            break
        if user_input.strip().lower() in {"exit", "quit"}:
            break
        print(f"Friday: {friday.respond(user_input)}")


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    config = FridayConfig.from_json(CONFIG_PATH)
    tool_map = load_tools(TOOLS_DIR)
    friday = Friday(config=config, tools=tool_map)
    run_cli(friday, args.prompt)


if __name__ == "__main__":  # pragma: no cover - entrypoint guard
    main()
