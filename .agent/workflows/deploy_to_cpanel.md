---
description: How to deploy the JHST Journal Django application to a cPanel server.
---

# Deploying to cPanel

This guide details the steps to deploy the JHST Journal Django application to a hosting environment using cPanel with the "Setup Python App" feature.

## 1. Prepare Local Project

Before uploading, ensure your project is ready for production.

### Requirements

Ensure your `requirements.txt` is up to date.

```bash
pip freeze > requirements.txt
```

### Settings Configuration

In `journal_system/settings.py`, you will need to update a few settings for the production environment. You can either change them directly or use environment variables.

1.  **Debug Mode**: Set `DEBUG = False`.
2.  **Allowed Hosts**: Add your domain name.
    ```python
    ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
    ```
3.  **Static Files**: Ensure `STATIC_ROOT` is set (already done in your project):
    ```python
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    ```

## 2. cPanel Setup

1.  Log in to your **cPanel**.
2.  Find the **"Setup Python App"** tool (under Software).
3.  Click **"Create Application"**.
4.  **Python Version**: Select a version that matches your local environment (e.g., 3.9+).
5.  **Application Root**: Enter the path where you will upload your files (e.g., `jhst-journal`).
6.  **Application URL**: Select the domain/subdomain.
7.  **Application Startup File**: Enter `passenger_wsgi.py`.
8.  **Application Entry Point**: Enter `application`.
9.  Click **Create**.

## 3. Upload Files

1.  Use **File Manager** or **FTP** to upload your project files to the **Application Root** folder you defined (e.g., `/home/username/jhst-journal`).
2.  Upload the entire project folder _contents_ (manage.py, journal_system, journal, requirements.txt, etc.).
3.  **Exclude**: `venv` or `env` folders, `.git`, `__pycache__`.

## 4. Install Dependencies

1.  Go back to the **"Setup Python App"** page in cPanel.
2.  Find your application and scroll down to "Configuration files".
3.  Ensure `requirements.txt` is listed.
4.  Click **"Run Pip Install"**.
    - _Troubleshooting_: If this fails, you may need to SSH into the server, activate the virtual environment command provided at the top of the Python App page, and run `pip install -r requirements.txt` manually.

## 5. Configure WSGI (passenger_wsgi.py)

cPanel uses Phusion Passenger to serve Python apps. You need to create a special file named `passenger_wsgi.py` in your **Application Root**.

Create `passenger_wsgi.py` with the following content:

```python
import os
import sys

# Add your project directory to the sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Set the settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'journal_system.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 6. Static Files

For static files (CSS, JS) to work:

1.  Activate the virtual environment (use the command shown in the Python App UI, e.g., `source /home/user/virtualenv/jhst-journal/3.9/bin/activate`).
2.  Run `collectstatic`:
    ```bash
    python manage.py collectstatic
    ```
3.  **Important**: cPanel often aliases `/static` to a public folder. You might need to configure a symlink or alias in cPanel **Static Files** section if available, OR move the contents of `staticfiles` to `public_html/static` (if hosting on the main domain).
    - _Alternative_: Use `Whitenoise` for serving static files directly from Django (easier for cPanel).
      1.  `pip install whitenoise`
      2.  Add `'whitenoise.middleware.WhiteNoiseMiddleware'` after `SecurityMiddleware` in `settings.py`.
      3.  Set `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`.

## 7. Database Migration

1.  While the virtual environment is active (via SSH or Terminal in cPanel):
    ```bash
    python manage.py migrate
    ```

## 8. Final Steps

1.  **Restart** the application from the cPanel "Setup Python App" page.
2.  Visit your URL.
3.  If you see "Internal Server Error", check the `passenger.log` file in your application root for error details.
