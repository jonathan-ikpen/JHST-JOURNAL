import os
import time
import glob
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8080"
IMAGE_DIR = os.path.join("docs", "images")

# Clean image dir completely
os.makedirs(IMAGE_DIR, exist_ok=True)
for f in glob.glob(os.path.join(IMAGE_DIR, "*.png")):
    try:
        os.remove(f)
    except:
        pass

def login(page, username, password):
    page.goto(f"{BASE_URL}/login/")
    page.fill("input[name='username']", username)
    page.fill("input[name='password']", password)
    page.click("button:has-text('Login')")
    time.sleep(2)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        # ---------------- FLOWCHART ----------------
        # Load local HTML file
        page.goto(f"file:///{os.path.abspath('flowchart.html').replace(chr(92), '/')}")
        time.sleep(3) # Wait for mermaid to render
        try:
            element = page.locator(".mermaid")
            element.screenshot(path=os.path.join(IMAGE_DIR, "flowchart.png"))
        except:
            page.screenshot(path=os.path.join(IMAGE_DIR, "flowchart.png"))

        # ---------------- AUTHOR ----------------
        login(page, "JonathanIkpen", "Password@123")
        page.goto(f"{BASE_URL}/dashboard/")
        time.sleep(2)
        page.screenshot(path=os.path.join(IMAGE_DIR, "author_dashboard.png"))

        page.goto(f"{BASE_URL}/submit/")
        time.sleep(2)
        page.screenshot(path=os.path.join(IMAGE_DIR, "new_submission.png"))
        
        page.goto(f"{BASE_URL}/dashboard/my-submission/7/submit-revision/")
        time.sleep(2)
        page.screenshot(path=os.path.join(IMAGE_DIR, "submit_revision.png"))

        page.goto(f"{BASE_URL}/logout/")
        time.sleep(1)

        # ---------------- REVIEWER ----------------
        login(page, "timothy", "Password@123")
        page.goto(f"{BASE_URL}/dashboard/")
        time.sleep(2)
        page.screenshot(path=os.path.join(IMAGE_DIR, "reviewer_invitation.png"))
        
        page.goto(f"{BASE_URL}/submit_review/7/")
        time.sleep(2)
        page.screenshot(path=os.path.join(IMAGE_DIR, "submit_review.png"))
            
        page.goto(f"{BASE_URL}/logout/")
        time.sleep(1)

        # ---------------- EDITOR ----------------
        login(page, "jay", "Password@123")
        page.goto(f"{BASE_URL}/dashboard/")
        time.sleep(2)
        page.screenshot(path=os.path.join(IMAGE_DIR, "editor_dashboard.png"))
        
        page.goto(f"{BASE_URL}/assign_reviewer/12/")
        time.sleep(2)
        page.screenshot(path=os.path.join(IMAGE_DIR, "assign_reviewer.png"))

        page.goto(f"{BASE_URL}/make_decision/10/")
        time.sleep(2)
        page.screenshot(path=os.path.join(IMAGE_DIR, "make_decision.png"))

        page.goto(f"{BASE_URL}/dashboard/?status=accepted")
        time.sleep(2)
        page.screenshot(path=os.path.join(IMAGE_DIR, "publish_article.png"))

        page.goto(f"{BASE_URL}/logout/")
        time.sleep(1)

        # ---------------- ADMIN (DJANGO ADMIN) ----------------
        login(page, "admin", "admin")
        page.goto(f"{BASE_URL}/admin/journal/volume/")
        time.sleep(2)
        page.screenshot(path=os.path.join(IMAGE_DIR, "django_admin_volumes.png"))

        page.goto(f"{BASE_URL}/admin/journal/user/")
        time.sleep(2)
        page.screenshot(path=os.path.join(IMAGE_DIR, "django_admin_users.png"))

        page.goto(f"{BASE_URL}/admin/logout/")
        
        browser.close()

if __name__ == "__main__":
    run()
