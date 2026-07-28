import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from pathlib import Path

URL = "https://www.mypetrolprice.com/11/Fuel-Prices-in-Goa"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_price(text):
    m = re.search(r"([\d]+(?:\.\d+)?)", text)
    if m:
        return float(m.group(1))
    return None


def scrape_fuel():
    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()

    with open("goa.html", "w", encoding="utf-8") as f:
        f.write(r.text)

    soup = BeautifulSoup(r.text, "lxml")

    result = {
        "petrol": {},
        "diesel": {},
        "lpg": {},
        "cng": {}
    }

    ids = {
        "petrol": [
            "BC_ctl05_CheapestPrice",
            "BC_ctl05_HeigestPrice"
        ],
        "diesel": [
            "BC_ctl11_CheapestPrice",
            "BC_ctl11_HeigestPrice"
        ],
        "autogas": [
            "BC_ctl17_CheapestPrice",
            "BC_ctl17_HeigestPrice"
        ],
        "cng": [
            "BC_ctl23_CheapestPrice",
            "BC_ctl23_HeigestPrice"
        ]
    }

    for fuel, box_ids in ids.items():
        for box_id in box_ids:
            box = soup.find(id=box_id)

            if not box:
                continue

            text = box.get_text(" ", strip=True)

            city = None

            if "Margao" in text:
                city = "Margao"
            elif "Panjim" in text:
                city = "Panjim"

            price = get_price(text)

            if city and price is not None:
                result[fuel][city] = price

    return result


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

fuel_data = {
    "updated": datetime.now().strftime("%Y-%m-%d"),
    **scrape_fuel()
}

with open(DATA_DIR / "fuel.json", "w", encoding="utf-8") as f:
    json.dump(fuel_data, f, indent=2, ensure_ascii=False)

history_file = DATA_DIR / "fuel-history.json"

history = []

if history_file.exists():
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    except Exception:
        history = []

history = [x for x in history if x.get("updated") != fuel_data["updated"]]
history.append(fuel_data)

history.sort(key=lambda x: x["updated"])

with open(history_file, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

print("Done")
print(json.dumps(fuel_data, indent=2))
