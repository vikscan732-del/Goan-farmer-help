from playwright.sync_api import sync_playwright

URL = "https://www.facebook.com/GSHCLgoa/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("Opening Facebook...")
    page.goto(URL, wait_until="networkidle", timeout=60000)

    html = page.content()

    with open("facebook_page.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Saved facebook_page.html")

    browser.close()
