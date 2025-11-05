"""Runtime utilities for the Friday AI workflow."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import module1

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunReport:
    """Details about a system run."""

    started_at: datetime
    run_at: datetime
    status: str
    message: str


_last_report: Optional[RunReport] = None

__all__ = ["RunReport", "run", "get_last_run_report"]


def run(status: str = "operational", message: str | None = None) -> RunReport:
    """Execute the system run and store a report."""

    global _last_report
    context = module1.ensure_started()
    run_time = datetime.now(timezone.utc)
    run_message = message or "Friday runtime online."
    _last_report = RunReport(
        started_at=context.started_at,
        run_at=run_time,
        status=status,
        message=run_message,
    )
    logger.info("%s", run_message)
    return _last_report


def get_last_run_report() -> RunReport:
    """Return the most recent run report.

    Raises:
        RuntimeError: If :func:`run` has not been called yet.
    """

    if _last_report is None:
        raise RuntimeError("module2.run() has not been called yet.")
    return _last_report
