# Low-Level Design

## Repository layout

```text
backend/
  config/                 Django settings, URL routing, Celery wiring
  apps/core/              Shared UUID/timestamp model and health endpoint
  apps/identity/          Profiles, organizations, memberships, sessions, security events
  apps/referrals/         Referral aggregate, API, services, tasks, tests
  manage.py
frontend/
  app/                    Next.js App Router routes and global styles
  components/             Accessible product and workspace components
  lib/                    Typed API client and domain contracts
infra/                    Container entry points when needed
docs/                     Product and engineering documentation
worklog/                  Numbered immutable Markdown entries
```

## Referral aggregate

`ReferralCase` is the aggregate root. Related records cannot exist without a case.

| Entity | Key fields | Important invariant |
|---|---|---|
| `ReferralCase` | UUID, human reference, specialty, sourced summary, clinical question, status, consent status, next action/owner/due date | V0 rows are always marked synthetic; planned care must be confirmed |
| `CaseParticipant` | case, display name, role, organization, access scope/state | Unique active presentation identity per case/role/name |
| `RecordItem` | case, label, category, clinical date, source, readiness state | Metadata only in V0; never contains an object URL or raw file |
| `InformationRequest` | case, requested item, requester, reason, state, due date | Requester and reason are attributable |
| `ProviderResponse` | case, author, organization, response type, summary, limitations, issued time | Clinical and commercial authorship remain separate |
| `CaseEvent` | case, event type, actor label/role, safe summary, occurred time | Append-only through application services |
| `CaseAssignment` | case, organization membership, purpose, active interval | The exact membership, not only its role or organization, is assigned |
| `CaseAccessGrant` | case, organization membership, assignment, grant/revoke/expiry facts | One current grant per case membership; revocation does not delete history |
| `GrantScope` | grant, scope | Normalized and unique; the authorization query requires the requested scope |

All identifiers exposed outside the service are UUIDs or non-sequential references. Human references are not authorization tokens.

## Case state model

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> AwaitingConsent
    AwaitingConsent --> CompletenessReview: consent granted
    CompletenessReview --> ReadyToRoute: required packet complete
    ReadyToRoute --> ProviderReview: explicit case share accepted
    ProviderReview --> InformationRequired: attributed request
    InformationRequired --> ProviderReview: item answered
    ProviderReview --> ResponseReady: opinion/proposal issued
    ResponseReady --> PatientDecision
    PatientDecision --> PreparingTravel: proceed
    PatientDecision --> Closed: decline / stop
    PreparingTravel --> Treatment
    Treatment --> Handback
    Handback --> Closed
    AwaitingConsent --> Closed: declined / withdrawn
    CompletenessReview --> Closed: out of scope
```

V0 displays these stages but exposes only the safe creation command. Later mutation endpoints must use an explicit transition function with actor, preconditions, event creation, and `select_for_update()`.

## Identity model

The project retains Django's default `User` because its migrations already exist. Login usernames are normalized lowercase synthetic email addresses. Domain identity data is kept in explicit UUID entities:

| Entity | Purpose | Invariant |
|---|---|---|
| `IdentityProfile` | Display name, normalized email, account type, verification and account state | One profile per user; normalized email is unique |
| `Organization` | Platform, hospital, or referring-practice boundary | Stable unique slug; suspension blocks its memberships |
| `OrganizationMembership` | A user's role in one organization | Role is explicit; only active rows authorize |
| `SecurityEvent` | Authentication and case-access evidence | Append-only through the model/manager; metadata is allowlisted and contains no clinical text |

Demo identities are created only when a long password is supplied through local environment configuration. No password is committed, logged, or returned by the seed command.

## Authorization model

Scopes are namespaced strings such as `case:view` and `case:create`. A selector evaluates active profile, verified email, active organization, active membership, active assignment interval, active grant, grant expiry/revocation, and normalized scope in one filtered queryset. Detail endpoints query only this authorized queryset, so an inaccessible UUID produces `404`.

Creation is a separate capability: it requires an active verified `referrer` membership. The service derives the referrer's presentation identity from that membership; it never trusts a submitted referrer name or organization.

## API contract

| Method and path | Purpose | V0 access |
|---|---|---|
| `GET /api/v1/health/` | Liveness/readiness summary without secrets | Anonymous |
| `GET /api/v1/auth/csrf/` | Issue a masked CSRF token and CSRF cookie | Anonymous, throttled |
| `POST /api/v1/auth/login/` | Establish a rotated server-side session | Anonymous, CSRF-protected, tightly throttled |
| `GET /api/v1/auth/session/` | Return the active profile and memberships | Authenticated |
| `POST /api/v1/auth/logout/` | Flush the current session | Authenticated, CSRF-protected |
| `GET /api/v1/cases/` | List only authorized synthetic rehearsal cases | Authenticated and case-scoped |
| `POST /api/v1/cases/` | Create a synthetic planned-care referral rehearsal | Active verified referrer membership, CSRF-protected |
| `GET /api/v1/cases/{uuid}/` | Complete synthetic case workspace | Authenticated `case:view` grant or `404` |
| `GET /api/v1/demo/workspace/` | Stable seeded workspace for the frontend | Authenticated `case:view` grant or `404` |

The API never returns stack traces, environment variables, database details, storage paths, or raw exception text. V0 parsers accept JSON only. Request size and list/page sizes are bounded.

## Create-case command

1. DRF authenticates the session and resolves an active verified referrer membership.
2. DRF validates length, enum, date, and planned-care confirmation.
3. Serializer rejects emergency wording and likely direct identifiers in the synthetic patient label.
4. `create_referral_case()` opens a database transaction and derives the referrer identity from the membership.
5. A `ReferralCase`, assignment, scoped grant, and initial `CaseEvent` are written atomically.
6. `transaction.on_commit()` sends only the case UUID to Celery.
7. The worker records operational metrics without logging clinical text.

The emergency keyword check is a prototype safety guard, not clinical triage. It redirects the user to local emergency services and must never claim to determine urgency.

## Database behavior

- PostgreSQL is the runtime database and owns constraints/indexes.
- UUID primary keys reduce enumeration risk but do not replace authorization.
- Case status, consent status, due date, and update time are indexed for queues.
- Related rows use explicit `PROTECT` or `CASCADE` according to aggregate ownership.
- Querysets for workspace responses use `select_related`/`prefetch_related` to bound query count.
- Migrations are committed and run before application start.
- SQLite is permitted only through `DATABASE_ENGINE=sqlite` for fast unit tests; PostgreSQL integration tests remain a release requirement.

## Frontend component model

- Server routes own metadata and initial data boundaries.
- Client components are limited to session actions, workspace tabs, and the referral composer.
- The typed API client validates response shape defensively and uses an HTTP-only same-origin session cookie, never browser token storage.
- The workspace role comes from the active membership returned by the server; the V0 presentation-only role switch is removed.
- Loading, empty, and unavailable states use plain language and a recoverable action.
- No patient-sensitive value appears in URLs, analytics, or browser persistence.

## Celery behavior

- Redis is broker/result transport for V0.
- Tasks accept UUIDs, not serialized models or health information.
- Tasks are idempotent and have finite retry/backoff policies.
- The periodic deadline scan reads indexed due dates in bounded batches.
- Worker logs include task and case IDs, never clinical questions, names, or documents.

## Future storage interface

When secure record upload is authorized, application code will depend on a storage service with `create_upload_intent`, `finalize_after_scan`, `create_view_intent`, and `restrict_object` operations. The adapter may use S3, but database rows remain authoritative for consent scope, scan state, retention, and audit. Direct public bucket URLs are forbidden.
