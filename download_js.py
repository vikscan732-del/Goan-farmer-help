import requests

url = "https://anonyig.com/en/instagram-profile-viewer/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(url, headers=headers).text

open("page.html", "w", encoding="utf-8").write(html)

print("Downloaded HTML")
