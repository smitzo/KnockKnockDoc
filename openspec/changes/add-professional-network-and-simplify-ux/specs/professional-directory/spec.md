# Professional Directory Specification

## Requirement: verified doctors discover bounded profiles

The system SHALL expose discoverable professional cards only to active, verified doctors with an eligible referring-doctor or specialist membership. Patient and non-clinical operator accounts SHALL receive `403`. The representation SHALL expose specialty, experience, location, organization, languages, summary and verification label while excluding direct contact details, admin-lab operational fields, credential internals, and patient data.

### Scenario: eligible doctor searches

- **WHEN** an eligible verified professional searches by name, specialty, country, city, or organization
- **THEN** the server returns only discoverable fictional professional cards matching the bounded query

### Scenario: patient searches

- **WHEN** a patient account requests the professional directory
- **THEN** the server returns `403` and no professional card

## Requirement: synthetic directory is unmistakable

Every prototype directory response and card SHALL state that the profile is fictional and SHALL not imply a real credential, endorsement, capacity, or outcome.

## Requirement: ratings describe attributable peer collaboration

Directory cards SHALL show the aggregate and count of fictional peer ratings for communication, referral collaboration, and handback reliability. The UI SHALL label them as synthetic professional-collaboration signals and SHALL NOT describe them as clinical quality, treatment success, or patient outcome.

### Scenario: doctor compares specialists

- **WHEN** a referring doctor reviews directory results
- **THEN** each rated profile shows the aggregate, rating count, category meaning, and synthetic provenance without a “best doctor” ranking claim

### Scenario: profile has no eligible ratings

- **WHEN** a profile has no rating records
- **THEN** the card shows `No peer collaboration ratings yet` rather than a zero score
