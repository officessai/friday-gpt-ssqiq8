"""Mock weather provider for Friday."""

from datetime import datetime


def get_weather(city: str) -> str:
    """Return a lightweight mock weather message for the requested city."""

    today = datetime.now().strftime("%d.%m.%Y")
    return (
        f"{today} – pogoda w {city}: 18°C, delikatny wiatr i pełen chill. "
        "(Mock danych – podłącz realne API, kiedy będziesz chciał/a)."
    )
