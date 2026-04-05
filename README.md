# Portfolio Backend (Django + DRF)

Production-grade, lightweight backend for the portfolio frontend.

## Stack

- Django + Django REST Framework
- PostgreSQL
- Redis cache + broker/result backend
- JWT auth (`djangorestframework-simplejwt`)
- OpenAPI docs (`drf-spectacular`)
- Cloudinary media storage
- Celery worker + beat + Flower monitoring
- Sentry error tracking + tracing
- Docker + Docker Compose + Nginx

## Architecture

- `apps/users`: auth + public profile API
- `apps/portfolio`: services and projects APIs
- `apps/blog`: blog posts and tags APIs
- `apps/core`: health, contact workflows, links, media uploads

Each app follows strict separation:

- models: schema only
- serializers: validation/transformation
- services: business/query orchestration
- views: thin HTTP controllers

## Environment

1. Copy `.env.example` to `.env` inside `backend/`.
2. Fill every variable (no silent defaults are used for runtime config).
3. Keep `DJANGO_ENV` explicit (`dev`, `test`, `prod`).

## API v1

- `GET /health/`
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
- `POST /api/v1/media/project-cover/` (JWT protected)
- `POST /api/v1/auth/token/`
- `POST /api/v1/auth/token/refresh/`
- `GET /api/v1/schema/`
- `GET /api/v1/docs/`

## Query Performance

- N+1 prevention for portfolio endpoints via `prefetch_related("images", "metrics", "links__content_type")`
- N+1 prevention for blog endpoints via `select_related("author")` + `prefetch_related("tags")`
- Payload shaping with `only()` + `annotate(image_count=Count("images"))`
- Atomic view counters with `F("view_count") + 1`

## Local Commands

Run from backend repository root:

- `/home/roni/Desktop/Portfolio/.venv/bin/uv sync`
- `DJANGO_SETTINGS_MODULE=config.settings.test /home/roni/Desktop/Portfolio/.venv/bin/uv run pytest -q`
- `DJANGO_SETTINGS_MODULE=config.settings.test /home/roni/Desktop/Portfolio/.venv/bin/uv run ruff check .`
- `DJANGO_SETTINGS_MODULE=config.settings.test /home/roni/Desktop/Portfolio/.venv/bin/uv run mypy .`

## VPS Deployment (Docker + Nginx)

Run from backend folder:

- `docker compose build`
- `docker compose up -d`

If Redis logs warn about `vm.overcommit_memory`, see `backend/docs/vps-docker-deploy.md`.

Services:

- `web`: Django + Gunicorn
- `db`: PostgreSQL (optional; only starts with `--profile local-db`)
- `redis`: cache + broker + result backend
- `worker`: Celery worker
- `beat`: Celery scheduler
- `flower`: Celery monitoring on `127.0.0.1:${FLOWER_HOST_PORT:-5555}`

This compose stack exposes the API only on `127.0.0.1:${WEB_HOST_PORT:-8004}`.

Recommended `.env` values on multi-project VPS hosts:

- `WEB_HOST_PORT=8004` (set any free local port per project)
- `FLOWER_HOST_PORT=5555` (set any free local port if Flower is used)

On a VPS running multiple sites, keep a single host-level Nginx bound to ports `80/443` and proxy `api.roniahamed.com` to `http://127.0.0.1:${WEB_HOST_PORT:-8004}`.

Startup behavior:

- `web` runs migrations and `collectstatic` during boot.
- `worker`, `beat`, and `flower` do not run Django management commands at startup.

Manual management commands:

- `docker compose run --rm -e RUN_MIGRATIONS=false -e COLLECT_STATIC=false web python manage.py makemigrations`
- `docker compose run --rm -e RUN_MIGRATIONS=false -e COLLECT_STATIC=false web python manage.py migrate`

External PostgreSQL mode (Neon, Supabase, RDS):

- Set `DATABASE_URL` in `.env` to your external PostgreSQL URL.
- Start app stack (local `db` is not started by default):
	- `docker compose up -d`
- Local PostgreSQL service is optional and only started when profile is enabled:
	- `docker compose --profile local-db up -d db`

## Uptime Monitoring

- Better Stack setup guide: `backend/docs/betterstack-monitoring.md`
