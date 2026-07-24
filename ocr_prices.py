import re
import os
import json
from datetime import datetime
from PIL import Image
import pytesseract

IMAGE = "latest_price.jpg"

print("Loading image...")

img = Image.open(IMAGE)

# Better OCR settings
text = pytesseract.image_to_string(
    img,
    lang="eng",
    config="--oem 3 --psm 6"
)

print("\n========== OCR TEXT ==========")
print(text)

# OCR corrections
FIXES = {
    "Carot": "Carrot",
    "Carot ": "Carrot",
    "Chilly": "Chilli",
    "Chili": "Chilli",
    "Cl beans": "Cluster Beans",
    "CI beans": "Cluster Beans",
    "F beans": "French Beans",
    "Flowers/pc": "Cauliflower",
    "Flower/pc": "Cauliflower",
    "Bhindi": "Bhendi",
    "Capsicum ": "Capsicum"
}

# Emoji map
EMOJI = {
    "Bhendi": "🌿",
    "Cabbage": "🥬",
    "Carrot": "🥕",
    "Cauliflower": "🥦",
    "Cluster Beans": "🫛",
    "French Beans": "🫛",
    "Chilli": "🌶️",
    "Onion": "🧅",
    "Potato": "🥔",
    "Tomato": "🍅",
    "Brinjal": "🍆",
    "Cucumber": "🥒",
    "Pumpkin": "🎃",
    "Bottle Gourd": "🥒",
    "Green Peas": "🫛",
    "Beetroot": "🫜",
    "Radish": "🫜",
    "Spinach": "🥬",
    "Coriander": "🌿",
    "Ginger": "🫚",
    "Garlic": "🧄",
    "Sweet Potato": "🍠",
    "Capsicum": "🫑",
    "Lemon": "🍋",
    "Banana": "🍌"
}

prices = []

for line in text.splitlines():

    line = line.strip()

    if not line:
        continue

    if "GSHCL" in line.upper():
        continue

    line = line.replace("•", "")
    line = line.replace("*", "")
    line = line.replace("—", "-")

    match = re.search(r"(.+?)\s*[-:]\s*(\d{1,3})$", line)

    if not match:
        continue

    name = match.group(1).strip()
    price = int(match.group(2))

    # Apply OCR fixes
    for wrong, correct in FIXES.items():
        if name.lower() == wrong.lower():
            name = correct
            break

    emoji = EMOJI.get(name, "🥗")

    prices.append({
        "name": name,
        "emoji": emoji,
        "price": price,
        "unit": "kg"
    })

# Sort alphabetically
prices.sort(key=lambda x: x["name"])

now = datetime.now()

output = {
    "priceDate": now.strftime("%d %b %Y"),
    "updatedAt": now.strftime("%I:%M %p"),
    "vegetables": prices
}

today = now.strftime("%Y-%m-%d")

# Load history
history = {}

if os.path.exists("history.json"):
    try:
        with open("history.json", "r", encoding="utf-8") as f:
            history = json.load(f)
    except:
        history = {}

# Update history
for veg in prices:

    name = veg["name"]
    price = veg["price"]

    if name not in history:
        history[name] = []

    found = False

    for item in history[name]:
        if item["date"] == today:
            item["price"] = price
            found = True
            break

    if not found:
        history[name].append({
            "date": today,
            "price": price
        })

# Save history
with open("history.json", "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

# Save today's prices
with open("prices.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("\n========== FINAL JSON ==========")
print(json.dumps(output, indent=2, ensure_ascii=False))

print(f"\n✅ Saved {len(prices)} vegetables.")
print("✅ Updated history.json")
print("✅ Updated prices.json")
