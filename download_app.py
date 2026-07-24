import requests

url = "https://anonyig.com/js/app.js?id=fa126ae263832ae8b210a240bd405e9d"

r = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

print("Status:", r.status_code)

with open("app.js", "wb") as f:
    f.write(r.content)

print("Saved app.js")
