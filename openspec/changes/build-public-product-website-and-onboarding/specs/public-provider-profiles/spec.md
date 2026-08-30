# Public Provider Profiles Specification

## ADDED Requirements

### Requirement: public doctor records are explicit publications

Anonymous visitors SHALL receive only approved fields from doctor records whose publication state is `published` and professional verification is valid. Public doctor fields SHALL include specialty, subspecialties, designation, reviewed experience, qualifications, published affiliations, languages, location, summary, interests, approved image, and clearly scoped collaboration signals where eligible.

#### Scenario: pending doctor profile is requested

- **WHEN** an anonymous visitor guesses the identifier or slug of a draft, synthetic-admin, expired, suspended, or unpublished doctor
- **THEN** the server returns `404` and no private or existence information

#### Scenario: published doctor is displayed

- **WHEN** a valid published profile is opened
- **THEN** the page shows verification meaning/date, source-aware professional facts, and no raw council number, email, phone, credential evidence, clinical outcome claim, or paid rank

### Requirement: public hospital records are explicit publications

Anonymous visitors SHALL receive only approved fields from hospitals whose publication state is `published` and verification is valid. Accreditation, capacity, and facility facts SHALL include provenance and reviewed/as-of dates.

#### Scenario: accreditation has expired

- **WHEN** a published hospital's accreditation validity ends without reverification
- **THEN** the system stops presenting it as currently accredited and flags the record for review

### Requirement: admin fixtures cannot become public search results

Public provider queries SHALL not read `SyntheticDoctorProfile`, `SyntheticPatientProfile`, synthetic professional-network profiles, demo account identities, or admin-lab serializers.

#### Scenario: administrator loads the synthetic fixture collection

- **WHEN** the admin loads all demo doctors, patients, ratings, and accounts
- **THEN** anonymous doctor and hospital queries remain unchanged and contain none of those fixture records
