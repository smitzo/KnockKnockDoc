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

The server SHALL lock the application while transitioning it, enforce `submitted|changes_requested -> under_review -> changes_requested|approved|rejected`, derive the reviewer from the active session, and reject stale or repeated actions. Request-changes and reject actions SHALL require a bounded reason code; a private reviewer note SHALL never be copied into a security event.

#### Scenario: applicant tries to approve itself

- **WHEN** an applicant calls a review or activation endpoint
- **THEN** the server returns `403` and leaves application, membership, and publication states unchanged

#### Scenario: two reviewers act on the same application

- **WHEN** two platform reviewers attempt competing terminal actions
- **THEN** a row lock and current-state check allow at most one valid transition and the losing request changes no activation records

### Requirement: synthetic approval projects access atomically

For Prototype V0, a platform administrator MAY approve only an explicitly synthetic `.test` application through a labelled synthetic-review action. Doctor approval SHALL atomically activate the account, create an identity profile, create the appropriate referring-practice or hospital organization membership, and create one synthetic professional-directory projection. Hospital approval SHALL atomically activate the representative, hospital organization, and hospital-coordinator membership but SHALL NOT create a doctor directory profile. A failed projection SHALL roll back the status change and every access record.

Synthetic admin review SHALL be stored as a distinct verification basis and SHALL NOT be described as real mailbox, professional-credential, facility, accreditation, or public-profile verification.

#### Scenario: referring doctor is approved

- **WHEN** a platform administrator starts review and approves a valid synthetic referring-doctor application
- **THEN** the account can sign in, has one active referrer membership and one bounded synthetic directory card, and no patient/case access is granted

#### Scenario: hospital is approved

- **WHEN** a platform administrator starts review and approves a valid synthetic hospital application
- **THEN** the representative can sign in with one hospital-coordinator membership and no professional doctor directory card

#### Scenario: activation projection fails

- **WHEN** an organization, membership, identity, or directory invariant prevents approval
- **THEN** the transaction leaves the application under review, the account inactive, and no partial access projection exists

### Requirement: reviewer queue is private and bounded

Only an active platform administrator SHALL list or inspect applications. The reviewer representation SHALL omit password hashes and SHALL expose only bounded application/detail fields needed for the decision. Reads and mutations SHALL be throttled and application status filtering SHALL be bounded.

#### Scenario: professional requests the reviewer queue

- **WHEN** a doctor, hospital coordinator, pending applicant, patient, outsider, or anonymous visitor requests review data
- **THEN** the server returns `403` and no application email, legal name, review note, or detail is returned

### Requirement: email verification is not credential verification

Verification tokens SHALL be hashed, purpose-bound, single use, expiring, and invalidated after success or replacement. The interface SHALL explain that mailbox verification does not prove medical credentials or hospital authority.

#### Scenario: verification token is replayed

- **WHEN** an applicant submits an expired, replaced, malformed, or previously used email-verification token
- **THEN** the server returns a generic invalid-token result, changes no verification or access state, and records no secret token value

#### Scenario: prototype uses synthetic admin review

- **WHEN** the local synthetic prototype activates a `.test` account before email delivery exists
- **THEN** the identity records `synthetic_admin_review` as its verification basis and every reviewer/user surface states that no real mailbox or professional credential was verified
