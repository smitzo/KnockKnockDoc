## ADDED Requirements

### Requirement: Evidence-backed professional profiles
The product SHALL expose a doctor or hospital as verified only after an authorized verifier records the checked claim, source, result, scope, and verification date. The displayed status SHALL NOT imply guaranteed competence, quality, or outcome.

#### Scenario: Verified doctor becomes discoverable
- **WHEN** an authorized verifier approves a doctor's identity, licence scope, specialty, and current hospital affiliation
- **THEN** the doctor becomes discoverable with the verified claims and verification date visible

#### Scenario: Unresolved verification blocks clinical participation
- **WHEN** a doctor's licence or affiliation evidence is missing, inconsistent, expired, suspended, or rejected
- **THEN** the product prevents the doctor from being presented as verified or assigned to issue a case opinion

### Requirement: Focused professional discovery
The product SHALL let eligible users find the curated receiving roster by name, specialty/subspecialty or controlled procedure tag, current hospital, country/city, language, and current international-referral availability. Default ordering MUST NOT be based on payment, popularity, followers, or unvalidated outcomes.

#### Scenario: Referrer finds an eligible specialist
- **WHEN** a verified referrer filters for a supported specialty, language, and accepting-referrals state
- **THEN** the product returns only approved matching specialists and explains the matching fields

### Requirement: Lightweight professional relationships
The product SHALL support connection request, accept, decline, view, remove, block, and report actions between verified professionals without requiring social-feed mechanics.

#### Scenario: Connection becomes reusable
- **WHEN** a verified receiving doctor accepts a verified referrer's connection request
- **THEN** both doctors can find the relationship later and use it to initiate a permitted referral or bounded professional message

### Requirement: Spam-resistant messaging boundary
The product MUST prevent open patient-specific messaging before a consented case exists. A pre-connection user may send only a bounded connection note; limited non-case messaging may begin after acceptance; patient information MUST move into a case-bound channel.

#### Scenario: Patient information is attempted before connection
- **WHEN** a doctor attempts to attach patient records or send patient-specific content in a connection request
- **THEN** the product blocks the action and directs the doctor to the referral and patient-consent flow

### Requirement: Free doctor participation and non-gamified visibility
V0 SHALL NOT require a doctor to pay to create an approved profile, search the supported network, connect, create/receive referrals, or participate in an assigned case. V0 SHALL NOT include followers, likes, public endorsements, star ratings, or paid clinical ordering.

#### Scenario: Verified doctor uses the referral network
- **WHEN** a verified doctor performs the V0 network and referral actions
- **THEN** no doctor membership or per-referral participation fee is required and no paid visibility changes discovery order
