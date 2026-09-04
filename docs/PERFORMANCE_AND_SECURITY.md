# Performance and Security

## Current posture

Prototype V0 is **not approved for real identities, personal data, or health data**. It implements meaningful security foundations—server-side sessions, CSRF, account/membership state, participant authorization, case assignments/scoped grants, throttling, bounded JSON, fixture isolation, and append-only security evidence—but it lacks the controls and operations required for real healthcare use.

The allowed operating boundary is:

- fictional `.test` / `.example` identities and synthetic scenarios only;
- loopback or tightly controlled internal demonstration only;
- no medical file upload or external object storage;
- no real email/SMS delivery, credential documents, payments, or clinical integrations;
- no analytics or logs containing entered free text;
- no clinical advice, emergency service, treatment-quality ranking, or outcome promise.

## Trust boundaries

| Boundary | Current control | Remaining gate |
|---|---|---|
| Anonymous → account | Login throttle, generic failure, password hashing, CSRF session establishment | MFA, breached-password service, recovery, email/channel verification, bot/abuse controls |
| Applicant → professional | Account remains inactive after submission | Reviewer workflow, credential evidence, dual control, appeal, reverification, suspension |
| Professional → directory | Active eligible identity and bounded professional card | Real verification/publication methodology, moderation, blocking/reporting |
| Professional → connection | Server-derived actor, canonical unique pair, purpose, actor-specific state transitions | Block lists, reporting, abuse investigation, retention policy |
| Participant → conversation | Accepted connection and exact participant query; append-only bounded messages | Moderation/DLP, notification privacy, deletion/export policy, delivery semantics |
| Member → referral case | Active profile + organization + exact membership + assignment + current scoped grant | Enforceable consent, record-category/document scopes, audited downloads/denies |
| Admin → fixture | Platform-admin permission, CSRF, mutation throttle, namespace lock, exact delete phrase, security event | MFA/step-up, privileged-access monitoring, dual control for high-risk production operations |
| App → database/queue | Private Compose network, parameterized ORM, UUID task arguments | TLS, managed secrets, least privilege, rotation, monitored backups/restores |
| App → future files | No upload surface exists | Private quarantine, scan/CDR, immutable originals, safe previews, signed access, retention/audit |

## Threat model and controls

| Threat | Implemented V0 control | Production requirement |
|---|---|---|
| Unauthorized case access | Deny-by-default assignment/grant/scope selectors; concealed `404`; cross-hospital tests | Complete consent/document permission matrix, audited deny, MFA, independent assessment |
| Patient fixture disclosure | Admin-only patient API; professional/public serializers use separate models; negative tests | Formal data classification, monitoring, privacy testing |
| Conversation leakage | Participant-shaped querysets; accepted connection required; server-derived sender | Continuous authorization, moderation, export/deletion rules, security testing |
| ID enumeration | UUIDs plus authorization-shaped queries | Rate/anomaly detection; UUID remains non-secret |
| CSRF/session fixation | Masked CSRF token, same-origin rewrite, origin allowlist, session rotation, HTTP-only cookies, logout flush | TLS/proxy validation, trusted-origin review, step-up auth, session inventory/revocation |
| Credential stuffing | Dedicated login throttle; generic failure | Distributed rate limiting, MFA/passkeys, breached-password checks, alerting |
| Mass application spam | Registration throttle, strict fictional domains, bounded JSON | Bot defense, verified invitations, abuse scoring, WAF |
| Stored/reflected injection | Django ORM, DRF validation, React escaping, JSON-only parser, restrictive headers | CSP nonces/hashes, stored-content review, security automation and penetration testing |
| Malicious files | Upload absent; request file count zero | Quarantine, type detection, malware/CDR, preview isolation, private storage |
| Sensitive logging | No request-body logging; allowlisted event metadata; UUID task args | Central redaction, access controls, retention, alerting, audit separation |
| Queue exposure | UUID arguments only; finite retries | Private TLS/auth queue, short retention, key rotation, least privilege |
| Fixture lifecycle race | Transaction + platform namespace row lock + expected-count verification | Operational locking/observability appropriate to production admin jobs |
| Database loss | Local retained volume | Encrypted backups, PITR, restore exercises, RPO/RTO, disaster recovery |
| Supply-chain compromise | Pinned framework versions, lockfile, minimal dependency set, audit gate | Automated SCA/container/IaC scan, signed builds, SBOM, patch SLA |

## Implemented application controls

- Django debug is off by default outside Compose; non-prototype startup requires a unique secret of at least 50 characters.
- Allowed hosts are explicit; non-debug production-shaped mode enables HTTPS redirect, HSTS, secure cookies, referrer policy, MIME-sniffing protection, and frame denial.
- API parsing/rendering is JSON only; request memory, form count, file count, field length, page size, search length, and task batch are bounded.
- Session cookies are HTTP-only and SameSite; the browser stores no bearer token. Unsafe requests require CSRF.
- Prototype debug mode derives CSRF trusted origins only for `localhost` and `127.0.0.1` on the configured frontend port. Explicit deployment origins replace that default.
- Login rotates/creates the session; logout flushes it; active identity state is rechecked by permission classes/selectors.
- Django password validators and hashers apply. Login errors do not reveal account existence.
- The local `admin` / `admin` escape hatch is disabled by default and accepted only with prototype mode + debug + explicit opt-in. Startup refuses that opt-in outside the boundary.
- Partner applications create inactive accounts and cannot self-assign organization membership or professional privileges.
- Professional directory output is a dedicated bounded serializer/model, separate from admin fixtures and private application fields.
- Connection pair uniqueness and database constraints prevent self/duplicate relationships; transitions use server-derived actor rules.
- Conversations and messages are visible only to accepted participants; messages are append-only and attachments are absent.
- Referral selectors require exact active membership, assignment, grant, expiry/revocation state, and normalized scope.
- Admin fixture endpoints require platform-admin membership, CSRF, throttling, and audited mutations; data is not seeded automatically.
- Security events are append-only and metadata is allowlisted. Message/case free text is not recorded in security events.
- Celery receives opaque UUIDs only and uses finite retries. No external AI, email/SMS, payment, S3, or analytics integration exists.

## Local weak-admin exception

`admin` / `admin` exists solely to remove friction in this loopback demo. The backend accepts it only when:

1. `PROTOTYPE_MODE=true`;
2. `DJANGO_DEBUG=true`; and
3. `ALLOW_INSECURE_LOCAL_DEMO_ADMIN=true`.

Compose binds the browser/API ports to `127.0.0.1`. The weak-admin flag is false in `.env.example`. It is a stop-ship configuration for any tunnel, shared network, CI artifact, hosted demo, staging, or production deployment. Real environments require unique managed credentials, MFA, secret rotation, and administrator step-up authentication.

## Security gates before any real person or patient

All gates are mandatory; a policy document or cloud service selection does not replace implementation evidence.

1. Phishing-resistant staff authentication, verified patient channel, MFA/passkey policy, secure recovery, session inventory and global revocation.
2. Professional/facility credential evidence with issuer/source, scope, dates, reviewer, expiry, reverification, suspension, correction, appeal, and audit.
3. Versioned reviewed notices and consent; purpose, recipient, duration, withdrawal, re-consent, and record-category/document authorization enforced server-side.
4. Complete positive and negative permission matrix for every route, mutation, role, organization, participant, consent state, and document category.
5. Private upload quarantine, content-type detection, malware/CDR scanning, immutable originals, isolated previews, encrypted objects, short-lived signed access, and download audit.
6. Message/profile moderation, blocking/reporting, abuse operations, fraud/conflict controls for ratings, right of reply/appeal, and published methodology.
7. Central secrets/key management, private networking, TLS everywhere, least-privilege database/object/queue identities, rotation playbooks, and no developer production access by default.
8. Immutable access/security audit, monitored privileged operations, evidence export, security alerting, and rehearsed incident response.
9. Encrypted backups, PITR, restore rehearsal, tested RPO/RTO, business continuity, retention schedule, restriction/deletion/export workflows, and disaster recovery.
10. SAST, dependency/container/IaC scanning, SBOM/signing, abuse testing, privacy threat model, accessibility assessment, penetration test, code review, and remediation SLA.
11. Corridor-specific privacy, cross-border transfer, professional practice, telemedicine, clinical, consumer, advertising, anti-kickback/referral-fee, medical-tourism, and commercial review.
12. Named security and clinical escalation owners with separate emergency boundaries and 24/7 incident paths where promised.

Do not use “HIPAA compliant,” “DPDP compliant,” “GDPR compliant,” “verified provider,” “secure medical record,” or equivalent language without scoped evidence and qualified review.

## Performance objectives for a measured pilot

These are targets to test in a deployed environment, not current measurements.

| Path | p95 target | Design constraint |
|---|---:|---|
| Health | 100 ms server time | Bounded response; no infrastructure details |
| Professional directory | 350 ms | Paginated/filterable; aggregate ratings without N+1 |
| Connections/conversations | 300 ms | Participant-shaped indexed query |
| Append message | 350 ms | One bounded transaction; no synchronous notification |
| Case list | 300 ms | Default page at most 20 |
| Case workspace | 500 ms | Bounded aggregate prefetch; no file payload |
| Create synthetic case | 500 ms | Durable transaction excludes background processing |
| Load fixture | 10 s admin operation | Versioned bounded fixture; transactional count verification |
| Largest Contentful Paint | under 2.5 s | Representative mobile network/device |
| Interaction to Next Paint | under 200 ms | Avoid large client bundles and layout work |

## Performance design

- Render stable public content and initial protected reads on the server; keep client islands narrow.
- Use the Tailwind build pipeline and route-level CSS Modules; no charting library, runtime CSS-in-JS, or third-party font request.
- Paginate lists and bound directory search, message bodies, article payloads, fixture counts, and background batches.
- Use indexed discoverability/specialty/location, connection participant/state, conversation timestamp, and case due/status fields.
- Use `select_related()` / `prefetch_related()` and add query-budget tests before pilot traffic.
- Commit the database transaction before Celery; do not place files or free text in the queue.
- Keep future file bytes out of API memory by uploading directly to private quarantine with short-lived intent.
- Measure Web Vitals, API percentiles, database time, and queue delay in the actual target topology; do not extrapolate laptop timings.

## Safe observability

Allowed dimensions: request ID, route template, HTTP method/status, duration, deployment version, bounded error class, task name, opaque case/connection/conversation UUID, queue delay, fixture version/state, and structured workflow stage duration.

Prohibited dimensions: names, emails, phone/address, IP retained beyond approved security need, passwords, tokens/cookies, message bodies, clinical questions, record labels, application summaries, request/response bodies, signed URLs, and unbounded free text.

Initial service-level indicators:

- frontend availability and Web Vitals without identity/health dimensions;
- API availability, latency, and 4xx/5xx rate by route template;
- login/registration throttle events and unusual authorization denials without payload capture;
- database pool/query latency and constraint/lock errors;
- queue depth, age, success/failure/retry rate;
- fixture load/delete outcome and duration;
- referral stage duration derived from structured events.

## Capacity and scaling path

Keep one deployable modular monolith through the first validated corridor. Scale stateless Next.js/API replicas horizontally, tune PostgreSQL pooling, and scale Celery queues by measured workload. Extract a service only when independent scaling, security isolation, failure containment, or team ownership is evidenced and cannot be handled cleanly inside the monolith.
