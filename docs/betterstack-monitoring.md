# Better Stack Uptime Monitor Setup

Use this monitor to keep free-tier backend instances warm by hitting a lightweight public endpoint.

## Health Endpoint Contract

- URL path: `/health/`
- Method: `GET`
- Auth: none
- Response body: `{"status":"ok","database":"connected"}`

## Better Stack Dashboard Setup (Recommended)

1. Open Better Stack and go to Uptime.
2. Click `Add monitor`.
3. Configure:
   - Monitor type: `HTTP(s)`
   - URL: `https://<your-domain>/health/`
   - Check frequency: `3 minutes`
   - Regions: `Default`
4. Optional alerting:
   - Enable email alerts for downtime.
5. Save monitor.

## Verification

- In Better Stack, check that the monitor status becomes `Up`.
- Test endpoint directly:

```bash
curl -sS https://<your-domain>/health/
```

Expected:

```json
{"status":"ok","database":"connected"}
```

## Notes

- Replace `<your-domain>` with your deployed backend domain.
- This endpoint is intentionally lightweight so frequent checks are low-cost.
