import requests

url = "https://www.instagram.com/api/v1/users/web_profile_info/?username=gshclgoa"

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-IG-App-ID": "936619743392459",
    "Referer": "https://www.instagram.com/gshclgoa/"
}

r = requests.get(url, headers=headers, timeout=30)

print("Status:", r.status_code)

with open("instagram_api.json", "w", encoding="utf-8") as f:
    f.write(r.text)

print("Saved instagram_api.json")
