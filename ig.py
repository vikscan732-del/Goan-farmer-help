from playwright.sync_api import sync_playwright

URL = "https://www.instagram.com/gshclgoa/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/138.0 Safari/537.36"
    )

    page.goto(URL, wait_until="networkidle", timeout=90000)

    with open("instagram.html", "w", encoding="utf-8") as f:
        f.write(page.content())

    print(page.title())

    browser.close()
