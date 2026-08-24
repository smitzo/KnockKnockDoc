# Design

## Product boundary

Network messaging is a professional relationship tool, not a clinical case channel. Only active verified professional identities can discover profiles. A connection needs a declared purpose. Only accepted participants can read/write its conversation. The UI and API require synthetic-only confirmation in this prototype; attachments are not represented.

Patient-specific work belongs to a case because a case can carry assignment, grant, purpose, scope, consent, and audit semantics. A generic conversation cannot safely inherit those conditions.

## Directory data separation

`ProfessionalDirectoryProfile` is a minimal discoverable card: display name, professional role, specialty, country/city, organization label, languages, short professional summary, verification state, avatar key, and connection availability. It does not expose the admin lab’s login email, capacity rehearsal, response-hour metric, credential internals, or patient fixture data.

For Prototype V0 all directory profiles are fictional and labelled synthetic. In production, discoverability would require a separate verification and publication workflow.

## Connection state machine

`pending -> accepted | declined | withdrawn`.

- requester may withdraw only a pending request;
- recipient may accept or decline only a pending request;
- neither side may create a second connection in either direction while one pair exists;
- self-connections are invalid;
- conversation exists only after acceptance.

Blocking/reporting is a production requirement and a prototype gap. Until it exists, the feature is restricted to synthetic accounts and no public signup.

## Message model

Messages are append-only application records with sender, conversation, bounded body, and timestamp. Edits, deletion, reactions, receipts, attachments, embeds, and clinical content are absent. The API never returns messages to a non-participant. Prototype validation rejects common direct-contact/patient-identifier patterns and requires the sender to confirm fictional content.

HTTP polling is sufficient for the synthetic prototype. WebSockets would add connection authentication, authorization refresh, fan-out, delivery, retry, presence, and operational burden without validated user need.

## UX direction

- Use a legible system sans-serif stack; reserve no decorative type for primary tasks.
- Default body size at least 16px on public/product explanations and 14px in dense application lists.
- One primary action per page.
- Use direct labels: `Find doctors`, `Connections`, `Messages`, `Referrals`.
- Explain the product with `Find -> Connect -> Refer`, then disclose safety boundaries.
- Hide access-control mechanics until they explain a denial or build user trust.
- Keep advanced admin/flow inspection outside normal professional navigation.

## Security and abuse controls

- session auth, CSRF, active verified identity and eligible professional membership;
- explicit object-participant checks on every connection/conversation query;
- server-derived sender/requester identity;
- per-user throttles for directory, connection requests, and messages;
- bounded JSON-only payloads and no upload surface;
- safe security events without message bodies;
- no patient accounts in the directory or chat APIs;
- synthetic-only release boundary until moderation, reporting/blocking, production verification, retention, and privacy gates exist.
