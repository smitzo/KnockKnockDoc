# Delivery checkpoints

## 1. Research and information architecture

- [x] 1.1 Benchmark Vaidam's public sitemap, doctor/hospital detail fields, About, knowledge, and partner surfaces using official pages.
- [x] 1.2 Reconcile the benchmark with the doctor-first thesis and record rejected marketplace patterns.
- [x] 1.3 Define the public sitemap, audience hierarchy, profile fields, application states, publication states, and safety boundaries.
- [ ] 1.4 Capture desktop/mobile before evidence and test the proposed navigation labels with at least five target doctors.

## 2. Public product shell

- [ ] 2.1 Build one accessible responsive header/footer with Home, Doctors, Hospitals, How it works, Insights, About, Join, and Sign in.
- [ ] 2.2 Rewrite Home around `Discover -> Compare -> Connect -> Refer`, with one doctor-first primary action and direct prototype disclosure.
- [ ] 2.3 Build About and How it works routes with company purpose, operating boundary, role responsibilities, and trust explanation.
- [ ] 2.4 Make all five reusable articles visible from the header, home page, footer, listing, and stable detail routes.
- [ ] 2.5 Add Privacy, Terms, Accessibility, Contact, medical-information, and emergency boundaries before any real launch claim.

## 3. Public provider discovery

- [ ] 3.1 Add public doctor list/detail read models with publication filters, specialty/location search, profile provenance, and no private fields.
- [ ] 3.2 Add public hospital list/detail read models with accreditation/capacity provenance, department/location search, and approved media only.
- [ ] 3.3 Build accessible doctor and hospital list/detail pages with honest empty states and no synthetic-publication shortcut.
- [ ] 3.4 Add sitemap metadata, canonical URLs, structured data only for verified facts, and `noindex` for private/admin/auth routes.

## 4. Secure registration and review

- [ ] 4.1 Add doctor and hospital application models, state machines, immutable acknowledgement evidence, and migrations.
- [ ] 4.2 Add normalized-email registration, password validation, generic responses, throttling, and hashed single-use email verification.
- [ ] 4.3 Add role-specific multi-step forms, accessible validation, resume-safe drafts, and clear review expectations.
- [x] 4.4a Add a bounded platform-admin application review list/detail API and frontend queue.
- [x] 4.4b Add row-locked start-review/change-request/approve/reject services with safe security events.
- [x] 4.4c Atomically project approved synthetic doctors/hospitals into only their eligible identity, organization, membership, and directory boundaries.
- [x] 4.5 Prove duplicate/race handling, applicant isolation, field-level privacy, invalid transition denial, activation rollback, and reviewer-only access.

## 5. Documentation, validation, and commits

- [x] 5.1 Update high/low-level design, agent context, data flow/method calls, performance/security, README, and append-only worklog.
- [ ] 5.2 Run backend checks/migrations/tests, frontend lint/typecheck/build, dependency audits, and keyboard/mobile/browser smoke tests.
- [ ] 5.3 Prove anonymous/public/applicant/admin role isolation and that admin fixtures never enter public provider APIs.
- [x] 5.4 Create narrow convention-compliant product, backend, frontend, docs, and worklog commits.

## 6. Real-launch gates

- [ ] 6.1 Complete credential evidence storage/review, moderation, reverification, correction, appeal, suspension, and takedown operations.
- [ ] 6.2 Obtain privacy, advertising, clinical, anti-kickback, and medical-tourism review for the first corridor.
- [ ] 6.3 Complete accessibility review, account recovery/MFA, monitoring, incident response, and backup/restore proof.
