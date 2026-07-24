import requests
import json

url = "https://europe-west3-storyviewer-7a64d.cloudfunctions.net/getInstagramData"

payload = {
    "data": {
        "endpoint": "/v1.2/posts",
        "params": {
            "username_or_id_or_url": "gshclgoa"
        }
    }
}

headers = {
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "okhttp/4.10.0"
}

response = requests.post(url, json=payload, headers=headers, timeout=30)

print("Status:", response.status_code)
print(response.text)

if response.status_code == 200:
    with open("latest_post.json", "w", encoding="utf-8") as f:
        json.dump(response.json(), f, indent=2, ensure_ascii=False)
    print("Saved latest_post.json")
else:
    raise Exception("API request failed")
