"""Core primitives for HuAI v1.

HuAI (Human-Aware Intelligence) is designed around explicit, inspectable flow.
This module defines the data contracts used across planning, execution, and
human-centered RSI semantics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol


class Role(str, Enum):
    """Conversation role used in interaction history."""

    SYSTEM = "system"
    HUMAN = "human"
    ASSISTANT = "assistant"


@dataclass(slots=True)
class Message:
    """A normalized message in the interaction timeline."""

    role: Role
    content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class RSIStatus(str, Enum):
    """Human-centered RSI (Respect, Safety, Intent) evaluation status."""

    PASS = "pass"
    CAUTION = "caution"
    BLOCK = "block"


@dataclass(slots=True)
class RSISignal:
    """Single RSI signal emitted during analysis."""

    dimension: str
    status: RSIStatus
    note: str


@dataclass(slots=True)
class RSIReport:
    """Aggregate RSI report, designed for display and future policy wiring."""

    summary: str
    status: RSIStatus
    signals: List[RSISignal] = field(default_factory=list)


@dataclass(slots=True)
class HuAIContext:
    """Shared runtime context passed through the orchestrated flow."""

    user_input: str
    history: List[Message] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class HuAIPlan:
    """Execution plan with explicit steps and rationale."""

    objective: str
    steps: List[str]
    rationale: str


@dataclass(slots=True)
class HuAIResponse:
    """Final orchestrator output with trace artifacts."""

    text: str
    plan: HuAIPlan
    rsi: RSIReport
    trace: List[str] = field(default_factory=list)


class Analyzer(Protocol):
    """Extension point: produces an RSI report from context."""

    def evaluate(self, context: HuAIContext) -> RSIReport:
        ...


class Planner(Protocol):
    """Extension point: generates explicit actionable plan from context."""

    def build_plan(self, context: HuAIContext, rsi: RSIReport) -> HuAIPlan:
        ...


class Executor(Protocol):
    """Extension point: executes plan and returns a user-facing response."""

    def execute(self, context: HuAIContext, plan: HuAIPlan, rsi: RSIReport) -> str:
        ...
