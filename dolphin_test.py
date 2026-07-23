import requests

url = "https://www.dolphinradar.com/web-viewer-for-instagram"

params = {
    "username": "gshclgoa"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, params=params, headers=headers, timeout=30)

print("Status:", r.status_code)
print("Final URL:", r.url)

with open("dolphin.html", "w", encoding="utf-8") as f:
    f.write(r.text)

print("Saved dolphin.html")
