import requests
from bs4 import BeautifulSoup
import json

URL = "https://goabagayatdar.com/pricing/"

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 16; I2219 Build/BP2A.250605.031.A3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.7871.46 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://goabagayatdar.com/",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1"
}

response = requests.get(URL, headers=headers, timeout=30)

print("Status:", response.status_code)
print("Length:", len(response.text))

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table")

data = []

if table:
    rows = table.find_all("tr")

    for row in rows:
        cols = row.find_all(["th", "td"])
        if cols:
            data.append([c.get_text(strip=True) for c in cols])

print("Rows found:", len(data))

with open("prices.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("prices.json created successfully!")
