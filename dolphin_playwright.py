from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.on(
        "request",
        lambda r: print(
            "\n==== REQUEST ====",
            "\nMETHOD:", r.method,
            "\nURL:", r.url,
            "\nHEADERS:", r.headers,
            "\nPOST DATA:", r.post_data
        )
    )

    page.on(
        "response",
        lambda r: print(
            "\n==== RESPONSE ====",
            "\nSTATUS:", r.status,
            "\nURL:", r.url
        )
    )

    page.goto(
    "https://anonyig.com/en/instagram-profile-viewer/",
    wait_until="networkidle"
)

page.locator("input").first.fill("gshclgoa")

print("Buttons found:")

buttons = page.locator("button")

for i in range(buttons.count()):
    try:
        print(i, buttons.nth(i).inner_text())
    except:
        print(i, "No text")

browser.close()
