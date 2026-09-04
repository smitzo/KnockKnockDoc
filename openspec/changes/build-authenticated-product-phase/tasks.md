# Delivery checkpoints

## 1. Identity and referral authorization

- [x] 1.1 Add secure session identities, profiles, organizations, memberships, CSRF, throttling, and security events.
- [x] 1.2 Add case assignments, scoped grants, server-derived referrer identity, and deny-by-default queries.
- [x] 1.3 Prove anonymous denial, revoked/expired/suspended denial, and Hospital A/Hospital B isolation in backend tests.
- [x] 1.4 Replace frontend role preview and fallback workspace with authenticated session UX.

## 2. Admin-only synthetic data lab

- [x] 2.1 Model bounded synthetic doctor and patient profiles without real personal or health data.
- [x] 2.2 Seed at least 30 fictional doctors and 30 fictional patients plus useful organizations and account states.
- [x] 2.3 Add deterministic local avatar keys and clear fictional-data labels.
- [x] 2.4 Add platform-admin-only list/summary APIs and a negative permission matrix.
- [x] 2.5 Build the responsive admin data-lab route with search, filters, summaries, and flow inspection.
- [x] 2.6 Move all synthetic catalog/network/referral records into a versioned, validated JSON fixture collection without credentials.
- [x] 2.7 Add an admin-only load/delete toggle, exact deletion confirmation, persistent admin bootstrap, mutation audit, and negative permission tests.
- [ ] 2.8 Persist standard/demo mode, gate every synthetic product selector, keep normal feature shells/blogs available, and add a privacy-bounded admin coverage preview.

## 3. Education and visual onboarding

- [x] 3.1 Research current authoritative India medical-travel statistics and record direct source URLs and review dates.
- [x] 3.2 Publish at least five sourced articles with uncertainty and medical-advice boundaries.
- [x] 3.2a Move articles into a validated, file-backed content collection with reusable listing and reader components.
- [x] 3.3 Generate original local editorial imagery and label illustrative AI-generated scenes.
- [x] 3.4 Build an annotated how-to guide with arrows, route-specific actions, role expectations, and safety boundaries.

## 4. Runtime and documentation

- [x] 4.1 Require local strong demo passwords without committing credentials.
- [ ] 4.2 Update startup, environment examples, developer handoff, architecture, data flow, security, and agent context.
- [ ] 4.3 Append worklog entries for request, decisions, implementation, evidence, limitations, and next gate.

## 5. Validation

- [ ] 5.1 Pass Django checks, migrations, full tests, and PostgreSQL-backed authorization tests in the venv.
- [ ] 5.2 Pass frontend lint, typecheck, production build, dependency audit, and accessibility-focused browser smoke tests.
- [ ] 5.3 Pass Compose health, Redis/Celery, login/CSRF/logout, admin isolation, and cross-hospital runtime smoke tests.
- [ ] 5.4 Inspect every staged diff and create convention-compliant feature commits.

## 6. Business and product scrutiny

- [x] 6.1 Create a permanently git-ignored business workspace with evidence, thesis, use cases, economics, probability, sales, outreach, roadmap, and decision reports.
- [x] 6.2 Separate sourced facts, inferences, assumptions, targets, and stop conditions; reject unsupported top-down TAM claims.
- [x] 6.3 Record an adversarial product/engineering review and reconcile missing authentication requirements.
- [x] 6.3a Add an investor/founder diligence questionnaire covering thesis, economics, GTM, safety, technology, traction, fundraise, and hostile questions.
- [ ] 6.4 Founder decides whether the company sources demand or sells neutral referral workflow.
- [ ] 6.5 Validate the first corridor, specialty, buyer, budget, and baseline through the interview thresholds in the business roadmap.

## 7. Real-data release gates (future, explicit stop-ship)

- [ ] 7.1 Obtain corridor-specific privacy, clinical, telemedicine, and commercial review.
- [ ] 7.2 Specify patient authorization/withdrawal, administrative separation, MFA/recovery, retention/deletion, and clinical issuance/addendum behavior.
- [ ] 7.3 Prove private document security, immutable audit, observability, incident response, backup/restore, RPO/RTO, and independent security testing.
- [ ] 7.4 Approve production infrastructure only after residency, procurement, workload, recovery, integration, and cost requirements are measured.
