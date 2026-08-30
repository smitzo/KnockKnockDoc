# Professional Onboarding Specification

## ADDED Requirements

### Requirement: registration is role specific and verification gated

A visitor SHALL choose `Join as a doctor` or `Join as a hospital`. The server SHALL validate the shared and role-specific fields, normalize the email, enforce password policy, record versioned acknowledgements, and create a private application. Submission SHALL NOT create an active professional membership, active hospital, discoverable profile, or public publication.

#### Scenario: doctor submits a complete application

- **WHEN** a doctor submits valid identity, professional, council, qualification, organization, and declaration fields
- **THEN** the system creates a private submitted application, initiates purpose-bound email verification, returns a non-enumerating response, and grants no network/referral access

#### Scenario: hospital representative submits a complete application

- **WHEN** an authorized representative submits valid organization, address, domain, accreditation, department, capacity-provenance, and authority fields
- **THEN** the system creates a private hospital application and grants no organization administration rights

### Requirement: review transitions are server controlled

Only a platform administrator SHALL transition submitted applications through under-review, changes-requested, approved, rejected, or withdrawn rules. Every reviewer transition SHALL be audited without credential evidence or sensitive free text in security metadata.

#### Scenario: applicant tries to approve itself

- **WHEN** an applicant calls a review or activation endpoint
- **THEN** the server returns `403` and leaves application, membership, and publication states unchanged

### Requirement: email verification is not credential verification

Verification tokens SHALL be hashed, purpose-bound, single use, expiring, and invalidated after success or replacement. The interface SHALL explain that mailbox verification does not prove medical credentials or hospital authority.

#### Scenario: verification token is replayed

- **WHEN** an applicant submits an expired, replaced, malformed, or previously used email-verification token
- **THEN** the server returns a generic invalid-token result, changes no verification or access state, and records no secret token value
