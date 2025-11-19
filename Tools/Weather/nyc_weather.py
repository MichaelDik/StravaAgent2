"""Helpers to fetch the NYC forecast using the internal weather module."""

from __future__ import annotations

import asyncio

from .weather import get_forecast

NYC_LATITUDE = 40.7128
NYC_LONGITUDE = -74.0060


async def get_nyc_weather_async() -> str:
    """Return the forecast string for New York City."""
    return await get_forecast(NYC_LATITUDE, NYC_LONGITUDE)


def get_nyc_weather() -> str:
    """Sync wrapper so callers don't have to manage asyncio."""
    return asyncio.run(get_nyc_weather_async())


if __name__ == "__main__":
    print(get_nyc_weather())
