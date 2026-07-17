import requests

url = "https://goabagayatdar.com/pricing/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers)

with open("page.html", "w", encoding="utf-8") as f:
    f.write(r.text)

print("HTML saved")
