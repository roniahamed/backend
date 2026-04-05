# Render Deployment for api.roniahamed.com

This runbook deploys the Django backend to Render and maps it to `api.roniahamed.com`.

## 1. Create Render Service

1. In Render: `New +` -> `Web Service`.
2. Connect the GitHub repo.
3. Select the backend service (or use `render.yaml` from repo root).
4. Confirm:
   - Runtime: `Python`
   - Root Directory: `backend`
   - Build Command:
     ```bash
     pip install -r requirements.txt
     python manage.py collectstatic --noinput
     python manage.py migrate
     ```
   - Start Command:
     ```bash
     gunicorn config.wsgi:application --bind
     ```

## 2. Set Environment Variables

Required values:

- `DJANGO_ENV=prod`
- `DJANGO_DEBUG=false`
- `DJANGO_ALLOWED_HOSTS=api.roniahamed.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://api.roniahamed.com`
- `CORS_ALLOWED_ORIGINS=https://<your-frontend-domain>`
- `DATABASE_URL=<neon-or-prod-postgres-url>`
- `DJANGO_SECRET_KEY=<strong-random-secret>`

Also set email/cloudinary/runtime vars listed in `render.yaml`.

## 3. Add Custom Domain

1. Open Render -> Service -> `Settings` -> `Custom Domains`.
2. Add `api.roniahamed.com`.
3. Copy the CNAME target Render provides.

## 4. DNS (Cloudflare/Namecheap/etc.)

Add:

- Type: `CNAME`
- Name: `api`
- Target: `<render-provided-domain>`

Wait for propagation.

## 5. SSL

Render provisions TLS automatically after DNS is valid.

Verify:

- `https://api.roniahamed.com/health/`

Expected response:

```json
{"status":"ok","database":"connected"}
```

## 6. Frontend API Base URL

Set frontend production variable:

```bash
VITE_API_BASE_URL=https://api.roniahamed.com/api/v1
```

## 7. Validate End-to-End

1. Open frontend production site.
2. Check browser devtools for no CORS errors.
3. Verify endpoints:
   - `/profile/`
   - `/services/`
   - `/projects/`
   - `/blog/posts/`
   - `/health/`
