# Adversarial product and engineering review

Review date: 2026-08-11. Lens: senior product management, healthcare operations, software management, staff architecture, security, and founder economics.

## Executive verdict

The phase is appropriate as a **synthetic workflow prototype** and inappropriate as a production health-data system. Authentication and scoped case access materially improve the demo, but they do not close the patient-consent, organization lifecycle, privacy, clinical-governance, reliability, and operational-security gaps needed for real data.

The largest risk is strategic, not technical: the repository currently contains two plausible companies.

1. A network that recruits/refers demand and sells hospitals a corridor pilot with qualified referrals.
2. A neutral B2B workflow product that improves continuity for demand a hospital/referrer already has.

The earlier refined spec leans toward (1); the new business review recommends (2) because discovery/concierge is crowded, government-backed alternatives exist, and treatment-linked incentives can damage trust. This must be an explicit founder decision before GTM or data architecture hardens around it.

## What is strong

- The closed-loop referral, named actors, attributable response, patient choice, and handback are more defensible than a directory.
- Synthetic-only data and disabled uploads correctly limit current harm.
- Deny-by-default authorization has real domain entities instead of a cosmetic role switch.
- The admin catalog is separated from case grants.
- Editorial sources, dates, and uncertainty avoid unsupported city/provider ranking.
- AWS is deferred until workload, residency, recovery, procurement, and cost requirements exist.

## P0 contradictions and missing decisions

### 1. Demand engine versus neutral workflow

The commercial spec says qualified incremental referrals are the first hospital value. The product phase implements no ethical, measurable acquisition/referrer-density engine. If the company promises demand, the current product is not the product being sold. If it sells workflow, ROI must come from time, conversion discipline, safety, and handback—not lead volume.

**Recommended default:** neutral workflow vendor, fixed subscription/pilot, no paid ranking or treatment-value commission. Validate demand sourcing as a separate business experiment.

### 2. “Admin” is under-specified

A platform superuser, hospital organization admin, privacy auditor, catalog operator, and support agent are materially different. One `admin` role will accumulate dangerous authority.

**Required next:** define administrative personas, separation of duties, step-up/MFA, support-access approval, and auditable impersonation policy before real data.

### 3. Grant is not patient consent

A technical access grant cannot substitute for informed, purpose-specific, withdrawable patient authorization. Proxy/minor/incapacity cases, scope categories, expiry, withdrawal consequences, and handback authorization are absent.

**Required next:** model consent/authorization separately with versioned notice, actor authority, purpose, recipients, categories, expiry, withdrawal, and downstream obligations. Clinical/privacy counsel must approve semantics.

### 4. Session security is necessary but incomplete

There is no invitation lifecycle, email ownership proof, MFA, recovery, lockout strategy, device/session management, admin step-up, breached-password screening, or organization offboarding.

**Required next:** production identity spec and threat model; consider managed identity only after procurement/residency requirements.

### 5. Audit is append-only only by application convention

Application-level prevention does not stop database administrators, compromised credentials, or direct SQL. Logs also need privacy minimization, integrity, retention, export, alerting, time synchronization, and incident correlation.

**Required next:** immutable/tamper-evident security logging architecture and access-review process.

## Production stop-ship gaps

The following remain explicit blockers for any real personal/health data:

- corridor-specific legal/privacy/clinical review and controller/processor roles;
- patient authorization and withdrawal lifecycle;
- verified provider/facility onboarding and re-verification;
- MFA, invitation, recovery, session/device controls, and admin separation;
- data classification, minimization, retention, erasure, export, legal hold, and residency decisions;
- private object storage, malware scanning, content validation, quarantine, category authorization, encryption/key rotation, and safe preview;
- threat model, secure SDLC, dependency/container scanning, secrets management, rate/abuse controls, independent penetration test;
- backup/restore proof, RPO/RTO, high availability, capacity model, observability/SLOs, incident response and breach communications;
- idempotency, concurrency/version control, durable job semantics, dead-letter/replay, and external integration contracts;
- accessibility audit, low-bandwidth behavior, localization, timezone/currency semantics, and assisted-use design;
- clinical content governance, authorship/issuance immutability, correction/addendum rules, and emergency escalation boundaries;
- signed customer agreements, support model, DPA/subprocessors, insurance, and production change approval.

## Functional challenges

- One synthetic case cannot prove multi-case navigation, queue aging, duplicate/referral matching, reassignment, cancellation, or closure.
- Patients do not yet exercise a real share/revoke/decline flow.
- The “response” is display data; issuance, addendum, retraction, and clinical sign-off are not modeled.
- Missing-record requests lack owner, due date, reminders, resolution evidence, and category-level access.
- Organization admins cannot invite/offboard people or run periodic access reviews.
- There is no explicit corridor, facility capacity, language, timezone, or interpreter workflow.
- No operational baseline instrumentation proves economic value.
- Public education can drift without an editorial owner and expiry/review enforcement.

## Technical challenges

- Default Django user is pragmatic now but email/login semantics and future federation need an architecture decision before production migration cost rises.
- Query-level permissions need systematic service boundaries; view-by-view checks will eventually drift.
- A modular monolith is correct, but app ownership and dependency rules need automated enforcement.
- Celery/Redis exist architecturally but no durable business job contract, idempotency key, retry taxonomy, or dead-letter operation is specified.
- PostgreSQL runtime authorization and transaction/concurrency behavior must be tested; SQLite proof is insufficient.
- Frontend server/client error taxonomy and observability are thin; an API outage must not look like “access denied.”
- Generated assets need performance budgets and image optimization evidence.
- Tailwind/CSS Modules should stop stylesheet growth; the legacy global surface needs a bounded migration, not a rewrite project.

## Required founder answers

1. Is the company paid to source demand or to operate referrals already sourced?
2. Which exact corridor and specialty is first, and what evidence—not convenience—selects it?
3. Who is the buyer, budget owner, workflow champion, clinical governor, and security approver?
4. Will the company prohibit referral commissions and paid clinical ranking?
5. What is the 6-month cash/time stop-loss and which result triggers shutdown or pivot?
6. Who owns patient authorization and follow-up when the patient returns home?
7. What one baseline operational metric will the first paid pilot improve?

Recommended defaults are documented in the ignored `business/08-founder-decision-register.md`. Implementation may continue with synthetic data, but these answers gate commercial positioning and real-data work.
