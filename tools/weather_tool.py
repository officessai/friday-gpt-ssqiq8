"""Mock weather tool used to demonstrate the Friday tool API."""

from __future__ import annotations

import datetime as _dt


class WeatherTool:
    name = "weather"
    description = "Zgaduje pogodę na podstawie kosmicznych wibracji."

    def run(self, query: str) -> str:
        location = query.strip() or "Twoja miejscówka"
        today = _dt.datetime.now().strftime("%A")
        vibe = "słonecznie" if len(location) % 2 == 0 else "pochmurno z błyskiem inspiracji"
        return (
            f"{location}: {vibe}. Dzień jak złoto, bo jest {today}."
            " Zawsze możesz wyjść na balkon i potwierdzić."
        )


tool = WeatherTool()
