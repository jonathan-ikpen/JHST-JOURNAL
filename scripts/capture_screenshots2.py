import os
import time
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8080"
IMAGE_DIR = os.path.join("docs", "images")

os.makedirs(IMAGE_DIR, exist_ok=True)

def login(page, username, password):
    page.goto(f"{BASE_URL}/login/")
    page.fill("input[name='username']", username)
    page.fill("input[name='password']", password)
    page.click("button[type='submit']")
    page.wait_for_load_state('networkidle')
    time.sleep(1)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        # ---------------- AUTHOR ----------------
        login(page, "JonathanIkpen", "Password@123")
        page.goto(f"{BASE_URL}/dashboard/")
        try:
            page.click("text=Hydrological Modeling")
            time.sleep(2)
            page.screenshot(path=os.path.join(IMAGE_DIR, "submit_revision.png"))
        except Exception as e:
            print("Could not get submit_revision:", e)
        page.goto(f"{BASE_URL}/logout/")

        # ---------------- REVIEWER ----------------
        login(page, "timothy", "Password@123")
        page.goto(f"{BASE_URL}/dashboard/")
        try:
            page.click("text=Desalination Efficiency")
            time.sleep(2)
            page.screenshot(path=os.path.join(IMAGE_DIR, "submit_review.png"))
        except Exception as e:
            print("Could not get submit_review:", e)
        page.goto(f"{BASE_URL}/logout/")

        # ---------------- EDITOR ----------------
        login(page, "jay", "Password@123")
        page.goto(f"{BASE_URL}/dashboard/")
        try:
            page.click("text=Assessing River Water")
            time.sleep(2)
            # Find and click + Assign Reviewer button
            page.click("text=Assign Reviewer")
            time.sleep(1)
            page.screenshot(path=os.path.join(IMAGE_DIR, "assign_reviewer.png"))
        except Exception as e:
            print("Could not get assign_reviewer:", e)

        page.goto(f"{BASE_URL}/dashboard/")
        try:
            page.click("text=Sustainable Water Management")
            time.sleep(2)
            page.click("text=Make Decision")
            time.sleep(1)
            page.screenshot(path=os.path.join(IMAGE_DIR, "make_decision.png"))
        except Exception as e:
            print("Could not get make_decision:", e)

        page.goto(f"{BASE_URL}/logout/")
        browser.close()

if __name__ == "__main__":
    run()
