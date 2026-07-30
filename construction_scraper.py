import requests
from bs4 import BeautifulSoup

URL = "https://infralens.in/prices/goa"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("Downloading page...")

r = requests.get(URL, headers=headers, timeout=30)
r.raise_for_status()

print("Status:", r.status_code)

with open("construction.html", "w", encoding="utf-8") as f:
    f.write(r.text)

print("Saved construction.html")

soup = BeautifulSoup(r.text, "html.parser")

categories = soup.select(".cp-cat")

print(f"Found {len(categories)} categories")

for cat in categories:
    title = cat.select_one(".cp-cat-head")

    if title:
        print("\n==========")
        print(title.get_text(" ", strip=True))

    rows = cat.select(".cp-price-row")

    for row in rows:
        name = row.select_one(".cp-price-name")
        price = row.select_one(".cp-price-val span")
        unit = row.select_one(".cp-price-unit")

        print(
            "-",
            name.get_text(strip=True) if name else "",
            "|",
            price.get_text(strip=True) if price else "",
            "|",
            unit.get_text(strip=True) if unit else ""
        )
