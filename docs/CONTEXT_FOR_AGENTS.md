# Context for Agents

## Read first

Before changing product behavior, read in this order:

1. `docs/REFINED_PRODUCT_BUSINESS_SPECIFICATION.md` — active product and V0 scope.
2. `docs/FUNCTIONAL_PRODUCT_SPECIFICATION.md` — detailed safety, consent, permission, record, and workflow constraints.
3. `docs/HIGH_LEVEL_DESIGN.md` and `docs/LOW_LEVEL_DESIGN.md` — technical decisions.
4. `docs/PERFORMANCE_AND_SECURITY.md` — release gates and threat boundaries.
5. `docs/COMMIT_CONVENTION.md` — mandatory commit format and boundaries.
6. Every file in `worklog/` in filename order — append-only execution history.

## Product invariant

The unit of value is the completed referral loop:

`verified referrer → consented structured case → authorized provider review → attributable response → patient decision/care → handback`

Profiles, messages, dashboards, and quotations support that loop. They are not the product by themselves.

## Current implementation scope

- Prototype V0 only.
- Synthetic data only.
- No authentication or real authorization yet.
- No real patient or doctor onboarding.
- No file upload or external object storage.
- One Django/DRF modular monolith, PostgreSQL, Celery/Redis, and Next.js frontend.
- AWS S3/RDS are future architecture choices, not current dependencies.

Do not silently broaden this scope into a production medical system.

## Non-negotiable product boundaries

- Never diagnose, prescribe, prognose, triage, or rank treatment quality.
- Never represent an estimate as a guaranteed price.
- Never represent coordination as emergency support.
- Never use “verified” without the verified claim, evidence/source, date, scope, and current state.
- Never share one hospital's response with another hospital.
- Never let a profile, organization membership, or UUID imply case access.
- Never log patient names, clinical text, record labels, tokens, or object URLs.
- Never add real upload before the security gates in `PERFORMANCE_AND_SECURITY.md` are implemented and tested.
- Never add hidden ranking, referral commissions, sponsored clinical placement, or public doctor ratings.

## Engineering conventions

- Keep domain behavior out of DRF views; call a service command.
- Validate at both transport and domain boundaries.
- Create a case event for every material state change.
- Treat medical/clinical artifacts as immutable and version corrections.
- Prefer database constraints for invariants and explicit transactions for commands.
- Use UUIDs in background task arguments and logs.
- Bound list endpoints, task batches, text lengths, and retries.
- Keep frontend dependencies small; prefer semantic HTML and CSS over a generic component kit.
- Accessibility is acceptance criteria, not a polish pass.
- Add tests for a behavior change and run both frontend build and backend tests before declaring it complete.
- Follow `docs/COMMIT_CONVENTION.md` for every commit; inspect the staged diff before committing.

## Work-log protocol

`worklog/` is append-only.

- Create a new file named `YYYY-MM-DD-NNN-short-description.md` for each material work session or correction.
- Record the request, decisions, implementation, verification evidence, limitations, and next safe step.
- Do not edit or delete an existing entry. If it is wrong, append a correction entry that identifies the earlier filename.
- Do not put credentials, tokens, patient data, private links, or secrets in a work log.

## Definition of done for prototype changes

1. Behavior matches the active specification and explicitly states any deliberate exception.
2. Empty, loading, error, keyboard, small-screen, and reduced-motion behavior are considered.
3. Backend validation and domain invariants are tested.
4. `python manage.py check`, migrations, backend tests, frontend lint, and frontend production build pass, or the work log names the exact blocker.
5. Documentation and a new work-log entry describe material architecture/security changes.
6. No claim of production readiness is made while anonymous access remains.
