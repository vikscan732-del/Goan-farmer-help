import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

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
# Website
# -----------------------------
URL = "https://goabagayatdar.com/pricing/"


headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://goabagayatdar.com/",
    "Connection": "keep-alive"
}

# -----------------------------
# Download page
# -----------------------------
response = requests.get(URL, headers=headers, timeout=120)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table")

products = []

today = datetime.now().strftime("%Y-%m-%d")

if table:

    rows = table.find_all("tr")

    for row in rows:

        cols = row.find_all(["th", "td"])

        if len(cols) < 2:
            continue

        name = cols[0].get_text(strip=True)
        price_text = cols[1].get_text(strip=True)

        # Keep only digits and decimal point
        clean = "".join(c for c in price_text if c.isdigit() or c == ".")

        try:
            price = float(clean)
        except:
            continue

        products.append({
            "name": name,
            "price": price
        })

print("Products Found:", len(products))

with open("prices.json", "w", encoding="utf-8") as f:
    json.dump(products, f, indent=4, ensure_ascii=False)

print("prices.json updated.")



# -----------------------------
# Upload with History
# -----------------------------

for item in products:

    docs = list(
        db.collection("products")
        .where("name", "==", item["name"])
        .limit(1)
        .stream()
    )

    current_price = item["price"]

    if docs:

        doc_ref = docs[0].reference
        old = docs[0].to_dict()

        history = old.get("history", [])

        # Remove today's entry if it already exists
        history = [h for h in history if h.get("date") != today]

        # Add today's price
        history.append({
            "date": today,
            "price": current_price
        })

        # Keep only the latest 365 records
        history = sorted(history, key=lambda x: x["date"])
        history = history[-365:]

        prices = [x["price"] for x in history]

        highest = max(prices)
        lowest = min(prices)
        average = round(sum(prices) / len(prices), 2)

        if len(history) >= 2:
            yesterday = history[-2]["price"]
        else:
            yesterday = current_price

        change = round(current_price - yesterday, 2)

        if yesterday != 0:
            change_percent = round((change / yesterday) * 100, 2)
        else:
            change_percent = 0

        doc_ref.update({

            "price": current_price,
            "history": history,

            "highest": highest,
            "lowest": lowest,
            "average": average,

            "yesterdayPrice": yesterday,

            "change": change,
            "changePercent": change_percent,

            "updated": firestore.SERVER_TIMESTAMP

        })

    else:

        history = [{
            "date": today,
            "price": current_price
        }]

        db.collection("products").add({

            "name": item["name"],
            "price": current_price,

            "history": history,

            "highest": current_price,
            "lowest": current_price,
            "average": current_price,

            "yesterdayPrice": current_price,

            "change": 0,
            "changePercent": 0,

            "updated": firestore.SERVER_TIMESTAMP

        })

print("Firestore updated successfully.")
