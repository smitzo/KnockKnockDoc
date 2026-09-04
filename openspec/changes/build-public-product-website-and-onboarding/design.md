# Design

## Audience hierarchy

1. Referring doctor: primary user and primary home-page action.
2. Receiving specialist: network participant and onboarding path.
3. Hospital partnership/operations lead: organization applicant and likely buyer/influencer.
4. Patient/family: public reader who needs plain-language trust and boundaries, not professional-network access.
5. Platform reviewer: verifies applications and controls publication/activation.

This hierarchy prevents a common marketplace failure: trying to serve patients, doctors, hospitals, coordinators, and investors with equal visual weight in the first viewport.

## Public sitemap

```text
Home
├── Doctors
│   ├── Search and filters
│   └── Doctor detail
├── Hospitals
│   ├── Search and filters
│   └── Hospital detail
├── How it works
├── Insights
│   └── Article detail
├── About
├── Join
│   ├── Join as a doctor
│   └── Join as a hospital
└── Sign in
```

The first viewport answers: who this is for, what job it completes, how it works, and what action to take. It uses a legible system sans stack, restrained type scale, one dominant action, and no architecture/security jargon.

## Doctor public profile

A public doctor profile is a curated publication, not the raw identity record and not the admin synthetic profile. Required reviewable fields:

- legal name (private review field) and approved display name;
- professional role, primary specialty, subspecialties, current designation;
- medical council/jurisdiction, registration number (private by default), verification state/date;
- qualification entries with institution, country, and year;
- years of experience derived from reviewed career start year, not freely claimed text;
- affiliated published hospitals;
- languages, city, country, professional summary, clinical interests;
- optional memberships/publications with provenance URLs reviewed before publication;
- profile image with consent, rights confirmation, alt text, and moderation status;
- collaboration-signal methodology/count where eligible, clearly separated from clinical quality;
- accepted professional connection purposes.

No phone, private email, identity document, raw credential file, patient data, success rate, outcome claim, or paid rank is public.

## Hospital public profile

Required reviewable fields:

- legal entity name (private review field), approved display name, organization type;
- authorized representative and work contact (private);
- address, city, region, country, timezone, website domain;
- establishment year, specialty model, departments and available programs;
- accreditation entries with issuer, identifier, validity dates, and verification state;
- bed/ICU/operating-theatre counts with `as of` date and provenance;
- international-patient services, languages, accessibility, transport/accommodation coordination flags;
- published doctors, facilities, infrastructure summary, emergency capability boundary;
- approved gallery images with ownership, alt text, and moderation status;
- public contact path routed through the product, not raw staff credentials.

Statistics and accreditation never appear without provenance and a review/expiry state.

## Registration and activation state machines

Application: `draft -> submitted -> under_review -> changes_requested | approved | rejected | withdrawn`.

Publication: `private -> approved_unpublished -> published -> suspended | archived`.

Identity access is separate. Email verification proves mailbox control, not professional credentials. An approved application may create or activate the correct membership only through a server-side reviewer action. Hospital applicants cannot self-create an active hospital or assign themselves admin privileges.

### Prototype review projection

The V0 reviewer queue is platform-admin-only. `start_review`, `request_changes`, `approve`, and `reject` are explicit service commands over a row-locked application; the browser never submits reviewer identity or target membership. Request-changes/reject store a bounded private reason and note, while the append-only security event records only action, application type, and reason code.

Approval is one transaction. A synthetic doctor application creates/activates its identity, a dedicated organization, the role-specific membership, and one discoverable synthetic professional card. A synthetic hospital application creates/activates its identity, hospital organization, and hospital-coordinator membership but no doctor card. No approval creates referral assignments, grants, patient access, ratings, connections, or public publication.

Because V0 has no outbound email provider, local `.test` activation records `synthetic_admin_review` as a distinct identity verification basis. This is a labelled rehearsal exception, allowed only for synthetic applications in prototype mode. It must not be reused as evidence of mailbox control or credentials; hashed email-token verification remains a real-launch requirement.

## Registration fields

Shared fields: account path, legal name, preferred display name, work email, password/passphrase, country, timezone, preferred language, terms/privacy acknowledgement versions, and email verification.

Doctor-only fields: professional role, specialty/subspecialties, council jurisdiction and number, qualifications, experience start year, current organization/designation, languages, professional summary, credential evidence, and declarations of truth/authority. Sensitive credential files are future-gated until private object storage, malware scanning, retention, and reviewer access controls exist; V0 captures metadata only.

Hospital-only fields: legal/display name, organization type, website domain, registered address, country/city/timezone, authorized representative/title/work email, specialties/departments, accreditation metadata, establishment year, capacity metadata with dates, services/languages, and authority/truth declarations.

## Security and privacy

- Same-origin session auth and CSRF for state changes.
- Generic registration responses where account enumeration is possible.
- Per-IP and normalized-email throttles, bounded JSON, password validation, breached/common-password rejection, and no secrets in logs.
- Email verification tokens are hashed, single use, purpose-bound, short lived, and invalidated on use or replacement.
- Reviewer actions are platform-admin-only, re-authorized, and audited without credential contents.
- Public queries filter `publication_state=published` and a valid verification state server-side.
- Search engines never index admin routes, pending profiles, private fields, or synthetic lab records.
- Consent/terms versions and timestamps are immutable evidence; marketing consent is separate and optional.

## Demo-data boundary

Only a platform admin can load, inspect in full, or delete the versioned synthetic fixture collection. Eligible synthetic professional accounts may see the bounded doctor cards required to rehearse the network, but cannot access patient fixtures, login metadata, private credential fields, or admin-lab controls. Public provider endpoints never read admin-lab fixture models and never expose synthetic fixtures to anonymous visitors.

## Accessibility and content

All public routes target WCAG 2.2 AA fundamentals: semantic landmarks/headings, keyboard navigation, visible focus, 44px primary targets, labelled errors, error summary, autocomplete attributes, reduced-motion support, responsive zoom, and meaningful image alternatives. Health and economic articles retain reviewed dates, named sources, uncertainty, and no-medical-advice boundaries.
