## Context

The application already has a Django/DRF modular monolith, Next.js App Router frontend, PostgreSQL, Redis/Celery, a synthetic referral aggregate, and an append-only worklog protocol. The default Django user model is already migrated, so replacing it would create avoidable migration and identity risk.

## Decisions

### Extend the migrated Django user

Django continues to own password hashing and server-side sessions. UUID `IdentityProfile`, `Organization`, and `OrganizationMembership` entities hold domain identity. Login usernames are normalized synthetic email addresses. There is no browser bearer-token storage.

### Deny case access by default

Every case query requires active user and profile state, verified email, active organization membership, active assignment interval, current unrevoked/unexpired grant, and the requested normalized scope. An inaccessible UUID returns `404`.

### Separate the operator lab from care workspaces

Synthetic doctor and patient catalog rows are not referral participants and do not imply case access. Only an active platform-admin membership can call the lab API or render its route. Non-admin users receive `403`; anonymous users receive an authentication failure. The lab exposes fictional operational fields only and no passwords.

### Make demo state an explicit data switch

Prototype/debug configuration describes the deployment safety boundary; it must not make fixtures visible. A persisted single product-mode record starts in `standard`. The fixture load transaction flips it to `demo` only after manifest/count verification, and confirmed deletion flips it back to `standard` while removing fixture-owned records. Normal routes remain present in both modes. Product selectors return synthetic rows only in demo mode; standard mode renders honest empty/live-ready states and omits demo-specific copy.

The admin control center may show bounded demo coverage across providers, hospitals, connections, referrals, and messages. It does not inherit participant access: no generic admin message-body reading, case content access, or role impersonation is introduced.

### Use local fictional visual assets

Generated editorial images are stored in the repository and carry descriptive alt text. Directory avatars are deterministic local synthetic visuals, not photos scraped from real people. The UI labels all people and metrics as fictional.

### Keep education attributable

Each article stores a source list with publisher, title, URL, publication/access date, and the claim it supports. Government and primary statistical sources are preferred. Case examples are clearly identified as published institutional examples or composite explanations; no invented person is presented as a real patient.

### Keep secrets out of seed data

The seed command reads `DEMO_ADMIN_PASSWORD` and `DEMO_ACCOUNT_PASSWORD` from local environment configuration, applies a minimum length plus Django validators, and never prints either value. Weak defaults are rejected even in prototype mode.

### Bound frontend style ownership

Tailwind CSS provides the utility/base pipeline. New authenticated, admin, editorial, and guide surfaces use feature-scoped CSS Modules so the global stylesheet does not continue growing. The original V0 global rules are migrated incrementally rather than rewritten during a security-sensitive phase.

### Keep founder strategy local

Business hypotheses, economics, outreach material, and private founder questions live under the git-ignored `/business/` workspace. Product requirements and release gates remain in tracked OpenSpec/docs; an ignored strategy document cannot authorize a production feature or weaken a safety requirement.

## Risks and controls

- Large synthetic fixtures may look real: fixture data is absent in standard mode and every fixture-backed API/card labels demo provenance after explicit activation.
- Admin directory leakage: permission checks are enforced at the API queryset and page gate, with negative tests for patient, doctor, hospital, and anonymous sessions.
- Editorial claims may drift: articles display “last reviewed” dates and direct sources; they avoid superlatives not supported by evidence.
- Generated imagery may imply a real endorsement: captions state that people/scenes are illustrative and AI-generated.
- Session auth introduces CSRF: Django CSRF middleware, same-origin proxying, masked token retrieval, SameSite cookies, and mutation tests are mandatory.
- Mode/data drift may leak partial fixtures: mode changes share the fixture transaction, selectors require `demo`, and expected-count verification precedes activation.

## Rollback

The new tables are additive. Frontend routes can be disabled without deleting data. Seed commands are idempotent. No production data migration or external object-store mutation exists in this phase.
