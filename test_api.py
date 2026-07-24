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
    # Intentionally NOT sending Firebase-Instance-ID-Token
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

    print("\n========== RESPONSE HEADERS ==========")
    for k, v in response.headers.items():
        print(f"{k}: {v}")

    print("\n========== RESPONSE TEXT (First 1000 chars) ==========")
    print(response.text[:1000])

    print("\n========== TRYING JSON ==========")

    try:
        data = response.json()

        print("✓ JSON parsed successfully")

        with open("response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print("Saved response.json")

        items = (
            data.get("result", {})
                .get("data", {})
                .get("items", [])
        )

        print(f"\nPosts Found: {len(items)}")

        if items:
            first = items[0]

            print("\nLatest Post ID:")
            print(first.get("id"))

            print("\nInstagram Code:")
            print(first.get("code"))

            try:
                img = first["image_versions"]["items"][0]["url"]
                print("\nImage URL:")
                print(img)
            except Exception:
                print("\nNo image URL found.")

    except Exception:
        print("\nCould not parse JSON.")
        traceback.print_exc()

image_url = latest["image_versions"]["items"][0]["url"]

print("\nImage URL:")
print(image_url)

print("\nDownloading image...")

img = requests.get(image_url, stream=True)
img.raise_for_status()

with open("latest_price.jpg", "wb") as f:
    for chunk in img.iter_content(8192):
        if chunk:
            f.write(chunk)

print("✅ Image saved as latest_price.jpg")

except Exception:
    print("\nRequest Failed!")
    traceback.print_exc()
