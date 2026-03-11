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
  - id: docker-compose
    content: Create docker-compose.yml with app, db, and tests services
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
├── docker-compose.yml            # Orchestrates app + db + tests
├── .env
├── .gitignore
└── README.md
```

The outer `app/` is just a container directory. Inside it, `financeapp/` is the Django project Python package (holding `settings.py`, `urls.py`, etc.), and `pages/` is a Django app sitting alongside it. This avoids the confusing `financeapp/financeapp/` double-nesting while keeping the Django package properly named.

Django REST Framework is included from the start so the app serves both HTML pages and a REST API. This API will be the single source of truth for a future mobile app and content automation service (both in their own separate repos).

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
- `uv init` to create `pyproject.toml`, then add dependencies: `django`, `djangorestframework`, `psycopg2-binary`, `gunicorn`
- `uv venv .venv --python=3.12`
- `uv run django-admin startproject financeapp .` -- creates `manage.py` + `financeapp/` package
- `uv run python manage.py startapp pages` -- creates the first app

### 3. Configure Django settings

- In `app/financeapp/settings.py`:
  - Register `pages` and `rest_framework` in `INSTALLED_APPS`
  - Set `TEMPLATES DIRS` to `BASE_DIR / 'templates'`
  - Configure `DATABASES` for PostgreSQL using `os.environ` (from `.env`):
    - ENGINE, HOST, PORT, NAME, USER, PASSWORD
  - Set `STATIC_URL` and `STATICFILES_DIRS`
  - Add basic `REST_FRAMEWORK` config (default permission classes, pagination)

### 4. Create the one-page view, template, and API endpoint

- `pages/views.py`: `HomePageView` using `TemplateView` + a simple DRF `APIView` at `/api/status/`
- `pages/urls.py`: route `''` to `HomePageView`
- `pages/api_urls.py`: route `/api/status/` to the API status view
- `financeapp/urls.py`: include `pages.urls` and `pages.api_urls`
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

### 9. Create `docker-compose.yml` at the repo root

Three services orchestrated together:

- **db** (PostgreSQL):
  - Image: `postgres:16`
  - Env vars from `.env` for `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
  - Named volume for data persistence
  - Healthcheck so app waits for DB readiness

- **app** (Django):
  - Build context: `./app`
  - `depends_on: db` (with healthcheck condition)
  - Env vars from `.env` (DB connection, SECRET_KEY)
  - Exposes port `8000`

- **tests** (pytest):
  - Build context: `./tests`
  - `depends_on: app`
  - Runs `pytest` against `http://app:8000/`
  - Exits after test run completes

Run everything: `docker compose up --build --abort-on-container-exit`

```mermaid
graph LR
  db["db (postgres:16)"] -->|"5432"| app["app (Django :8000)"]
  app -->|"8000"| tests["tests (pytest)"]
```

### 10. Update root files

- Update `.gitignore` to cover both `.venv/` dirs, `__pycache__/`, `db.sqlite3`, `.env`
- Update `README.md` with setup and run instructions

