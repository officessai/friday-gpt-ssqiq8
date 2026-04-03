# HuAI Framework v1

Production-quality starter framework for **Human-Aware Intelligence (HuAI)** in Python.

## What is included
- Core classes and typed contracts (`huai/core.py`)
- Explicit orchestration flow (`huai/flow.py`, `huai/orchestrator.py`)
- Human-centered RSI semantics (Respect, Safety, Intent)
- Readable terminal trace output (`huai/terminal.py`)
- Future-ready expansion points (Analyzer / Planner / Executor protocols + hooks)

## Quick start
```bash
python3 examples/run_v1.py
```

## Design goals
1. **Explainability first** — every phase is explicit and traceable.
2. **Safety-aware by default** — RSI analysis runs before planning and execution.
3. **Easy to extend** — swap components without breaking the orchestrator API.
4. **Deployable everywhere** — dependency-free standard library implementation.
