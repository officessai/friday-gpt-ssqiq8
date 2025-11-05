"""Utilities for starting the Friday AI workflow."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class StartupContext:
    """Information captured when the system is started."""

    started_at: datetime
    message: str


_context: Optional[StartupContext] = None

__all__ = ["StartupContext", "start", "ensure_started", "get_context"]


def start(message: str | None = None) -> StartupContext:
    """Initialise the system and return the startup context.

    Subsequent calls reuse the first created context to prevent duplicated
    initialisation work.  The optional ``message`` argument lets callers
    customise the user-facing notification logged during start-up.
    """

    global _context
    if _context is None:
        startup_message = message or "Friday core warming up."
        _context = StartupContext(
            started_at=datetime.now(timezone.utc), message=startup_message
        )
        logger.info("%s", startup_message)
    else:
        logger.debug("start() called again – reusing existing startup context.")
    return _context


def ensure_started(message: str | None = None) -> StartupContext:
    """Ensure a startup context exists and return it."""

    return start(message) if _context is None else _context


def get_context() -> StartupContext:
    """Return the existing startup context.

    Raises:
        RuntimeError: If :func:`start` has not been called yet.
    """

    if _context is None:
        raise RuntimeError("Friday has not been started yet. Call start() first.")
    return _context
