
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})

    page.goto(
        "https://www.dolphinradar.com/web-viewer-for-instagram",
        wait_until="networkidle"
    )

    page.locator("input").first.fill("gshclgoa")

    # Click the purple button
    page.locator("button").first.click()

    page.wait_for_timeout(8000)

    print("Final URL:", page.url)
    print("Title:", page.title())

    with open("result.html", "w", encoding="utf-8") as f:
        f.write(page.content())

    browser.close()
