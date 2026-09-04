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

### Requirement: fixture lifecycle controls visible product mode

The system SHALL have an explicit persisted `standard` or `demo` product mode. `Load demo data` SHALL switch to demo mode only after the complete versioned fixture reaches its expected counts. `Delete demo data` SHALL switch back to standard mode in the same transaction that removes fixture-owned records. Startup SHALL default to standard mode and SHALL never infer demo visibility from prototype/debug configuration alone.

In standard mode, public/product routes, blogs, navigation, authentication, and empty feature shells SHALL remain available, but no synthetic person, provider, rating, connection, message, referral, or demo-specific product copy SHALL be returned. In demo mode, bounded fixture records MAY appear only through the role-authorized product APIs that own them and SHALL be clearly identified as demo data.

#### Scenario: administrator has not loaded demo data

- **WHEN** any visitor or authenticated user opens a normal product route in standard mode
- **THEN** the route remains usable with a production-shaped empty state and contains no fixture record or demo-data banner

#### Scenario: fixture load succeeds

- **WHEN** the platform administrator loads the validated fixture and all expected counts match
- **THEN** product mode becomes `demo` and authorized directory/referral/admin views may return their bounded fixture records

#### Scenario: fixture load fails or is partial

- **WHEN** validation, seed, or expected-count verification fails
- **THEN** the transaction rolls back, product mode remains `standard`, and no partial fixture becomes product-visible

#### Scenario: administrator deletes demo data

- **WHEN** confirmed deletion succeeds
- **THEN** product mode becomes `standard`, subsequent normal product requests return no synthetic records, and the persistent admin remains available

### Requirement: administrator preview does not bypass participant privacy

When demo mode is enabled, a platform administrator MAY see the bounded demo doctor directory and aggregate hospital, connection, referral, and message counts required to understand product coverage. Administrator status SHALL NOT automatically grant a case assignment, conversation participation, message-body access, or patient record access.

#### Scenario: administrator previews demo coverage

- **WHEN** a platform administrator opens the demo control center in demo mode
- **THEN** the system may return bounded provider cards and operational counts but omits participant-only message bodies and scoped case contents unless a separate explicit grant exists
