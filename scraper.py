import requests
from bs4 import BeautifulSoup
import json

url = "https://goabagayatdar.com/pricing/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers, timeout=30)

soup = BeautifulSoup(r.text, "lxml")

table = soup.find("table")

data = []

if table:
    rows = table.find_all("tr")

    for row in rows:
        cols = [td.get_text(" ", strip=True) for td in row.find_all(["th","td"])]
        if cols:
            data.append(cols)

with open("prices.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(data)
