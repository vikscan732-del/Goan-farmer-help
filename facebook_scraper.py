
from playwright.sync_api import sync_playwright

URL = "https://www.facebook.com/GSHCLgoa/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("Opening Facebook...")
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)

    print("Title:", page.title())

    browser.close()
