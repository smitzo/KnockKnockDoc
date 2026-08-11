# Commit Convention

Every commit in this repository must follow this convention. It is a delivery contract, not a suggestion.

## Required format

```text
<type>(<scope>): <imperative summary>

[optional body]

[optional footer]
```

The first line must be lowercase, use the imperative mood, contain no trailing period, and stay at or below 72 characters.

## Allowed types

| Type | Use for |
|---|---|
| `feat` | A user-visible or API-visible capability |
| `fix` | A defect correction |
| `docs` | Documentation-only behavior or guidance |
| `test` | Test-only additions or corrections |
| `refactor` | Internal restructuring with no intended behavior change |
| `perf` | A measured performance improvement |
| `security` | A security control or vulnerability remediation |
| `build` | Dependencies, packaging, containers, or build tooling |
| `ci` | Continuous-integration configuration |
| `chore` | Narrow repository maintenance that fits no type above |

## Allowed scopes

- `product` — product specifications or feature scope.
- `docs` — system design, engineering guidance, or architecture decisions.
- `backend` — Django, DRF, database, or Celery behavior.
- `frontend` — Next.js, React, UX, accessibility, or browser behavior.
- `infra` — Compose, runtime containers, deployment, or environment configuration.
- `repo` — repository-wide developer tooling or conventions.
- `worklog` — append-only execution records.

Add a new scope only by updating this file in a dedicated `docs(repo)` commit.

## Summary rules

Good summaries complete the sentence: “If applied, this commit will…”

- Start with a verb such as `add`, `build`, `enforce`, `document`, `prevent`, or `refine`.
- Describe one coherent outcome, not a file list.
- Do not use vague subjects such as `changes`, `updates`, `misc`, `work`, `wip`, or `fix stuff`.
- Do not include issue IDs in the summary; put them in the footer.
- Do not mention an AI tool or model as the author of the change.

## Commit boundaries

Each commit must be independently understandable and leave the repository internally consistent for its scope.

- Separate product/design documents, backend behavior, frontend behavior, infrastructure, and tests when each is independently reviewable.
- Keep implementation and the tests required to prove that implementation in the same commit unless the test itself is the feature.
- Keep a migration with the model change that requires it.
- Keep generated dependency lockfiles with the dependency change.
- Do not mix unrelated formatting, cleanup, or documentation rewrites into a feature commit.
- Never commit secrets, credentials, real patient data, build output, editor state, or local databases.
- Use a body when the reason, safety boundary, migration effect, or non-obvious trade-off matters.

## Breaking changes and references

Use standard footers:

```text
BREAKING CHANGE: explain the incompatible behavior and migration path
Refs: KND-123
Fixes: KND-456
```

A breaking change must use both a `!` after type/scope and a `BREAKING CHANGE:` footer:

```text
feat(backend)!: replace the referral status contract
```

## Examples

```text
docs(repo): define the fixed commit convention

feat(backend): add the synthetic referral workspace API

Keep all V0 cases synthetic while authentication and case-level
authorization remain intentionally deferred.

feat(frontend): build the patient referral workspace

security(backend): reject direct identifiers in prototype aliases

build(infra): add the local postgres and redis stack
```

## Before committing

1. Inspect the exact staged diff with `git diff --cached`.
2. Confirm it represents one outcome and contains no secret or real health data.
3. Run the validation appropriate to the touched scope.
4. Check the summary against the type, scope, imperative, lowercase, and length rules.
5. Commit only after the staged diff and test evidence agree.
