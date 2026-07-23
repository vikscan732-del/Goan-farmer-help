import instaloader

L = instaloader.Instaloader(
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=False,
    save_metadata=False,
    compress_json=False
)

profile = instaloader.Profile.from_username(L.context, "gshclgoa")

print(profile.username)
print(profile.mediacount)
