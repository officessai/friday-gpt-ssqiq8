"""Boot sequence helpers for the Friday AI workflow."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING

import module2

logger = logging.getLogger(__name__)

if TYPE_CHECKING:  # pragma: no cover - import for type checkers only
    from module2 import RunReport


@dataclass(frozen=True)
class BootStatus:
    """A snapshot of the system boot state."""

    run_report: "RunReport"
    booted_at: datetime
    ready: bool
    message: str

    @property
    def started_at(self) -> datetime:
        """Shortcut to the startup timestamp."""

        return self.run_report.started_at

    @property
    def run_at(self) -> datetime:
        """Shortcut to the runtime timestamp."""

        return self.run_report.run_at


__all__ = ["BootStatus", "boot"]


def boot(message: str | None = None) -> BootStatus:
    """Complete the boot sequence using the latest run report."""

    report = module2.get_last_run_report()
    boot_message = message or "Friday AI fully operational."
    status = BootStatus(
        run_report=report,
        booted_at=datetime.now(timezone.utc),
        ready=True,
        message=boot_message,
    )
    logger.info("%s", boot_message)
    return status
