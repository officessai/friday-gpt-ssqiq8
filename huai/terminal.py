"""Readable terminal output for HuAI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .core import RSIReport


@dataclass(slots=True)
class TerminalTheme:
    prefix_info: str = "[HuAI]"
    prefix_step: str = "  →"
    prefix_good: str = "  ✓"
    prefix_warn: str = "  !"


class TerminalRenderer:
    """Human-readable console renderer.

    Intentionally dependency-free to keep HuAI deployable in minimal runtimes.
    """

    def __init__(self, theme: TerminalTheme | None = None) -> None:
        self.theme = theme or TerminalTheme()

    def banner(self, title: str) -> str:
        return f"{self.theme.prefix_info} {title}"

    def step(self, text: str) -> str:
        return f"{self.theme.prefix_step} {text}"

    def success(self, text: str) -> str:
        return f"{self.theme.prefix_good} {text}"

    def warning(self, text: str) -> str:
        return f"{self.theme.prefix_warn} {text}"

    def render_rsi(self, report: RSIReport) -> Iterable[str]:
        yield self.step(f"RSI summary: {report.summary} [{report.status.value}]")
        for signal in report.signals:
            prefix = self.success if signal.status.value == "pass" else self.warning
            yield prefix(f"{signal.dimension}: {signal.note}")
