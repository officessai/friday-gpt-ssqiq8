"""Tests for the Friday AI workflow modules."""

from __future__ import annotations

import importlib
from datetime import datetime, timezone

import pytest

import module1
import module2
import module3


@pytest.fixture(autouse=True)
def fresh_modules():
    """Reload modules before each test to ensure isolated state."""

    for module in (module1, module2, module3):
        importlib.reload(module)
    yield
    for module in (module1, module2, module3):
        importlib.reload(module)


def test_full_workflow():
    """The happy path should populate each phase object."""

    context = module1.start("Test start-up sequence.")
    assert isinstance(context.started_at, datetime)
    assert context.started_at.tzinfo == timezone.utc
    assert context.message == "Test start-up sequence."

    report = module2.run(message="Test runtime execution.")
    assert report.started_at == context.started_at
    assert report.run_at >= context.started_at
    assert report.status == "operational"
    assert report.message == "Test runtime execution."

    status = module3.boot(message="Test boot confirmation.")
    assert status.ready is True
    assert status.run_report == report
    assert status.booted_at >= report.run_at
    assert status.message == "Test boot confirmation."
    assert status.started_at == context.started_at
    assert status.run_at == report.run_at


def test_get_last_run_report_requires_run():
    """Attempting to fetch a report without running should fail."""

    with pytest.raises(RuntimeError):
        module2.get_last_run_report()


def test_boot_requires_run():
    """Boot should not proceed without a prior run."""

    module1.start()
    with pytest.raises(RuntimeError):
        module3.boot()


def test_start_is_idempotent():
    """Calling ``start`` repeatedly should reuse the first context."""

    first = module1.start("Initial start message.")
    second = module1.start("Second attempt should be ignored.")
    assert first is second
    assert second.message == "Initial start message."
