# Educational Content and Onboarding Specification

## ADDED Requirements

### Requirement: sourced educational articles

The product SHALL publish at least five relevant articles from an extensible content collection rather than an in-component article array. Each content document SHALL pass build-time schema validation. Material statistical, financial, economic, and policy claims SHALL link to a credible direct source and display a last-reviewed date. Content SHALL distinguish evidence from inference and SHALL not provide medical advice or guarantee outcomes, savings, visas, or treatment suitability.

#### Scenario: reader checks a statistic

- **WHEN** an article presents a material number
- **THEN** a nearby source link identifies the publisher and page that supports the claim

#### Scenario: evidence is insufficient

- **WHEN** city-level or patient-nationality data cannot be supported by a credible current source
- **THEN** the article describes the limitation instead of inventing a ranking or count

#### Scenario: editor adds an article

- **WHEN** an editor adds a valid article document to the content collection
- **THEN** the shared loader, listing cards, reader, source panel, metadata, and static route render it without duplicating page logic

#### Scenario: content document is unsafe or incomplete

- **WHEN** a content document has a duplicate/unsafe slug, non-local image, non-HTTPS source, missing section, or missing source
- **THEN** the production build fails with the offending content filename

### Requirement: visual product guide

The product SHALL provide a keyboard-accessible how-to guide using original local imagery, code-native arrows/annotations, numbered steps, role ownership, expected outcomes, and explicit safety boundaries.

#### Scenario: new user follows the guide

- **WHEN** a user opens the guide
- **THEN** the guide explains sign-in, referral creation, patient sharing review, provider response, decision, and handback with links to available routes

### Requirement: generated-scene disclosure

Any AI-generated editorial scene SHALL be captioned as illustrative and SHALL not imply a real patient, doctor, hospital endorsement, or documented outcome.

#### Scenario: generated editorial image is displayed

- **WHEN** an article or guide renders an AI-generated scene
- **THEN** nearby text labels it illustrative and fictional without implying a real person, provider, or outcome
