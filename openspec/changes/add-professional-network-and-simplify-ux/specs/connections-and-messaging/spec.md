# Connections and Messaging Specification

## ADDED Requirements

### Requirement: connection requests are purpose-bound

An eligible professional SHALL be able to request one connection with another discoverable professional by selecting a professional purpose and optional bounded note. The server SHALL derive the requester from the session and reject self, duplicate/reversed-pair, patient, and unconfirmed synthetic requests.

#### Scenario: recipient accepts

- **WHEN** the intended recipient accepts a pending connection
- **THEN** the connection becomes accepted once and a single conversation becomes available to both participants

#### Scenario: unrelated user changes a connection

- **WHEN** any user other than the correct requester/recipient attempts a state transition
- **THEN** the server returns not found and leaves the connection unchanged

### Requirement: messaging requires an accepted connection

Only the two participants of an accepted connection SHALL read or append messages. Messages SHALL be server-attributed, bounded, append-only, JSON text with no attachment representation, and confirmed synthetic-only in Prototype V0.

#### Scenario: participant sends fictional professional message

- **WHEN** an accepted participant submits a bounded message and synthetic-only confirmation
- **THEN** the server appends it, returns its server timestamp/sender, and records a security event without the body

#### Scenario: pending connection attempts chat

- **WHEN** either participant attempts to read or send messages before acceptance
- **THEN** the server denies access and returns no message data

#### Scenario: patient-specific identifier is submitted

- **WHEN** a message contains a common direct-contact or patient-identifier pattern
- **THEN** the server rejects it and directs the user to keep all content fictional and patient-specific work case-bound
