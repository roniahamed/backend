# SSL Setup for api.roniahamed.com (Host Nginx + Let's Encrypt)

On a multi-project VPS, one host-level Nginx should own ports `80/443` for all domains.
This Docker Compose stack does not bind `80/443`; it exposes the API on `127.0.0.1:8004`.

Important:
- `api.roniahamed.com` must point to this VPS (A/AAAA record).
- Port `80` must be reachable for Let's Encrypt HTTP-01 validation.

## 1. Start stack

```bash
cd /home/roni/Desktop/Portfolio/backend
docker compose up -d
```

Notes:
- `cert-init` auto-creates a short-lived self-signed certificate if Let's Encrypt files are not present yet.
- This keeps `nginx` from crashing on first boot.

## 2. Issue certificate on the VPS host

Use your existing host Nginx + Certbot.

If you already have certbot installed, common options are:

- Nginx plugin (recommended when available): `sudo certbot --nginx -d api.roniahamed.com`
- Webroot: `sudo certbot certonly --webroot -w /var/www/html -d api.roniahamed.com`

## 4. Verify

```bash
curl -vk https://api.roniahamed.com/health/
```

## 5. Renewal strategy

Certbot on the host typically installs an auto-renewal timer. Verify with:

```bash
sudo systemctl list-timers | grep certbot || true
```
