# Comprehensible Navigation Specification

## Requirement: product purpose is understandable before domain mechanics

The public page SHALL describe the product in plain language using three primary actions: find a doctor, connect professionally, and create/manage a referral. Primary headings SHALL use a legible sans-serif system with responsive scale and SHALL avoid unexplained access-control or medical-tourism jargon.

### Scenario: new visitor scans the first viewport

- **WHEN** a visitor views the page on desktop or a 390px mobile viewport
- **THEN** they can identify the intended users, the three-step workflow, one primary next action, and the fictional/non-medical boundary without scrolling through technical concepts

## Requirement: authenticated navigation follows user tasks

Eligible professionals SHALL receive persistent navigation labelled `Find doctors`, `Connections`, `Messages`, and `Referrals`. Patient accounts SHALL not receive professional discovery or chat links.

### Scenario: professional opens the application

- **WHEN** an eligible professional signs in
- **THEN** the page presents the four task destinations and a concise current-state summary without an editable role selector
