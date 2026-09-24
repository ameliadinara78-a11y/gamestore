# Open Arcade Index

A catalog of free and open-source games, built with Django, PostgreSQL, Tailwind, htmx, and Alpine.js. Filtering and search swap only the results grid over htmx, so browsing feels like a single-page app without a JavaScript framework.

## Stack

- Django 5 (class-based views, custom model manager for search/filter)
- PostgreSQL
- Tailwind CSS, htmx, Alpine.js (loaded via CDN for development)
- WhiteNoise for static files
- Gunicorn + Docker for serving

## Run with Docker

```bash
cp .env.example .env
docker compose up --build
```

The web container runs migrations, seeds the catalog, collects static files, and starts Gunicorn. Open http://localhost:8000.

## Run locally

Requires Python 3.12+ and a running PostgreSQL instance.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

python manage.py migrate
python manage.py seed_catalog
python manage.py createsuperuser
python manage.py runserver
```

## Auto-start on boot (Linux VPS)

Both services carry `restart: unless-stopped`, so Docker brings them back up on its own after a crash or a host reboot — as long as the Docker daemon itself is enabled to start at boot:

```bash
sudo systemctl enable --now docker

cd /path/to/gamecatalog
cp .env.example .env   # edit with real production values first
docker compose up -d --build
```

That's it — no extra systemd unit is needed. `docker compose up -d` starts the containers once; after that, `systemd` restarts `docker.service` on every boot, and `docker.service` restarts any container whose restart policy says so (`unless-stopped` = always, unless someone explicitly ran `docker compose stop`).

Verify after a reboot:

```bash
docker compose ps        # both services should show "Up"
curl -I http://localhost:8000/
```

## Notes

- `seed_catalog` is idempotent and ships a curated list of real open-source games with their homepages and source repositories. Re-run it any time to refresh the data.
- Manage the catalog through the Django admin at `/admin/`.
- The CDN builds of Tailwind, htmx, and Alpine keep setup simple. For production, replace the Tailwind CDN with a compiled stylesheet (Tailwind CLI or PostCSS) and pin the htmx/Alpine assets locally.
- Set a strong `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, and a real `DJANGO_ALLOWED_HOSTS` before deploying. Serve behind nginx with TLS terminated at the proxy.
