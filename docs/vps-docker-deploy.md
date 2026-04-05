# VPS Deployment: Docker + Nginx + Celery

## 1. Prepare Server

- Install Docker Engine and Docker Compose plugin.
- Open ports `80` (HTTP) and `5555` (optional Flower UI).
- Clone repository and create `.env` from `.env.example` inside `backend/`.

## 2. Required Environment Contract

Every variable in `.env.example` is required.

Critical runtime values:

- `DJANGO_ENV=prod`
- `DATABASE_URL=postgresql://<user>:<password>@db:5432/<db_name>`
- `REDIS_CACHE_URL=redis://redis:6379/1`
- `CELERY_BROKER_URL=redis://redis:6379/0`
- `CELERY_RESULT_BACKEND=redis://redis:6379/2`
- `SENTRY_DSN=<dsn>`

## 3. Build and Launch

From `backend/`:

```bash
docker compose build
docker compose up -d
```

## 4. Validate Services

```bash
docker compose ps
docker compose logs -f web
docker compose logs -f worker
docker compose logs -f beat
```

Health endpoint:

```bash
curl http://<server-ip>/health/
```

## 5. Runtime Architecture

- `nginx` receives all inbound traffic and proxies app requests to `web`.
- `web` runs Gunicorn and only handles short-lived request logic.
- `worker` handles email delivery, media optimization, and cache warming jobs.
- `beat` schedules periodic jobs (cache warmup, analytics aggregation).
- `redis` serves both Django cache and Celery broker/result backend.
- `db` serves PostgreSQL persistence.

## 6. Operational Notes

- Keep `CELERY_TASK_ALWAYS_EAGER=false` in production.
- Keep `DJANGO_DEBUG=false` in production.
- Scale workers independently when background load grows:

```bash
docker compose up -d --scale worker=4
```

- Rotate credentials and signing keys through env updates, then restart services:

```bash
docker compose up -d --force-recreate
```
