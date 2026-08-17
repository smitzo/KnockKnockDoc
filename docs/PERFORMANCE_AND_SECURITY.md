# Performance and Security

## Security posture

Prototype V0 is **not approved for real personal or health data**. Authentication has been deliberately deferred, so every API resource is effectively public to a caller who can reach the service. UUIDs, a hidden URL, CORS, or a role-preview switch do not change that fact.

The safe V0 posture is therefore:

- synthetic scenarios only;
- local or tightly controlled internal demonstration only;
- JSON metadata only, no medical-file upload;
- no email/SMS invitation delivery;
- no production analytics containing entered text;
- prominent UI and API disclosure of prototype mode.

## Threat model summary

| Threat | V0 control | Required production control |
|---|---|---|
| Unauthorized case access | Synthetic-only data; no real deployment | Strong authentication, role + assignment + consent policy, object-level tests, audited denies |
| ID enumeration | UUID identifiers | Authorization still mandatory; anomaly detection and rate limits |
| Mass anonymous creation | DRF anonymous throttles, body/field limits, local exposure | Auth, abuse scoring, verified invitations, WAF/rate limits |
| Malicious files | Upload not implemented; JSON parser only | Quarantine, type inspection, malware/CDR scan, safe preview, private bucket |
| Injection/XSS | ORM parameters, DRF validation, React escaping, restrictive headers | CSP nonces, dependency scanning, security tests, stored-content review |
| CSRF | No cookie authentication or stateful browser session in V0 | SameSite/secure cookies and CSRF tokens when session auth is introduced |
| Sensitive logging | Safe operational IDs only; no request body logging | Central redaction, access control, retention, alerting, audit separation |
| Queue data exposure | UUID task arguments only | TLS/auth/private Redis, short retention, key rotation, least privilege |
| Database loss | Container volume for prototype | Encrypted managed backups, PITR, restore exercises, region/retention decision |
| Supply-chain vulnerability | Patched pinned framework versions and minimal dependencies | Automated advisory scanning, lock review, signed builds/SBOM, patch SLA |
| Broken consent/revocation | Not represented as enforceable security in V0 | Versioned consent and grant engine, immediate session/access revocation, recipient workflow |

## Implemented application controls

- Django `DEBUG` off by default.
- Required non-placeholder secret when not in prototype debug mode.
- Explicit allowed-host parsing.
- HTTPS redirect, HSTS, secure cookies, referrer policy, MIME sniffing protection, and clickjacking protection in non-debug mode.
- DRF JSON-only parsing and JSON-only rendering.
- Bounded anonymous/user throttles and page size.
- Bounded Django request body size and form/file counts.
- UUID primary keys.
- Database constraints for synthetic-only V0 and planned-care confirmation.
- No raw file, S3, email, SMS, analytics, or external AI integration.
- Background jobs take UUIDs only and use finite retries.

## Security gates before any real patient

All gates are mandatory; none is replaced by a policy document.

1. Phishing-resistant staff authentication, patient channel verification, recovery, session rotation/revocation, and MFA policy.
2. Organization membership, role, case assignment, consent, purpose, category, and document-level authorization enforced server-side.
3. Negative permission matrix tests covering every role and Hospital A/Hospital B isolation.
4. Reviewed, versioned notices and consent; grant/withdrawal semantics; participant access view; export/restriction/deletion request workflow.
5. Credential and facility verification evidence model with expiry/suspension.
6. Private upload quarantine, malware scanning, safe preview, immutable originals, derived versions, encrypted object storage, short-lived signed access, and download audit.
7. Central secrets and key management, private networking, TLS everywhere, database/object encryption, rotation playbooks, no developer production access by default.
8. Append-only access/security audit with monitored privileged access and tested incident-response export.
9. Backups, point-in-time recovery, restore rehearsal, retention schedule, secure deletion/restriction, business continuity, and disaster recovery targets.
10. SAST, dependency/container/IaC scanning, penetration test, abuse test, privacy threat model, code review, and a remediation SLA.
11. Corridor-specific legal, professional, privacy, cross-border transfer, clinical, commercial, and telemedicine review.
12. Named 24/7 security escalation and clearly separate clinical/emergency operating playbooks.

No engineer should use “HIPAA compliant,” “DPDP compliant,” “GDPR compliant,” “secure medical record,” or equivalent language without evidence and qualified review.

## Performance objectives for pilot scale

These are engineering targets to verify, not current measurements.

| Path | Target at p95 | Notes |
|---|---:|---|
| Health | 100 ms server time | No database details returned |
| Case list | 300 ms server time | Paginated, at most 20 rows by default |
| Case workspace | 500 ms server time | One bounded aggregate query set; no file payloads |
| Create synthetic case | 500 ms server time | Durable transaction excludes background work |
| Largest Contentful Paint | under 2.5 s on representative mobile network | Measure in deployed environment |
| Interaction to Next Paint | under 200 ms | Avoid large client bundles and layout work |

## Performance design

- Render stable content on the server and keep client components small.
- Use no general UI framework, charting library, icon package, or runtime CSS-in-JS in V0.
- Use responsive CSS and system fonts to avoid third-party font requests.
- Paginate list endpoints and bound all query/task batches.
- Prefetch related aggregate rows to avoid N+1 queries.
- Index queue-driving status and due-date fields.
- Keep record files out of application server memory; future uploads go directly to quarantine storage.
- Move slow notifications/scans to Celery only after the database transaction succeeds.
- Add query budgets and load tests before pilot traffic; do not extrapolate local timings to production.

## Observability without health-data leakage

Allowed dimensions include request ID, route template, method, response code, duration, task name, opaque case UUID, queue delay, deployment version, and bounded error class. Names, emails, phone numbers, clinical questions, document labels, response bodies, tokens, signed URLs, and free text are prohibited.

Initial service-level indicators:

- API availability and latency by route template;
- 4xx/5xx rate without payload capture;
- database pool and query latency;
- queue depth, age, success/failure/retry rate;
- case workflow stage duration from structured events;
- frontend Web Vitals with no health/personal dimensions.

## Capacity and scaling path

Keep one deployable modular monolith through the first corridor. Scale stateless Next.js/API replicas horizontally, tune PostgreSQL connections, and scale Celery worker queues by workload. Extract a service only when independent scaling, security isolation, or team ownership is measured and cannot be handled cleanly within the monolith.
