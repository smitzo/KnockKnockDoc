## Context

The initial idea combined medical-tourism facilitation, doctor networking, patient case management, hospital CRM, and travel coordination. That scope did not establish why hospitals would pay, why foreign doctors would repeat, or why a new entrant could beat hospital international-patient desks and established facilitators.

The refined design makes one transaction primary: a verified foreign doctor sends a consented, structured referral to an eligible Indian specialist/hospital; the receiving team responds; the patient decides; and the care loop returns to the home doctor. The detailed consent, permission, document, verification, journey, and safety behavior in `docs/FUNCTIONAL_PRODUCT_SPECIFICATION.md` remains a constraint library. The founder-facing product and commercial source of truth is `docs/REFINED_PRODUCT_BUSINESS_SPECIFICATION.md`.

No technical architecture, stack, database schema, or application implementation is selected in this change.

## Goals / Non-Goals

**Goals:**

- Define a commercially credible product that can close the first 10 cross-border referrals.
- Make the verified professional relationship and closed-loop referral—not listings or concierge—the core product.
- Explain repeat value for doctors, patients, specialists, hospitals, and operators.
- Make the Indian hospital the primary buyer through one testable initial offer.
- Bound launch to one evidence-selected country/specialty corridor and two to five hospital partners.
- Separate fundamental software from manual operations and later automation.
- Establish a V0 acceptance scenario, bottom-up economic model, GTM implications, and commercial proof.
- Preserve patient consent, case isolation, attributable clinician authorship, and coordination-only boundaries.

**Non-Goals:**

- Global or all-specialty availability.
- Independent diagnosis, prescribing, prognosis, treatment ranking, or emergency response.
- Public social feeds, followers, endorsements, reviews, or doctor popularity mechanics.
- Full EHR, billing, travel marketplace, insurance, financing, payment custody, or native video.
- Unreviewed referral commissions, doctor kickbacks, hidden patient markups, or paid clinical ranking.
- Broad hospital integration or workflow automation before real cases prove the pattern.

## Decisions

### Decision 1: Optimize for the closed-loop referral

The completed referral loop is the unit of value and primary MVP loop. Profile views, connections, leads, and messages are supporting events, not success.

**Alternative considered:** Build a large verified doctor directory/social network first. Rejected because profiles without a useful transaction have weak retention and no hospital ROI.

### Decision 2: Launch one dense corridor

Launch with one source country, one specialty (a second only if operationally equivalent), 20–100 verified referrers, and two to five Indian hospital facilities. Select it using the weighted evidence scorecard in the refined specification.

**Alternative considered:** Offer global/all-specialty intake and route manually. Rejected because it prevents reliable supply, verification, document requirements, service levels, GTM, and economics.

### Decision 3: Doctors join free; hospitals pay

Foreign and Indian doctors are free professional participants. The first commercial offer is a fixed-fee, bounded hospital corridor pilot combining a recruited/verified referrer cohort, case workflow, managed response SLA, and pilot reporting.

**Alternative considered:** Doctor subscriptions or referral commissions. Rejected initially because density is absent, doctor willingness-to-pay is weak, and referral compensation creates trust and professional-conduct risk.

### Decision 4: Demand plus conversion discipline—not CRM alone—is the hospital value

Qualified incremental referrals rank first in likely hospital willingness-to-pay. Workflow is essential because it improves completeness, response, conversion, source attribution, and relationship retention. A dashboard without demand is insufficient.

**Alternative considered:** Sell generic international-patient CRM SaaS first. Rejected because hospitals already have CRMs, spreadsheets, inboxes, coordinators, and customization capacity.

### Decision 5: Four surfaces share one workflow

The professional network, patient case workspace, hospital CRM, and platform operations console are separate role experiences around the same referral/provider-request lifecycle. The hospital EHR remains the clinical system of record.

### Decision 6: Patient-specific communication is case-bound

Connections support a short request and limited professional exchange. Patient-specific data and clinical collaboration move into a consented case. Open pre-connection chat, bulk hospital outreach, and patient solicitation are excluded.

### Decision 7: Human operations are a product component

V0 software records identity, referral, access, documents, recipients, ownership, response, and outcome. Humans verify, assess completeness, match, chase, normalize, translate, coordinate travel, and manage exceptions. Automation begins only after stable repetition and measurable benefit.

### Decision 8: Commercial proof is part of V0

The product must capture qualified referrals, response intervals, stages, decisions, arrivals, lost reasons, repeat referrers, handback, and operator effort. A pilot that cannot demonstrate hospital value or true service cost has not validated the business.

### Decision 9: Compliance is a release gate, not the product thesis

Patient authorization, isolated provider access, clinician authorship, verification evidence, and audit are fundamental product behavior. Broader jurisdictional conclusions remain professional-review gates and do not justify unrelated feature growth.

## Risks / Trade-offs

- **Hospitals demand guaranteed volume before paying** → Sell a bounded design-partner pilot with named referrer recruitment evidence and explicit learning goals; do not promise volume the platform cannot control.
- **Doctors join but never refer** → Measure verified-to-first-referral and repeat-referral behavior, not registrations; concierge-operate the first eligible case.
- **Hospital response fails** → Contract named owners/capacity/SLA, monitor manually, and remove unavailable supply from discovery.
- **The service remains labour-heavy** → Measure cost per qualified and successful case; cap pilot volume; automate only repeated, stable tasks.
- **Hospital payment compromises neutrality** → Disclose commercial participation; prohibit paid ordering; document human routing rationale; isolate competing providers.
- **A corridor is too narrow for scale** → Prove one corridor's repeatability and unit economics before testing adjacent playbook reuse.
- **A competitor copies the workflow** → Build active referrer relationships, handback reliability, embedded hospital operations, and corridor expertise; accept that UI is not defensible.
- **Professional or privacy rules block workflow/revenue** → Obtain corridor-specific counsel before real data/cases and prefer fixed pilot pricing over commissions initially.
- **Doctors prefer WhatsApp/email** → Make acknowledgement, response, history, and handback materially better while allowing approved notifications and capturing material off-platform events.

## Validation Before Implementation

1. Interview at least 10 relevant foreign doctors in each shortlisted corridor using recent real referral journeys.
2. Interview at least five hospital IPD/business leaders and five service-line/clinical leaders; require named workflow/SLA commitments from two partners.
3. Reconstruct at least five recent patient journeys in each finalist corridor.
4. Run a synthetic referral rehearsal with actual pilot staff through the V0 acceptance scenario.
5. Seek a paid 90–180 day corridor pilot or binding procurement commitment before broad build.
6. Model pricing with real case value, conversion, operator time, hospital contribution, and implementation cost.
7. Complete corridor-specific professional, privacy, commercial, and telemedicine review before the first real case.

## Open Questions

1. Which exact country, referrer segment, specialty, and Indian facilities form the first corridor?
2. Can a hospital pay a fixed pilot price without guaranteed volume, and which budget owner signs?
3. What response SLA will named specialist departments actually commit to?
4. Will foreign doctors submit a real case without referral compensation, and what handback promise drives repeat use?
5. Is the first route exclusive to one hospital per case or routinely multi-provider?
6. Which proposal fields can partner hospitals consistently provide?
7. What event defines a commercially successful case if a later fixed coordination fee is considered?
8. What is the measured operator cost per qualified and successful case?
9. Which corridor-specific legal roles/agreements and data-transfer mechanisms are required?
10. What evidence triggers expansion to the second corridor rather than deeper density in the first?
