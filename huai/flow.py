"""Explicit flow definition for HuAI orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, List


class FlowStep(str, Enum):
    """Top-level orchestrator phases."""

    INGEST = "ingest"
    ANALYZE_RSI = "analyze_rsi"
    PLAN = "plan"
    EXECUTE = "execute"
    RESPOND = "respond"


@dataclass(slots=True)
class FlowHook:
    """Hook registration for cross-cutting behavior (telemetry, audit, etc.)."""

    step: FlowStep
    callback: Callable[[FlowStep, str], None]


class FlowRegistry:
    """Simple hook manager to support future expansion without API breakage."""

    def __init__(self) -> None:
        self._hooks: List[FlowHook] = []

    def register(self, hook: FlowHook) -> None:
        self._hooks.append(hook)

    def emit(self, step: FlowStep, event: str) -> None:
        for hook in self._hooks:
            if hook.step == step:
                hook.callback(step, event)
