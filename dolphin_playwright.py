from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    def log_request(request):
        print(request.method, request.url)

    page.on("request", log_request)

    page.goto(
        "https://www.dolphinradar.com/web-viewer-for-instagram",
        wait_until="networkidle"
    )

    page.locator("input").first.fill("gshclgoa")
    page.locator("button").first.click()

    page.wait_for_timeout(10000)

    browser.close()
