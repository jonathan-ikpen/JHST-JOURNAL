import os
import time
from playwright.sync_api import sync_playwright

IMAGE_DIR = os.path.join("docs", "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use high device_scale_factor for retina quality
        context = browser.new_context(viewport={'width': 1280, 'height': 1200}, device_scale_factor=2)
        page = context.new_page()

        # Load local HTML file
        page.goto(f"file:///{os.path.abspath('flowchart.html').replace(chr(92), '/')}")
        time.sleep(3) # Wait for mermaid to render
        try:
            element = page.locator(".mermaid")
            element.screenshot(path=os.path.join(IMAGE_DIR, "flowchart.png"))
        except:
            page.screenshot(path=os.path.join(IMAGE_DIR, "flowchart.png"))

        browser.close()

if __name__ == "__main__":
    run()
