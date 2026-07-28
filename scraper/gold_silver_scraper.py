import requests
import json
from pathlib import Path
from datetime import datetime

API_KEY = "goldapi-b6db8a5fa9851cec87ced073b8636dc9-io"

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

result = {
    "updated": datetime.now().strftime("%Y-%m-%d"),

    "gold_24k": gold_data.get("price_gram_24k"),
    "gold_22k": gold_data.get("price_gram_22k"),
    "gold_21k": gold_data.get("price_gram_21k"),
    "gold_20k": gold_data.get("price_gram_20k"),
    "gold_18k": gold_data.get("price_gram_18k"),

    "silver": (
        silver_data.get("price_gram")
        or silver_data.get("price_gram_24k")
        or silver_data.get("price")
    )
}

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# ---------- Save today's data ----------
with open(DATA_DIR / "gold_silver.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

# ---------- Update history ----------
history_file = DATA_DIR / "gold_silver-history.json"

history = []

if history_file.exists():
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    except Exception:
        history = []

# Remove duplicate entry for today's date
history = [x for x in history if x.get("updated") != result["updated"]]

# Add today's prices
history.append(result)

# Sort by date
history.sort(key=lambda x: x["updated"])

# Optional: keep only the latest 365 days
history = history[-365:]

with open(history_file, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

print("Gold API Response:")
print(gold_data)

print("\nSilver API Response:")
print(silver_data)

print("\nFinal JSON:")
print(json.dumps(result, indent=2))

print("\nHistory updated successfully.")
