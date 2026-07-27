import requests
from pathlib import Path

URLS = {
    "petrol": "https://www.mypetrolprice.com/petrol-price-in-india.aspx?stateId=11",
    "diesel": "https://www.mypetrolprice.com/diesel-price-in-india.aspx?stateId=11",
    "lpg": "https://www.mypetrolprice.com/lpg-price-in-india.aspx?stateId=11",
    "cng": "https://www.mypetrolprice.com/cng-price-in-india.aspx?stateId=11"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

Path("debug").mkdir(exist_ok=True)

for fuel, url in URLS.items():
    print(f"Downloading {fuel}...")

    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    with open(f"debug/{fuel}.html", "w", encoding="utf-8") as f:
        f.write(r.text)

print("Done.")