# VPS Deployment: Docker + Nginx + Celery

## 1. Prepare Server

- Install Docker Engine and Docker Compose plugin.
- Ensure your existing host Nginx is bound to ports `80/443`.
- Do not bind this compose stack to `80/443` (avoids conflicts with other sites).
- Open port `5555` only if you want Flower UI accessible.
- Clone repository and create `.env` from `.env.example` inside `backend/`.

### Kernel tuning (Redis)

If you see this warning in Redis logs:

> WARNING Memory overcommit must be enabled!

Apply on the VPS host (not inside the container):

```bash
sudo sysctl -w vm.overcommit_memory=1
```

Persist across reboots:

```bash
echo 'vm.overcommit_memory = 1' | sudo tee /etc/sysctl.d/99-redis.conf
sudo sysctl --system
```

## 2. Required Environment Contract

Every variable in `.env.example` is required.

Critical runtime values:

- `DJANGO_ENV=prod`
- `DATABASE_URL=postgresql://<user>:<password>@db:5432/<db_name>`
- `REDIS_CACHE_URL=redis://redis:6379/1`
- `CELERY_BROKER_URL=redis://redis:6379/0`
- `CELERY_RESULT_BACKEND=redis://redis:6379/2`
- `SENTRY_DSN=<dsn>`
- `WEB_HOST_PORT=8004` (choose a unique free local port for this project)
- `FLOWER_HOST_PORT=5555` (choose a unique free local port, optional)

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
curl -vk https://api.roniahamed.com/health/
```

### Host Nginx config (example)

Add this to your host Nginx (the one already serving multiple projects) and reload:

```nginx
server {
	listen 80;
	server_name api.roniahamed.com;
	return 301 https://$host$request_uri;
}

server {
	listen 443 ssl;
	server_name api.roniahamed.com;

	ssl_certificate /etc/letsencrypt/live/api.roniahamed.com/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/api.roniahamed.com/privkey.pem;

	location / {
		proxy_pass http://127.0.0.1:8004;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
	}
}
```

If you set a different `WEB_HOST_PORT`, update `proxy_pass` accordingly.

## 5. Runtime Architecture

- Host Nginx (ports `80/443`) receives all inbound traffic and proxies app requests to this stack on `127.0.0.1:${WEB_HOST_PORT}`.
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
