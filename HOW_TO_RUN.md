# How to Run IP-SAKTI Dashboard (Windows 11)

## One-time setup (already done on this machine)

```bash
# Backend: venv + dependencies + database + demo data
cd ip-sakti-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# .env and ipsakti_db already exist; run these only on a fresh machine:
python manage.py migrate
python manage.py seed_data
```

```bash
# Frontend: dependencies
cd ip-sakti-frontend
npm install
```

## Run — every day (3 terminals)

**Terminal 1 — Backend API** (http://127.0.0.1:8000 — API only, no UI here. The root URL shows an endpoint index page; the dashboard UI is on :5173)

```bash
cd ip-sakti-backend
venv\Scripts\activate
python manage.py runserver
```

**Terminal 2 — Frontend dev server** (http://localhost:5173)

```bash
cd ip-sakti-frontend
npm run dev
```

**Terminal 3 — Celery worker (optional; only needed for background tasks)**

```bash
cd ip-sakti-backend
venv\Scripts\activate
celery -A ip_sakti worker --pool=solo -l info
```

> Memurai (Redis) is now installed and runs as a Windows service (port 6379) — it starts automatically on boot. The Celery worker connects to it for background tasks like biopiracy detection and daily stats.

## Open the app

1. Go to **http://localhost:5173**
2. Login with demo credentials (pre-filled): `admin@ipsakti.gov.in` / `admin123`
3. Other roles: `official@ipsakti.gov.in` / `official123`, `analyst@ipsakti.gov.in` / `analyst123`, `viewer@ipsakti.gov.in` / `viewer123`

## Verify it's healthy

```bash
curl http://127.0.0.1:8000/admin/ -o /dev/null -w "%{http_code}\n"   # 302
curl http://localhost:5173 -o /dev/null -w "%{http_code}\n"          # 200
"/c/Program Files/Memurai/memurai-cli.exe" ping                       # PONG
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `python` opens Microsoft Store | Use the full path: `C:\Users\<you>\AppData\Local\Programs\Python\Python312\python.exe`, or reinstall Python with "Add to PATH" checked |
| `node: command not found` | Close and reopen the terminal (PATH refresh), or use `"/c/Program Files/nodejs/npm.cmd"` in Git Bash |
| `psql` not recognized | PostgreSQL CLI is at `"/c/Program Files/PostgreSQL/16/bin/psql.exe"` — add that folder to PATH |
| DB connection refused | Start PostgreSQL: `net start postgresql-x64-16` (admin terminal) |
| Port 8000 already in use | `netstat -ano \| findstr :8000` then `taskkill //F //PID <pid>` |
| Memurai/Redis down | Check `sc query Memurai` and start it with `net start Memurai` (admin). Cache falls back to local memory meanwhile (`SKIP_REDIS=true` in `.env`) — only use that as a temporary fallback |

## What was fixed to make this run

- Added missing `manage.py`, `__init__.py` files, `wsgi.py`, `asgi.py`, `apps.py`
- Moved `User` model to `ip_sakti/users/models.py` (canonical for `AUTH_USER_MODEL`), re-exported from `ip_sakti/models.py`
- Added `users/serializers.py`, `dashboard/views.py`, `notifications/views.py` re-export shims
- Fixed missing `include` imports in `users/urls.py` and `notifications/urls.py`
- Fixed `AYUSHFormulation.state` → `state_of_origin` in views/serializers
- Fixed `seed_data.py` (`IPActivity` import, `username` for `create_user`)
- Added `seed_data` management command (README's `python manage.py seed_data` now works)
- Removed non-existent `static` dir from `STATICFILES_DIRS`; added `SKIP_REDIS` fallback cache
- Trimmed requirements (dropped spacy/nltk/weasyprint; added `requests`)
- Frontend: added `postcss.config.js`, `public/favicon.svg`, fixed all `../../services/api` → `../services/api` import paths
