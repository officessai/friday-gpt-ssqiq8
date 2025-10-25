from datetime import datetime, timezone
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from echo_agent import EchoAgent, Entry


@pytest.fixture
def fixed_clock():
    moment = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    def _clock():
        return moment

    return _clock


def test_observe_ignores_non_command(fixed_clock):
    agent = EchoAgent(clock=fixed_clock)

    assert agent.observe("Hej, co tam?") is None
    assert list(agent.history()) == []


def test_observe_records_command(fixed_clock):
    agent = EchoAgent(clock=fixed_clock)

    entry = agent.observe("Zarejestruj: Wyprawa rozpoczęta")
    assert isinstance(entry, Entry)
    assert entry.payload == "Wyprawa rozpoczęta"
    assert entry.style == "poetic"
    assert entry.render().endswith("Wyprawa rozpoczęta.")


def test_styles_alternate(fixed_clock):
    agent = EchoAgent(clock=fixed_clock)

    first = agent.observe("Zarejestruj pierwsza fala")
    second = agent.observe("Zarejestruj druga fala")

    assert first.style != second.style


def test_register_direct_payload(fixed_clock):
    agent = EchoAgent(clock=fixed_clock, styles=("documentary",))

    entry = agent.register("Decyzja zachowana")
    assert entry.style == "documentary"
    assert "Decyzja zachowana." in entry.render()


def test_custom_styles_validation(fixed_clock):
    with pytest.raises(ValueError):
        EchoAgent(clock=fixed_clock, styles=())
