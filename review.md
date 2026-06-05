# JHST Journal System — Project Audit & CMS Status Report

**Date:** 2026-06-05  
**Branch:** `page_model`  
**Author:** Roland-Jephtha

---

## 1. What This Project Is

This is a **Django-based academic journal management system** for the *Journal of Hydrocarbon Science and Technology (JHST)*, published by the Petroleum Training Institute (PTI). It handles the full lifecycle of academic publishing:

- Researcher submits a manuscript
- Editor assigns a reviewer
- Reviewer submits comments and recommendation
- Editor accepts or rejects the manuscript
- Accepted manuscript is assigned to a volume/issue and published as an article

On top of that workflow, there is a **CMS layer** (`pages` app) that manages all the static informational content of the journal website — About, Policies, Guidelines, Editorial Team, Metrics, etc.

**Tech stack:**

| Layer | Technology |
|---|---|
| Framework | Django 6.0 |
| Database | SQLite (dev) |
| Frontend | Tailwind CSS (CDN), Material Icons, Vanilla JS |
| Images | Pillow 12.0.0 |
| Static Files | WhiteNoise 6.11.0 |
| Rich Text Editor | **NONE — this is the main problem** |
| Admin | Django Admin (custom classes) |

---

## 2. Directory Structure

```
JHST-JOURNAL-main/
├── journal/                  # Core journal app — submissions, reviews, articles
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── feeds.py              # RSS feed
│   └── migrations/
├── pages/                    # CMS app — all static/informational pages
│   ├── models.py             # 25+ singleton page models
│   ├── views.py
│   ├── admin.py
│   └── migrations/
├── journal_system/           # Django project settings
│   ├── settings.py
│   └── urls.py
├── templates/
│   ├── base.html
│   ├── dashboard/            # All dashboard templates
│   ├── journal/              # All public-facing templates
│   └── includes/             # Header, footer, sidebar
├── static/assets/            # Images and legacy HTML stitches
├── media/                    # User uploads (avatars, manuscripts, PDFs)
├── db.sqlite3
└── manage.py
```

---

## 3. All Models

### 3.1 `journal` App Models

#### `User` (extends `AbstractUser`)
```
- is_researcher (bool)
- is_reviewer (bool)
- is_editor (bool)
- affiliation (str)
- avatar (ImageField)
- orcid (str)
```

#### `Manuscript`
```
- title (str, max 255)
- abstract (TextField)
- file (FileField)
- author (FK → User)
- co_authors (str)
- affiliations (TextField)
- reviewer (FK → User, nullable)
- status (submitted | under_review | accepted | rejected | published)
- submitted_date (auto_now_add)
- keywords (str)
- is_paid (bool)
```

#### `Review`
```
- manuscript (FK → Manuscript)
- reviewer (FK → User)
- comments (TextField)
- recommendation (accept | revise | reject)
- date_assigned (auto_now_add)
- due_date (nullable)
- date_completed (nullable)
```

#### `Volume`
```
- number (int)
- year (int)
```

#### `Issue`
```
- volume (FK → Volume)
- number (int)
- publication_date (Date)
```

#### `Article`
```
- manuscript (OneToOneField → Manuscript)
- issue (FK → Issue)
- page_start (int, nullable)
- page_end (int, nullable)
- doi (str, unique, nullable)
```

#### `Notification`
```
- recipient (FK → User)
- message (TextField)
- is_read (bool)
- created_at (auto_now_add)
- link (str, nullable)
```

#### `Announcement`
```
- title (str, max 255)
- short_description (TextField, max 500)
- content (TextField)            ← plain text, no rich text
- category (news | call_for_papers | maintenance | general)
- image (ImageField, nullable)
- date_created (DateTime)
- is_active (bool)
```

---

### 3.2 `pages` App Models (Singleton Pattern)

Every model below follows a **singleton pattern** — only one record (pk=1) ever exists, edited through the Django admin. This covers all the informational pages of the site.

| Model | Purpose |
|---|---|
| `HomePage` | Intro video, mission, organogram, chief editor |
| `AboutPage` | About, mission, vision, objectives |
| `AimScopePage` | Journal aims and scope |
| `ContactPage` | Editorial office and contact details |
| `PublicationFeesPage` | APC (Article Processing Charge) info |
| `EditorialTeamPage` | Team section descriptions |
| `TeamMember` | Individual team member profiles |
| `IndexingPage` | Indexing section intro |
| `IndexingEntry` | Individual indexing services |
| `PoliciesPage` | Open access, copyright, ethics, peer review |
| `AuthorGuidelinesPage` | 27 fields covering all submission guidance |
| `EthicsMalpracticePage` | Ethics standards and procedures |
| `OpenAccessPolicyPage` | Open access policy |
| `PeerReviewPolicyPage` | Double-blind review details |
| `ArchivingPolicyPage` | Archiving policy |
| `PlagiarismPolicyPage` | Plagiarism policy |
| `SubscriptionAdvertisingPage` | Subscription and ads info |
| `EditorialPolicyPage` | Editorial policy |
| `PublicationSchedulePage` | Biannual, online-first, special issues |
| `GuidelinesPage` | Guidelines landing page |
| `ReviewerGuidelinesPage` | 8 fields for reviewer instructions |
| `MetricsPage` | Impact factor, H-index, usage stats |
| `JhstJournalsPage` | Other PTI journals |
| `PtiJournal` | Individual journal listings |
| `PublicationsPage` | Publications section intro |

**Every single content field across all 25 models is a plain `TextField`. None of them use a rich text field.**

---

## 4. Views & URL Routing

### Public Routes
| URL | View | Purpose |
|---|---|---|
| `/` | `index` | Homepage with latest issues |
| `/issues/<id>/` | `issue_detail` | Issue articles |
| `/article/<id>/` | `article_detail` | Article with PDF download |
| `/search/` | `search` | Search by title, author, year |
| `/publications/archives/` | `archives` | All volumes |
| `/publications/current/` | `current_issue` | Latest issue |
| `/announcements/` | `announcements` | Paginated list |
| `/announcements/<id>/` | `announcement_detail` | Single announcement |
| `/about/`, `/about/aim-scope/`, etc. | Singleton views | Info pages |
| `/guidelines/author/`, `/guidelines/reviewer/` | Singleton views | Guideline pages |
| `/policies/ethics/`, `/policies/open-access/`, etc. | Singleton views | Policy pages |
| `/rss/` | `LatestArticlesFeed` | RSS feed |

### Dashboard/Submission Routes
| URL | View | Role |
|---|---|---|
| `/dashboard/` | `dashboard` | All roles |
| `/register/` | `register` | Public |
| `/submit/` | `submit_manuscript` | Researcher |
| `/dashboard/my-submissions/` | `my_submissions` | Researcher |
| `/dashboard/assigned-reviews/` | `assigned_reviews` | Reviewer |
| `/assign_reviewer/<id>/` | `assign_reviewer` | Editor |
| `/submit_review/<id>/` | `submit_review` | Reviewer |
| `/make_decision/<id>/` | `make_decision` | Editor |
| `/publish_article/<id>/` | `publish_article` | Editor |
| `/mark_as_paid/<id>/` | `mark_as_paid` | Editor |
| `/create_volume/`, `/create_issue/` | create views | Editor |
| `/manage_volumes/` | `manage_volumes` | Editor |

---

## 5. What Has Been Done (CMS Progress)

### Done ✅

- **All singleton page models exist** — every section of the journal site (About, Policies, Guidelines, Editorial Team, Metrics, Indexing, Publications, etc.) has a corresponding Django model in the `pages` app.
- **Admin interface works** — editors can log into `/admin/` and update any of these pages through Django Admin fieldsets.
- **Templates render all pages** — every page model has a matching view and template that reads and displays the content.
- **Announcement system** — full model with category, image, active/inactive toggle, and a public-facing list and detail view.
- **Basic media uploads** — author avatars, announcement images, manuscript PDFs all upload to `/media/`.
- **`SingletonPageAdmin`** — prevents creating duplicate page records and hides the Delete button; the admin enforces one record per page type.
- **Draggable ordering** — `TeamMember`, `IndexingEntry`, `PtiJournal` support drag-and-drop reordering via `OrderedModel`.
- **Category-based styling on Announcements** — icons and color badges map to category.
- **RSS feed** for articles.
- **WhiteNoise** serving static files.

### Partially Done ⚠️

- **Media handling** — uploads work but there is no media library or asset browser. You cannot browse or reuse uploaded files.
- **Content rendering** — templates use `|safe|linebreaks` on announcement content, which does apply basic line breaks but does not render HTML formatting like bold, links, or lists. It is also an XSS risk if unchecked.

### Not Started ❌

- **Rich text editor** — no TinyMCE, CKEditor, Quill, Froala, or Summernote. This is the single biggest gap.
- **Draft/publish workflow** — every saved record is immediately live. No draft state, no scheduled publishing.
- **Content versioning** — no revision history. If someone overwrites a page in admin, the old content is gone.
- **SEO fields** — no meta description, meta keywords, or Open Graph fields on any page model.
- **URL slugs for announcements** — announcements use integer PKs (`/announcements/3/`) not slugs.
- **Dynamic page creation** — to add a new page type you have to write a new model and migration; non-developers cannot do this.

---

## 6. What Is Wrong With the CMS — Full Breakdown

This is the critical section. Here is every problem, in priority order.

---

### 6.1 No Rich Text Editor (CRITICAL)

**Where it hurts:** Every `TextField` on every model in the `pages` app and on `Announcement.content`. That is every piece of editable content on the site.

**What happens now:** An admin types plain text into a `<textarea>`. If they write `**bold**` or `<b>bold</b>`, the template just shows it as raw characters, not formatted text (except for `Announcement.content` where `|safe` is applied — but that's dangerous, see 6.2).

**What should happen:** A WYSIWYG editor (bold, italic, underline, links, bullet lists, headings, image insertion) appears in the admin form, saves HTML, and the template renders that HTML safely.

**Root cause:** No rich text package installed. The `requirements.txt` / `pip freeze` shows:
```
asgiref, Django, pillow, sqlparse, tzdata, whitenoise
```
No `django-ckeditor`, `django-tinymce`, `django-quill-editor`, etc.

**No widget is assigned** anywhere in `pages/admin.py` or `journal/admin.py` to swap the default `Textarea` for a rich text widget.

---

### 6.2 XSS Vulnerability on Announcement Content

**File:** [journal/templates/journal/announcement_detail.html](journal/templates/journal/announcement_detail.html)

```django
{{ announcement.content|safe|linebreaks }}
```

The `|safe` filter marks the content as trusted HTML and Django will render any HTML tags in it. If any user-supplied or carelessly pasted content contains `<script>` tags or malicious `<a href="javascript:...">` links, those will execute in visitors' browsers.

**Why it exists:** Someone tried to enable HTML rendering for announcements by applying `|safe` but there is no sanitization happening before the content is saved. This is the wrong approach.

**Fix needed:** Either:
1. Use a rich text editor that sanitizes output on save, then render with `|safe`.
2. Strip and sanitize HTML server-side using `bleach` before rendering.

---

### 6.3 Duplicate Code in views.py

**File:** [journal/views.py](journal/views.py) — around line 361

```python
reviews = manuscript.reviews.all()
reviews = manuscript.reviews.all()   # exact duplicate line
```

This is harmless (second assignment just overwrites with same value) but indicates copy-paste sloppiness.

---

### 6.4 Duplicate Import in forms.py

**File:** [journal/forms.py](journal/forms.py) — top of file

```python
from django import forms
from django import forms   # duplicate
```

Again harmless, but messy.

---

### 6.5 All CMS Content Is One Big Flat Text Field

The `AuthorGuidelinesPage` model has **27 separate `TextField` fields** like:
```
manuscript_format_title
manuscript_format_intro
manuscript_format_text
title_requirements_title
title_requirements_text
...
```

This approach stores content but has two problems:

1. **No formatting** — each field is plain text. An admin cannot make a heading bold or add a hyperlink to a section.
2. **Rigid structure** — to add a new section to the Author Guidelines, a developer has to write a migration. A content editor cannot add, remove, or reorder sections without developer involvement.

---

### 6.6 No Slug on Announcements

**File:** [journal/models.py](journal/models.py) — `Announcement` model

Announcements use auto-increment integer PKs in their URLs (`/announcements/3/`). This is bad for SEO and produces ugly, non-descriptive URLs. A `SlugField` (auto-populated from the title) is standard practice.

---

### 6.7 No Draft/Publish State on Page Models

Every singleton page is always live. There is no way to:
- Save a draft of the About page without it immediately going live.
- Schedule a page update for a future date.
- Roll back to a previous version.

For a journal that has editorial standards, this is a notable omission.

---

### 6.8 Admin Forms Are Bare Textareas

All the page model admin forms use Django's default `Textarea` widget. For a field like `AuthorGuidelinesPage.manuscript_format_text` that is intended to hold several paragraphs of formatted instructions, the admin provides a plain unstyled box with no toolbar.

No `formfield_overrides`, no custom widget, no Markdown preview.

---

### 6.9 No Media Library

Images can be uploaded to specific fields (`Announcement.image`, `User.avatar`) but:
- You cannot browse previously uploaded images.
- You cannot reuse an image across multiple announcements.
- There is no image resizing or thumbnail generation (Pillow is installed but not used for resizing).

---

### 6.10 Settings Not Configured for a Rich Text Editor

[journal_system/settings.py](journal_system/settings.py) has no configuration block for any rich text editor. When you install `django-ckeditor` or `django-tinymce`, you must add them to `INSTALLED_APPS` and add their configuration dictionary. None of this exists.

---

## 7. Summary Table

| Feature | Status | Notes |
|---|---|---|
| Singleton CMS page models | ✅ Done | All 25 pages exist |
| Admin editing interface | ✅ Done | Works, but only plain text |
| Template rendering | ✅ Done | Content displays on site |
| Announcement system | ✅ Done | Category, image, active toggle |
| Media uploads | ✅ Done | Avatars, manuscripts, images |
| Draggable ordering | ✅ Done | Teams, indexing, journals |
| **Rich text editor** | ❌ Missing | No package, no widget, no config |
| HTML formatting (bold, links, etc.) | ❌ Missing | Follows from above |
| XSS-safe HTML rendering | ❌ Missing | `\|safe` used without sanitization |
| Draft/publish workflow | ❌ Missing | All saves go live immediately |
| Content versioning | ❌ Missing | No revision history |
| SEO fields | ❌ Missing | No meta description/OG fields |
| Announcement slugs | ❌ Missing | Uses integer PKs in URLs |
| Media library | ❌ Missing | No asset browser |
| Dynamic page creation | ❌ Missing | Needs developer + migration |

---

## 8. What Needs to Be Done Next (Priority Order)

### Priority 1 — Rich Text Editor (fixes 6.1, 6.2, 6.8)

Install and wire up a rich text editor. The recommended approach for this project is **CKEditor 5** via `django-ckeditor-5` or classic **TinyMCE** via `django-tinymce`.

Steps:
1. `pip install django-tinymce` (or `django-ckeditor-5`)
2. Add to `INSTALLED_APPS` and add config block in `settings.py`
3. Change affected `TextField` fields to `HTMLField` (tinymce) or `RichTextField` (ckeditor)
4. Run `makemigrations` and `migrate`
5. Update templates: change `|linebreaks` to `|safe` with server-side bleach sanitization

Affects: All 25 page models + `Announcement.content`.

### Priority 2 — Fix XSS on Announcements (fixes 6.2)

While the rich text editor is being wired up, immediately fix the raw `|safe` usage:

```python
pip install bleach
```

In the view or a template filter, sanitize before rendering:
```python
import bleach
ALLOWED_TAGS = ['p','br','strong','em','u','a','ul','ol','li','h1','h2','h3']
clean_content = bleach.clean(announcement.content, tags=ALLOWED_TAGS, strip=True)
```

### Priority 3 — Add Slugs to Announcements (fixes 6.6)

Add a `SlugField` to `Announcement`, auto-populate it from the title on save, and update the URL pattern and view.

### Priority 4 — Draft State on Announcements (partial fix for 6.7)

`Announcement` already has `is_active`. Extend this pattern to the singleton page models with a simple `is_published` flag or a `last_published_at` timestamp.

### Priority 5 — Clean Up Duplicate Code (fixes 6.3, 6.4)

Remove the duplicate `reviews = manuscript.reviews.all()` line and the duplicate `from django import forms` import.

---

## 9. Quick Reference — Key Files

| File | Purpose |
|---|---|
| [journal/models.py](journal/models.py) | Core models: User, Manuscript, Review, Article, Announcement |
| [pages/models.py](pages/models.py) | 25 singleton CMS page models |
| [journal/views.py](journal/views.py) | All views — submission workflow + public pages |
| [pages/views.py](pages/views.py) | Singleton page rendering views |
| [journal/forms.py](journal/forms.py) | All Django forms |
| [journal/admin.py](journal/admin.py) | Core model admin config |
| [pages/admin.py](pages/admin.py) | Singleton page admin with fieldsets |
| [journal_system/settings.py](journal_system/settings.py) | Django settings — no RTE config present |
| [journal/urls.py](journal/urls.py) | All URL patterns |
| [templates/base.html](templates/base.html) | Master layout |
| [templates/journal/announcement_detail.html](templates/journal/announcement_detail.html) | Contains unsafe `\|safe` filter |
