# Doctor Catalogue and Long-form Insights

## Request

Improve the short blog articles and make doctor networking useful as a specialist catalogue, using Vaidam's current doctor discovery experience as a reference for cards and search by specialty, experience, and location.

## Reference and product decision

- Reviewed Vaidam's current general doctor search and oncology catalogue on 12 August 2026.
- Adapted the useful interaction patterns: a prominent search area, structured filters, dense specialist cards, visible experience/location/hospital context, progressive detail, and clear actions.
- Did not copy Vaidam content, rankings, appointment promises, patient lead forms, or clinical superlatives.
- Preserved Knock Knock Doc's professional-network boundary: the catalogue remains authenticated and synthetic records remain server-gated behind demo mode. Directory ratings describe fictional peer collaboration, not patient outcomes or clinical quality.

## Implementation

- Added server-side directory filters for specialty, city, minimum experience, and language.
- Expanded keyword search to professional summaries and added recommended, experience, and name sorting.
- Rebuilt the Discover view as an India specialist catalogue with a multi-field filter panel, specialty shortcuts, clearer result counts, richer two-column doctor cards, experience/location highlights, expandable profile context, and the existing purpose-bound connection action.
- Added backend regression tests proving combined specialty, location, experience, language, sorting, and summary search behavior.
- Expanded all five sourced articles from roughly 275-405 words to roughly 1,000-1,250 words each. New content includes decision sequences, comparison fields, red flags, evidence limitations, continuity checks, total-journey economics, visa readiness, and handback measures.

## Validation

- Focused professional-network tests: 12 passed with SQLite.
- Full backend product suite: 60 passed with SQLite.
- Rebuilt Compose backend and frontend images successfully; the Next.js Turbopack production build passed inside the frontend image.
- Focused professional-network suite passed against PostgreSQL in Compose after rebuild.
- Frontend ESLint, TypeScript, and webpack production build passed.
- Expanded article sections were served by the rebuilt local frontend.
- `git diff --check` passed.

## Limitations and next gate

- The directory intentionally shows synthetic professionals only in administrator-controlled demo mode. Publishing real profiles still requires current credential evidence, publication consent, correction and takedown operations, and a public read model that cannot expose private application data.
- Profile detail is progressive within the catalogue card; dedicated public doctor detail routes remain a later production gate.
- Independent mobile, keyboard, screen-reader, and target-doctor usability review remains outstanding.
