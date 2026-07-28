import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from pathlib import Path

URL = "https://www.mypetrolprice.com/4/11/Subsidised_14__2_Kg_LPG-Prices-in-Goa"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_price(text):
    m = re.search(r"([\d]+(?:\.\d+)?)", text)
    if m:
        return float(m.group(1))
    return None

r = requests.get(URL, headers=HEADERS, timeout=30)
r.raise_for_status()

with open("lpg.html", "w", encoding="utf-8") as f:
    f.write(r.text)

soup = BeautifulSoup(r.text, "lxml")

result = {
    "updated": datetime.now().strftime("%Y-%m-%d"),
    "panjim": None,
    "average": None
}

highest = soup.find(id="BC_StateAveragePriceControl_HeigestPrice")
average = soup.find(id="BC_StateAveragePriceControl_AvragePrice")

if highest:
    result["panjim"] = get_price(highest.get_text(" ", strip=True))

if average:
    result["average"] = get_price(average.get_text(" ", strip=True))

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Save today's LPG prices
with open(DATA_DIR / "lpg.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

# Update history
history_file = DATA_DIR / "lpg-history.json"

history = []

if history_file.exists():
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    except Exception:
        history = []

# Remove duplicate entry for today's date
history = [x for x in history if x.get("updated") != result["updated"]]

# Add today's data
history.append(result)

# Sort by date
history.sort(key=lambda x: x["updated"])

# Keep only the latest 365 days
history = history[-365:]

# Save history
with open(history_file, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

print("LPG history updated successfully.")
print(json.dumps(result, indent=2))
