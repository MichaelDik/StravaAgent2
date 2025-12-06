import httpx

# will have to figure out how to handle token refreshing
url = "https://www.strava.com/api/v3/athlete/activities?access_token=9a0fac24405bcb092d8b154d637bbacffbdeae5d"

try:
    response = httpx.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    data = response.json()
    print("API Response:")
    print(data)

except httpx.HTTPError as e:
    print(f"Error calling API: {e}")
    if hasattr(e, "response") and e.response is not None:
        print(f"Status Code: {e.response.status_code}")
        print(f"Response: {e.response.text}")
