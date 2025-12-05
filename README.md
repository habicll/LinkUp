# LinkUp — Fullstack (Django REST + Vue 3/Vite)

A recruitment-style web app: Django REST backend (Token auth + dj-rest-auth) and a Vue 3 + Vite frontend. This README covers setup for development (backend + frontend), database/migrations, API endpoints and a short tech stack overview.

---

## Table of contents
- Project layout
- Quick start (dev)
- Backend
  - Prerequisites
  - Install & run
  - Environment & DB
  - Migrations
  - Useful management commands
- Frontend
  - Prerequisites
  - Install & run
- API (endpoints summary)
- Tech stack
- Troubleshooting
- License / notes

---

## Project layout

Top-level folders:

- `LinkUpB/LinkUpBack/` — Django backend project (`manage.py`, project settings, `myapp/` app)
- `LinkUpF/` — Vue 3 frontend (Vite) app
- `requirements.txt` — Python dependencies for backend

Key backend app: `LinkUpB/LinkUpBack/myapp/` (models, serializers, views, urls, migrations)

Key frontend: `LinkUpF/src/` (components, views, router)

---

## Quick start (dev)

1. Start the database (MySQL). The project expects a MySQL server on `127.0.0.1:3306` with a database named `linkup` (default credentials shown in `settings.py`).
2. Set up and run the backend (see below).
3. Set up and run the frontend (see below).

Open the frontend at `http://127.0.0.1:5173` (Vite default) and the backend at `http://127.0.0.1:8000` (Django runserver default).

---

## Backend

Location: `LinkUpB/LinkUpBack`

### Prerequisites

- Python 3.10+ (project references Python 3.10/3.13 in the workspace)
- MySQL server (client + server) and the `mysqlclient` Python package
- Recommended: create a virtualenv

### Install

From the repository root (or inside `LinkUpB/LinkUpBack`):

```bash
# create & activate a virtualenv (example)
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

Notes:
- `requirements.txt` is at the repo root and includes the backend requirements (Django 5.2.x, djangorestframework, dj-rest-auth, mysqlclient, etc.).

### Database / Environment

Default DB settings (in `LinkUpB/LinkUpBack/LinkUpBack/settings.py`):

- ENGINE: `django.db.backends.mysql`
- NAME: `whatever`
- USER: `root`
- PASSWORD: `whatever`
- HOST: `127.0.0.1`
- PORT: `3306`

If you want to start from a clean DB (recommended during development when schema changed):

```sql
-- run in your MySQL client
DROP DATABASE IF EXISTS linkup;
CREATE DATABASE linkup CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Or (from shell):

```bash
mysql -u root -p -e "DROP DATABASE IF EXISTS linkup; CREATE DATABASE linkup CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### Migrations & run

From `LinkUpB/LinkUpBack` (where `manage.py` lives):

```bash
# apply migrations
python manage.py migrate

# create a superuser (optional)
python manage.py createsuperuser

# run development server
python manage.py runserver 0.0.0.0:8000
```

Important: If you edited migrations manually or renamed models (ex: jobs→advertisements), and your DB contains old tables, either drop the DB and recreate, or generate proper rename migrations. This repo has changed migrations in-development, so a clean DB is the simplest path.

### Useful management commands

- `python manage.py shell` — open Django shell
- `python manage.py showmigrations` — migrations status
- `python manage.py makemigrations myapp` — create migrations when models change

---

## Frontend

Location: `LinkUpF/` (Vite + Vue 3)

### Prerequisites

- Node.js 18+ and npm (or pnpm/yarn)

### Install & run

From `LinkUpF/`:

```bash
npm install
npm run dev
```

Vite serves the app by default on `http://127.0.0.1:5173`.

If you change API base URLs in the frontend, they are hard-coded in files like `src/components/swipe.vue`, `choice.vue`, `status.vue`, `Form.vue` — search for `http://127.0.0.1:8000/` or the resource names (`advertisements`, `people`, `applications`). Consider moving the API base to an environment variable (`import.meta.env`) for easier config.

---

## API — Endpoints summary

The backend exposes Django REST Framework viewsets and some auth endpoints. The common resource names used by the frontend are:

- `/profils/` — profiles
- `/people/` — seekers / people
- `/companies/` — companies
- `/advertisements/` — job advertisements (fields: `short_description`, `long_description`, etc.)
- `/applications/` — relations / applications (fields: `Id_Profil`, `Id_Job`, `accept`, `message`)

Authentication:
- Token authentication is used. The frontend stores the token in `localStorage` under `access_token` and sends headers: `Authorization: Token <token>`.
- Registration and login routes use dj-rest-auth / allauth endpoints with a custom registration flow. The backend returns/creates tokens on registration/login.

Common request examples

- Get advertisements (authenticated):

  GET /advertisements/

- Create application (authenticated):

  POST /applications/
  Body (JSON): { "Id_Job": <ad_id>, "message": "..." }

- Accept an application (company):

  PATCH /applications/<id>/
  Body: { "accept": 1 }

- Reject an application (company):

  PATCH /applications/<id>/
  Body: { "accept": 0 }

Note: The backend may expect `Id_Profil` to be set server-side (the serializer create method sets the current user as the profile). If the client still sends it, it will be ignored/overridden.

---

## Tech stack

- Backend: Django 5.2, Django REST Framework, dj-rest-auth, django-allauth, MySQL (mysqlclient)
- Frontend: Vue 3, Vite, Vuetify (UI components), Swiper (carousel), Axios (HTTP)
- Authentication: Token auth (DRF Token) with dj-rest-auth endpoints