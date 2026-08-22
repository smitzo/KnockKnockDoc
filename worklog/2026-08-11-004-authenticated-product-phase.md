# Authenticated Product Phase — Scope and Checkpoint

## Request

Continue beyond Prototype V0 with meaningful convention-compliant commits. Add production-shaped authentication and authorization, a realistic demo dataset with at least 30 fictional doctors and 30 fictional patients, admin-only visibility for that dataset, visual onboarding, and at least five sourced articles related to the product and India medical travel. Keep OpenSpec checkpoints current and maintain documentation throughout.

The request also proposed a hard-coded administrator password of `admin`.

## Decisions

- Preserve Django's already-migrated default user model and extend it with UUID identity profiles, organizations, and memberships.
- Use server-side sessions, HTTP-only cookies, CSRF protection, normalized synthetic email usernames, bounded login throttling, and Django password hashing/validation.
- Require active identity, organization membership, case assignment, current scoped grant, and requested scope for every case read.
- Return `404` for inaccessible case UUIDs and prove Hospital A/Hospital B isolation.
- Reject a committed or hard-coded weak administrator credential. Seed admin and demo accounts only when strong local environment passwords are supplied and never print them.
- Keep every profile and case fictional. Authentication does not lift the prohibition on real personal or health data.
- Keep the admin synthetic lab separate from case participants and access grants; directory presence never grants case access.
- Use original local imagery for editorial onboarding and deterministic fictional visuals for directory profiles. Do not scrape or imply endorsement by real people.
- Treat article sourcing, dates, inference labels, and uncertainty as product requirements.

## Completed at this checkpoint

- Added and committed the phase architecture design.
- Added and committed identity profiles, organizations, memberships, session endpoints, CSRF, throttling, and append-only security events.
- Added and committed case assignments, grants, normalized scopes, server-derived referrer identity, authenticated case APIs, and access-isolation tests.
- Added an OpenSpec change with explicit delivery checkpoints for the expanded phase.

## Current limitations

- The existing frontend has not yet been converted from the V0 role preview to authenticated routes.
- The admin synthetic lab, sourced articles, generated guide assets, and how-to page are pending.
- No claim of production approval is made; the real-data release gates in `docs/PERFORMANCE_AND_SECURITY.md` remain mandatory.

## Next checkpoint

Implement admin-only synthetic catalog models, seed 30 doctor and 30 patient profiles, prove isolation in API tests, then build the authenticated frontend surfaces.
