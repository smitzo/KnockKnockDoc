# Comprehensible Navigation Specification

## ADDED Requirements

### Requirement: product purpose is understandable before domain mechanics

The public page SHALL identify doctors as the primary users and describe the flow in plain language: discover specialists, compare bounded professional signals, connect, discuss, and start/manage a referral. Primary headings SHALL use a legible sans-serif system with responsive scale and SHALL avoid unexplained access-control or medical-tourism jargon.

#### Scenario: new visitor scans the first viewport

- **WHEN** a visitor views the page on desktop or a 390px mobile viewport
- **THEN** they can identify the intended users, the three-step workflow, one primary next action, and the fictional/non-medical boundary without scrolling through technical concepts

### Requirement: authenticated navigation follows user tasks

Eligible doctors SHALL receive persistent navigation labelled `Discover`, `My network`, `Messages`, and `Referrals`. Patient and non-clinical operator accounts SHALL not receive professional discovery or chat links.

#### Scenario: professional opens the application

- **WHEN** an eligible professional signs in
- **THEN** the page presents the four task destinations and a concise current-state summary without an editable role selector
