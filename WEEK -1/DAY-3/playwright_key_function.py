from playwright.sync_api import sync_playwright
import time
import traceback

print("Starting test...")

try:
    with sync_playwright() as p:

        print("STEP 1: Launching installed Google Chrome...")

        browser = p.chromium.launch(
            channel="chrome",
            headless=False
        )

        print("STEP 2: Chrome opened successfully.")

        page = browser.new_page()

        print("STEP 3: New page created.")

        page.goto(
            "https://www.google.com",
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("STEP 4: Google loaded successfully.")

        print("Chrome will remain open for 60 seconds.")

        time.sleep(60)

        print("Closing browser...")

        browser.close()

except Exception as error:

    print("\n" + "=" * 60)
    print("PLAYWRIGHT ERROR")
    print("=" * 60)

    print(error)

    print("\nFULL TRACEBACK:")
    traceback.print_exc()

    input("\nPress Enter to close this program...")