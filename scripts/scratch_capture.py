# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright
import time
import os

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1280, 'height': 800})
    page = context.new_page()
    
    print('Navigating to admin login...')
    page.goto('http://127.0.0.1:8080/admin/')
    
    print('Logging in...')
    page.fill('input[name="username"]', 'admin')
    page.fill('input[name="password"]', 'admin')
    page.click('input[type="submit"]')
    
    print('Waiting for login to complete...')
    page.wait_for_url('**/admin/')
    
    print('Navigating to Pages section...')
    page.goto('http://127.0.0.1:8080/admin/pages/')
    page.wait_for_load_state('networkidle')
    
    out_dir = 'c:/jojo/school/jhst-journal/docs/images'
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'cms_screenshot.png')
    
    print(f'Taking screenshot and saving to {out_path}...')
    page.screenshot(path=out_path, full_page=True)
    
    print('Done.')
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
