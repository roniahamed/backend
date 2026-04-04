# Portfolio Backend (Django + DRF)

Production-grade, lightweight backend for the portfolio frontend.

## Stack

- Django + Django REST Framework
- PostgreSQL (via `DATABASE_URL`)
- JWT auth (`djangorestframework-simplejwt`)
- OpenAPI docs (`drf-spectacular`)
- Cloudinary media storage
- LocMem cache (free-tier friendly)

## Architecture

- `apps/users`: auth + public profile API
- `apps/portfolio`: services and projects APIs
- `apps/blog`: blog posts and tags APIs
- `apps/core`: health check and contact submissions

## Environment

1. Copy `.env.example` to `.env` inside `backend/`.
2. Fill every variable (no silent defaults are used for runtime config).

## API v1

- `GET /api/v1/health/`
- `GET /api/v1/profile/`
- `GET /api/v1/services/`
- `GET /api/v1/services/{slug}/`
- `GET /api/v1/projects/`
- `GET /api/v1/projects/{slug}/`
- `GET /api/v1/blog/posts/`
- `GET /api/v1/blog/posts/{slug}/`
- `GET /api/v1/blog/tags/`
- `POST /api/v1/contact/`
- `POST /api/v1/auth/token/`
- `POST /api/v1/auth/token/refresh/`
- `GET /api/v1/schema/`
- `GET /api/v1/docs/`

## Local Commands

Run from repository root:

- `uv sync`
- `DJANGO_ENV=test uv run python backend/manage.py migrate`
- `cd backend && DJANGO_ENV=test uv run pytest -q`
- `cd backend && DJANGO_ENV=test uv run ruff check .`
- `uv run sphinx-build docs docs/_build`
