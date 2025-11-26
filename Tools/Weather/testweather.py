"""Helper script for experimenting with ``weather.py`` from the CLI."""

from __future__ import annotations

import asyncio

from weather import get_forecast

NYC_LATITUDE = 40.7128
NYC_LONGITUDE = -74.0060


async def get_todays_weather() -> str:
    """Return only the first forecast period (typically 'Today' or 'Tonight')."""
    forecast = await get_forecast(NYC_LATITUDE, NYC_LONGITUDE)
    if "\n---\n" not in forecast:
        return forecast
    return forecast.split("\n---\n", 1)[0].strip()


def main() -> None:
    """Fetch and print just today's NYC weather."""
    print(asyncio.run(get_todays_weather()))


if __name__ == "__main__":
    main()
