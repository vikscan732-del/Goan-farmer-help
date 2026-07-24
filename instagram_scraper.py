import requests
import json

url = "https://europe-west3-storyviewer-7a64d.cloudfunctions.net/getInstagramData"

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

print("Fetching latest post...")

response = requests.post(url, json=payload, headers=headers)

print("Status:", response.status_code)

response.raise_for_status()

data = response.json()

with open("latest_post.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Saved latest_post.json")
