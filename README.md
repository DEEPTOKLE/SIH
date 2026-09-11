# IP-SAKTI Dashboard

**Intellectual Property Protection System for AYUSH Traditional Knowledge**

Ministry of Ayush | Smart India Hackathon 2026 (SIH26045)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0-green)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-18-blue)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://postgresql.org)

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Running the Application](#running-the-application)
8. [Production Deployment](#production-deployment)
9. [API Documentation](#api-documentation)
10. [SIH Demo Guide](#sih-demo-guide)
11. [Compliance](#compliance)
12. [License](#license)

---

## Overview

IP-SAKTI is a real-time analytics and monitoring portal for the Ministry of Ayush to track the health of India's AYUSH IP ecosystem. The system helps protect India's traditional knowledge from biopiracy by:

- Tracking GI tags issued across India
- Monitoring patents filed on AYUSH formulations
- Detecting and alerting on biopiracy attempts globally
- Tracking TKDL (Traditional Knowledge Digital Library) database coverage
- Providing state-wise analytics on AYUSH IP activity
- Enabling policy decisions through trend analysis

### Problem Statement
**SIH26045** - Protecting India's traditional AYUSH knowledge from biopiracy and strengthening India's IP ecosystem

---

## Features

### Core Features
- **KPI Dashboard**: Real-time metrics for GI tags, patents, biopiracy alerts, and digitized texts
- **India State-wise Heatmap**: Interactive Leaflet.js map showing IP activity across states
- **Trend Analysis**: Monthly trends for GI tags, patents, and biopiracy cases
- **Category Distribution**: AYUSH category-wise breakdown (Ayurveda, Yoga, Unani, Siddha, Homoeopathy)
- **Case Tracker**: Advanced filtering and case management for biopiracy cases
- **Alert Management**: Real-time notification system for biopiracy attempts
- **Reports**: Export data as CSV and PDF
- **State Comparison**: Compare IP metrics between multiple states

### Demo-Winning Features
- **Live Simulation**: Simulate real-time biopiracy alerts
- **India First Counter**: Track successful prior art submissions
- **Success Stories**: Showcase landmark cases (Turmeric 1995, Neem 2000, Basmati 2001)
- **Offline-first PWA**: Works without internet for field officials
- **Bilingual Support**: English + Hindi (i18next)

---

## Tech Stack

### Backend
- **Python 3.11+**
- **Django 5.0** + Django REST Framework
- **PostgreSQL 16**
- **Redis** + Celery (background tasks)
- **JWT Authentication** (SimpleJWT)
- **spaCy** (local NLP for biopiracy detection)

### Frontend
- **React 18** + Vite
- **TailwindCSS** for styling
- **Recharts** for charts
- **Leaflet.js** for India map
- **React Query** for data fetching
- **i18next** for internationalization
- **Zustand** for state management

### DevOps
- **Nginx** (reverse proxy)
- **Gunicorn** (WSGI server)
- **NO DOCKER** - Native deployment only

---

## Project Structure

```
ip-sakti-backend/
├── ip_sakti/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── celery.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tasks.py
│   ├── seed_data.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── dashboard/
│   │   ├── __init__.py
│   │   ├── views.py
│   │   └── urls.py
│   └── notifications/
│       ├── __init__.py
│       ├── views.py
│       └── urls.py
├── requirements.txt
└── manage.py

ip-sakti-frontend/
├── src/
│   ├── components/
│   │   ├── Layout.jsx
│   │   ├── KPICards.jsx
│   │   ├── IndiaMap.jsx
│   │   ├── CategoryChart.jsx
│   │   ├── MonthlyTrends.jsx
│   │   ├── RecentAlerts.jsx
│   │   ├── SuccessStories.jsx
│   │   ├── ThemeProvider.jsx
│   │   └── ProtectedRoute.jsx
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── CaseTracker.jsx
│   │   ├── Analytics.jsx
│   │   ├── AlertManagement.jsx
│   │   ├── Reports.jsx
│   │   ├── Profile.jsx
│   │   └── Login.jsx
│   ├── services/
│   │   └── api.js
│   ├── i18n/
│   │   ├── index.js
│   │   ├── locales/en.json
│   │   └── locales/hi.json
│   ├── utils/
│   │   └── simulation.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── package.json
├── vite.config.js
├── tailwind.config.js
└── index.html

setup_local.bat        # Windows development setup
setup_local.sh         # Linux / macOS development setup
deploy_local.sh        # Linux production deployment (native, no Docker)
deploy_local.bat       # Windows production setup (native, no Docker)
README.md
```

---

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 16
- Redis 7+
- Node.js 18+
- npm or yarn

### Windows Users
- **Recommended**: Use WSL2 (Ubuntu) and follow the Linux instructions below, OR
- Use the provided `setup_local.bat` for a guided setup, OR
- Use the native Windows steps described in [Running the Application](#running-the-application-windows)

> Note: Linux shell scripts (`.sh`) cannot run directly on Windows. Use WSL2 or Git Bash if you want to run the Linux scripts from Windows.

### Quick Setup (Automated)

#### Windows
```batch
setup_local.bat
```

#### Linux / macOS
```bash
chmod +x setup_local.sh
./setup_local.sh
```

### Manual Setup

#### 1. Clone and setup backend

```bash
# Linux / macOS
cd ip-sakti-backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux / macOS:
source venv/bin/activate
# Windows (PowerShell / CMD):
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Setup PostgreSQL

```bash
# Create database
psql -U postgres -c "CREATE DATABASE ipsakti_db;"

# Create user (optional)
psql -U postgres -c "CREATE USER ipsakti_user WITH PASSWORD 'your_password';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ipsakti_db TO ipsakti_user;"
```

#### 3. Configure Django

Create a `.env` file in `ip-sakti-backend/`:

```env
# Django
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key-here

# Database
DB_NAME=ipsakti_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gov.in
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=IP-SAKTI <no-reply@ipsakti.gov.in>

# External APIs (Mock for demo)
IP_INDIA_API_URL=https://ipindia.gov.in
TKDL_API_URL=https://tkdl.csir.res.in
GI_REGISTRY_URL=https://ipindia.gov.in/girindia

# Notifications
MSG91_API_KEY=your-msg91-api-key
MSG91_SENDER_ID=IPSKTI
```

#### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Seed sample data

```bash
python manage.py seed_data
```

#### 6. Create superuser

```bash
python manage.py createsuperuser
```

#### 7. Setup frontend

```bash
# Linux / macOS / Windows
cd ip-sakti-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## Configuration

### Environment Variables

Create a `.env` file in `ip-sakti-backend/`:

```env
# Django
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key-here

# Database
DB_NAME=ipsakti_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gov.in
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=IP-SAKTI <no-reply@ipsakti.gov.in>

# External APIs (Mock for demo)
IP_INDIA_API_URL=https://ipindia.gov.in
TKDL_API_URL=https://tkdl.csir.res.in
GI_REGISTRY_URL=https://ipindia.gov.in/girindia

# Notifications
MSG91_API_KEY=your-msg91-api-key
MSG91_SENDER_ID=IPSKTI
```

---

## Running the Application

### Development Mode

#### Backend

```bash
# Linux / macOS
cd ip-sakti-backend
source venv/bin/activate
python manage.py runserver

# In a new terminal, start Celery worker
# Linux / macOS:
celery -A ip_sakti worker -l info
# Windows:
# celery -A ip_sakti worker --pool=solo -l info

# In a new terminal, start Celery Beat (optional, for scheduled tasks)
celery -A ip_sakti beat -l info
```

#### Frontend

```bash
# All platforms
cd ip-sakti-frontend
npm install
npm run dev

# Open browser to http://localhost:5173
```

---

## Production Deployment

### Linux (Ubuntu / RHEL / macOS)

```bash
# Make script executable
chmod +x deploy_local.sh

# Run deployment
sudo ./deploy_local.sh

# Start services
sudo systemctl start redis-server
sudo systemctl start postgresql
sudo systemctl start ipsakti
sudo systemctl start ipsakti-celery
sudo systemctl start ipsakti-celery-beat
sudo systemctl status ipsakti
```

### Windows

```batch
deploy_local.bat
```

This will:
1. Create `.env` with generated credentials
2. Install Python dependencies + Waitress
3. Setup PostgreSQL user and database
4. Run Django migrations and collectstatic
5. Build frontend (if Node.js is available)
6. Create `run_django.bat`, `run_celery.bat`, and `run_frontend.bat`

To run on Windows:
```batch
REM Start Redis first
redis-server

REM Terminal 1: Django
cd ip-sakti-backend
run_django.bat

REM Terminal 2: Celery
cd ip-sakti-backend
run_celery.bat

REM Terminal 3: Frontend (dev)
cd ip-sakti-frontend
run_frontend.bat
```

### Manual Nginx Configuration (Linux)

`deploy_local.sh` creates `/etc/nginx/sites-available/ipsakti` automatically.

If you need to configure manually:

```nginx
server {
    listen 80;
    server_name _;

    client_max_body_size 100M;

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        root /path/to/ip-sakti-backend/staticfiles;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        root /path/to/ip-sakti-frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

Enable the site:
```bash
sudo ln -sf /etc/nginx/sites-available/ipsakti /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

### Gunicorn Service (Linux)

`deploy_local.sh` creates `/etc/systemd/system/ipsakti.service` automatically.

If you need to configure manually, create `/etc/systemd/system/ipsakti.service`:

```ini
[Unit]
Description=IP-SAKTI Django Application
After=network.target

[Service]
User=your-user
Group=your-user
WorkingDirectory=/path/to/ip-sakti-backend
Environment="PATH=/path/to/ip-sakti-backend/venv/bin"
ExecStart=/path/to/ip-sakti-backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 ip_sakti.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ipsakti
sudo systemctl start ipsakti
```

---

## API Documentation

### Authentication

All API endpoints require JWT authentication.

```bash
# Login
POST /api/auth/token/
{
  "email": "admin@ipsakti.gov.in",
  "password": "admin123"
}

# Response
{
  "refresh": "...",
  "access": "..."
}
```

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dashboard/kpis/` | GET | Dashboard KPIs |
| `/api/gi-tags/` | GET | List GI tags |
| `/api/patents/` | GET | List patents |
| `/api/biopiracy-cases/` | GET | List biopiracy cases |
| `/api/alerts/` | GET | List alerts |
| `/api/alerts/unread-count/` | GET | Unread alerts count |
| `/api/states/` | GET | List states |
| `/api/dashboard/state-analytics/` | GET | State analytics |
| `/api/dashboard/compare-states/` | POST | Compare states |

### Sample API Response

```json
{
  "total_gi_tags": 342,
  "total_patents": 567,
  "total_biopiracy_alerts": 89,
  "active_biopiracy_cases": 23,
  "resolved_biopiracy_cases": 66,
  "texts_digitized": 4750,
  "total_formulations": 215,
  "registered_formulations": 189,
  "india_prior_art_success": 67,
  "monthly_trends": {
    "2024-01": {
      "gi_tags": 12,
      "patents": 25,
      "biopiracy_cases": 5
    }
  },
  "category_distribution": {
    "AYURVEDA": {
      "gi_tags": 180,
      "patents": 320,
      "formulations": 120
    }
  },
  "state_wise_data": [
    {
      "state_id": "...",
      "state_name": "Kerala",
      "gi_tags": 45,
      "patents": 0,
      "formulations": 32,
      "biopiracy_cases": 8
    }
  ]
}
```

---

## SIH Demo Guide

### Demo Flow for Judges (10 minutes)

1. **Login** (30 seconds)
   - Show DigiLocker mock option
   - Login with demo credentials

2. **Dashboard Overview** (2 minutes)
   - Show 6 KPI cards with live data
   - Click on India map to show state drill-down
   - Show monthly trends chart

3. **Live Simulation** (1 minute)
   - Click "Live Simulation" button
   - Show real-time alert appearing
   - Demonstrate notification badge

4. **Case Tracker** (2 minutes)
   - Show filterable table
   - Apply filters (status, priority, date)
   - Export as CSV

5. **Alert Management** (2 minutes)
   - Show critical biopiracy alert
   - Assign to analyst
   - Mark as resolved

6. **Analytics** (1.5 minutes)
   - Show state comparison
   - Category distribution chart
   - Top 15 states bar chart

7. **Success Stories** (1 minute)
   - Turmeric Patent Case 1995
   - India First counter

### Key Talking Points

- **No external AI APIs**: All biopiracy detection uses local NLP (spaCy) and rule-based logic
- **Offline-first PWA**: Works without internet for field officials
- **Multilingual**: English + Hindi support
- **Scalable**: Designed for 4GB RAM servers
- **Compliant**: MeitY guidelines, WCAG 2.1 AA

---

## Compliance

### MeitY Guidelines
- Data stored in India (AWS Mumbai / NIC Cloud)
- Open source licenses (MIT, Apache 2.0)
- No Docker - native deployment
- WCAG 2.1 AA accessibility

### Security
- JWT authentication with refresh tokens
- Role-based access control
- CSRF protection
- SQL injection prevention (Django ORM)
- XSS protection

### Accessibility
- Keyboard navigation
- Screen reader friendly
- High contrast mode support
- ARIA labels

---

## Default Credentials

| Role | Email | Password |
|------|-------|----------|
| Administrator | admin@ipsakti.gov.in | admin123 |
| Ministry Official | official@ipsakti.gov.in | official123 |
| Analyst | analyst@ipsakti.gov.in | analyst123 |
| Viewer | viewer@ipsakti.gov.in | viewer123 |

---

## Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify credentials in .env file
```

### Redis Connection Error
```bash
# Start Redis
redis-server

# Check Redis is running
redis-cli ping
```

### Port Already in Use
```bash
# Change port in vite.config.js for frontend
# Change port in Django settings.py for backend
```

### Celery Worker Not Starting
```bash
# Windows: Use --pool=solo flag
celery -A ip_sakti worker --pool=solo -l info

# Linux/macOS: Use --pool=solo if needed
celery -A ip_sakti worker --pool=solo -l info
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/your-repo/issues)
- Email: support@ipsakti.gov.in

---

## Acknowledgments

- Ministry of Ayush for the problem statement
- TKDL (Traditional Knowledge Digital Library) for data
- IP India for patent data
- GI Registry for GI tag data

---

**Made with ❤️ for India's Traditional Knowledge Protection**

Jai Hind! 🇮🇳🌿
