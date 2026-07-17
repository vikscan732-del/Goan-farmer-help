
import requests
from bs4 import BeautifulSoup
import json

URL = "https://goabagayatdar.com/pricing/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

data = []

tables = soup.find_all("table")

for table in tables:
    rows = table.find_all("tr")

    for row in rows:
        cols = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]

        if len(cols) >= 2:
            data.append(cols)

with open("prices.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("prices.json created successfully!")
