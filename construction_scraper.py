import requests
from bs4 import BeautifulSoup

URL = "https://infralens.in/prices/goa"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

print("Downloading construction prices...")

response = requests.get(URL, headers=HEADERS, timeout=30)
response.raise_for_status()

print("Status:", response.status_code)

# Save page for debugging
with open("construction.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("Saved construction.html")

soup = BeautifulSoup(response.text, "html.parser")

categories = soup.select(".cp-cat")

print("Categories found:", len(categories))

for category in categories:
    head = category.select_one(".cp-cat-head")

    if head:
        print("\n========================")
        print(head.get_text(" ", strip=True))

    for row in category.select(".cp-price-row"):
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
