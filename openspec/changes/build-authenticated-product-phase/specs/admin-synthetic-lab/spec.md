# Admin Synthetic Lab Specification

## ADDED Requirements

### Requirement: admin-only visibility

The system SHALL expose synthetic directory data only to an authenticated user with an active verified identity and an active platform organization membership whose role is `admin`.

#### Scenario: platform admin reads the lab

- **WHEN** an active platform admin requests the lab summary or directory
- **THEN** the system returns bounded fictional rows and marks the response synthetic-only

#### Scenario: non-admin is denied

- **WHEN** a patient, referrer, specialist, hospital coordinator, or platform coordinator requests the lab
- **THEN** the system returns `403` and no directory row

#### Scenario: anonymous caller is denied

- **WHEN** an anonymous caller requests the lab
- **THEN** the system returns an authentication failure and no directory row

### Requirement: realistic bounded fixture

The seed SHALL create at least 30 fictional doctor profiles and 30 fictional patient profiles with local visual references and workflow-useful structured fields. It SHALL be idempotent and SHALL NOT contain real people, credentials, direct contact details, or raw medical records.

#### Scenario: repeated seed

- **WHEN** the seed command runs twice
- **THEN** stable fixture keys are updated without duplicate profiles and the counts remain bounded

### Requirement: catalog identity does not grant care access

Directory presence SHALL NOT create a case assignment, case grant, or authenticated session. Patient and doctor demo accounts MAY exist for role rehearsal, but no directory API becomes visible to them.

#### Scenario: doctor account exists

- **WHEN** a seeded doctor authenticates successfully
- **THEN** that doctor still receives `403` from the admin lab unless separately granted an active platform-admin membership

### Requirement: administrator controls the fixture lifecycle

All synthetic catalog, professional-network, and referral-rehearsal records SHALL be sourced from a versioned JSON fixture collection that rejects secret-bearing keys and declares expected counts. Only an active platform administrator SHALL load or delete that collection. Startup SHALL preserve/bootstrap only the administrator and SHALL NOT load product fixtures automatically.

#### Scenario: empty administrator loads demo data

- **WHEN** an active platform administrator selects `Load demo data`
- **THEN** the server validates the fixture manifest, idempotently creates the exact expected records, audits the action without credentials, and reports the collection loaded

#### Scenario: administrator deletes demo data

- **WHEN** an active platform administrator submits the exact destructive confirmation
- **THEN** the server deletes fixture accounts, profiles, ratings, connections, messages, and referral rehearsals while preserving the active administrator so the collection can be loaded again

#### Scenario: non-admin calls a lifecycle endpoint

- **WHEN** an anonymous, doctor, patient, specialist, hospital, or coordinator account calls load or delete
- **THEN** the server returns `403`, changes no fixture state, and exposes no fixture rows
