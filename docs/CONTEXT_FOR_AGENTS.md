# Context for Agents

## Read before changing behavior

1. `docs/REFINED_PRODUCT_BUSINESS_SPECIFICATION.md` — active product and commercial boundary.
2. `docs/FUNCTIONAL_PRODUCT_SPECIFICATION.md` — workflow, permission, safety, and consent rules.
3. The relevant active change under `openspec/changes/` — proposal, specs, design, adversarial review, then tasks.
4. `docs/HIGH_LEVEL_DESIGN.md` and `docs/LOW_LEVEL_DESIGN.md` — architectural and code-level decisions.
5. `docs/DATA_FLOW_AND_METHOD_CALLS.md` — concrete request paths.
6. `docs/PERFORMANCE_AND_SECURITY.md` — threat boundary and real-launch stop gates.
7. `docs/COMMIT_CONVENTION.md` — mandatory commit format and scope.
8. Every file in `worklog/` in filename order — append-only execution history.

## Product invariant

The primary user is a doctor. The unit of value is not a profile, lead, chat message, quote, or trip booking; it is a completed accountable referral loop:

`trusted doctor discovery → purpose-bound connection → consented structured case → authorized specialist response → patient decision/care → home-doctor handback`

Professional messaging builds the relationship. Patient-specific discussion belongs in a referral case because the case can carry purpose, assignment, grant, scope, consent, and audit semantics.

## Current implementation snapshot

- Public product routes: `/`, `/doctors`, `/hospitals`, `/how-to`, `/blog`, `/blog/[slug]`, `/about`, `/join`, `/register/doctor`, `/register/hospital`, `/login`.
- Authenticated routes: `/network`, `/refer`, `/workspace`.
- Platform admin route: `/admin/lab`.
- Session authentication, CSRF, active identity/membership checks, case assignments/scoped grants, and append-only security events are implemented.
- Professional directory, synthetic collaboration ratings, connection transitions, accepted-connection conversations, and append-only messages are implemented.
- Partner application submission is implemented, but review activation, email verification, publication, and credential evidence are not.
- A versioned JSON fixture contains at least 30 fictional doctors and 30 fictional patients; only a platform admin can load, fully inspect, or delete it.
- Eligible synthetic professionals can see bounded professional cards; patient fixtures and operational login fields remain admin-only.
- Five validated JSON articles with sources and local editorial images are reusable across the public site.
- Django/DRF modular monolith, PostgreSQL, Celery/Redis, Next.js, Tailwind pipeline, and CSS Modules are in place.
- No file upload, real email/SMS, public synthetic provider publication, WebSocket service, or AWS dependency exists.

This is a production-shaped synthetic prototype, not a production medical system.

## Non-negotiable boundaries

- Never accept or invent real personal/health data in fixtures, tests, screenshots, logs, URLs, or worklogs.
- Never diagnose, prescribe, prognose, triage, or present coordination as emergency support.
- Never call professional collaboration ratings treatment quality, clinical competence, success rate, or patient outcome.
- Never call an identity/profile/provider “verified” without claim, evidence/source, date, scope, state, and reviewer semantics.
- Never let email control, application approval, a role, membership, participant row, profile, organization, or UUID imply case access.
- Never let a generic professional conversation inherit patient-case access. Move patient-specific work into a case.
- Never expose admin fixture patients, login emails, capacity rehearsals, or operational fields through public or professional APIs.
- Never expose one hospital's response to another hospital.
- Never log names, emails, message bodies, clinical text, record labels, credentials, tokens, signed URLs, or request/response bodies.
- Never implement direct public file upload. The storage gates in `PERFORMANCE_AND_SECURITY.md` are mandatory.
- Never add hidden ranking, sponsored clinical placement, outcome claims, or unreviewed referral commissions.

## Local demo rule

Normal demo credentials must pass the configured strong-password policy. This checkout also supports a deliberately weak local `admin` / `admin` shortcut only when all three conditions are explicit: prototype mode, Django debug mode, and `ALLOW_INSECURE_LOCAL_DEMO_ADMIN=true`. The stack binds host ports to loopback, and startup refuses the weak-admin flag outside that boundary.

Do not copy that exception into CI, a shared environment, staging, a tunnel, a cloud host, or production. Never commit `.env` or any other credential.

The application bootstraps the administrator only. Demo records are loaded explicitly from `/admin/lab`; they must never be auto-seeded at startup.

## Engineering conventions

- Keep domain transitions out of views; DRF calls a service command.
- Keep authorization-shaped reads in selectors and start them from the session user.
- Derive requester, sender, referrer, reviewer, and administrator identity on the server.
- Validate at transport and domain boundaries; enforce stable invariants with database constraints.
- Use explicit transactions and row locks for state transitions and fixture lifecycle operations.
- Create a security/case event for every material action without including free text.
- Keep clinical artifacts, security events, and professional messages append-only; corrections become new facts.
- Use UUIDs in API paths, queue arguments, and safe operational logs.
- Bound list endpoints, search strings, fields, message bodies, request size, task batches, and retry counts.
- Keep client components narrow and never store bearer tokens or sensitive state in browser persistence.
- Use task-first, doctor-first copy. Architecture/security jargon belongs in docs or contextual denial explanations, not first-run marketing UI.
- Use Tailwind/CSS Modules for new UI; do not add new route-specific selectors to the legacy global stylesheet.
- Treat accessibility, empty/loading/error states, mobile reflow, and reduced motion as acceptance criteria.
- Add negative permission tests whenever a new positive access path is added.
- Run frontend build plus backend tests before completion and record exact evidence.

## OpenSpec checkpointing

- Add material requirements to the relevant proposal/spec/design before or with implementation.
- Check off a task only when behavior and proportional verification exist.
- Split partially delivered tasks instead of marking them complete by implication.
- Keep real-launch gates unchecked until evidence exists; documentation is not implementation proof.
- If a decision is challenged by user evidence, update the adversarial review/design and append a worklog correction.

## Worklog protocol

`worklog/` is append-only.

- Add `YYYY-MM-DD-NNN-short-description.md` for each material phase or correction.
- Record request, challenged decisions, implementation, commit IDs, verification evidence, known limits, and next gate.
- Never edit or delete an existing worklog. Correct it in a later entry naming the stale file.
- Never write credentials beyond the explicitly public local alias, secrets, tokens, private links, or any real identity/health data.

## Definition of done

1. Behavior matches the active spec; deliberate exceptions are explicit and narrowly bounded.
2. Authorization includes negative tests for outsider, wrong role, wrong participant, revoked/suspended, and anonymous access where relevant.
3. Empty, loading, error, keyboard, mobile, zoom, and reduced-motion behavior are considered.
4. Django check, migration drift check, explicit backend app tests, frontend lint, typecheck, production build, dependency audit, and Compose/runtime smokes pass—or the exact blocker is recorded.
5. Architecture/security docs, OpenSpec tasks, and a new append-only worklog are current.
6. The staged diff is inspected and committed as one convention-compliant outcome.
7. No production, compliance, verification, clinical-quality, or real-data-readiness claim exceeds the evidence.
