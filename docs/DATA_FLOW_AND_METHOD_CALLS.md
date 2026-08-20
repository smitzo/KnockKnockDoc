# Data Flow and Method Calls

## Read a case workspace

```mermaid
sequenceDiagram
    actor User as Patient / doctor / coordinator
    participant UI as Next.js workspace
    participant API as DRF CaseViewSet
    participant Query as referrals.selectors
    participant DB as PostgreSQL

    User->>UI: Open synthetic workspace
    UI->>API: GET /api/v1/demo/workspace/ + session cookie
    API->>Query: authorized_workspace(user, case:view)
    Query->>DB: Active profile + membership + assignment + grant + scope
    Query->>DB: Authorized case + prefetched related records
    DB-->>Query: Aggregate rows
    Query-->>API: ReferralCase
    API-->>UI: Bounded JSON representation
    UI-->>User: Next action, status, access, missing items, response
```

Expected call path:

```text
app/workspace/page.tsx
  -> lib/api.ts:getDemoWorkspace(cookie)
    -> GET /api/v1/demo/workspace/ + session cookie
      -> SessionAuthentication
      -> referrals.api.views.DemoWorkspaceView.get()
        -> referrals.selectors.get_authorized_demo_workspace(user, "case:view")
          -> identity state + membership + assignment + grant + scope filters
        -> referrals.selectors.referral_workspace_queryset()
          -> ReferralCase.objects.select_related(...).prefetch_related(...)
        -> referrals.api.serializers.ReferralCaseDetailSerializer
```

## Create a synthetic referral

```mermaid
sequenceDiagram
    actor User
    participant Form as Referral composer
    participant API as DRF CaseViewSet
    participant Serializer as CaseCreateSerializer
    participant Service as create_referral_case
    participant DB as PostgreSQL
    participant Queue as Redis
    participant Worker as Celery

    User->>Form: Enter synthetic planned-care scenario
    Form->>API: POST JSON /api/v1/cases/ + session + CSRF token
    API->>DB: Resolve active verified referrer membership
    API->>Serializer: Validate shape and safety boundaries
    Serializer->>Service: create_referral_case(validated_data, membership)
    Service->>DB: BEGIN
    Service->>DB: INSERT case
    Service->>DB: INSERT assignment + scoped access grant
    Service->>DB: INSERT append-only case and security events
    Service->>DB: COMMIT
    Service-->>Queue: enqueue(case UUID) after commit
    API-->>Form: 201 + case representation
    Queue->>Worker: record_case_created(case UUID)
    Worker->>DB: Idempotent operational follow-up
```

Failure rules:

- Validation errors return field-specific `400` responses without echoing unsafe content into logs.
- A database failure rolls back case and initial event together.
- A broker failure after commit does not lose the referral; the durable case remains and a periodic reconciliation task can recover it.
- A rejected emergency-like scenario returns a coordination-boundary message and local-emergency direction. It is not categorized or stored.

## Deadline scan

```text
Celery beat (future scheduler)
  -> referrals.tasks.scan_referral_deadlines(batch_size)
    -> ReferralCase.objects.filter(next_action_due__lt=now, status__in=open_states)
      -> values_list("id", flat=True)[:bounded_batch]
        -> safe operational counter / future outbox notification
```

No task argument or queue payload contains patient name, clinical question, document name, or message content.

## Future secure upload flow — not implemented

```mermaid
sequenceDiagram
    actor User
    participant API
    participant DB
    participant Store as Private object quarantine
    participant Scan as Malware scanner

    User->>API: Request upload intent for authorized case/category
    API->>DB: Check identity + assignment + consent + category scope
    API-->>User: Short-lived restricted upload intent
    User->>Store: Upload directly to quarantine key
    Store-->>Scan: Object-created event
    Scan->>Store: Validate type, malware, safe metadata
    Scan->>API: Signed scan result callback
    API->>DB: Mark clean or rejected; append audit event
    API-->>User: Authorized short-lived view intent only after clean
```

This flow requires authentication, object-level permission evaluation, separate quarantine, content-type detection, malware scanning, safe preview generation, encryption/key policy, audit, retention, and incident response. Adding an S3 SDK alone is not an implementation of this design.

## Authorization decision flow — implemented for synthetic cases

```text
authenticated session
  -> active verified identity profile
  -> active organization and membership
  -> active case assignment in its valid interval
  -> active, unexpired, unrevoked case access grant
  -> normalized requested scope
  -> allow with append-only security event OR conceal case existence
```

Every condition is conjunctive. A verified doctor or hospital membership alone never grants case access. Consent and document-category scope remain future mandatory gates before real data.
