## Why

Prototype V0 proves the referral workspace visually but cannot support realistic role rehearsal while its cases are anonymous and its sample set contains one case. The next phase needs authenticated, organization-scoped case access plus a safe operator-only synthetic data lab large enough to inspect directory, case, and account states. It also needs sourced public education and a visual product guide so a new user can understand the workflow without a live facilitator.

## What Changes

- Add Django session authentication, verified identity profiles, organizations, memberships, assignments, scoped case grants, CSRF protection, and append-only security events.
- Replace the presentation-only role switch with the role granted to the signed-in membership.
- Add an admin-only synthetic data lab with at least 30 fictional doctors and 30 fictional patients, local visual assets, useful filters, and case-flow summaries.
- Seed demo accounts only when strong local passwords are supplied through ignored environment configuration; never commit `admin/admin` or another reusable credential.
- Add five evidence-backed educational articles about India medical travel, with source links, dates, uncertainty, and non-medical-advice boundaries.
- Add an illustrated, annotated “how to use the product” guide linked to the real authenticated routes.
- Keep every row fictional, disable file upload, and preserve all remaining real-data release gates.

## Non-goals

- Production approval for real personal or health data.
- Medical advice, treatment ranking, outcome promises, emergency support, or unqualified compliance claims.
- Scraped real doctor/patient profiles or implied endorsements.
- A hard-coded weak administrator password.
- AWS selection, real S3 objects, payments, travel booking, or hospital-system integration.

## Impact

This change adds identity and authorization tables, admin-only synthetic catalog entities, authenticated Next.js routes, public editorial content, local imagery, expanded seeding, and validation. PostgreSQL and Redis remain local runtime dependencies. The modular-monolith boundary remains unchanged.
