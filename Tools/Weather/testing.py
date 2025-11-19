import asyncio
from weather import get_forecast  # or: from weather import *

async def main():
    forecast = await get_forecast(40.7128, -74.0060)
    print(forecast)

if __name__ == "__main__":
    asyncio.run(main())
