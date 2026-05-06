import os
import requests

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")


def test_connection():
    if not WEATHER_API_KEY:
        return False
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": "Fullerton", "appid": WEATHER_API_KEY},
            timeout=10,
        )
        return response.status_code == 200
    except Exception:
        return False


def fetch_weather():
    if not WEATHER_API_KEY:
        return {}
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": "Fullerton", "appid": WEATHER_API_KEY, "units": "imperial"},
            timeout=10,
        )
        data = response.json()

        if response.status_code != 200:
            return {}

        return {
            "city":        data.get("name", "Fullerton"),
            "temperature": data["main"]["temp"],
            "conditions":  data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "humidity":    data["main"]["humidity"],
            "wind_speed":  data["wind"]["speed"],
        }
    except Exception:
        return {}
