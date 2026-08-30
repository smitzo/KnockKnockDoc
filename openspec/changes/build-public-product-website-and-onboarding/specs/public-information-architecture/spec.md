# Public Information Architecture Specification

## ADDED Requirements

### Requirement: one coherent public product shell

The public site SHALL expose a consistent responsive header and footer linking Home, Doctors, Hospitals, How it works, Insights, About, Join, and Sign in. The current route SHALL be identified accessibly and the mobile navigation SHALL be keyboard operable without obscuring content.

#### Scenario: first-time doctor scans Home

- **WHEN** a doctor opens Home on desktop or a 390px viewport
- **THEN** the first viewport identifies doctors as the primary user, explains discover/connect/refer in plain language, presents one primary next action, and discloses that Prototype V0 uses fictional data

#### Scenario: visitor looks for educational content

- **WHEN** any visitor opens the header or footer
- **THEN** an `Insights` link reaches the reusable five-article collection without requiring authentication

### Requirement: public routes use task language

Headings and actions SHALL use plain task labels and a legible sans-serif scale. Public content SHALL not lead with authorization, architecture, handoff, attribution, or medical-tourism jargon without explanation.

#### Scenario: visitor reads a primary task page

- **WHEN** a visitor scans a page heading, description, and primary action
- **THEN** each label describes the user job directly without requiring knowledge of platform architecture or access-control terms

### Requirement: private routes are visibly separate

Admin, applicant-review, authenticated messaging, and referral-workspace routes SHALL not appear as anonymous public destinations and SHALL carry `noindex` metadata.

#### Scenario: search engine or anonymous visitor reaches a private route

- **WHEN** a private route is requested without an eligible session
- **THEN** the route reveals no protected content and its metadata instructs search engines not to index it
