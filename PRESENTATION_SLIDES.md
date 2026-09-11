# IP-SAKTI Dashboard - Presentation Slides
## Smart India Hackathon 2026 (SIH26045)
### Ministry of Ayush

---

## Slide 1: Title Slide

**IP-SAKTI Dashboard**
Intellectual Property Protection System for AYUSH Traditional Knowledge

**Team:** [Your Team Name]
**Problem Statement:** SIH26045
**Ministry:** Ministry of Ayush
**Idea:** IP-SAKTI Dashboard (Ministry Analytics Portal)

**Tagline:** *"Protecting India's Traditional Knowledge from Biopiracy"*

---

## Slide 2: Problem Statement

### The Challenge
- **Biopiracy** is the unauthorized use of traditional knowledge by foreign entities
- India has lost several patents on traditional formulations (Turmeric, Neem, Basmati)
- **TKDL** (Traditional Knowledge Digital Library) exists but lacks real-time monitoring
- Ministry officials need a unified dashboard to track IP activity

### Statistics
- **2,000+** traditional formulations documented in TKDL
- **300+** GI tags issued across India
- **500+** AYUSH-related patents filed annually
- **50+** biopiracy attempts detected yearly

### Our Solution
A real-time analytics portal that:
- Monitors patents for biopiracy
- Tracks GI tags across India
- Provides state-wise analytics
- Enables quick prior art filing

---

## Slide 3: Solution Overview

### IP-SAKTI Dashboard Features

1. **Real-time KPI Dashboard**
   - Total GI Tags, Patents, Alerts, Digitized Texts
   - Live updates every 60 seconds

2. **India State-wise Heatmap**
   - Interactive Leaflet.js map
   - Drill-down from national → state → district

3. **Biopiracy Detection**
   - Rule-based detection (no external AI APIs)
   - Risk scoring algorithm
   - Real-time alerts

4. **Case Management**
   - Assign cases to analysts
   - Track resolution status
   - Export reports

5. **Multilingual Support**
   - English + Hindi
   - i18next internationalization

6. **Offline-first PWA**
   - Works without internet
   - For field officials

---

## Slide 4: Technology Stack

### Backend
- **Python 3.11+** with **Django 5.0**
- **Django REST Framework** for APIs
- **PostgreSQL 16** for database
- **Redis + Celery** for background tasks
- **JWT Authentication** (SimpleJWT)
- **spaCy + NLTK** for local NLP

### Frontend
- **React 18** + **Vite**
- **TailwindCSS** for styling
- **Recharts** for charts
- **Leaflet.js** for India map
- **React Query** for data fetching
- **i18next** for i18n

### DevOps
- **Nginx** + **Gunicorn**
- **NO DOCKER** - Native deployment
- Supports AWS Mumbai / NIC Cloud

### Why These Technologies?
- All open source (MIT/Apache licenses)
- No external AI API dependencies
- Works on 4GB RAM servers
- MeitY compliant

---

## Slide 5: System Architecture

```
┌─────────────────────────────────────────┐
│         IP-SAKTI Frontend (React)        │
│  - Dashboard, Charts, Maps, Reports      │
│  - PWA, i18n, Dark Mode                  │
└──────────────┬──────────────────────────┘
               │ HTTPS/REST API
┌──────────────▼──────────────────────────┐
│      Django REST Framework (Backend)     │
│  - Authentication (JWT)                  │
│  - Role-based Access (RBAC)              │
│  - API Endpoints (DRF ViewSets)          │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼────┐ ┌──▼────┐ ┌──▼─────┐
│PostgreSQL│ │ Redis │ │ Celery │
│ (Data)  │ │(Cache)│ │(Tasks) │
└─────────┘ └───────┘ └────────┘
               │
       ┌───────▼────────┐
       │  Data Sources  │
       │ - IP India     │
       │ - TKDL         │
       │ - GI Registry  │
       └────────────────┘
```

---

## Slide 6: Database Schema

### Core Models

**Users**: id, email, role, department, created_at
- Roles: ADMIN, MINISTRY, ANALYST, VIEWER

**States**: id, name, code, region, coordinates
- 28 states + 8 UTs with AYUSH council names

**GITags**: id, name, product, state_id, status, issued_date
- Track GI tags across India

**Patents**: id, title, applicant, country, filing_date, status
- AYUSH category classification
- Biopiracy suspect flag

**BiopiracyCases**: id, patent_id, formulation_id, status, priority
- Detection, review, escalation, resolution workflow

**AYUSHFormulations**: id, name, ingredients, category, source_text
- Traditional knowledge database

**Alerts**: id, type, severity, message, created_at
- Real-time notification system

**TKDL_Entries**: id, formulation_name, digitized_date, coverage%
- Digital library tracking

---

## Slide 7: Key Features - Demo

### 1. Live Dashboard
- **6 KPI Cards** with real-time data
- **India Heatmap** showing IP activity
- **Monthly Trends** line chart
- **Category Distribution** pie chart

### 2. Live Simulation Mode
- Button to simulate biopiracy alerts
- Demonstrates real-time notification system
- Shows alert severity and assignment workflow

### 3. Case Tracker
- Advanced filters (state, status, type, date)
- Export to CSV/PDF
- Case assignment and resolution

### 4. State Comparison
- Compare 2-4 states side-by-side
- GI tags, patents, formulations, biopiracy cases

### 5. Success Stories
- Turmeric Patent Case 1995 - India Won
- Neem Patent Challenge 2000
- Basmati Rice Patent 2001

### 6. India First Counter
- Shows successful prior art submissions
- Motivates officials to act

---

## Slide 8: Security & Compliance

### Security Features
- **JWT Authentication** with refresh tokens
- **Role-based Access Control** (4 roles)
- **CSRF Protection** (Django built-in)
- **SQL Injection Prevention** (Django ORM)
- **XSS Protection** (React sanitization)
- **HTTPS Enforcement** (Nginx)

### Compliance
- **MeitY Guidelines** compliant
- **WCAG 2.1 AA** accessible
- **Data Residency**: India (AWS Mumbai / NIC Cloud)
- **Open Source**: MIT/Apache 2.0 licenses only
- **No External AI APIs**: Local NLP only

### Privacy
- User data encrypted at rest
- No PII logging
- Audit trails for all actions

---

## Slide 9: Scalability & Performance

### Performance Optimizations
- **Redis Caching**: Dashboard KPIs cached for 5 minutes
- **Celery Beat**: Scheduled tasks for data fetching
- **Database Indexing**: Optimized queries
- **Frontend Code Splitting**: React lazy loading
- **PWA Caching**: Offline support

### Scalability
- **4GB RAM** server compatible
- **Gunicorn** with 3 workers
- **PostgreSQL** connection pooling
- **Static files** served by Nginx

### Deployment Options
- **NIC Cloud** (recommended for government)
- **AWS Mumbai Region**
- **On-premises** server
- **NO DOCKER** required

---

## Slide 10: Future Roadmap

### Phase 1 (Current - Demo)
- ✅ Core dashboard with KPIs
- ✅ Biopiracy detection (rule-based)
- ✅ Case management
- ✅ Reports export

### Phase 2 (3 months)
- Integration with IP India API
- Automated patent monitoring
- Local ML (scikit-learn) biopiracy detection
- Mobile app (React Native)

### Phase 3 (6 months)
- Blockchain for prior art verification
- Local NLP (spaCy, RapidFuzz) formulation matching
- Multi-language support (12+ Indian languages)
- Integration with DigiLocker for authentication

### Impact
- **Protect** 10,000+ traditional formulations
- **Prevent** biopiracy of Indian knowledge
- **Empower** 1000+ ministry officials
- **Support** policy decisions with data

---

## Thank You

### Questions?

**IP-SAKTI Dashboard**
*Ministry of Ayush | Smart India Hackathon 2026*

**Contact:** [Your Contact Information]

**GitHub:** [Repository Link]

---

*"सत्यमेव जयते" - Truth Alone Triumphs*
