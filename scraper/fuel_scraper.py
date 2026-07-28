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
    "petrol": "https://www.mypetrolprice.com/11/Fuel-Prices-in-Goa",
    "diesel": "https://www.mypetrolprice.com/11/Fuel-Prices-in-Goa",
    "lpg": "https://www.mypetrolprice.com/11/Fuel-Prices-in-Goa",
    "cng": "https://www.mypetrolprice.com/11/Fuel-Prices-in-Goa"
}


def get_price(text):
    m = re.search(r"([\d.]+)", text)
    if m:
        return float(m.group(1))
    return None


def scrape_fuel(url):
    print(f"\nDownloading: {url}")

    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    with open("goa.html", "w", encoding="utf-8") as f:
    f.write(r.text)

print("Saved goa.html")

    soup = BeautifulSoup(r.text, "lxml")

    result = {}

    cards = soup.find_all("div", class_="SF")

    print("Cards found:", len(cards))

    for card in cards:
        ch = card.find("div", class_="CH")
        txt = card.find("div", class_="txtC")

        if not ch or not txt:
            continue

        city_link = ch.find("a")
        price_tag = txt.find("b")

        if not city_link or not price_tag:
            continue

        city = city_link.get_text(strip=True)
        price = get_price(price_tag.get_text())

        print(city, price)

        if city in ("Margao", "Panjim"):
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

with open(DATA_DIR / "fuel.json", "w", encoding="utf-8") as f:
    json.dump(fuel_data, f, indent=2, ensure_ascii=False)

history_file = DATA_DIR / "fuel-history.json"

history = []

if history_file.exists():
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    except:
        history = []

history = [x for x in history if x["updated"] != fuel_data["updated"]]
history.append(fuel_data)

with open(history_file, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

print("\nDone.")
print(json.dumps(fuel_data, indent=2))
