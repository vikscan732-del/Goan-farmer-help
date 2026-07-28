³import requests
import json
from pathlib import Path
from datetime import datetime

API_KEY = "goldapi-b6db8a5fa9851cec87ced073b8636dc9-io"  # Replace with your real key

URL = "https://www.goldapi.io/api/XAU/INR"

HEADERS = {
    "x-access-token": API_KEY,
    "Content-Type": "application/json"
}

response = requests.get(URL, headers=HEADERS, timeout=30)
response.raise_for_status()

data = response.json()

result = {
    "updated": datetime.now().strftime("%Y-%m-%d"),
    "gold_24k": data.get("price_gram_24k"),
    "gold_22k": data.get("price_gram_22k"),
    "gold_18k": data.get("price_gram_18k")
}

# Get silver price
silver = requests.get(
    "https://www.goldapi.io/api/XAG/INR",
    headers=HEADERS,
    timeout=30
)
silver.raise_for_status()

silver_data = silver.json()

result["silver_per_gram"] = silver_data.get("price_gram")
result["silver_per_kg"] = silver_data.get("price_kg")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

with open(DATA_DIR / "gold_silver.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(json.dumps(result, indent=2))
