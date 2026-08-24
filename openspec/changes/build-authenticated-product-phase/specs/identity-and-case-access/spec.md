# Identity and Case Access Specification

## Requirement: server-managed authenticated session

The system SHALL authenticate users with the framework password hasher and a server-managed session cookie. The browser SHALL NOT store bearer credentials. Login and all authenticated mutations SHALL enforce CSRF, and login attempts SHALL be throttled.

### Scenario: valid account signs in

- **WHEN** an active user with an active identity profile submits valid credentials and CSRF token
- **THEN** the server rotates/creates the session and returns the verified profile and active memberships without returning password material

### Scenario: mutation omits CSRF

- **WHEN** a browser session submits login, logout, referral creation, or another state-changing request without a valid CSRF token
- **THEN** the server rejects the mutation and does not change domain state

### Scenario: weak seed credential is supplied

- **WHEN** a demo seed is invoked with a missing, reused, or weak administrator/account password
- **THEN** the command fails without creating accounts or printing secret material

## Requirement: referral access is deny-by-default

Every referral read SHALL require an active user, active and verified profile, active membership in the relevant organization, active case assignment, current unrevoked/unexpired access grant, and the normalized scope required by the operation. Client-provided roles or referrer identity SHALL NOT grant access.

### Scenario: authorized participant reads a case

- **WHEN** every identity, membership, assignment, grant, and scope condition is current
- **THEN** the server returns only the assigned case representation allowed by that scope

### Scenario: any authorization link is missing or stale

- **WHEN** the user is suspended, unverified, unassigned, expired, revoked, in another organization, or lacks the requested scope
- **THEN** the server returns not found for that case and does not disclose its existence

### Scenario: user attempts to select a different role

- **WHEN** a client supplies a role or organization not present in the active server session and grants
- **THEN** the supplied value is ignored for authorization and no extra case data is returned

## Requirement: authenticated frontend has no synthetic fallback

Authenticated pages SHALL derive identity, membership, and case data from the backend session. An API failure or inaccessible case SHALL render a signed-out, denied, or unavailable state; it SHALL NOT substitute local demo case data.

### Scenario: backend case request fails

- **WHEN** the frontend cannot retrieve an authorized case
- **THEN** the page exposes no local fallback case and presents a bounded recovery or access-denied path

## Requirement: security-relevant events are attributable

The application SHALL append an attributable security event for login success/failure, logout, material grant lifecycle actions, and admin synthetic-lab access. Application code SHALL not update or delete an existing security-event row.

### Scenario: administrator reads synthetic catalog data

- **WHEN** an authorized platform admin requests the admin lab
- **THEN** the application records the actor, action, target/context, outcome, and timestamp without secrets or patient health data
