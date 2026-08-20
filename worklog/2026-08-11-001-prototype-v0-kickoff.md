# Work log — Prototype V0 kickoff

**Date:** 11 August 2026
**Entry:** 001
**Status:** In progress

## Request received

Build a Prototype V0 of Knock Knock Doc with:

- an elegant, light-mode, highly usable healthcare experience designed for patients and doctors;
- a Next.js frontend;
- a Django REST Framework backend;
- PostgreSQL, Celery, and Redis;
- a modular-monolith architecture;
- no authentication in V0;
- AWS S3 and RDS left as explicit future decisions;
- secure engineering defaults and clear security boundaries;
- an append-only Markdown work log;
- high-level design, low-level design, agent context, method/data flow, and performance/security documentation.

## Product interpretation

The existing product specifications make the completed cross-border referral loop the V0 unit of value. The prototype therefore concentrates on a synthetic referral case workspace and its supporting patient, referring-doctor, hospital, and coordinator views. It is not a provider-ranking marketplace, social network, diagnostic tool, emergency service, or production medical-record system.

## Decisions made

1. Use a monorepo with `frontend/`, `backend/`, `docs/`, `infra/`, and `worklog/` boundaries.
2. Keep the backend a modular monolith: one deployable Django application with explicit domain modules and service-layer commands.
3. Use UUID primary keys and append-only case events so future authorization/audit features do not require redesigning identifiers or history.
4. Run the normal development stack through Docker Compose with PostgreSQL and Redis; allow SQLite only as an explicit unit-test adapter.
5. Treat authentication-free V0 as synthetic-data-only. The prototype must not accept or claim to protect real patient data.
6. Do not implement file upload in this release. The UI models document metadata only; real uploads require authentication, case-scoped authorization, consent enforcement, malware scanning, safe preview, and private object storage.
7. Keep AWS undecided behind documented boundaries. PostgreSQL and a storage abstraction allow later RDS/S3 adoption without making AWS part of local development.
8. Use Next.js 16.2 Active LTS and React 19.2 with patched versions, based on current official release/security guidance reviewed at implementation time.

## Planned first vertical slice

- Public product landing page with clinical and operational boundaries.
- Synthetic case workspace answering: what is being asked, who can see it, what is missing, what response exists, and who acts next.
- Role-preview control for patient, referrer, hospital, and platform-coordinator perspectives; explicitly labelled as a UI preview, not access control.
- DRF health, case-list, case-detail, demo-workspace, and safe synthetic case-creation endpoints.
- PostgreSQL schema, seed command, Celery task boundary, Redis broker, Docker Compose stack, and backend tests.

## Verification to record in a later entry

- Backend system checks, migrations, and tests.
- Frontend type/lint/build validation.
- Docker Compose configuration validation and, where practical, service health.
- Static security and configuration checks.

This file is immutable after creation. Corrections or continuation belong in a new numbered Markdown entry.
