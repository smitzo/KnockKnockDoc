# Knock Knock Doc — Doctor Referral Network Prototype

Knock Knock Doc is a light-mode, doctor-first product prototype for discovering trusted professional peers, connecting with them, discussing a potential collaboration, and opening a structured cross-border referral. It combines a public product website, an authenticated professional network, an admin-controlled synthetic demo, and a consent-shaped referral workspace.

> **Synthetic data only.** Do not enter real identities, patient information, clinical records, or medical files. This prototype does not diagnose, prescribe, triage emergencies, verify real credentials, or make treatment-quality claims.

## What works now

- Public website: Home, Doctors, Hospitals, How it works, Blogs, About, Join, and Sign in.
- Five reusable, file-backed, sourced long-form articles with stable detail routes, practical checklists, evidence limits, and direct sources.
- Doctor and hospital application forms with strict fictional `.test` / `.example` inputs and review-gated inactive accounts.
- Platform-admin application review queue with audited start-review, request-changes, approve, and reject transitions.
- Atomic synthetic approval that activates only the eligible doctor or hospital-coordinator boundary, plus a dedicated hospital workspace.
- Django session authentication, CSRF protection, throttling, and append-only security events.
- Doctor-only professional discovery with Vaidam-informed catalogue cards; keyword, specialty, Indian location, experience, language, and sorting controls; expandable profile context; and fictional collaboration ratings.
- Purpose-bound connection requests, accept/decline/withdraw transitions, and participant-only messaging.
- Structured synthetic referral creation with assignment and scoped-grant authorization.
- Platform-admin-only demo controls for loading or deleting 30 fictional doctors, 30 fictional patients, network records, ratings, and a referral workspace.
- Django/DRF modular monolith, PostgreSQL, Celery/Redis, and a Next.js 16 / React 19 frontend using the Tailwind build pipeline, route-level CSS Modules, and a legacy global shell being migrated.

The active product and safety boundary is described in [the refined specification](docs/REFINED_PRODUCT_BUSINESS_SPECIFICATION.md). Architecture details live in [the high-level design](docs/HIGH_LEVEL_DESIGN.md), [low-level design](docs/LOW_LEVEL_DESIGN.md), and [security document](docs/PERFORMANCE_AND_SECURITY.md).

Every commit follows [the repository commit convention](docs/COMMIT_CONVENTION.md): Conventional Commit type and scope, imperative lowercase summary, and one coherent reviewable outcome.

## Start the complete stack

Requirements: Docker with Compose.

```bash
docker compose up --build
```

The default local URLs are:

- Website: <http://localhost:3000>
- Sign in: <http://localhost:3000/login>
- Blogs: <http://localhost:3000/blog>
- Join the network: <http://localhost:3000/join>
- API health: <http://localhost:8000/api/v1/health/>

This checkout uses ignored local environment values for ports `3011` and `8011`, so its active sign-in URL is <http://localhost:3011/login>. Host ports bind to `127.0.0.1`; PostgreSQL and Redis are not exposed to the host.

### Local admin demo

Demo records are never loaded automatically. The intended flow is:

1. Open `/login` and sign in as the platform administrator.
2. Land on `/admin/lab`.
3. Select **Load demo data** to create the complete fictional dataset.
4. Explore the doctor network, messages, referrals, admin-only patient catalog, and partner-application review queue.
5. Submit a doctor or hospital application from **Join**, then review and activate it from the **Applications** tab.
6. Select **Delete demo data** to remove fixture and synthetic review-created records while preserving the administrator.

Outside demo mode, the complete public sitemap, articles, normal sign-in surface, provider gateways, and authenticated empty states remain available. The persisted product mode fails closed to `standard`; fixture profiles, ratings, connections, messages, referrals, and synthetic applications remain hidden and non-mutable until the administrator loads demo data.

This working tree has an ignored local-only opt-in for `admin` / `admin`. The shortcut is accepted only when `PROTOTYPE_MODE=true`, `DJANGO_DEBUG=true`, and `ALLOW_INSECURE_LOCAL_DEMO_ADMIN=true`; startup refuses that flag outside prototype debug mode. Never use it in shared, hosted, staging, or production environments.

For another checkout, copy `.env.example` to `.env`, provide a strong `DEMO_ACCOUNT_PASSWORD`, and normally use a strong `DEMO_ADMIN_PASSWORD`. Do not commit `.env`.

Stop the stack with:

```bash
docker compose down
```

The PostgreSQL volume is retained. Removing it is an explicit destructive operation and is not part of normal demo reset; use the admin fixture delete control instead.

## Run the frontend locally

Requires Node.js 20.9 or newer.

```bash
cd frontend
npm install
npm run dev
```

The browser uses same-origin `/api/backend/` rewrites. Server components use `BACKEND_INTERNAL_URL`. There is no synthetic fallback when the API or session is unavailable; the UI shows an honest sign-in, empty, or error state.

Validation:

```bash
cd frontend
npm run lint
npm run typecheck
npm run build -- --webpack
npm audit --audit-level=high
```

## Run the backend in a venv

PostgreSQL is the runtime database. SQLite is an explicit fast-test adapter only.

```bash
cd backend
python -m venv .venv
.venv/bin/pip install -r requirements.txt
DATABASE_ENGINE=sqlite SQLITE_PATH=:memory: CELERY_TASK_ALWAYS_EAGER=true \
  .venv/bin/python manage.py test \
  apps.demo_lab.tests apps.identity.tests apps.partner_onboarding.tests \
  apps.professional_network.tests apps.referrals.tests
```

Run migration and configuration checks as separate gates:

```bash
cd backend
DATABASE_ENGINE=sqlite SQLITE_PATH=:memory: .venv/bin/python manage.py check
DATABASE_ENGINE=sqlite SQLITE_PATH=:memory: .venv/bin/python manage.py makemigrations --check --dry-run
```

Compose smoke tests are still required because SQLite cannot prove PostgreSQL constraints, transaction behavior, Redis/Celery wiring, or browser-origin CSRF behavior.

## API surface

| Method | Path | Access and purpose |
|---|---|---|
| `GET` | `/api/v1/health/` | Anonymous bounded readiness response |
| `GET` | `/api/v1/product-mode/` | Anonymous bounded standard/demo state |
| `GET` | `/api/v1/auth/csrf/` | Anonymous throttled CSRF token issue |
| `POST` | `/api/v1/auth/login/` | CSRF-protected session login |
| `GET` | `/api/v1/auth/session/` | Active authenticated identity and memberships |
| `POST` | `/api/v1/auth/logout/` | CSRF-protected session flush |
| `POST` | `/api/v1/onboarding/applications/` | Fictional doctor/hospital application submission |
| `GET` | `/api/v1/onboarding/review/applications/` | Platform-admin minimal application queue |
| `GET` | `/api/v1/onboarding/review/applications/{uuid}/` | Platform-admin private application detail |
| `POST` | `/api/v1/onboarding/review/applications/{uuid}/{action}/` | Row-locked admin review transition and optional activation |
| `GET` | `/api/v1/network/doctors/` | Eligible verified professional directory |
| `GET/POST` | `/api/v1/network/connections/` | Participant-visible connections / request creation |
| `POST` | `/api/v1/network/connections/{uuid}/{action}/` | Authorized accept, decline, or withdraw transition |
| `GET` | `/api/v1/network/conversations/` | Accepted-connection conversations for the participant |
| `GET/POST` | `/api/v1/network/conversations/{uuid}/messages/` | Participant-only append/read messages |
| `GET/POST` | `/api/v1/cases/` | Authorized case list / verified-referrer creation |
| `GET` | `/api/v1/cases/{uuid}/` | Scoped synthetic case detail or concealed `404` |
| `GET` | `/api/v1/demo/workspace/` | Authorized seeded referral workspace |
| `GET` | `/api/v1/admin/lab/summary/` | Platform-admin-only fixture summary |
| `POST/DELETE` | `/api/v1/admin/lab/fixtures/` | Platform-admin-only load / confirmed delete |
| `GET` | `/api/v1/admin/lab/doctors/` | Platform-admin-only full synthetic doctor catalog |
| `GET` | `/api/v1/admin/lab/patients/` | Platform-admin-only synthetic patient catalog |

## Repository guide

```text
backend/        Django/DRF modular monolith and Celery worker tasks
frontend/       Next.js App Router website and authenticated product
docs/           Product, architecture, flow, security, and agent context
openspec/       Checkpointed proposals, specifications, designs, and tasks
worklog/        Append-only implementation history
business/       Local founder strategy workspace; permanently git-ignored
compose.yaml    PostgreSQL + Redis + API + worker + frontend
```

## Real-launch stop gates

This is production-shaped software, not a production medical system. Real identities or health data remain blocked until credential verification, MFA/recovery, enforceable consent and document-category authorization, private quarantined uploads, malware scanning, audited object access, moderation/reporting, incident response, backup/restore exercises, retention/deletion, accessibility testing, independent security assessment, and corridor-specific legal/clinical review are complete.

AWS RDS and S3 remain future architecture decisions. Local development does not depend on AWS.
