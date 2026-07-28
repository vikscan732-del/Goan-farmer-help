import requests

url = "https://www.mypetrolprice.com/4/11/Subsidised_14__2_Kg_LPG-Prices-in-Goa"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()

with open("lpg.html", "w", encoding="utf-8") as f:
    f.write(r.text)

print("lpg.html saved")
