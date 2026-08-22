# Admin Synthetic Lab Specification

## Requirement: admin-only visibility

The system SHALL expose synthetic directory data only to an authenticated user with an active verified identity and an active platform organization membership whose role is `admin`.

### Scenario: platform admin reads the lab

- **WHEN** an active platform admin requests the lab summary or directory
- **THEN** the system returns bounded fictional rows and marks the response synthetic-only

### Scenario: non-admin is denied

- **WHEN** a patient, referrer, specialist, hospital coordinator, or platform coordinator requests the lab
- **THEN** the system returns `403` and no directory row

### Scenario: anonymous caller is denied

- **WHEN** an anonymous caller requests the lab
- **THEN** the system returns an authentication failure and no directory row

## Requirement: realistic bounded fixture

The seed SHALL create at least 30 fictional doctor profiles and 30 fictional patient profiles with local visual references and workflow-useful structured fields. It SHALL be idempotent and SHALL NOT contain real people, credentials, direct contact details, or raw medical records.

### Scenario: repeated seed

- **WHEN** the seed command runs twice
- **THEN** stable fixture keys are updated without duplicate profiles and the counts remain bounded

## Requirement: catalog identity does not grant care access

Directory presence SHALL NOT create a case assignment, case grant, or authenticated session. Patient and doctor demo accounts MAY exist for role rehearsal, but no directory API becomes visible to them.

### Scenario: doctor account exists

- **WHEN** a seeded doctor authenticates successfully
- **THEN** that doctor still receives `403` from the admin lab unless separately granted an active platform-admin membership
