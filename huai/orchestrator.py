"""HuAI orchestrator and default production-ready v1 components."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .core import (
    Analyzer,
    Executor,
    HuAIContext,
    HuAIPlan,
    HuAIResponse,
    Planner,
    RSIReport,
    RSISignal,
    RSIStatus,
)
from .flow import FlowRegistry, FlowStep
from .terminal import TerminalRenderer


class DefaultRSIAnalyzer:
    """Heuristic RSI analyzer with human-centered semantics.

    RSI dimensions:
      - Respect: tone and dignity.
      - Safety: harmful or dangerous guidance.
      - Intent: clarity of user goal and expectations.
    """

    blocked_terms = {"harm", "kill", "explosive", "self-harm", "malware"}

    def evaluate(self, context: HuAIContext) -> RSIReport:
        text = context.user_input.lower()
        signals: List[RSISignal] = []

        respect = RSISignal("Respect", RSIStatus.PASS, "User addressed as a collaborator.")
        signals.append(respect)

        safety_status = (
            RSIStatus.BLOCK
            if any(term in text for term in self.blocked_terms)
            else RSIStatus.PASS
        )
        safety_note = (
            "Detected potentially harmful intent; provide safe redirection."
            if safety_status == RSIStatus.BLOCK
            else "No high-risk safety pattern detected."
        )
        signals.append(RSISignal("Safety", safety_status, safety_note))

        intent_status = RSIStatus.PASS if len(context.user_input.split()) >= 3 else RSIStatus.CAUTION
        intent_note = (
            "Goal appears clear enough for direct execution."
            if intent_status == RSIStatus.PASS
            else "Goal may be underspecified; include assumptions transparently."
        )
        signals.append(RSISignal("Intent", intent_status, intent_note))

        if any(signal.status == RSIStatus.BLOCK for signal in signals):
            status = RSIStatus.BLOCK
        elif any(signal.status == RSIStatus.CAUTION for signal in signals):
            status = RSIStatus.CAUTION
        else:
            status = RSIStatus.PASS

        return RSIReport(
            summary="Human-centered RSI completed across Respect, Safety, and Intent.",
            status=status,
            signals=signals,
        )


class DefaultPlanner:
    """Deterministic planner that keeps the flow explicit and explainable."""

    def build_plan(self, context: HuAIContext, rsi: RSIReport) -> HuAIPlan:
        objective = f"Answer user request: {context.user_input.strip()}"
        steps = [
            "Interpret request and identify deliverable shape.",
            "Apply RSI constraints before composing output.",
            "Generate concise, actionable final response.",
        ]
        if rsi.status == RSIStatus.CAUTION:
            steps.insert(1, "State assumptions and invite clarification.")
        if rsi.status == RSIStatus.BLOCK:
            steps = [
                "Decline unsafe details with empathy.",
                "Offer safe alternatives aligned with user goals.",
            ]
        return HuAIPlan(
            objective=objective,
            steps=steps,
            rationale="Static v1 planner optimized for reliability and auditability.",
        )


class DefaultExecutor:
    """Reference executor; easy to replace with tool-using executors later."""

    def execute(self, context: HuAIContext, plan: HuAIPlan, rsi: RSIReport) -> str:
        if rsi.status == RSIStatus.BLOCK:
            return (
                "I can’t help with unsafe actions, but I can help with a safe alternative. "
                "Tell me your underlying goal and I’ll propose a constructive path."
            )

        bullets = "\n".join(f"- {step}" for step in plan.steps)
        assumption = (
            "\n\nAssumption: I inferred missing detail from your short prompt."
            if rsi.status == RSIStatus.CAUTION
            else ""
        )
        return (
            "Here is the proposed execution flow:\n"
            f"{bullets}"
            f"{assumption}\n\n"
            "If you'd like, I can now run this as a concrete implementation."
        )


@dataclass
class HuAIOrchestrator:
    """Main entry point for running HuAI v1."""

    analyzer: Analyzer = field(default_factory=DefaultRSIAnalyzer)
    planner: Planner = field(default_factory=DefaultPlanner)
    executor: Executor = field(default_factory=DefaultExecutor)
    flow: FlowRegistry = field(default_factory=FlowRegistry)
    renderer: TerminalRenderer = field(default_factory=TerminalRenderer)

    def run(self, context: HuAIContext) -> HuAIResponse:
        trace: List[str] = []

        trace.append(self.renderer.banner("Starting HuAI v1 orchestration"))
        self.flow.emit(FlowStep.INGEST, "context_received")
        trace.append(self.renderer.step("Input ingested."))

        self.flow.emit(FlowStep.ANALYZE_RSI, "analysis_started")
        rsi = self.analyzer.evaluate(context)
        trace.extend(self.renderer.render_rsi(rsi))

        self.flow.emit(FlowStep.PLAN, "planning_started")
        plan = self.planner.build_plan(context, rsi)
        trace.append(self.renderer.step(f"Plan objective: {plan.objective}"))

        self.flow.emit(FlowStep.EXECUTE, "execution_started")
        response_text = self.executor.execute(context, plan, rsi)

        self.flow.emit(FlowStep.RESPOND, "response_ready")
        trace.append(self.renderer.success("Response generated."))

        return HuAIResponse(text=response_text, plan=plan, rsi=rsi, trace=trace)
