import requests
import json
from pathlib import Path
from datetime import datetime

API_KEY = "goldapi-b6db8a5fa9851cec87ced073b8636dc9-io"  # Replace with your real API key

HEADERS = {
    "x-access-token": API_KEY,
    "Content-Type": "application/json"
}

# ---------------- Gold ----------------
gold = requests.get(
    "https://www.goldapi.io/api/XAU/INR",
    headers=HEADERS,
    timeout=30
)
gold.raise_for_status()
gold_data = gold.json()

# ---------------- Silver ----------------
silver = requests.get(
    "https://www.goldapi.io/api/XAG/INR",
    headers=HEADERS,
    timeout=30
)
silver.raise_for_status()
silver_data = silver.json()

# Uncomment the next line if you want to see the full API response
print(silver_data)

result = {
    "updated": datetime.now().strftime("%Y-%m-%d"),

    # Gold
    "gold_24k": gold_data.get("price_gram_24k"),
    "gold_22k": gold_data.get("price_gram_22k"),
    "gold_21k": gold_data.get("price_gram_21k"),
    "gold_20k": gold_data.get("price_gram_20k"),
    "gold_18k": gold_data.get("price_gram_18k"),

    # Silver
    "silver": (
        silver_data.get("price_gram")
        or silver_data.get("price_gram_24k")
        or silver_data.get("price")
    )
}

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

with open(DATA_DIR / "gold_silver.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)


print("Gold API Response:")
print(gold_data)

print("\nSilver API Response:")
print(silver_data)

print("\nFinal JSON:")
print(json.dumps(result, indent=2))
