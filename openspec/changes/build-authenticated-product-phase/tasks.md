# Delivery checkpoints

## 1. Identity and referral authorization

- [x] 1.1 Add secure session identities, profiles, organizations, memberships, CSRF, throttling, and security events.
- [x] 1.2 Add case assignments, scoped grants, server-derived referrer identity, and deny-by-default queries.
- [x] 1.3 Prove anonymous denial, revoked/expired/suspended denial, and Hospital A/Hospital B isolation in backend tests.
- [ ] 1.4 Replace frontend role preview and fallback workspace with authenticated session UX.

## 2. Admin-only synthetic data lab

- [ ] 2.1 Model bounded synthetic doctor and patient profiles without real personal or health data.
- [ ] 2.2 Seed at least 30 fictional doctors and 30 fictional patients plus useful organizations and account states.
- [ ] 2.3 Add deterministic local avatars and clear fictional-data labels.
- [ ] 2.4 Add platform-admin-only list/detail/summary APIs and a negative permission matrix.
- [ ] 2.5 Build the responsive admin data-lab route with search, filters, summaries, and flow inspection.

## 3. Education and visual onboarding

- [ ] 3.1 Research current authoritative India medical-travel statistics and record direct source URLs and review dates.
- [ ] 3.2 Publish at least five sourced articles with uncertainty and medical-advice boundaries.
- [ ] 3.3 Generate original local editorial imagery and label illustrative AI-generated scenes.
- [ ] 3.4 Build an annotated how-to guide with arrows, route-specific actions, role expectations, and safety boundaries.

## 4. Runtime and documentation

- [ ] 4.1 Require local strong demo passwords without committing credentials.
- [ ] 4.2 Update startup, environment examples, developer handoff, architecture, data flow, security, and agent context.
- [ ] 4.3 Append worklog entries for request, decisions, implementation, evidence, limitations, and next gate.

## 5. Validation

- [ ] 5.1 Pass Django checks, migrations, full tests, and PostgreSQL-backed authorization tests in the venv.
- [ ] 5.2 Pass frontend lint, typecheck, production build, dependency audit, and accessibility-focused browser smoke tests.
- [ ] 5.3 Pass Compose health, Redis/Celery, login/CSRF/logout, admin isolation, and cross-hospital runtime smoke tests.
- [ ] 5.4 Inspect every staged diff and create convention-compliant feature commits.
