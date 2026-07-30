import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://infralens.in/prices/goa"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def fix_text(text):
    """Fix broken UTF-8 characters like â¹ -> ₹"""
    if not text:
        return ""
    try:
        return text.encode("latin1").decode("utf-8")
    except Exception:
        return text


print("Downloading construction prices...")

response = requests.get(URL, headers=HEADERS, timeout=30)
response.raise_for_status()

# Force UTF-8 decoding
response.encoding = "utf-8"

soup = BeautifulSoup(response.text, "html.parser")

categories = []

for cat in soup.select(".cp-cat"):

    head = cat.select_one(".cp-cat-head")
    if not head:
        continue

    category_name = fix_text(head.get_text(" ", strip=True))

    items = []

    for row in cat.select(".cp-price-row"):

        name = row.select_one(".cp-price-name")
        price = row.select_one(".cp-price-val span")
        unit = row.select_one(".cp-price-unit")

        items.append({
            "name": fix_text(name.get_text(strip=True)) if name else "",
            "price": fix_text(price.get_text(strip=True)) if price else "",
            "unit": fix_text(unit.get_text(strip=True)) if unit else ""
        })

    categories.append({
        "category": category_name,
        "items": items
    })

# Don't overwrite existing file if nothing was scraped
if len(categories) == 0:
    print("⚠️ No construction materials found.")
    print("⚠️ Keeping existing construction.json")
    exit(0)

os.makedirs("data", exist_ok=True)

output = {
    "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_categories": len(categories),
    "categories": categories
}

with open("data/construction.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("✅ Saved data/construction.json")
print("✅ Categories:", len(categories))
