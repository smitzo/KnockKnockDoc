# Trust and Content Specification

## ADDED Requirements

### Requirement: company and service boundaries are public

The site SHALL provide About and How it works pages stating the company purpose, primary users, role responsibilities, operating model, fictional prototype boundary, medical-information disclaimer, and emergency limitation. It SHALL not imply that the software diagnoses, prescribes, guarantees outcomes, verifies real providers in V0, or replaces licensed care.

#### Scenario: patient reads the service explanation

- **WHEN** a patient or family member opens About or How it works
- **THEN** they can distinguish coordination from clinical care and see that emergencies require local emergency services

### Requirement: evidence articles remain reusable and attributable

The public Insights listing SHALL render article metadata and content from the validated file-backed collection rather than duplicating article markup. Every article SHALL have a reviewed date, local image with alt text, direct sources, uncertainty where appropriate, and a no-medical-advice boundary.

#### Scenario: a new valid article file is added

- **WHEN** a maintainer adds a schema-valid JSON article and local image
- **THEN** the listing, route generation, and home-page preview can include it without adding a hard-coded page component

#### Scenario: article source is unsafe or missing

- **WHEN** a content file omits required provenance or uses a non-HTTPS source
- **THEN** the production build fails with a content validation error
