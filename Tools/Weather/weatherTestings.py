"""Tiny helper to print the NYC forecast request."""

REQUEST = (
    "GET /points/40.7128,-74.0060 HTTP/1.1\n"
    "Host: api.weather.gov\n"
    "User-Agent: weather-app/1.0\n"
    "Accept: application/geo+json"
)


def get_nyc_weather_request() -> str:
    return REQUEST


if __name__ == "__main__":
    print(get_nyc_weather_request())
