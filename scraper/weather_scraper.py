import requests
import json
from pathlib import Path
from datetime import datetime

WEATHER = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Cloudy",
    45: "Fog",
    48: "Depositing Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Heavy Drizzle",
    56: "Freezing Drizzle",
    57: "Heavy Freezing Drizzle",
    61: "Light Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    66: "Freezing Rain",
    67: "Heavy Freezing Rain",
    71: "Light Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    77: "Snow Grains",
    80: "Light Rain Showers",
    81: "Moderate Rain Showers",
    82: "Violent Rain Showers",
    85: "Light Snow Showers",
    86: "Heavy Snow Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Hail",
    99: "Severe Thunderstorm"
}

URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=15.4909"
    "&longitude=73.8278"
    "&daily=temperature_2m_max,temperature_2m_min,weather_code"
    "&forecast_days=7"
    "&timezone=Asia/Kolkata"
)

response = requests.get(URL, timeout=30)
response.raise_for_status()

data = response.json()

result = {
    "updated": datetime.now().strftime("%Y-%m-%d"),
    "forecast": []
}

for i in range(len(data["daily"]["time"])):
    code = data["daily"]["weather_code"][i]

    result["forecast"].append({
        "date": data["daily"]["time"][i],
        "max": data["daily"]["temperature_2m_max"][i],
        "min": data["daily"]["temperature_2m_min"][i],
        "weather": WEATHER.get(code, "Unknown"),
        "weather_code": code
    })

Path("data").mkdir(exist_ok=True)

with open("data/weather.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("Weather updated successfully!")
print(json.dumps(result, indent=2))
