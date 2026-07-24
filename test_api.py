import json
import requests

URL = "https://europe-west3-storyviewer-7a64d.cloudfunctions.net/getInstagramData"

payload = {
    "data": {
        "endpoint": "/v1.2/posts",
        "params": {
            "username_or_id_or_url": "gshclgoa",
            "count": 1
        }
    }
}

headers = {
    "Content-Type": "application/json"
}

print("Fetching latest Instagram post...")

r = requests.post(URL, json=payload, headers=headers, timeout=30)

print("Status Code:", r.status_code)

r.raise_for_status()

data = r.json()

with open("latest_post.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Saved latest_post.json")
