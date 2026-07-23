import json
import os
import instaloader

STATE_FILE = "state.json"

# Load previous state
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
else:
    state = {"last_post_id": ""}

L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=False,
    save_metadata=False,
    compress_json=False
)

profile = instaloader.Profile.from_username(L.context, "gshclgoa")

post = next(profile.get_posts())

post_id = str(post.mediaid)

print(f"Latest Post ID: {post_id}")

if state.get("last_post_id") == post_id:
    print("No new post found.")
    exit()

print("New post found!")

state["last_post_id"] = post_id

with open(STATE_FILE, "w") as f:
    json.dump(state, f, indent=2)

print("state.json updated successfully.")
