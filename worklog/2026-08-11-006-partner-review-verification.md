# Partner Review and Demo Mode — Verification Checkpoint

## Request

After maximizing implementation work, verify the new product phase, keep normal product content available in standard mode, and ensure synthetic doctors, patients, hospitals, network activity, referrals, and review-created accounts exist only while an administrator has enabled demo data.

## Verified product flow

- Started from standard mode and confirmed the public Home, Insights, Join, Doctors, and Hospitals routes remained available without a demo banner.
- Signed in through the browser-origin API as the local platform administrator and loaded the versioned fixture collection.
- Confirmed the fixture produced 30 fictional doctors, 30 fictional patients, eight fixture hospitals, 32 initial directory profiles, and the documented ratings/network/referral coverage.
- Submitted one synthetic doctor application and one synthetic hospital application.
- Confirmed the administrator queue returned only minimized rows and loaded private application evidence only from the selected detail endpoint.
- Started review and approved both applications.
- Signed in as the approved doctor, confirmed the referrer membership, and confirmed the network returned 32 peer cards while excluding the signed-in doctor's own card.
- Signed in as the approved hospital representative, confirmed the hospital-coordinator membership and hospital workspace, and confirmed `/network` redirected to the role-appropriate hospital route.
- Deleted demo data and confirmed review-created applications, identities, organizations, memberships, directory projections, and authenticated sessions were invalidated.
- Returned the database to standard mode with one persistent administrator and zero synthetic applications, doctors, patients, or directory cards.

## Defect found and corrected

PostgreSQL rejected an application review lock because `SELECT FOR UPDATE` crossed a nullable outer join. The review service now locks only the application and required user rows, then fetches immutable subtype evidence separately. This preserves serialization without relying on a PostgreSQL-invalid nullable join. The focused regression suite passed after the correction in `ccdff8c fix(backend): lock application without nullable joins`.

## Automated evidence

- Backend Django/DRF suite: 58 tests passed across demo mode, identity, onboarding, professional network, and referrals.
- Partner-review tests cover reviewer-only list/detail access, private-field minimization, doctor and hospital projection, duplicate and invalid transitions, rollback, standard-mode hiding, and deletion of review-created access.
- Django system check passed and migration drift check reported no changes.
- Frontend ESLint, TypeScript, and the webpack production build passed. The default local Turbopack command remained blocked by this execution sandbox's internal-port restriction; the rebuilt Compose frontend had already passed the Turbopack build.
- Production dependency audit reported zero runtime vulnerabilities.
- All three active OpenSpec changes passed strict validation.
- PostgreSQL, Redis, Django, Celery, and Next.js were healthy in Compose during the browser-origin flow.

## Clean handoff state

The local database is in `standard` mode. Synthetic fixture and review-created records are absent. All ten stale local smoke-test sessions were removed; the persistent local administrator account remains. The administrator can enable the complete synthetic workspace again from the admin demo page.

## Remaining gates

This is production-shaped prototype code, not approval for real clinical or patient data. Real mailbox verification, credential and accreditation evidence, MFA and recovery, moderation and appeals, patient authorization, private object storage, backup/restore exercises, monitoring and incident response, accessibility assessment, independent security testing, and corridor-specific legal and clinical review remain stop-ship gates.
