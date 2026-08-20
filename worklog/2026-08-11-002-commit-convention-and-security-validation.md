# Work log — Commit convention and security validation

**Date:** 11 August 2026
**Entry:** 002
**Status:** In progress

## Additional request received

Create the repository in meaningful feature commits, define a fixed commit convention in a file, and follow it properly. Use a Python virtual environment for backend work.

## Actions and decisions

1. Added `docs/COMMIT_CONVENTION.md` with a mandatory Conventional Commit structure, fixed type/scope lists, one-outcome commit boundaries, subject rules, and staged-diff checks.
2. Linked the convention from the agent context and repository README.
3. Initialized the previously empty `.git` metadata and selected the `main` branch.
4. Created `backend/.venv` with Python 3.10.12 and installed all pinned backend dependencies inside it. The virtual environment is ignored and will not be committed.
5. Ran Django system checks, migration drift detection, and five API/safety tests from the virtual environment.
6. The first test run exposed a sliced reverse-prefetch bug in the case timeline. Corrected it by prefetching the ordered relation and capping the serialized representation at 12 events.
7. The second backend run passed: system check clean, no migration changes, and 5 tests passed.
8. Frontend dependency installation reported three high-severity advisories in Next.js 16.2.11's bundled PostCSS and Sharp versions.
9. Verified npm's current official distribution metadata: `next@latest` is 16.3.0 and it updates the affected dependencies to PostCSS 8.5.23 and Sharp 0.35.x. Updated Next.js and its ESLint configuration to 16.3.0 before committing or building.

## Commit plan

1. Repository commit convention.
2. Product/OpenSpec source of truth.
3. Prototype architecture and security documentation.
4. Synthetic Django/DRF referral workspace API with tests.
5. Accessible light-mode Next.js referral experience.
6. Local PostgreSQL/Redis/Celery container stack and developer handoff.
7. Append-only work-log record.

## Remaining verification

- Regenerate the frontend lockfile at 16.3.0.
- Confirm `npm audit` has no known vulnerabilities.
- Run frontend lint, typecheck, and production build.
- Validate Compose configuration and PostgreSQL-backed application behavior.
- Inspect and commit each staged feature boundary using the documented convention.

This entry is append-only and must not be edited. Continuation belongs in the next numbered file.
