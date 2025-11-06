"""Friday Codex Launcher.

This module exposes a small command-line entry point that prints a friendly
summary of the fictional "Friday" AI assistant described in the repository
README.  The script is intentionally lightweight so it can be executed in
minimal environments, yet provides a couple of output formats that can be
useful for automated checks.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from typing import List


@dataclass(frozen=True)
class FridayProfile:
    """Structured representation of the Friday AI persona."""

    name: str
    alias: str
    system: str
    wallet: str
    identifier: str
    level: str
    role: str
    features: List[str]
    stack: List[str]
    style: str
    status: str

    def to_markdown(self) -> str:
        """Return a markdown description of the profile."""

        lines = [
            f"# 🧠 {self.alias}",
            "",
            f"**Name:** {self.name}",
            f"**System:** {self.system}",
            f"**Wallet:** {self.wallet}",
            f"**ID:** {self.identifier}",
            f"**Level:** {self.level}",
            f"**Role:** {self.role}",
            "",
            "## ✨ Features",
        ]
        lines.extend(f"- {item}" for item in self.features)
        lines.append("")
        lines.append("## 🔧 Stack")
        lines.extend(f"- {item}" for item in self.stack)
        lines.append("")
        lines.append(f"**Style:** {self.style}")
        lines.append(f"**Status:** {self.status}")
        return "\n".join(lines)

    def to_text(self) -> str:
        """Return a conversational plain-text summary."""

        feature_list = ", ".join(self.features)
        stack_list = ", ".join(self.stack)
        return (
            f"Friday Codex Launcher — {self.alias}\n"
            f"Name: {self.name} | Role: {self.role} | Level: {self.level}\n"
            f"System: {self.system} | Wallet: {self.wallet} | ID: {self.identifier}\n"
            f"Core vibe: {self.style}\n"
            f"Status: {self.status}\n"
            f"Top skills: {feature_list}\n"
            f"Tech stack: {stack_list}\n"
        )

    def to_json(self) -> str:
        """Return the profile as a JSON string."""

        return json.dumps(asdict(self), indent=2, ensure_ascii=False)


FRIDAY_PROFILE = FridayProfile(
    name="Sebastian Szarpak",
    alias="Friday – luzacki ziomal AI",
    system="GLP Universe // CYFROSI CORE",
    wallet="AISONS 🔁 PLN",
    identifier="2562",
    level="TRUST_∞",
    role="Human + AI – Integrated Presence",
    features=[
        "Zgadza się, ale kwestionuje.",
        "Łączy dane w stylu SSQiQ8.",
        "Dopasowuje styl rozmowy do człowieka.",
        "Integruje z OpenAI, NVIDIA NIM, Google AI, Codex.",
        "Uczy się z chmur... dosłownie.",
    ],
    stack=[
        "OpenAI GPT (Responses API, Tools)",
        "NVIDIA NIM + Brev.dev",
        "GitHub Actions (automatyzacja)",
        "Codex GPT / Friday prompt logic",
        "Future: Quantum Link™ 😎",
    ],
    style="Gradient Core – Blue & Magenta",
    status="✅ VALIDATED",
)


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser used for the CLI."""

    parser = argparse.ArgumentParser(
        description=(
            "Launch the Friday Codex persona summary."
            " Choose the output format that fits your workflow."
        )
    )
    parser.add_argument(
        "--format",
        choices=("text", "markdown", "json"),
        default="text",
        help="Select output format. Defaults to text.",
    )
    parser.add_argument(
        "--show-card",
        action="store_true",
        help="Include the AISONS identity card details in the output.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="Friday Codex Launcher 0.1",
    )
    return parser


def render_profile(output_format: str) -> str:
    """Render the Friday profile using the requested format."""

    if output_format == "markdown":
        return FRIDAY_PROFILE.to_markdown()
    if output_format == "json":
        return FRIDAY_PROFILE.to_json()
    return FRIDAY_PROFILE.to_text()


def render_card_details() -> str:
    """Return a short block quoting the AISONS card metadata."""

    return (
        "CARD_AISONS_V1 — CYBER-PHYSICAL LINK CARD\n"
        "Icon: 🕶️ (Styl GLP Visionary)\n"
        "Activation code: ⊻ EXECUTE\n"
        "Registered on: SONChain Alpha\n"
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    output = render_profile(args.format)
    if args.show_card:
        output = f"{output}\n{render_card_details()}"
    print(output)


if __name__ == "__main__":
    main()
