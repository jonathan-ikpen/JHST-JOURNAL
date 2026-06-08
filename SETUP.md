# JHST Journal CMS — New Developer Setup Guide

Everything a new developer needs to get the project running from scratch.

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.10 or higher |
| pip | bundled with Python |
| Git | any recent version |

---

## 1. Get the Code

```bash
# Clone the repository
git clone <repository-url>
cd JHST-JOURNAL
```

---

## 2. Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt after activation.

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django 4.2.1
- django-ckeditor 6.5.1 (rich text editor for admin)
- Pillow (image handling)
- WhiteNoise (static file serving)

---

## 4. Run Migrations

```bash
python manage.py migrate
```

This creates the SQLite database and applies all schema and data migrations, including pre-populating the Peer Review Policy and Aim & Scope page with content.

---

## 5. Create an Admin Superuser

```bash
python manage.py createsuperuser
```

Enter a username, email, and password when prompted. This account is used to log in to `/admin/` and manage all site content.

---

## 6. Collect Static Files

Required for WhiteNoise to serve CSS, JS, and images:

```bash
python manage.py collectstatic --noinput
```

---

## 7. Start the Development Server

```bash
python manage.py runserver
```

The site will be available at:
- **Public site**: http://127.0.0.1:8000/
- **Admin panel**: http://127.0.0.1:8000/admin/

---

## 8. Run the Test Suite

```bash
python manage.py test --verbosity=2
```

All 65 tests should pass. If any fail, check that migrations have been applied and dependencies are installed.

---

## 9. Populate Content in Admin

Every page on the site is managed through the admin panel. After first setup, you must enter content for each page before it will display correctly.

Go to **http://127.0.0.1:8000/admin/** and fill in the following sections:

### Pages App

| Admin Model | URL it controls |
|-------------|-----------------|
| Home Page | `/` |
| About Page | `/about/` |
| Aim & Scope Page | `/about/aim-scope/` |
| Contact Page | `/about/contact/` |
| Editorial Team Page | `/about/editorial-team/` |
| Publication Fees Page | `/about/publication-fees/` |
| Publication Schedule Page | `/about/publication-schedule/` |
| Indexing Page | `/indexing/` |
| Metrics Page | `/metrics/` |
| Guidelines Page | `/guidelines/` |
| Author Guidelines Page | `/guidelines/author/` |
| Reviewer Guidelines Page | `/guidelines/reviewer/` |
| Policies Page | `/policies/` |
| Ethics & Malpractice Page | `/policies/ethics/` |
| Open Access Policy Page | `/policies/open-access/` |
| Peer Review Policy Page | `/policies/peer-review/` |
| Archiving Policy Page | `/policies/archiving/` |
| Plagiarism Policy Page | `/policies/plagiarism/` |
| Editorial Policy Page | `/policies/editorial/` |
| Subscription & Advertising Page | `/policies/subscription/` |
| JHST Journals Page | `/jhst-journals/` |
| Publications Page | `/publications/` |

> **Shortcut:** Run `python manage.py populate_pages` to populate all 22 page models, editorial team, organogram, indexing entries, and PTI journals in one command. This is the fastest way to get a fully populated site. Fields can then be fine-tuned in the admin.

### Formatting in Admin

All content fields use **CKEditor**. Use the toolbar buttons for:
- **Bold / Italic / Underline** — inline formatting
- **Bullet List / Numbered List** — for any list content
- **Link / Unlink** — for hyperlinks

Do NOT type HTML manually unless you are using the `Source` button. The rendered HTML is stored directly and output with `|safe` in templates.

### Journal App

Also configure via admin:
- **Team Members** — editorial team roster (editor-in-chief, managing directors, reviewers, board)
- **Organogram Items** — homepage structure diagram
- **Indexing Entries** — indexing and abstracting services
- **PTI Journals** — related PTI journal listings
- **Announcements** — news and calls for papers

---

## 10. Create User Accounts

Register user accounts through the site at `/register/` or via the admin:
- **Researcher** — can submit manuscripts, track status
- **Reviewer** — assigned manuscripts to review
- **Editor** — full access to all submissions and assignments

To assign a role, go to **Admin → Users**, edit the user, and check the appropriate role checkbox (`is_researcher`, `is_reviewer`, `is_editor`).

---

## 11. Project Structure

```
JHST-JOURNAL/
├── journal/            # Core app: users, manuscripts, reviews, workflow
│   ├── models.py       # User, Manuscript, Review, Issue, Article, Announcement
│   ├── views.py        # All workflow views
│   ├── forms.py        # Registration, manuscript, review forms
│   ├── urls.py         # All URL patterns
│   └── tests.py        # 65 automated tests
├── pages/              # CMS app: singleton page models for all info pages
│   ├── models.py       # ~22 singleton page models
│   ├── views.py        # One view per page (gets pk=1 record)
│   ├── admin.py        # Admin configuration for all page models
│   └── migrations/     # All schema + data migrations
├── templates/
│   ├── base.html       # Public site base template
│   ├── journal/        # Public-facing page templates
│   └── dashboard/      # Authenticated dashboard templates
├── static/             # Source CSS, JS, images
├── staticfiles/        # Collected static files (generated by collectstatic)
├── media/              # User-uploaded files (manuscripts, avatars)
├── journal_system/     # Django project settings
│   ├── settings.py
│   └── urls.py
├── requirements.txt
└── manage.py
```

---

## 12. Common Commands Reference

| Task | Command |
|------|---------|
| Start dev server | `python manage.py runserver` |
| Run all tests | `python manage.py test` |
| Populate all page content | `python manage.py populate_pages` |
| Create migration | `python manage.py makemigrations` |
| Apply migrations | `python manage.py migrate` |
| Open Django shell | `python manage.py shell` |
| Collect static files | `python manage.py collectstatic` |
| Check for issues | `python manage.py check` |
| Create superuser | `python manage.py createsuperuser` |

---

## 13. Environment Notes

- **Database**: SQLite (`db.sqlite3`) — suitable for development. For production, switch to PostgreSQL in `settings.py`.
- **Static files**: WhiteNoise serves them directly from Django — no separate web server needed for development.
- **Media files**: Stored in `media/`. Not served by WhiteNoise — configure a web server (nginx/Apache) or cloud storage (S3) in production.
- **Email**: Not configured by default. Email notifications will print to the console in development. Configure `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` in `settings.py` for production.
- **Secret key**: The `SECRET_KEY` in `settings.py` must be changed before deploying to production.
- **DEBUG**: Set `DEBUG = False` in production and add your domain to `ALLOWED_HOSTS`.

---

## Quick Start (Summary)

```bash
git clone <repo-url> && cd JHST-JOURNAL
python -m venv venv && venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_pages          # populate all 22 page models with real content
python manage.py collectstatic --noinput
python manage.py runserver
# Open http://127.0.0.1:8000/ — the site is fully populated and ready
```
