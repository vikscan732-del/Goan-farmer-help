import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

URLS = {
    "petrol": "https://www.mypetrolprice.com/petrol-price-in-india.aspx?stateId=11",
    "diesel": "https://www.mypetrolprice.com/diesel-price-in-india.aspx?stateId=11",
    "lpg": "https://www.mypetrolprice.com/lpg-price-in-india.aspx?stateId=11",
    "cng": "https://www.mypetrolprice.com/cng-price-in-india.aspx?stateId=11"
}


def get_price(text):
    m = re.search(r"₹\s*([\d.]+)", text)
    if m:
        return float(m.group(1))
    return None


def scrape_fuel(url):
    print("Downloading:", url)

    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")

    result = {}

    cards = soup.find_all("div", class_="SF")

    for card in cards:

        city = None
        price = None

        ch = card.find("div", class_="CH")

        if ch:
            a = ch.find("a")
            if a:
                city = a.get_text(strip=True)

        txt = card.find("div", class_="txtC")

        if txt:
            b = txt.find("b")
            if b:
                price = get_price(b.get_text())

        if city in ["Margao", "Panjim"]:
            result[city] = price

    return result

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

fuel_data = {
    "updated": datetime.now().strftime("%Y-%m-%d"),
    "petrol": scrape_fuel(URLS["petrol"]),
    "diesel": scrape_fuel(URLS["diesel"]),
    "lpg": scrape_fuel(URLS["lpg"]),
    "cng": scrape_fuel(URLS["cng"])
}

fuel_file = DATA_DIR / "fuel.json"

with open(fuel_file, "w", encoding="utf-8") as f:
    json.dump(fuel_data, f, indent=2, ensure_ascii=False)

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

print("✓ fuel.json created")
print("✓ fuel-history.json updated")

