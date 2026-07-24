import requests
import json
import traceback

URL = "https://europe-west3-storyviewer-7a64d.cloudfunctions.net/getInstagramData"

payload = {
    "data": {
        "endpoint": "/v1.2/posts",
        "params": {
            "username_or_id_or_url": "gshclgoa"
        }
    }
}

headers = {
    "Content-Type": "application/json"
}

print("=" * 60)
print("Sending request...")
print("=" * 60)

try:
    response = requests.post(
        URL,
        json=payload,
        headers=headers,
        timeout=30
    )

    print(f"\nStatus Code : {response.status_code}")
    print(f"Reason      : {response.reason}")

    data = response.json()

    with open("response.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    items = data.get("result", {}).get("data", {}).get("items", [])

    print(f"\nPosts Found: {len(items)}")

    if not items:
        raise Exception("No posts found.")

    latest = items[0]

    print("\nLatest Post ID:")
    print(latest.get("id"))

    print("\nInstagram Code:")
    print(latest.get("code"))

    image_url = latest["image_versions"]["items"][0]["url"]

    print("\nImage URL:")
    print(image_url)

    print("\nDownloading image...")

    img = requests.get(image_url, timeout=30)
    img.raise_for_status()

    with open("latest_price.jpg", "wb") as f:
        f.write(img.content)

    print("✅ Image saved as latest_price.jpg")

except Exception:
    print("\nRequest Failed!")
    traceback.print_exc()
    raise
