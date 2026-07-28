import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

URL = "https://www.mypetrolprice.com/11/Fuel-Prices-in-Goa"


def get_price(text):
    m = re.search(r"([\d.]+)", text)
    if m:
        return float(m.group(1))
    return None


def scrape_fuel():
    print("Downloading:", URL)

    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()

    with open("goa.html", "w", encoding="utf-8") as f:
        f.write(r.text)

    print("Saved goa.html")

    soup = BeautifulSoup(r.text, "lxml")

    result = {
        "petrol": {},
        "diesel": {},
        "lpg": {},
        "cng": {}
    }

    cards = soup.find_all("div", class_="SF")

    print("Cards found:", len(cards))

    for card in cards:
        print(card.get_text(" ", strip=True))

    return result

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

scraped = scrape_fuel()

fuel_data = {
    "updated": datetime.now().strftime("%Y-%m-%d"),
    "petrol": scraped["petrol"],
    "diesel": scraped["diesel"],
    "lpg": scraped["lpg"],
    "cng": scraped["cng"]
}

fuel_file = DATA_DIR / "fuel.json"

with open(fuel_file, "w", encoding="utf-8") as f:
    json.dump(fuel_data, f, indent=2, ensure_ascii=False)

print("fuel.json saved")

history_file = DATA_DIR / "fuel-history.json"

history = []

if history_file.exists():
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    except Exception:
        history = []

today = fuel_data["updated"]

history = [item for item in history if item.get("updated") != today]
history.append(fuel_data)

history.sort(key=lambda x: x["updated"])

with open(history_file, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

print("fuel-history.json updated")
print(json.dumps(fuel_data, indent=2))
