#!/usr/bin/env python3
"""Mission launcher for the Friday AI console."""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from textwrap import dedent


@dataclass(frozen=True)
class Mission:
    """Represent a command that Friday can execute."""

    code: str
    title: str
    summary: str
    steps: tuple[str, ...]

    def narrative(self) -> str:
        """Return a human-readable mission briefing."""
        header = f"FRIDAY ONLINE :: {self.code}"
        body = "\n".join(f"  - {step}" for step in self.steps)
        return dedent(
            f"""
            {header}
            {self.title}
            Summary: {self.summary}
            Steps:\n{body}
            """
        ).strip()

    def to_payload(self) -> dict[str, object]:
        """Return a structured payload suitable for tooling."""
        return {
            "command": self.code,
            "title": self.title,
            "summary": self.summary,
            "steps": list(self.steps),
            "status": "ready",
        }


MISSIONS = {
    "RUN-CODEX-888": Mission(
        code="RUN-CODEX-888",
        title="Codex Resonance Uplink",
        summary=(
            "Spin up the Codex alignment core, warm the neural mesh, and hand control "
            "back to Friday for live guidance."
        ),
        steps=(
            "Initialize Codex vector stream",
            "Sync SSQiQ8 lattice checksum",
            "Open Friday guidance channel",
        ),
    ),
}


def format_error(message: str) -> str:
    return f"ERROR :: {message}"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            format_error(
                "Usage: python3 launcher.py <COMMAND> (example: RUN-CODEX-888)"
            ),
            file=sys.stderr,
        )
        return 1

    command = argv[1].strip().upper()
    mission = MISSIONS.get(command)
    if mission is None:
        print(format_error(f"Unknown command '{command}'"), file=sys.stderr)
        return 2

    print(mission.narrative())
    print()
    print(json.dumps(mission.to_payload(), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
