## ADDED Requirements

### Requirement: Verification and operations queues
The platform SHALL provide queues for pending provider verification, new case completeness, routing, missing information, hospital response/SLA, selected-case coordination, handback, and escalations, with an accountable owner and due state.

#### Scenario: Operator claims a new case
- **WHEN** a submitted case enters the completeness queue
- **THEN** an authorized case manager can claim it, become the owner, record missing/complete state, and set the next action

### Requirement: Human-approved completeness and routing
V0 MUST require a trained human to confirm case completeness and select each receiving hospital/specialist. The product SHALL record recipient, reason, authorization, shared manifest, and sent time; it MUST NOT autonomously diagnose or route based on an AI recommendation.

#### Scenario: Case is ready for a provider
- **WHEN** a case manager confirms corridor fit, completeness, recipient eligibility/capacity, and patient authorization
- **THEN** the product permits the manager to create the isolated provider review request and records the routing evidence

### Requirement: Response SLA and escalation visibility
The platform SHALL capture acknowledgement, information-request, opinion, proposal, decision, and handback timestamps and SHALL flag missed operational SLAs for human escalation.

#### Scenario: Hospital response is late
- **WHEN** a provider request passes its agreed response due state
- **THEN** the platform flags the case, notifies the accountable users, and allows a case manager to record chase, extension, or reroute action

### Requirement: Minimal journey coordination
For a selected case, V0 SHALL support a simple checklist/status and secure document area for hospital acceptance, invitation, pre-travel, arrival, discharge, and follow-up while leaving visa interpretation, bookings, partner selection, and exception handling to humans.

#### Scenario: Selected case begins pre-travel
- **WHEN** the patient chooses to proceed and the hospital confirms the case
- **THEN** the case manager can open the minimal journey checklist, record the next dependency, and share the hospital-issued invitation document without representing visa approval

### Requirement: Commercial proof and operating-cost evidence
The platform SHALL make it possible to reconcile qualified referrals, response intervals, stages, decisions, arrivals, lost reasons, active/repeat referrers, handback, hospital usage, and operator effort for each pilot.

#### Scenario: Pilot review is prepared
- **WHEN** an authorized operator generates the pilot evidence set
- **THEN** the output uses defined denominators and attributable events sufficient to discuss hospital value, renewal, and per-case operating cost

### Requirement: V0 scope gate
V0 SHALL exclude social feeds, followers, public ratings/endorsements, travel/insurance/finance marketplaces, payment custody, native video, native mobile apps, autonomous clinical AI, and broad hospital integrations.

#### Scenario: Non-core feature is proposed for V0
- **WHEN** a requested feature does not materially support the acceptance referral, coordination, trust, or commercial-proof workflow
- **THEN** it is excluded from V0 unless founders approve a documented change to this specification
