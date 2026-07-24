from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(
        "https://anonyig.com/en/instagram-profile-viewer/",
        wait_until="domcontentloaded"
    )

    page.wait_for_timeout(5000)

    print("TITLE:", page.title())

    print("\nINPUTS FOUND:")
    inputs = page.locator("input")
    print("Count:", inputs.count())

    for i in range(inputs.count()):
        print(i, inputs.nth(i).evaluate("e => e.outerHTML"))

    print("\nBUTTONS FOUND:")
    buttons = page.locator("button")
    print("Count:", buttons.count())

    for i in range(buttons.count()):
        print(i, buttons.nth(i).evaluate("e => e.outerHTML"))

    browser.close()
