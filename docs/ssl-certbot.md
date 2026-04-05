# SSL Setup for api.roniahamed.com on Port 8004

This stack serves HTTPS from Nginx TLS port 443 inside container, exposed as host port 8004, so it does not conflict with other projects using host ports 80/443.

Important:
- Let's Encrypt HTTP-01 challenge does not validate directly on port 8004.
- For this setup, use DNS-01 challenge (recommended).

## 1. Start stack

```bash
cd /home/roni/Desktop/Portfolio/backend
docker compose up -d web db redis worker beat nginx
```

Notes:
- `cert-init` auto-creates a short-lived self-signed certificate if Let's Encrypt files are not present yet.
- This keeps `nginx` from crashing on first boot.

## 2. Issue certificate using DNS challenge

Run this once and follow prompts to add TXT records:

```bash
cd /home/roni/Desktop/Portfolio/backend
docker compose run --rm --profile ops certbot certonly \
  --manual \
  --preferred-challenges dns \
  --email you@example.com \
  --agree-tos \
  --no-eff-email \
  -d api.roniahamed.com
```

This stores certs in Docker volume mounted at `/etc/letsencrypt`.

## 3. Reload Nginx after certificate is issued

```bash
cd /home/roni/Desktop/Portfolio/backend
docker compose restart nginx
```

## 4. Verify

```bash
curl -vk https://api.roniahamed.com:8004/health/
```

## 5. Renewal strategy

Manual DNS challenge needs periodic renewal. Recommended alternatives:
- Use DNS API plugin (Cloudflare/Route53) for automated renewals.
- Keep a central reverse proxy on 80/443 and forward to this service on 8004.
