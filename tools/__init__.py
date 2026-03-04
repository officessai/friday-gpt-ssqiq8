"""Utility helpers for dynamically discovering Friday tools."""

from __future__ import annotations

import importlib.util
import inspect
import sys
from pathlib import Path
from types import ModuleType
from typing import Dict, Iterable, Protocol


class Tool(Protocol):
    """Protocol that all Friday tools must follow."""

    name: str
    description: str

    def run(self, query: str) -> str:
        """Execute the tool with the provided query."""


def _iter_tool_modules(tool_dir: Path) -> Iterable[ModuleType]:
    """Yield tool modules discovered inside ``tool_dir``.

    A tool module is any ``*.py`` file that does not start with an underscore.
    The module must define a ``tool`` attribute that satisfies :class:`Tool`.
    """

    for script_path in sorted(tool_dir.glob("[!_]*.py")):
        spec = importlib.util.spec_from_file_location(script_path.stem, script_path)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        yield module


def load_tools(tool_dir: Path) -> Dict[str, Tool]:
    """Load all tools present in ``tool_dir``.

    Returns a dictionary mapping tool names to tool instances. Duplicate tool
    names are ignored in favour of the first definition.
    """

    loaded: Dict[str, Tool] = {}
    for module in _iter_tool_modules(tool_dir):
        candidate = getattr(module, "tool", None)
        if candidate is None:
            continue
        if not hasattr(candidate, "name") or not hasattr(candidate, "run"):
            continue
        name = getattr(candidate, "name")
        if not isinstance(name, str) or not name:
            continue
        if name in loaded:
            continue
        run_callable = getattr(candidate, "run")
        if not callable(run_callable):
            continue
        if inspect.signature(run_callable).parameters.get("query") is None:
            continue
        loaded[name] = candidate  # type: ignore[assignment]
    return loaded


__all__ = ["Tool", "load_tools"]
