# Work log — Prototype V0 validation

**Date:** 11 August 2026
**Entry:** 003
**Status:** Complete for synthetic Prototype V0

## Delivered

- Fixed repository commit convention with meaningful feature boundaries.
- Product and safety design documents for the modular monolith.
- Django 5.2 / DRF synthetic referral API with UUID aggregate, participants, record metadata, information requests, provider responses, and append-only timeline.
- JSON-only anonymous boundary, throttles, request limits, synthetic/planned-care database constraints, direct-identifier guard, urgent-care redirect language, and safe error response.
- PostgreSQL runtime, Celery 5.6 worker, and Redis transport.
- Stable synthetic seed case `KND-DEMO-001`.
- Next.js 16.3 / React 19.2 public landing page, referral rehearsal, and role-aware case workspace.
- Responsive light-mode visual design, semantic structure, focus states, touch sizes, reduced-motion support, and plain clinical/coordination boundaries.
- Docker Compose development stack with private PostgreSQL/Redis networking and overrideable localhost UI/API ports.
- Developer handoff and explicit S3/RDS future-decision boundary.

## Defects found and corrected during verification

1. Corrected an invalid sliced Django reverse prefetch by capping event serialization after the ordered relation is prefetched.
2. Corrected the frontend API error decoder to narrow `unknown` before traversal under strict TypeScript.
3. Updated Next.js 16.2.11 to 16.3.0 after npm identified high-severity PostCSS/Sharp advisories; the new lockfile audits clean.
4. Made host ports configurable after port 8000 was already occupied by an unrelated local service.
5. Added an explicit slash-preserving Next.js rewrite for the DRF case-creation route after an integrated POST rehearsal exposed path normalization at the proxy boundary.

## Verification evidence

### Backend virtual environment

- Python: 3.10.12 in `backend/.venv`.
- `manage.py check`: no issues.
- `makemigrations --check --dry-run`: no changes detected.
- SQLite adapter test run: 5 tests passed.

### Frontend

- `npm run lint`: passed with no warnings.
- `npm run typecheck`: passed.
- `npm run build`: passed on Next.js 16.3.0; `/`, `/refer`, and dynamic `/workspace` produced successfully.
- `npm audit --audit-level=high`: zero vulnerabilities.
- Desktop landing page, desktop workspace, and 390px mobile landing page were rendered in headless Chrome and visually inspected.

### Containers and PostgreSQL integration

- Backend, worker, and frontend images built successfully.
- PostgreSQL, Redis, backend, and frontend health checks became healthy; Celery worker became ready.
- Live `GET /api/v1/health/`: ready with PostgreSQL ready and `synthetic-only` policy.
- Live `GET /api/v1/demo/workspace/`: returned the complete seeded aggregate.
- Live product landing and API-backed workspace rendered through Next.js.
- Live `POST /api/backend/cases/`: HTTP 201, persisted a synthetic PostgreSQL case with two participants and initial event.
- Celery received and completed the case UUID task; its application log contained the opaque UUID and no clinical or patient text beyond the explicitly synthetic case identifier.
- PostgreSQL-backed Django test run: 5 tests passed.
- All temporary containers were stopped after validation. The local named PostgreSQL volume was preserved.

## Honest remaining boundaries

This is a working synthetic prototype, not a real-patient release. Authentication, organization membership, server-enforced case/document authorization, real consent enforcement, credential verification, secure file quarantine/scanning, private object storage, access audit, incident response, retention, restore exercises, and corridor-specific professional/legal review remain mandatory gates. AWS S3 and RDS remain undecided.

This file is append-only and must not be edited. Any later work belongs in a new numbered entry.
