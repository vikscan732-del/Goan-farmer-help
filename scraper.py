import requests
from bs4 import BeautifulSoup
import json
import os

import firebase_admin
from firebase_admin import credentials, firestore

# -----------------------------
# Firebase Setup
# -----------------------------
service_account = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])

cred = credentials.Certificate(service_account)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# -----------------------------
# Website to Scrape
# -----------------------------
URL = "https://goabagayatdar.com/pricing/"

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://goabagayatdar.com/"
}

# -----------------------------
# Download Page
# -----------------------------
response = requests.get(URL, headers=headers, timeout=120)

print("Status:", response.status_code)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table")

data = []

if table:
    rows = table.find_all("tr")

    for row in rows:
        cols = row.find_all(["th", "td"])

        if len(cols) >= 2:

            name = cols[0].get_text(strip=True)
            price = cols[1].get_text(strip=True)

            item = {
                "name": name,
                "price": price
            }

            data.append(item)

print("Rows Found:", len(data))

# -----------------------------
# Save JSON
# -----------------------------
with open("prices.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("prices.json created successfully!")

# -----------------------------
# Upload to Firestore
# -----------------------------
for item in data:
    db.collection("products").add({
        "name": item["name"],
        "price": item["price"],
        "updated": firestore.SERVER_TIMESTAMP
    })

print("Firestore updated successfully!")
