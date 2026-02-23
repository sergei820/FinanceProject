---
name: Django Project Setup
overview: Set up a Django project with two isolated directories -- `app/` (Django project with its own uv venv) and `tests/` (pytest suite with its own uv venv) -- each with its own Dockerfile, using PostgreSQL and pyproject.toml for dependency management.
todos:
  - id: cleanup
    content: Remove partial setup files and root .venv
    status: pending
  - id: django-project
    content: Create app/ dir, uv venv, Django project (financeapp) + pages app
    status: pending
  - id: django-settings
    content: Configure settings.py (PostgreSQL, templates, static, pages app)
    status: pending
  - id: view-template
    content: Create HomePageView, URLs, base.html, and home.html
    status: pending
  - id: app-dockerfile
    content: Create app/Dockerfile and app/pyproject.toml
    status: pending
  - id: tests-dir
    content: Create tests/ dir, uv venv, pytest scaffolding, and starter test
    status: pending
  - id: tests-dockerfile
    content: Create tests/Dockerfile and tests/pyproject.toml
    status: pending
  - id: root-files
    content: Update .gitignore and README.md
    status: pending
isProject: false
---

# Django Project Setup Plan

## Target Directory Structure

```
FinanceProject/
├── app/                          # Container directory
│   ├── .venv/                    # uv venv (Python 3.12, gitignored)
│   ├── Dockerfile
│   ├── pyproject.toml            # uv-managed dependencies
│   ├── uv.lock
│   ├── manage.py
│   ├── financeapp/               # Django project package (settings, urls, wsgi)
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── pages/                    # First Django app
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── migrations/
│   └── templates/
│       ├── base.html
│       └── pages/
│           └── home.html
├── tests/
│   ├── .venv/                    # uv venv (Python 3.12, gitignored)
│   ├── Dockerfile
│   ├── pyproject.toml            # uv-managed dependencies
│   ├── uv.lock
│   ├── pytest.ini
│   └── test_home.py              # Starter smoke test
├── .env
├── .gitignore
└── README.md
```

The outer `app/` is just a container directory. Inside it, `financeapp/` is the Django project Python package (holding `settings.py`, `urls.py`, etc.), and `pages/` is a Django app sitting alongside it. This avoids the confusing `financeapp/financeapp/` double-nesting while keeping the Django package properly named.

```mermaid
graph TB
  subgraph root ["FinanceProject (repo root)"]
    env[".env"]
    gitignore[".gitignore"]
    subgraph appDir ["app/ (container)"]
      venv1[".venv"]
      dockerfile1["Dockerfile"]
      pyproject1["pyproject.toml"]
      manage["manage.py"]
      subgraph djangoPkg ["financeapp/ (Django project pkg)"]
        settings["settings.py"]
        urls["urls.py"]
        wsgi["wsgi.py"]
      end
      subgraph pagesApp ["pages/ (Django app)"]
        views["views.py"]
        models["models.py"]
      end
      subgraph appTemplates ["templates/"]
        base["base.html"]
        homeHtml["pages/home.html"]
      end
    end
    subgraph testsDir ["tests/"]
      venv2[".venv"]
      dockerfile2["Dockerfile"]
      pyproject2["pyproject.toml"]
      pytestIni["pytest.ini"]
      testFiles["test_home.py"]
    end
  end
```



## Step-by-step

### 1. Clean up partial setup

- Remove files from the earlier aborted setup and the root-level `.venv`

### 2. Create `app/` Django project

- `mkdir app && cd app`
- `uv init` to create `pyproject.toml`, then add dependencies: `django`, `psycopg2-binary`, `gunicorn`
- `uv venv .venv --python=3.12`
- `uv run django-admin startproject financeapp .` -- creates `manage.py` + `financeapp/` package
- `uv run python manage.py startapp pages` -- creates the first app

### 3. Configure Django settings

- In `app/financeapp/settings.py`:
  - Register `pages` in `INSTALLED_APPS`
  - Set `TEMPLATES DIRS` to `BASE_DIR / 'templates'`
  - Configure `DATABASES` for PostgreSQL using `os.environ` (from `.env`):
    - ENGINE, HOST, PORT, NAME, USER, PASSWORD
  - Set `STATIC_URL` and `STATICFILES_DIRS`

### 4. Create the one-page view and template

- `pages/views.py`: `HomePageView` using `TemplateView`
- `pages/urls.py`: route `''` to `HomePageView`
- `financeapp/urls.py`: include `pages.urls`
- `app/templates/base.html`: base HTML skeleton
- `app/templates/pages/home.html`: landing page extending base

### 5. Create `app/Dockerfile`

- Based on `python:3.12-slim`
- Install uv, system deps for PostgreSQL (`libpq-dev`)
- Copy `pyproject.toml` + `uv.lock`, run `uv sync`
- Copy app code
- Expose port 8000, run with `gunicorn`

### 6. Create `tests/` directory

- `mkdir tests && cd tests`
- `uv init` to create `pyproject.toml`, then add: `pytest`, `requests`
- `uv venv .venv --python=3.12`
- Selenium/Playwright can be added later when needed

### 7. Create `tests/Dockerfile`

- Based on `python:3.12-slim`
- Install uv
- Copy `pyproject.toml` + `uv.lock`, run `uv sync`
- Copy test files
- Default CMD: `uv run pytest`

### 8. Create test scaffolding

- `tests/pytest.ini`: basic config
- `tests/test_home.py`: a simple smoke test that hits `http://app:8000/` and asserts HTTP 200

### 9. Update root files

- Update `.gitignore` to cover both `.venv/` dirs, `__pycache__/`, `db.sqlite3`, `.env`
- Update `README.md` with setup and run instructions

