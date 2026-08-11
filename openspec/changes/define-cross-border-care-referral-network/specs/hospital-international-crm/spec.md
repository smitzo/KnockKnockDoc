## ADDED Requirements

### Requirement: Qualified referral inbox
The hospital product SHALL show only cases explicitly shared with that hospital and SHALL include source/referrer, patient country, specialty, completeness, received time, stage, owner, next action, and SLA state.

#### Scenario: Hospital receives a new case
- **WHEN** an authorized provider review request is sent to a hospital
- **THEN** the case appears in that hospital's queue with enough scoped information to accept, decline, or request a correction

### Requirement: Qualification and named assignment
An authorized hospital user SHALL be able to accept, decline with a reason, or request information. Every accepted case MUST have a verified specialist, hospital coordinator, and response due state before medical review begins.

#### Scenario: Accepted case enters review
- **WHEN** the hospital accepts a case and assigns eligible owners
- **THEN** the product records the assignment, starts the agreed response state, and exposes the appropriate next action to each participant

### Requirement: Practical pipeline ownership
The hospital product SHALL support the defined lifecycle from new case through review, response, patient decision, selected-case journey, discharge, follow-up, and closure. Every transition SHALL record actor and time; every active case SHALL have one current owner and next action; branch outcomes SHALL record a reason.

#### Scenario: Case stalls before opinion
- **WHEN** an accepted case exceeds its current response due state without a blocking information request
- **THEN** the product flags it for hospital and platform escalation without automatically issuing or fabricating a response

### Requirement: Clinical and commercial authorship separation
The product MUST preserve clinician ownership of the opinion/clinical pathway and hospital ownership of operational and financial terms. Hospital staff MUST NOT silently edit an issued clinician opinion, and revisions SHALL create a new attributed version.

#### Scenario: Quote changes after issue
- **WHEN** hospital finance changes an issued indicative quotation
- **THEN** the product creates a new version with author, date, reason, and retained prior version while leaving the clinician opinion unchanged

### Requirement: Conversion and referrer relationship record
The hospital product SHALL record patient decision, selected/arrived/admitted/high-level treatment/discharged/closed milestones, lost outcome and reason, referring doctor, repeat-referral relationship, and response intervals needed to evaluate the pilot.

#### Scenario: Patient does not select the hospital
- **WHEN** the patient declines or selects another option
- **THEN** the hospital request records an appropriate lost/not-selected outcome and reason without closing or exposing other provider requests

### Requirement: Hospital role isolation
Hospital membership alone SHALL NOT grant every staff member access to every case. Clinical, coordinator, finance, and organization-administration actions SHALL be restricted to the approved case role and assignment.

#### Scenario: Hospital administrator lacks case role
- **WHEN** an organization administrator who has not been assigned clinical/coordinator/finance case access opens a patient case
- **THEN** the product denies the medical-case view while still allowing permitted membership administration
