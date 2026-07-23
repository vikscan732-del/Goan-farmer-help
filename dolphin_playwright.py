from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://www.dolphinradar.com/web-viewer-for-instagram", wait_until="networkidle")

    # Type username
    page.fill("input", "gshclgoa")

    # Click View
    page.click("text=View")

    page.wait_for_timeout(10000)

    # Save result
    with open("result.html", "w", encoding="utf-8") as f:
        f.write(page.content())

    print("Final URL:", page.url)
    print("Title:", page.title())

    browser.close()
