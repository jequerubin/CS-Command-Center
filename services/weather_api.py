import requests


def test_token(token):
    """
    Validates a Openweatherapi key
    Returns True if the server responds with HTTP 200, False otherwise.
    """
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": "Fullerton", "appid": token},
            timeout=10,
        )
        return response.status_code == 200
    except Exception:
        return False


def fetch_weather(token):
    """
    Fetches current weather for city
    """
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": token, "units": "imperial"},
            timeout=10,
        )
        data = response.json()

        if response.status_code != 200:
            return []

        return{
                "city":        data.get("name", city),
                "temperature": data["main"][["temp"]],
                "conditions":  data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
                "humidity":    data["main"]["humidity"],
                "wind_speed":  data["wind"]["speed"],
            }

    except Exception:
        return []


if __name__ == "__main__":
    token = "PASTE_YOUR_TOKEN_HERE"
    print(test_token(token))
    print(fetch_weather(token))
