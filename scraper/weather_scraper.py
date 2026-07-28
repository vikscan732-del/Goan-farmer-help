import requests
import json
from pathlib import Path
from datetime import datetime

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
    result["forecast"].append({
        "date": data["daily"]["time"][i],
        "max": data["daily"]["temperature_2m_max"][i],
        "min": data["daily"]["temperature_2m_min"][i],
        "weather_code": data["daily"]["weather_code"][i]
    })

Path("data").mkdir(exist_ok=True)

with open("data/weather.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print("Weather updated successfully!")
