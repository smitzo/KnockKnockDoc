# Demo Mode and Partner Review — Implementation Checkpoint

## Request

Keep the complete product, blogs, doctor network, hospital pages, and normal authenticated surfaces available in standard mode, but expose no synthetic people, organizations, ratings, connections, messages, referrals, or applications until the administrator selects **Load demo data**. When demo data is enabled, let the administrator inspect broad demo coverage without inheriting participant-only message or case access. Continue building the next planned feature with meaningful conventional commits, then defer verification briefly to maximize implementation.

## Product and architecture decisions

- Persist `standard|demo` in the database instead of treating fixture row existence or a frontend flag as product mode.
- Fail closed to standard mode when the mode row or frontend mode request is unavailable.
- Gate both reads and writes in backend selectors/services. UI hiding is presentation, not the security boundary.
- Keep public information architecture and articles available in both modes; fixture identities and activity are never anonymous public provider content.
- Permit platform admins to preview demo directory cards only. Admin status does not authorize connections, conversation bodies, or referral contents.
- Treat synthetic application approval as a distinct verification basis, never as real mailbox, credential, accreditation, facility, or public-profile verification.
- Minimize the reviewer queue payload; fetch private application evidence only when an admin opens one row.

## Implemented

- Added atomic demo load/enable and standardize/delete lifecycle, public bounded product-mode endpoint, fixture-owned hospital coverage, and server-side gates across admin catalog, network, onboarding, chat, and referrals.
- Added a global demo-mode banner only while enabled, production-copy empty states while standard, read-only admin doctor-network preview, and expanded admin demo coverage metrics.
- Fixed loopback CSRF origin derivation so the local `admin` alias can sign in through the configured frontend port.
- Added private admin application review list/detail endpoints and row-locked start-review, request-changes, approve, and reject services.
- Added bounded reason codes, private reviewer notes excluded from security-event metadata, and atomic doctor/hospital access projection.
- Added `synthetic_fixture`, `synthetic_admin_review`, `email_token`, and `unverified` identity provenance states; unverified identities cannot authorize access.
- Added the light-mode admin review queue and a role-specific hospital coordinator workspace.
- Extended demo deletion to remove synthetic application users, access projections, activity, and activated organizations while preserving the platform administrator.

## Commits

- `ec2dbb1 feat(backend): gate synthetic records behind demo mode`
- `a23f6a9 feat(frontend): switch product experience with demo data mode`
- `41234d9 feat(backend): review and activate partner applications`
- `6222b02 feat(frontend): add partner review and hospital workspaces`
- `fa1f94d refactor(backend): minimize application review queue data`
- `d20bd09 refactor(frontend): load private application detail on demand`

## Evidence completed before the build-only interval

- Focused backend suite: 50 tests passed.
- Frontend lint and TypeScript checks passed before the review feature was added.
- Next.js production build passed before the review feature was added.
- Production dependency audit reported zero vulnerabilities.
- Django production-mode deployment check passed; migration drift was empty at that checkpoint.
- All three active OpenSpec changes validated strictly.
- PostgreSQL, Redis, Django, Celery, and Next.js Compose services rebuilt and became healthy.
- Live standard mode returned no demo doctor or patient rows, kept five public routes available, and displayed the admin **Load demo data** control.
- Live demo activation produced 30 doctors, 30 patients, eight fixture hospitals, and 160 ratings.

## Deferred verification and current local state

At the user's request, verification stopped while the review/activation feature was implemented. The new migrations, endpoints, activation paths, admin queue, and hospital workspace have not yet received their post-change test/build/runtime pass. A smoke harness activated demo data and then stopped on an overly strict server-rendered directory-text assertion before its cleanup step, so the local PostgreSQL database may currently remain in demo mode. The next phase must test the new transition and rollback boundaries, rebuild Compose, complete a browser-origin doctor and hospital approval/login flow, delete demo data, clear test sessions, and only then check the corresponding OpenSpec tasks.

## Remaining real-launch gates

Real email verification, credential/accreditation evidence, MFA and recovery, moderation and appeals, public provider publication, consent enforcement for real referrals, private scanned object storage, audit/incident operations, accessibility assessment, independent security testing, and corridor-specific legal/clinical review remain mandatory stop gates.
