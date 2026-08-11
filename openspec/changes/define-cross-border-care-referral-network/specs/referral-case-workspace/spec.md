## ADDED Requirements

### Requirement: Structured doctor-originated referral and patient authorization
The product SHALL let a verified doctor create a referral containing the patient contact, sourced clinical summary, requested specialty, and clinical question, and SHALL obtain patient or authorized-representative approval before sharing the case with a receiving hospital except under a separately approved exception policy.

#### Scenario: Patient approves a referral
- **WHEN** the patient verifies their contact and approves the displayed referrer, purpose, recipient, and sharing scope
- **THEN** the case records an active authorization and becomes eligible for completeness review and routing

#### Scenario: Patient declines a referral
- **WHEN** the patient declines or does not provide required authorization
- **THEN** the product prevents provider sharing and shows the referrer only the appropriate non-disclosing status

### Requirement: Controlled records and isolated provider requests
The product SHALL support categorized PDF/image records and SHALL create a recipient-specific provider review request with an explicit share manifest. A hospital MUST NOT access a case that has not been shared with it, and one hospital MUST NOT see another hospital's request, opinion, proposal, or quotation.

#### Scenario: Case is shared with one hospital
- **WHEN** a case manager creates an authorized review request for Hospital A
- **THEN** Hospital A can access only the shared case and record set while Hospital B has no access or awareness of Hospital A's request

### Requirement: Case-bound collaboration and information requests
Authorized participants SHALL be able to send attributable case messages and structured information requests. Each active case SHALL display participants, current status, owner, next action, and material event history.

#### Scenario: Specialist requests a missing report
- **WHEN** the assigned specialist requests a named report with a reason
- **THEN** the patient/referrer sees the request, can upload/link/mark it unavailable, and the response appears in the same case history

### Requirement: Attributable clinical and hospital response
Only an assigned verified clinician SHALL issue a preliminary opinion. The hospital SHALL issue the operational proposal and indicative quotation as a separate attributable, versioned artifact with essential assumptions, inclusions/exclusions, currency, and validity.

#### Scenario: Complete response is delivered
- **WHEN** the assigned clinician issues an opinion and the hospital authorizes the related proposal and quotation
- **THEN** the patient and authorized referrer can view the permitted response with author, organization, date, version, limitations, and commercial assumptions

### Requirement: Patient decision and closed-loop handback
The product SHALL let the patient record proceed, clarify, decline, or pause; SHALL track a simple selected-case next step; and SHALL return discharge/follow-up documents to the patient and authorized referrer where treatment occurs and sharing remains permitted.

#### Scenario: Treatment handback completes
- **WHEN** a selected patient's hospital uploads the discharge/follow-up pack and the patient has authorized the referrer
- **THEN** both patient and referrer can receive the permitted documents and the referral records the handback disposition

### Requirement: Coordination-only product boundary
The product MUST NOT independently diagnose, prescribe, recommend a treatment, guarantee outcome/price/visa, or present a platform-generated clinical opinion.

#### Scenario: Operator handles a clinical question
- **WHEN** a patient asks a platform case manager which treatment to choose
- **THEN** the product/workflow directs the question to an authorized clinician and prevents the case manager from issuing a clinical recommendation as platform content
