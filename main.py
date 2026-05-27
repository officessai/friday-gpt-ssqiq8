"""Command-line entry point for the Friday project overview.

This module provides a simple executable script that mirrors the
high-level details from the project's README.  It is intentionally
lightweight so that `python main.py` offers an immediate way to learn
what Friday is about without opening the README manually.
"""

from __future__ import annotations

import textwrap
from typing import Iterable


def _section(title: str, lines: Iterable[str]) -> str:
    """Format a titled section with bullet points or paragraphs.

    Args:
        title: Heading for the section.
        lines: Collection of text entries to include. Bullet markers are
            added only if the string does not already start with a dash.
    """

    formatted_lines = []
    for line in lines:
        prefix = "- " if not line.lstrip().startswith("-") else ""
        formatted_lines.append(f"{prefix}{line}")
    body = "\n".join(formatted_lines)
    return f"{title}\n{textwrap.indent(body, '  ')}"


def main() -> None:
    """Print a friendly overview of the Friday project."""

    intro = textwrap.dedent(
        """
        🧠 Friday – luzacki ziomal AI

        "Podrzuć piątaka" – i Friday się budzi.
        Stworzony przez Sebastiana Szarpaka, Friday to Twój osobisty AI ziomal,
        który myśli fraktalnie, gada jak ziomek z osiedla i rozumie więcej niż
        by się wydawało.
        """
    ).strip()

    capabilities = [
        "Zgadza się, ale kwestionuje.",
        "Łączy dane w stylu SSQiQ8.",
        "Dopasowuje styl rozmowy do człowieka.",
        "Integruje z OpenAI, NVIDIA NIM, Google AI, Codex.",
        "Uczy się z chmur... dosłownie.",
    ]

    stack = [
        "OpenAI GPT (Responses API, Tools)",
        "NVIDIA NIM + Brev.dev",
        "GitHub Actions (automatyzacja)",
        "Codex GPT / Friday prompt logic",
        "Future: Quantum Link™ 😎",
    ]

    license_text = "MIT – bierz, używaj, rozwijaj. Zostaw kredyt dla Sebastiana."

    sections = [
        intro,
        _section("✨ Co potrafi?", capabilities),
        _section("🔧 Stack technologiczny", stack),
        _section("🔓 Licencja", [license_text]),
        "—\nWersja 0.1 – Friday jeszcze się uczy, ale już robi wrażenie!",
    ]

    print("\n\n".join(sections))


if __name__ == "__main__":
    main()
