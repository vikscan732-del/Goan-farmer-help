import requests
import json
from pathlib import Path
from datetime import datetime

URL = "https://api.imd.gov.in/api/v1/cityforecast?id=42182"

response = requests.get(URL, timeout=30)
response.raise_for_status()

data = response.json()

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

with open(DATA_DIR / "weather.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Weather data saved successfully.")
