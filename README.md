# Knock Knock Doc — Prototype V0

A light-mode, synthetic-only prototype of a consent-led cross-border healthcare referral network. It demonstrates the closed referral loop shared by a patient, a referring doctor, a receiving hospital team, and a human coordinator.

> **Do not use real personal or health data.** V0 has no authentication or enforceable role authorization. It is not a medical, diagnostic, triage, emergency, or production record service.

## What is implemented

- Next.js 16.3 / React 19.2 public landing page.
- Role-preview referral case workspace for patient, referrer, hospital, and coordinator perspectives.
- Synthetic referral creation rehearsal with urgent-care and direct-identifier guards.
- Django 5.2 LTS + DRF JSON API.
- PostgreSQL case aggregate and committed migrations.
- Append-only material case timeline.
- Celery/Redis task boundary using opaque UUIDs only.
- Docker Compose development stack with unexposed PostgreSQL/Redis services.
- Accessibility, security, performance, architecture, and agent documentation.

The exact product scope comes from [the refined product specification](docs/REFINED_PRODUCT_BUSINESS_SPECIFICATION.md). Technical decisions are summarized in [the high-level design](docs/HIGH_LEVEL_DESIGN.md) and [low-level design](docs/LOW_LEVEL_DESIGN.md).

Every commit must follow the fixed [repository commit convention](docs/COMMIT_CONVENTION.md): Conventional Commit type and scope, an imperative lowercase summary, and one coherent reviewable outcome.

## Run the complete stack

Requirements: Docker with Compose.

```bash
docker compose up --build
```

If ports 3000 or 8000 are already occupied, choose alternate localhost ports without changing container networking:

```bash
KND_FRONTEND_PORT=3011 KND_BACKEND_PORT=8011 docker compose up --build
```

Then open:

- Product UI: <http://localhost:3000>
- Synthetic workspace: <http://localhost:3000/workspace>
- Referral rehearsal: <http://localhost:3000/refer>
- API health: <http://localhost:8000/api/v1/health/>

The API container applies migrations and idempotently seeds `KND-DEMO-001` before serving. PostgreSQL and Redis bind only inside the Compose network. Host UI/API ports bind to `127.0.0.1`.

Stop services with:

```bash
docker compose down
```

This retains the prototype PostgreSQL volume. If a developer intentionally wants a fresh synthetic database, they can explicitly remove the named volume after confirming it contains no needed work.

## Run frontend locally

Requires Node.js 20.9 or newer.

```bash
cd frontend
npm install
npm run dev
```

The frontend reads the API from `BACKEND_INTERNAL_URL` and falls back to a clearly labelled built-in synthetic case when the API is unavailable. Browser mutations use the same-origin `/api/backend/` rewrite.

Validation:

```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

## Run backend tests locally

The normal runtime uses PostgreSQL. Fast unit tests can explicitly use the SQLite adapter:

```bash
cd backend
python -m venv .venv
.venv/bin/pip install -r requirements.txt
DATABASE_ENGINE=sqlite SQLITE_PATH=:memory: CELERY_TASK_ALWAYS_EAGER=true .venv/bin/python manage.py test
```

Runtime checks against PostgreSQL should also be run through Compose before a pilot rehearsal:

```bash
docker compose run --rm backend python manage.py check --deploy
docker compose run --rm backend python manage.py test
```

## API surface

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/v1/health/` | Database readiness and explicit prototype boundary |
| `GET` | `/api/v1/demo/workspace/` | Stable synthetic case aggregate |
| `GET` | `/api/v1/cases/` | Paginated synthetic case list |
| `POST` | `/api/v1/cases/` | Create a fictional planned-care rehearsal |
| `GET` | `/api/v1/cases/{uuid}/` | Synthetic case detail |

All V0 endpoints are anonymous and throttled. That is compatible only with fictional data in a controlled demonstration.

## Repository guide

```text
backend/        Django/DRF modular monolith and Celery tasks
frontend/       Next.js App Router experience
docs/           Product, architecture, flow, security, and agent context
openspec/       Original product-definition change
worklog/        Append-only implementation history
compose.yaml    PostgreSQL + Redis + API + worker + frontend
```

## Required gates before real use

Do not add a “production” environment variable and call the product ready. [Performance and security](docs/PERFORMANCE_AND_SECURITY.md) defines the full gate, including authentication, server-enforced case/document authorization, consent/grants, credential verification, private quarantined uploads, malware scanning, audited access, incident response, restore tests, role-isolation tests, and corridor-specific legal/clinical review.

AWS RDS and S3 remain future decisions. The application is shaped so managed PostgreSQL and a private object-storage adapter can be evaluated later without making AWS part of local development.
