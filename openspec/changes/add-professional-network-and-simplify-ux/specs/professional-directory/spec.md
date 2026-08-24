# Professional Directory Specification

## Requirement: verified professionals discover bounded profiles

The system SHALL expose discoverable professional cards only to active, verified identities with an eligible active professional or platform membership. Patient accounts SHALL receive `403`. The representation SHALL exclude credentials, direct contact details, admin-lab operational fields, and patient data.

### Scenario: eligible doctor searches

- **WHEN** an eligible verified professional searches by name, specialty, country, city, or organization
- **THEN** the server returns only discoverable fictional professional cards matching the bounded query

### Scenario: patient searches

- **WHEN** a patient account requests the professional directory
- **THEN** the server returns `403` and no professional card

## Requirement: synthetic directory is unmistakable

Every prototype directory response and card SHALL state that the profile is fictional and SHALL not imply a real credential, endorsement, capacity, or outcome.
