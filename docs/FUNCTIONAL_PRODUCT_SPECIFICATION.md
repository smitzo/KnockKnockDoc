# Cross-Border Care Referral Network

## Functional Product Specification

> **Background artifact:** This document preserves the detailed functional, consent, workflow, permission, and safety analysis from the first product pass. The active founder-facing thesis and V0 scope are in [`REFINED_PRODUCT_BUSINESS_SPECIFICATION.md`](REFINED_PRODUCT_BUSINESS_SPECIFICATION.md).

**Document status:** Pre-build discovery specification
**Version:** 1.0
**Date:** 11 August 2026
**Initial market assumption:** International patients considering planned treatment in India; exact source country and clinical wedge are deliberately unresolved.
**Product posture:** Coordination infrastructure, not a healthcare provider, diagnosing system, emergency service, insurer, immigration authority, or guarantor.

> **Professional-review boundary:** This document defines intended product behavior, not legal or clinical conclusions. Before handling real patient data or referrals, qualified counsel and healthcare-compliance professionals must review every launch jurisdiction, the platform's legal role, privacy notices and agreements, cross-border transfers, consent, telemedicine, clinician licensure, advertising, referral economics, visa assistance, record retention, and incident response.

## Executive challenge: reasons not to build the assumed product

The broad idea is attractive but not yet a product thesis. The following assumptions must be challenged:

1. **Concierge is not differentiation.** Large Indian hospital groups already offer remote opinions, invitation letters, accommodation, interpretation, airport assistance, admission coordination, and follow-up. Existing facilitators already offer provider comparison. A new entrant cannot win by reproducing those claims.
2. **“Verified” is a process, not a badge.** India's public doctor register itself warns that parts of its data are being updated. A safe product needs evidence sources, verification dates, scope, expiry, sanctions checks, and recurring review—not a permanent green tick.
3. **The foreign-doctor network is the highest-value and least-proven element.** Referring doctors may improve trust, record quality, and continuity, but may see no benefit, face liability or licensure uncertainty, fear losing the patient, or be unable to accept referral compensation. Their participation must be validated without assuming commissions.
4. **The paying customer can compromise neutrality.** If hospitals fund the platform, routing and comparison may favor commercial yield over patient fit. This conflict must be structurally disclosed and governed.
5. **A preliminary quote is not the price of treatment.** Clinical findings after arrival can change the procedure, length of stay, consumables, complications, and total bill. Showing one number as “the price” creates dangerous expectations.
6. **This is an operations business before it is a software business.** The first ten cases require trained case managers, hospital relationships, document chasing, escalation, and judgment. Automation cannot substitute for missing trust or weak operating agreements.
7. **More supply is not automatically better.** A directory of hundreds of providers worsens choice and verification. The launch should use two or three contracted hospitals, a small verified specialist set, one or two source-country corridors, and two or three planned-care pathways.
8. **Cross-border scope multiplies obligations.** Patient nationality, residence, referring-doctor country, hospital location, hosting, communications, and payment flows may each trigger different rules.
9. **Urgent cases are not good MVP cases.** The platform is not capable of emergency assessment or transport. It must redirect emergencies to local services and only coordinate stable, planned cases.
10. **Hospital CRM and patient marketplace are different businesses.** Selling enterprise workflow software and acquiring individual patients have different buyers, economics, cycles, and product demands. The MVP can use a shared workflow, but the founders must select the primary commercial motion.

**Recommended launch thesis:** Prove a managed referral service for a narrow country–specialty corridor, using a lightweight shared case workspace and two to three hospital design partners. The product succeeds only if it produces faster, more complete, more transparent clinical responses and preserves continuity with the patient's home clinician.

### Current external constraints informing this specification

- The [National Medical Commission's Indian Medical Register](https://www.nmc.org.in/information-desk/indian-medical-register/) supports searches by name, registration number, and state council, but notes incomplete/outdated coverage; verification therefore needs primary-source and hospital checks, not a one-time database match.
- [NABH operates an empanelment programme for Medical Value Travel Facilitators](https://nabh.co/programmes/medical-value-travel-facilitator-mvtf-empanelment-programme/) covering ethical, transparent, patient-centred coordination. The founders should assess eligibility and treat its current standard as an operating-design input.
- The official [Indian e-Visa portal](https://www.indianvisaonline.gov.in/evisa/) requires an Indian-hospital letter for e-Medical applications and publishes conditions that can vary by visa subtype, nationality, and current rules. The product must track documents and official status; it must not promise eligibility or approval.
- India's [Digital Personal Data Protection Rules, 2025](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa?hl=en-US) have phased commencement. Build to strong notice, purpose limitation, security, rights, and incident-response standards from day one rather than waiting for a particular enforcement date.
- The NMC-published [Code of Medical Ethics](https://www.nmc.org.in/rules-regulations/code-of-medical-ethics-regulations-2002/) prohibits physician commissions for procuring or referring patients. Counsel must confirm the operative framework and its application to every proposed fee, party, and jurisdiction before launch.
- For patients in jurisdictions such as the EEA, health data and transfers to India can trigger additional duties; the [European Commission's cross-border transfer guidance](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/obligations/what-rules-apply-if-my-organisation-transfers-data-outside-eu_en) illustrates why launch-country selection must precede legal design.

---

# 1. BUSINESS DEFINITION

## Exact problem

People considering planned treatment in India—and the clinicians and hospital teams helping them—cannot reliably move from “I need another treatment option” to a clinically reviewed, comprehensible, coordinated plan. Case data arrives incomplete through unsafe channels; hospitals duplicate intake; responsibility is unclear; preliminary opinions and quotations are inconsistent; patients cannot distinguish clinical differences from sales claims; referring clinicians disappear from the loop; and travel, admission, discharge, and follow-up are managed in disconnected conversations.

The product solves **trusted case coordination and continuity**, not provider discovery alone.

## Who experiences it

- International patients and family members making a high-stakes decision in an unfamiliar health system.
- Referring doctors who need an accountable handoff and appropriate post-treatment information.
- Indian specialists who receive poorly structured cases without consent or sufficient records.
- Hospital international-patient departments that manage leads across inboxes, chat, spreadsheets, and internal systems.
- Hospital coordinators responsible for response time and arrival readiness but lacking shared status.
- Platform case managers who must reconcile participants, documents, and promises.
- Carefully bounded travel, accommodation, transport, and interpreter partners.

## Why the current process is painful

- Patients do not know whether a provider, intermediary, quote, or testimonial is genuine.
- Reports are scattered, repeated, mislabeled, low quality, translated inconsistently, or sent to unintended recipients.
- The same case must be explained repeatedly, losing clinical context.
- Hospital “lead” workflows prioritize conversion but do not necessarily preserve patient consent or local-doctor continuity.
- Response ownership and deadlines are unclear.
- Proposals mix clinical recommendations with commercial packages, making comparison unsafe.
- Indicative estimates are mistaken for final bills.
- Visa, travel, and hospital readiness depend on one another but are tracked separately.
- Discharge summaries and follow-up instructions often do not reach the clinician who will care for the patient at home.
- Informal referral economics can create real or perceived conflicts of interest.

## How it is handled without the product

Patients typically use search, personal networks, brokers/facilitators, social media, embassy or diaspora contacts, or direct hospital inquiry forms. Reports and passport copies move through email or messaging. Hospital international desks manually forward cases to clinicians, build estimates, issue invitation letters, and coordinate travel. Referring doctors may give a name or letter but usually cannot see a structured downstream timeline. Families maintain the real source of truth in chat threads, folders, and spreadsheets.

This process can work, especially with a strong hospital coordinator. The platform must therefore demonstrate measurably better completeness, response accountability, consent evidence, cross-provider comparison, and continuity—not merely digitize a form.

## Value proposition by participant

| Participant | Value offered |
|---|---|
| Patient/family | One accountable case, verified counterparties, understandable options and uncertainty, fewer repeated submissions, coordinated next steps, and portable records. |
| Referring doctor | A consented structured referral, direct clarification channel, visible handoff status, and permitted return of opinion/discharge/follow-up documents. |
| Indian specialist | Clinically organized records, clear question, consent evidence, fewer irrelevant cases, bounded responsibility, and a documented response workflow. |
| Hospital/IPD | Qualified and complete cases, assignment and SLA control, standardized proposals/quotes, conversion/loss visibility, referral-source attribution, and fewer inbox handoffs. |
| Hospital coordinator | One task and communication timeline spanning documents, doctor review, quotation, visa letter, travel, admission, and follow-up. |
| Platform operator | A defensible coordination network and operational dataset built around service quality—not undisclosed lead resale. |
| Travel/concierge partner | Only the minimum confirmed logistics request needed to deliver an opted-in service, with clear ownership and no medical-record access. |

## Why use the platform instead of contacting one hospital directly?

Use the platform only when it provides at least one of these advantages:

- The patient wants a small, clinically appropriate multi-hospital review without resubmitting the case.
- A home doctor wants a documented clinician-to-clinician handoff and return path.
- The case needs independent coordination across hospital and non-hospital steps.
- The patient values a disclosed, normalized view of proposal assumptions, ranges, inclusions, exclusions, and response provenance.
- A hospital wants structured demand intake and international case operations that its general CRM does not provide.

If a patient already trusts one hospital and that hospital offers effective end-to-end coordination, direct contact may be simpler. The product should say so rather than manufacture intermediary value.

## What this product must explicitly not become

- A diagnostic, prescribing, triage, or clinical decision-making system.
- A substitute for the patient's treating or emergency clinician.
- A pay-to-rank hospital directory, lead auction, or undisclosed referral-commission network.
- A source of guaranteed outcomes, guaranteed prices, guaranteed visas, or “best doctor” claims.
- A general travel agency, flight/hotel inventory engine, insurer, lender, or payment custodian in the MVP.
- A public repository of patient cases or medical records.
- A place where unverified people can present themselves as clinicians.
- An open chat service that bypasses consent, hospital governance, or documentation.
- A global, all-specialty marketplace at launch.

## Product definition

**One sentence:** A consent-led cross-border referral and case-coordination network connecting international patients and their doctors with verified Indian hospital teams for planned treatment review, transparent proposals, travel readiness, and continuity of care.

**One paragraph:** The product provides a shared, auditable case workspace in which a patient or verified referring doctor submits structured history and records; trained platform staff validate completeness and route the case to a small number of authorized hospital teams; licensed Indian clinicians issue attributable opinions through their hospitals; hospitals provide versioned, assumption-based treatment proposals and cost ranges; and coordinators manage selection, visa-document readiness, appointments, arrival, admission, discharge, and permitted follow-up. It coordinates information and responsibility while clinical decisions remain with licensed professionals and official decisions remain with hospitals and authorities.

**Detailed description:** The platform combines three linked functions: (1) a patient/referrer intake and consent workspace; (2) an international-patient CRM used by hospital coordinators and clinical reviewers; and (3) a platform operations console for verification, completeness review, human-assisted matching, SLA monitoring, safeguarding, and escalations. Each patient case is distinct from each hospital review request so multiple hospitals can respond without seeing one another or receiving unshared data. Clinical opinions, commercial proposals, and logistics services are separated by authorship and scope. Every sensitive access and material change is attributable. The MVP deliberately relies on human case managers for specialty confirmation, sharing decisions, document-quality review, proposal normalization, visa checklists, and exceptions.

---

# 2. USER TYPES / ACTORS

| Actor | Goal and pain points | Platform needs and allowed actions | May see / must not see | Incentive |
|---|---|---|---|---|
| **International patient** | Obtain credible options and coordinate care; faces anxiety, information asymmetry, language, cost uncertainty, and unsafe sharing. | Register; create/authorize a case; upload records; invite family/referrer; set preferences; grant/revoke sharing; answer requests; view attributable proposals; select/withdraw; track steps; request support; access export. | Own case and access history, explicitly shared responses, logistics, and financial estimates. Must not see internal provider notes, other patients, hidden commercial scoring, or unrelated hospital data. | Fewer handoffs, better transparency, continuity, and one accountable coordinator. |
| **Patient attendant/family member** | Help a sick or less digitally capable patient; lacks authority clarity and shared status. | Accept an invitation; verify identity; act only within delegated scope; upload, message, schedule, or coordinate; acknowledge they are not the patient. | Only scopes granted by patient/guardian. Must not independently alter consent, select treatment, or see restricted documents unless explicitly authorized. | Practical ability to manage work without impersonating the patient. |
| **International/referring doctor** | Make a safe referral, ask a clinical question, retain continuity, and receive permitted downstream records; fears liability, lost time, and patient poaching. | Register; submit credential evidence; create/refine referral; capture or request patient consent; upload and classify records; communicate with assigned Indian clinicians; view shared opinions/status; upload home-country follow-up; close handoff. | Referred/invited cases and patient-authorized documents only. Must not see unrelated proposals, logistics, payment details, family communications, or cases. | Better specialist access and handoff quality, time saved, clinical collaboration, patient trust—without referral payment. |
| **Indian specialist** | Review relevant, complete cases and give bounded advice; receives poor records and sales pressure. | Verify identity/license/hospital relationship; state specialties/languages/availability; accept/decline review; request data; consult where permitted; author/sign opinion; outline pathway and uncertainties; participate in follow-up. | Only hospital-assigned, currently authorized cases and relevant records. Must not see competitor responses, patient acquisition economics, unrelated logistics, or broader hospital pipeline unless separately permitted. | Better case quality, less coordination overhead, international collaboration, attributable professional work. |
| **Indian hospital/IPD manager** | Convert appropriate international demand and coordinate delivery; struggles with fragmented leads and accountability. | Onboard organization; manage staff roles; accept/decline review request; assign coordinator/specialist; set SLAs; create proposals/quotes; issue documents; manage pipeline; record payment status; analyze source/conversion/loss. | Cases explicitly shared with its hospital, its own users' activity, and aggregated internal metrics. Must not see competitor proposals, unshared cases, or patient marketing data without permission. | Qualified demand plus an international-case operating system and measurable service levels. |
| **Hospital case coordinator** | Move each accepted case to the next safe step. | Review intake; request documents; schedule review/consultation; compile proposal; coordinate invitation, arrival, admission, discharge, and follow-up; maintain tasks and notes. | Assigned hospital cases; minimum necessary clinical and logistics data. Must not browse all cases by default or modify clinician-authored opinion. | Clear ownership, fewer lost handoffs, repeatable checklists, SLA evidence. |
| **Hospital finance user** | Issue and reconcile estimates, deposits, invoices, refunds, and balances. | Create/version commercial quote; mark payment status from hospital records; reconcile estimate versus actual; answer billing questions. | Financial and minimal identity/case context. Must not see unrestricted clinical records or private doctor conversations. | Fewer quote errors and clearer payment expectations. |
| **Platform case manager** | Make an incomplete, uncertain cross-border case operationally ready and keep it moving. | Verify patient contact; review completeness; communicate; classify administratively; propose routing; manage consent grants; normalize non-clinical proposal fields; coordinate next steps; log escalations. | Assigned cases and minimum necessary records. Must not issue clinical opinions, alter clinician content, promise price/outcome/visa, or access cases outside assignment except controlled escalation. | Ability to deliver a safe, measurable managed service. |
| **Platform verifier/compliance admin** | Ensure counterparties and evidence remain trustworthy. | Review identity/licence/accreditation/legal entity evidence; approve, reject, suspend, reverify; manage incidents, conflicts, audits, and access reviews. | Verification evidence and case data only when necessary for an investigation. Must not use health data for sales. | Reduced fraud, defensible trust claims, and safer network. |
| **Platform operations/admin** | Maintain service health, organizations, workflows, and support. | Configure specialties/statuses/SLAs; manage memberships; handle duplicates, routing, support, complaints, and partner access; report aggregate metrics. | Role-scoped operational data. No unrestricted clinical access merely because the user is an admin. | Consistent operations and accountability. |
| **Travel/concierge partner** | Deliver a confirmed, bounded service. | Accept/decline a service request; view itinerary/logistics; update fulfillment; message coordinator. | Name/contact, party size, language, accessibility, schedule, and pickup/accommodation needs after explicit consent. Must not see diagnosis, reports, proposals, passport copy unless strictly necessary and separately authorized. | Qualified bookings with clear requirements and payment terms. |
| **Interpreter** | Enable accurate communication. | Accept a session; see language, time, participants, and only session materials explicitly shared; attest confidentiality; record completion. | Minimum session content. No general case or document access; clinical interpretation requires appropriately qualified personnel. | Scheduled, scoped work and clear confidentiality expectations. |
| **Support/safety responder** | Handle urgent operational or safety reports. | Receive incident; contact appropriate human; freeze access if authorized; record actions and handoff. | Incident-specific minimum data. Must not provide medical emergency advice beyond directing the user to local emergency services. | Fast, accountable escalation. |

---

# 3. END-TO-END PATIENT JOURNEY

## State model

A single patient case may be shared with multiple hospitals. Therefore the system must keep two related lifecycles:

1. **Overall case lifecycle:** `DRAFT → SUBMITTED → TRIAGE → INFORMATION REQUIRED ↔ READY FOR ROUTING → OPTIONS IN REVIEW → OPTIONS READY → PATIENT DECIDING → PROCEEDING → PRE-TRAVEL → TRAVEL CONFIRMED → IN INDIA → IN CARE → DISCHARGED → FOLLOW-UP → CLOSED`.
2. **Per-hospital review lifecycle:** `NOT SHARED → INVITED → ACCEPTED FOR REVIEW | DECLINED → INFORMATION REQUESTED ↔ UNDER REVIEW → OPINION READY → PROPOSAL/QUOTE READY → SENT → SELECTED | NOT SELECTED | WITHDRAWN | EXPIRED`.

Overall terminal outcomes are separate from progress states: `CANCELLED_BY_PATIENT`, `NOT_CLINICALLY_SUITABLE`, `NO_PROVIDER_AVAILABLE`, `UNRESPONSIVE`, `VISA_NOT_OBTAINED`, `TRANSFERRED_OUT`, and `DECEASED`. A reason, actor, timestamp, and permitted next action are mandatory. Status changes never erase history.

## Stage-by-stage journey

| Stage | INPUT | SYSTEM ACTION | HUMAN ACTION | OUTPUT | NEXT STATE |
|---|---|---|---|---|---|
| 1. Need recognized | Patient/referrer describes planned treatment need and current location. | Shows scope, emergency warning, privacy summary, eligibility boundaries, and assisted route. | Patient/referrer confirms this is not a local emergency; case manager answers non-clinical questions. | In-scope intent or safe redirect. | `DRAFT` or `OUT_OF_SCOPE`. |
| 2. Account/contact | Email/phone, country, preferred language, role. | Verifies contact; creates user and resumable draft; prevents silent patient impersonation. | User proves control of channel and declares role. | Authenticated participant. | `DRAFT`. |
| 3. Case submission | Patient demographics, location, care question, known condition, symptoms/history as reported, urgency, preferences. | Validates required fields, labels patient-reported information, generates case reference. | Patient/referrer enters facts; case manager may assist without interpreting clinically. | Structured draft case. | `DRAFT_READY`. |
| 4. Report upload | PDF/images and report metadata. | Malware/scanning checks, file validation, category/date capture, timeline, upload receipt. | User classifies files; case manager corrects metadata without changing content. | Versioned medical-record set. | `DRAFT_READY` or `INFORMATION_REQUIRED`. |
| 5. Identity/contact | Patient identity, age/capacity, guardian/delegate if relevant; passport only when justified. | Separates account identity, patient identity, and travel identity; flags mismatch. | Case manager manually resolves mismatches; guardian evidence reviewed. | Verified or risk-accepted identity state. | `CONSENT_REQUIRED`. |
| 6. Consent | Plain-language purposes, recipients/classes, document scopes, duration, withdrawal method, referrer/delegate permissions. | Records version, timestamp, actor, scope, locale, evidence, and separate optional consents. | Patient/authorized representative provides informed consent; staff resolves capacity/language concerns. | Active consent grants. | `SUBMITTED`. |
| 7. Case review | Submitted case and records. | Creates completeness checklist and triage task; detects obvious duplicates; no automated diagnosis. | Trained case manager verifies readability, chronology, contactability, scope, and red flags; escalates clinical questions. | Completeness decision and missing-items list. | `TRIAGE`, then `INFORMATION_REQUIRED` or `READY_FOR_ROUTING`. |
| 8. Specialty classification | Stated diagnosis/question and available records. | Suggests controlled specialty/treatment taxonomy based on declared data only; logs provenance. | Qualified human confirms administrative route; clinician decides if ambiguous/high-risk. | One primary and optional secondary specialty plus routing rationale. | `READY_FOR_ROUTING`. |
| 9. Matching shortlist | Specialty, procedure, hospital capability, accreditation evidence, location, language, budget, urgency, availability, preferences. | Applies eligibility filters and creates an explainable candidate shortlist; excludes suspended/unverified providers. | Case manager confirms fit and conflict disclosures; patient approves recipients if consent is named-recipient based. | Approved shortlist, usually one to three hospitals. | `READY_FOR_ROUTING`. |
| 10. Request opinions | Authorized record subset, clinical question, response deadline. | Creates separate provider review request and case-access grant per hospital; notifies coordinator. | Hospital accepts/declines; assigns specialist and coordinator. | Review accepted with owner/SLA, or attributed decline. | Overall `OPTIONS_IN_REVIEW`; provider `ACCEPTED_FOR_REVIEW`/`DECLINED`. |
| 11. Additional information | Hospital/doctor question or required test. | Routes structured request to authorized submitter; tracks due date; prevents unapproved widening of access. | Doctor authors clinical request; patient/referrer supplies available material or explains absence. | Answered request or documented limitation. | Provider `INFORMATION_REQUESTED ↔ UNDER_REVIEW`. |
| 12. Medical opinion | Adequate records and clinical question. | Provides signed response structure and preserves immutable issued version. | Licensed clinician authors opinion, limitations, alternatives, additional tests, urgency advice, and consultation need. | Attributable preliminary opinion; not a final diagnosis or treatment guarantee. | Provider `OPINION_READY`. |
| 13. Treatment proposal | Clinician opinion plus hospital operational inputs. | Separates clinical pathway from commercial/logistics components and records authors. | Clinician approves clinical elements; hospital coordinator completes stay/timing; finance creates estimate. | Versioned hospital proposal. | Provider `PROPOSAL_READY`. |
| 14. Approximate cost | Proposed pathway, assumptions, currency, inclusions/exclusions, validity. | Requires range/estimate label, version, expiry, and change explanation; performs arithmetic/completeness checks only. | Hospital finance authorizes quote; case manager queries omissions but cannot edit hospital numbers. | Attributable indicative quotation. | Provider `SENT`; overall `OPTIONS_READY` when minimum response set is ready. |
| 15. Remote consultation | Doctor requests it or patient seeks clarification; permissions and scheduling inputs. | Confirms participants, consent, permitted jurisdictional mode, fee/status, and record of occurrence. | Hospital/doctor confirms legal/clinical suitability; patient attends; interpreter joins if authorized. | Consultation note or clarification, authored by clinician. | Remains `OPTIONS_READY` or returns to proposal revision. |
| 16. Option comparison | Two or more issued proposals or one proposal plus direct-care alternative. | Normalizes comparable fields; shows missing data, assumptions, conflicts, source, dates, and differences without ranking clinical quality. | Case manager explains navigation and uncertainties, not what treatment to choose; patient consults own doctor. | Patient-understandable comparison and questions list. | `PATIENT_DECIDING`. |
| 17. Selection | Patient decision, acknowledgment of provisional nature and conflicts. | Records selection and closes/non-selects other provider tracks without exposing competitors. | Patient/authorized representative selects, defers, or withdraws; hospital confirms capacity. | Selected hospital and confirmed next-step owner. | `PROCEEDING`. |
| 18. Case acceptance | Current records, selected proposal, expected timing, deposit rules. | Requests explicit hospital acceptance and tracks conditions. | Hospital verifies specialist/facility availability and accepts conditionally or finally. | Acceptance record with conditions and expiry. | `PRE_TRAVEL` or back to `PATIENT_DECIDING`. |
| 19. Visa/invitation | Passport data only when required, hospital acceptance, tentative admission/treatment date. | Produces checklist and securely transfers necessary fields to hospital; records letter status; links only to official application/status resources. | Hospital issues invitation on its letterhead; patient applies; case manager tracks self-reported status and exceptions. | Invitation document and visa status, never a guarantee. | `VISA_IN_PROGRESS` substate within `PRE_TRAVEL`. |
| 20. Travel planning | Visa result, clinical fitness instructions from hospital, preferred dates, attendant/accessibility needs. | Tracks dependencies, consented partner requests, and contingency contacts. | Patient books travel or explicitly requests partner help; hospital confirms arrival window; coordinator checks readiness. | Confirmed itinerary/readiness checklist. | `TRAVEL_CONFIRMED`. |
| 21. Appointment scheduling | Arrival plan, hospital capacity, required pre-assessment. | Records time, location, participants, change policy, reminders, and timezone. | Hospital confirms; patient acknowledges; coordinator resolves changes. | Confirmed appointment/admission plan. | `TRAVEL_CONFIRMED`. |
| 22. Arrival in India | Flight/arrival status and opted-in assistance. | Sends minimum logistics details to assigned provider; opens arrival support checklist. | Driver/interpreter/hospital desk confirms handoffs; patient reports arrival. | Arrival confirmation and exception log. | `IN_INDIA`. |
| 23. Hospital admission | Identity, visa/passport as hospital requires, appointment, deposit/authorization. | Records milestone and hospital reference; does not replace hospital registration/EHR. | Hospital admits and performs in-person assessment; coordinator reconciles discrepancies. | Admission confirmed or reason for delay/refusal. | `IN_CARE` or escalation. |
| 24. Treatment | Hospital clinical process and material pathway changes. | Tracks high-level milestones and new proposal/estimate versions; never directs care. | Treating team obtains its clinical consents and treats; hospital communicates material changes; patient decides with clinicians. | Current high-level status and documented changes. | `IN_CARE`. |
| 25. Discharge | Hospital discharge decision and documents. | Checks expected document set, permitted recipients, translations requested, outstanding follow-up tasks. | Hospital issues signed discharge summary, medication/instruction documents, final bill; patient acknowledges receipt. | Discharge pack and follow-up plan. | `DISCHARGED`. |
| 26. Return home | Fit-to-travel advice from hospital, itinerary, local support. | Tracks safe-handoff checklist and timezone-adjusted follow-up. | Hospital supplies advice; patient travels; case manager confirms return; local doctor is notified if permitted. | Return confirmation and continuity handoff. | `FOLLOW_UP`. |
| 27. Follow-up | Symptoms/questions, planned review date, local results, clinician availability. | Routes communications to the correct clinician; tracks response SLA and unresolved safety issue. | Patient/local doctor provides updates; Indian clinician/hospital responds within agreed scope or directs local assessment. | Follow-up note, next action, and closure criteria. | `FOLLOW_UP` or escalation/readmission track. |
| 28. Close | Completed tasks, documents, balances/status, unresolved complaint, consent/retention state. | Creates closure summary, exports permitted record, schedules retention/reverification actions, captures outcome reason. | Case manager confirms handoff; patient and referrer review accessible documents. | Closed case with auditable outcome. | `CLOSED`. |

## Manual operations that remain mandatory in the MVP

- Eligibility and emergency-screen review.
- Patient identity/authority exceptions, minor/capacity review, and consent-language assistance.
- Medical-record readability, chronology, missing-document identification, and translation quality check.
- Specialty confirmation and every provider-routing decision.
- Provider, doctor, hospital, and partner verification against authoritative sources.
- Hospital acceptance chasing, SLA escalation, and response-quality completeness review.
- Proposal normalization and discrepancy flagging without altering clinical or financial content.
- Visa checklist interpretation and official-source confirmation; no immigration advice guarantee.
- Travel, admission, discharge, and adverse-event escalation.
- Complaints, suspected fraud, access incidents, consent revocation, deletion/retention requests, and patient death.

---

# 4. REFERRING DOCTOR WORKFLOW

## Workflow

1. **Create account:** Doctor supplies professional name, country/jurisdiction, work contact, organization, primary specialty, preferred language, and secure authentication. Consumer social login alone is insufficient for a professional role.
2. **Verify credentials:** Platform collects regulator, registration/licence number, registered name, jurisdiction, specialty evidence where relevant, expiry/renewal status, practice address, and identity evidence. A verifier checks the applicable primary regulator and records source, result, date, scope, limitations, and recheck date. Until approval, the user can prepare but cannot present as a verified doctor or access a patient case.
3. **Create or join a referral:** The doctor either creates a referral for a named patient or accepts a patient invitation. The platform distinguishes the doctor's statement from confirmed diagnosis and identifies whether the doctor is current treating clinician, prior clinician, or adviser.
4. **Obtain patient consent:** Prefer patient self-consent through a direct link. If local practice permits clinician-mediated consent, preserve the notice version and evidence, but require patient confirmation before sharing beyond intake unless counsel approves a documented exception. Consent to care coordination, provider sharing, referrer access, consultation, and return records are separate.
5. **Describe the case:** Use a structured referral including presenting problem, relevant history, diagnoses as documented, treatments tried, current medication/allergies, functional status, infection/precaution information if appropriate, clinical question, desired specialty, urgency rationale, and what the patient expects. Free text supplements rather than replaces the structure.
6. **Upload and organize reports:** Upload documents with category, author/facility, date, language, and relevance. The doctor can mark superseded/incorrect material but not silently replace it.
7. **Specify specialist need:** Doctor selects a controlled specialty/treatment area and clinical question. Platform/hospital clinicians can correct routing with reason; the software does not infer a diagnosis.
8. **Track completeness and routing:** Doctor sees whether the case needs information, is under review, has a response, or is paused—subject to patient permission. Commercial lead scoring and other hospitals' internal notes remain hidden.
9. **Collaborate:** Within a case-bound professional conversation, the Indian clinician can ask clarifying questions. Each message shows professional identity, organization, timestamps, and whether the patient can see it. A private clinician-to-clinician channel is allowed only with patient authorization and a policy describing what becomes part of the record.
10. **Receive opinions:** The referring doctor receives clinician-authored documents when the patient has allowed it. The platform shows limitations and makes clear which Indian clinician and hospital issued the opinion.
11. **Follow the journey:** The doctor sees clinically relevant high-level milestones—not flight details, prices, family chat, or payment information—unless separately authorized.
12. **Receive discharge/follow-up:** Hospital shares the signed discharge summary, medication list, procedure report, results, and follow-up plan within the patient's consent. The referrer can acknowledge handoff, upload local follow-up results, and ask bounded questions.
13. **Close or withdraw:** The patient can revoke future referrer access. The doctor can end involvement, but authored referral content and prior accesses remain in audit/medical history subject to lawful retention.

## Why a foreign doctor might actually use it

The workflow is valuable only if it:

- saves time compared with personal email chasing;
- delivers reliable specialist responses within a known SLA;
- preserves the doctor's relationship and explicitly returns care to them;
- reduces incomplete-record loops with a reusable referral packet;
- provides transparent identity, authorship, and acknowledgement;
- allows questions to be answered by a named specialist rather than a sales representative;
- provides discharge/follow-up information in a useful, timely format;
- charges no referral participation fee and offers no patient-procurement commission;
- states professional responsibility boundaries and does not imply the foreign doctor endorsed a commercial provider merely by referring.

**Validation test:** Give foreign doctors a concierge-operated prototype using synthetic cases, then ask them to refer one eligible real patient under reviewed consent and contracting. Expressions of interest are insufficient; repeated completed referrals are the evidence.

---

# 5. PATIENT WORKFLOW

## Patient capabilities

- **Registration:** Create an account using verified contact details, select language/timezone, and invite a trusted family member without sharing credentials.
- **Assisted submission:** Save a draft, use plain-language prompts, request a call, or let a case manager transcribe information with patient confirmation and an audit mark.
- **Medical records:** Upload multiple files, label them, view a date-based timeline, correct metadata, mark a document disputed/superseded, and answer missing-record requests.
- **Treatment request:** State the question in the patient's own words, existing clinician diagnosis, previous treatment, desired consultation/treatment, and time constraints.
- **Preferences:** Record preferred city/hospital/doctor if any, budget range, language, accessibility, attendant count, accommodation needs, and willingness to consider alternatives. Preferences are not clinical routing decisions.
- **Consent and sharing:** See who has access, why, to which documents, until when; approve new hospital recipients; revoke future access; request an access report.
- **Communication:** Message the assigned case manager and authorized hospital team. Clinical questions are clearly routed to clinicians; case managers cannot answer them as medical advice.
- **Appointments:** Request or confirm consultations and hospital appointments, see timezone/local time, participants, preparation, fees, and change status.
- **Proposal and quote visibility:** View versioned clinical pathway, assumptions, cost range, currency, inclusions/exclusions, additional tests, likely stay, validity date, and responsible authors.
- **Comparison:** Compare normalized factual fields and unresolved questions. No “cheapest,” “best,” success-rate leaderboard, paid placement, or algorithmic treatment recommendation.
- **Decision:** Select, defer, decline, or seek more clarification. A selection is not consent to treatment; hospital clinical consent happens separately.
- **Visa documents:** See required checklist, safely submit required passport details, receive the hospital invitation, record official application reference/status, and access official links. The platform never marks a visa “approved” without patient-provided or official evidence.
- **Travel coordination:** Record itinerary and needs; opt into specific accommodation, transport, or interpreter sharing; view confirmed provider and emergency contact. The platform distinguishes recommendations from booked/confirmed services.
- **Timeline:** See the next action, owner, due date, and high-level journey milestones.
- **Payment visibility:** In MVP, view hospital-stated estimate, deposit request, and manually reconciled status. Payments go to the contracted recipient outside platform custody; bank-detail changes trigger verification warnings.
- **Support:** Access 24/7 emergency direction to local emergency services plus separately stated platform support hours, hospital contacts, and escalation channels. Never imply clinical emergency coverage.
- **Discharge and follow-up:** Download the hospital-authored discharge pack, choose permitted recipients, see follow-up schedule, upload local results, and request clarification.
- **Rights:** Export accessible case data, correct patient-entered data, request restriction/deletion, and receive a reason where legal/clinical retention prevents deletion.

## Required safety language

At submission, proposal, consultation, and follow-up, the interface must state in context that:

- patient-entered information is not a platform diagnosis;
- only an identified licensed clinician/hospital authors medical opinions;
- remote review may be limited and the plan/cost can change after examination and testing;
- provider verification confirms checked evidence as of a date, not quality or outcome;
- the platform does not guarantee treatment suitability, results, availability, price, or visa approval;
- emergencies require immediate local emergency care, not platform messaging.

---

# 6. INDIAN DOCTOR WORKFLOW

## Onboarding and professional profile

- Provide legal/professional name, identity, NMC/state council registration details, qualifications, specialty/subspecialty, languages, hospital affiliations, and professional contact.
- Platform verifies the registration against NMC and the relevant state council where possible, checks current sanctions/blacklist sources, and obtains hospital confirmation of active affiliation and privileges. Any ambiguity requires manual evidence and blocks clinical review access.
- The visible profile must distinguish verified facts, hospital-supplied facts, self-declared information, source, verification date, and expiry/recheck date.
- Experience may be stated as verifiable years, roles, qualifications, and selected areas of practice. Unverifiable superlatives, outcome promises, popularity rankings, and patient-procurement claims are prohibited.
- Doctor availability is a review-capacity signal, not a patient appointment guarantee. The hospital controls appointment and facility availability.

## Incoming case workflow

1. A hospital coordinator accepts a provider review request and assigns an eligible specialist.
2. The specialist sees a minimum case summary before accepting; health-record access begins only after assignment and an active case grant.
3. The specialist accepts, declines with a categorized reason, or asks the coordinator to reroute. Declining does not expose the patient to punitive loss of other options.
4. The doctor reviews authorized information, sees provenance and translations, and flags unreadable, inconsistent, or missing material.
5. Additional-report requests are structured by document/test needed, clinical reason, urgency, acceptable substitute, and whether review can proceed without it. A request is not represented as a prescription unless lawfully issued in a consultation.
6. If remote consultation is needed, the doctor/hospital confirms jurisdictional permission, modality, identity, consent, fee, participants, and whether a prescription can lawfully be issued.
7. The doctor authors and signs a preliminary opinion: reviewed records, stated diagnosis/history, clinical interpretation, limitations, recommended next evaluation/treatment pathway, reasonable alternatives where appropriate, key risks to discuss, urgency advice, required in-person assessment/tests, expected course as a range, and follow-up needs.
8. The doctor explicitly records whether the case is potentially suitable, unsuitable based on current information, or cannot be determined. “Acceptance” means willingness to review or provisionally receive the case—not guaranteed eligibility for a procedure.
9. Hospital staff builds operational and financial components around the locked clinician-authored opinion. A clinician must approve later edits to clinical fields.
10. Post-treatment, the treating doctor/hospital authors discharge and follow-up information. Messages after return are bounded follow-up, not implied continuous emergency monitoring.

## Doctor versus hospital ownership

| Doctor-owned clinical function | Hospital-owned operational/commercial function |
|---|---|
| Interpret available records and state limitations. | Accept the case into the hospital review process. |
| Ask clinically necessary clarification questions. | Assign specialists/coordinators and manage SLA. |
| Author/sign opinion and proposed clinical pathway. | Confirm facility, equipment, bed, and schedule availability. |
| Decide whether remote consultation is clinically appropriate. | Set consultation fee, booking, cancellation, and payment process. |
| Describe required tests and likely clinical sequence. | Create cost range, inclusions/exclusions, deposit, tax, refund, and validity terms. |
| Obtain/record clinical consent within the hospital process. | Issue visa invitation and administrative letters. |
| Document treatment changes, discharge instructions, and clinical follow-up. | Coordinate admission, billing, logistics, document release, and complaints. |

Neither party may edit the other's signed artifact. Corrections create a new version with an explicit reason.

---

# 7. HOSPITAL WORKFLOW

## Hospital as primary paying customer

The hospital product is an international-patient case-management workspace, not merely a lead inbox. It must show whether each case is authorized, medically reviewable, owned, progressing, commercially understood, and safely handed off.

## Core hospital workflow

- **Incoming leads/referrals:** Receive only explicitly shared cases; see referral source, source country, patient language, clinical category, completeness, consent scope, received time, and requested response SLA.
- **Qualification:** Accept for review, decline with reason, flag duplicate/existing hospital patient, or request a conflict/data correction.
- **Assignment:** Assign an IPD coordinator, clinical reviewer, optional second reviewer, finance owner, and escalation owner. Assignment must respect active employment/affiliation and role.
- **Document review:** View timeline, request missing records, mark translation required, record whether documents are adequate for preliminary review, and never overwrite originals.
- **Clinical review:** A verified clinician authors an attributable opinion. Hospital coordinators may compile but not impersonate the clinician.
- **Second opinions:** Create a distinct signed opinion or documented multidisciplinary review; do not merge conflicting opinions without attribution.
- **Proposal and quotation:** Combine the approved clinical pathway with expected stay, required tests, cost range, currency, inclusions, exclusions, assumptions, deposit, cancellation/refund terms, and validity. Revision requires a new version and reason.
- **Communication:** Maintain patient, referrer, and internal threads with clear audiences. Email/WhatsApp notifications must not become the only clinical record.
- **Visa invitation:** Generate or upload a hospital-authorized letter from verified patient/passport details and tentative treatment/admission dates. Track issued/reissued/withdrawn status.
- **Appointments/travel:** Coordinate consultations, tentative admission, arrival, airport transfer, accommodation, interpreter, and contact points without exposing clinical files to logistics providers.
- **Arrival/admission/treatment:** Record operational milestones and hospital identifiers. The platform does not replace the hospital EHR, admission consent, clinical orders, or billing system.
- **Discharge/follow-up:** Upload signed discharge artifacts, confirm patient/referrer receipt, schedule remote review, and close unresolved document or billing tasks.
- **Commercial reporting:** Track source country, referral source, acquisition/case coordinator, time in stage, response SLA, quote amount/range, selected/not selected, arrival, treatment start, close/loss reason, and follow-up completion.

## Improved pipeline

The pipeline separates **overall case**, **hospital review request**, **operational tasks**, and **outcome reason**. One overloaded status must not attempt to represent all four.

### Hospital review request stages

`RECEIVED → QUALIFICATION → ACCEPTED_FOR_REVIEW → INFORMATION_REQUIRED ↔ UNDER_MEDICAL_REVIEW → OPINION_ISSUED → PROPOSAL_PREPARATION → PROPOSAL_SENT → PATIENT_DECIDING → SELECTED → PRE_ARRIVAL → ARRIVAL_CONFIRMED → ADMITTED → TREATMENT_ACTIVE → DISCHARGE_PENDING → DISCHARGED → FOLLOW_UP → CLOSED`

### Branch/terminal states

- `DECLINED_BEFORE_REVIEW`
- `CLINICALLY_UNSUITABLE`
- `NOT_SELECTED`
- `WITHDRAWN_BY_PATIENT`
- `EXPIRED_NO_RESPONSE`
- `UNRESPONSIVE_PATIENT`
- `VISA_NOT_OBTAINED`
- `CANCELLED_CAPACITY_OR_SCHEDULE`
- `TRANSFERRED_TO_OTHER_FACILITY`
- `DECEASED`

### Required stage controls

Each stage transition records actor, timestamp, reason/comment, source, required evidence, and next owner. The system enforces only safe prerequisites—not clinical judgment. For example:

- `UNDER_MEDICAL_REVIEW` requires accepted request, assigned verified reviewer, and active access grant.
- `OPINION_ISSUED` requires a signed clinician-authored opinion with limitations.
- `PROPOSAL_SENT` requires current opinion plus quote currency, range or clearly labelled fixed component, inclusions, exclusions, assumptions, validity, and author.
- `SELECTED` requires patient action or an attributable case-manager recording confirmed off-platform instruction.
- `PRE_ARRIVAL` requires hospital acceptance; it does not require visa approval if a visa is not applicable.
- `ADMITTED` and `DISCHARGED` require confirmation by hospital staff, not patient location inference.
- `CLOSED` requires an outcome reason and unresolved-task review.

## Hospital views and controls

- Queue by owner, stage, age, SLA risk, country, specialty, and missing action.
- Case timeline that separates patient submissions, clinician documents, finance versions, logistics, and internal notes.
- Role-based internal notes invisible to patient/referrer; policy prevents copying material clinical decisions into hidden notes.
- Saved completeness and proposal checklists.
- Templates controlled per hospital but mapped to shared comparison fields.
- Audit and export for the hospital's authorized case record.
- Staff deactivation, reassignment, and periodic access certification.
- Lost-case reason taxonomy: clinical fit, price/financing, trust, response delay, visa, timing, competitor, local treatment, no response, duplicate, other with note.

---

# 8. PLATFORM ADMIN / CASE MANAGER

## Operational back office

### Work queues

- New submissions awaiting contact/completeness review.
- Identity, guardian, referring-doctor, Indian-doctor, hospital, and partner verification.
- Consent absent, ambiguous, expired, or revoked.
- Suspected duplicate patients/cases and existing-hospital-patient conflicts.
- Missing, corrupt, unreadable, mislabeled, or untranslated documents.
- Specialty/routing review and provider-capacity confirmation.
- Hospital acceptance and response SLA risk/breach.
- Proposal completeness, inconsistent assumptions, and expired quotes.
- Visa/travel dependencies and arrival readiness.
- Discharge-document and follow-up handoff gaps.
- Complaints, safety concerns, suspicious activity, access incidents, and disputes.
- Unresponsive participants and cases eligible for closure.

### Admin actions

- **Patient verification:** Verify contact, resolve identity/role mismatch, review guardian/delegate authority, and minimize passport collection until travel documentation is justified.
- **Doctor verification:** Record authoritative sources, licence scope/status, identity match, sanctions result, hospital affiliation, limitations, reviewer, and renewal date.
- **Hospital verification:** Check legal entity, clinical-establishment licensing as applicable, physical location, official domain/contact, international department authorization, accreditation scope/expiry, bank beneficiary, complaint contact, and signatory authority.
- **Case triage:** Determine operational eligibility, completeness, declared specialty, urgency handling, and whether clinician escalation is needed. Never diagnose.
- **Routing:** Create a shortlist, document rationale/conflict, secure patient permission if required, and send separate review requests.
- **Document operations:** Correct metadata with provenance, request originals, initiate approved translation, quarantine suspicious files, and never edit clinical content.
- **Duplicate resolution:** Compare minimum identifiers; merge only after human confirmation and preserve provenance/access boundaries.
- **Suspicious activity:** Hold sharing/payment changes, request verification, suspend users/organizations, preserve evidence, and escalate under policy.
- **SLA monitoring:** Track acceptance, information request, opinion, quote, and follow-up deadlines with human escalation paths.
- **Communication assistance:** Translate or relay operational content with clear attribution; never impersonate clinicians or silently rewrite medical statements.
- **Visa/travel coordination:** Maintain checklists and official-source links, verify hospital-issued documents, and avoid claims of approval or government affiliation.
- **Disputes/escalations:** Classify clinical, billing, logistics, privacy, conduct, fraud, or service complaint; preserve records; identify responsible party; communicate acknowledgement and target update time.
- **Partner management:** Verify identity/business, contract, service scope, insurance where relevant, data needs, conflicts, performance, complaints, and suspension.
- **Auditing:** Search attributable events, export scoped evidence, conduct access review, and report incidents/metrics.

## Absolutely necessary MVP admin workflows

1. User/organization verification with approve/reject/suspend/reverify.
2. Case completeness review, duplicate check, specialty confirmation, and human routing.
3. Consent/access overview and recipient-specific sharing.
4. Hospital response/SLA queue and escalation.
5. Proposal/quote completeness check and version comparison.
6. Case owner, next action, due date, and lifecycle control.
7. Secure support, complaint, suspicious-activity, and privacy-request queues.
8. Visa-document/travel/admission/discharge checklist for selected cases.
9. Full access/material-change audit search.
10. Basic operational funnel and outcome reporting.

Fraud scoring, automated triage, partner marketplaces, advanced analytics, and bulk campaigns are not MVP requirements.

---

# 9. CASE DATA MODEL — FUNCTIONAL VIEW

No database design is implied. “Update” below means the actor can propose or make a permitted business change; issued clinical and commercial artifacts remain versioned.

| Entity | Represents / important information | Relationships | Create / read / update |
|---|---|---|---|
| **Patient** | Person seeking care; legal name, contact, residence/nationality, language/timezone, date of birth, identity state, accessibility, guardian/delegate links. Travel identity is separately protected. | Has cases, consents, delegates, records, conversations, requests. | Patient/platform can create; patient and assigned staff read/update allowed fields; providers only within shared cases. |
| **Patient Case** | A bounded care-seeking episode and shared source of truth; case reference, stated need, history, urgency declaration, specialty, preferences, status, owner, next action, outcome. | Belongs to patient; may have referral, records, multiple provider review requests/proposals, appointments, journey items. | Patient/referrer/platform create; scoped participants read; only field owners update; transitions are audited. |
| **Case Participant/Delegate** | A person and their role in one case, including family authority and visibility scope. | Joins user to case and grants. | Patient/guardian invites; invitee accepts; platform verifies exceptions; patient changes future scope. |
| **Referral** | Clinician-to-clinician handoff or patient-origin source; referring clinician, organization, question, history summary, requested specialty, date, responsibility/handoff statement. | Links case, referring doctor, referral source, consent, records. | Verified referrer creates/updates until submitted; authorized participants read; amendments versioned. |
| **Referral Source** | How the case entered: self, doctor, hospital, community/partner, campaign, other; disclosure and attribution, not a clinical endorsement. | Links cases, organizations, commercial terms/conflicts. | Platform records; hospital sees source on shared case; patient sees material conflicts; restricted commercial details stay role-scoped. |
| **Doctor** | A clinician identity and professional status; regulator, licence, jurisdiction, qualifications, specialties, languages, verification, sanctions checks, affiliations. | Belongs to organizations; participates in referrals, reviews, opinions, consultations, follow-ups. | Doctor submits; verifier approves/updates status; case participants read appropriate verified profile. |
| **Hospital** | A healthcare organization/location; legal identity, contacts, licences, services, accreditations by site/scope, international department, verification status, commercial agreement. | Has users, doctors, review requests, proposals, appointments, visa documents, payments. | Hospital submits; platform verifies; patients see relevant verified facts; only authorized organization admins edit. |
| **Organization Membership** | A user's active role and authority in a hospital/platform/partner. | Links user, organization, roles, validity, inviter, deactivation. | Organization admin/platform create; user and admins read; authorized admins update; removal revokes associated access. |
| **Verification Record** | Evidence that a claim was checked; claim, source, document, result, verifier, dates, limitations, expiry/recheck, suspension. | Applies to user, doctor, hospital, membership, partner, bank beneficiary. | Subject submits; verifier creates/updates; public/case views expose result and safe evidence summary, not raw identity documents. |
| **Medical Record** | Original or translated patient health artifact; category, author/facility, report/service date, upload date, language, source, hash/identity, quality, sensitivity, timeline position, version/supersession. | Belongs to case; covered by consent/access grants; may answer information request. | Patient/referrer/hospital as authorized create; authorized case participants read; metadata corrections audited; content immutable. |
| **Diagnosis Information** | A claim about diagnosis/status with source and certainty—not platform truth; patient-reported, referrer-documented, report-derived, or treating-clinician-authored. | Part of case/referral/opinion. | Source actor creates; authorized participants read; corrections append/provenance rather than erase. |
| **Treatment Request** | What review/service is sought; clinical question, desired specialty/treatment, timing, preferences, prior alternatives. | Belongs to case and informs routing. | Patient/referrer creates; case manager clarifies; clinicians read; original wording preserved. |
| **Provider Review Request (Case Share)** | One invitation from platform/patient to one hospital; shared data manifest, purpose, grant, SLA, acceptance, owner, stage, decline reason. | Links case, hospital, access grant, information requests, opinions, proposal. | Platform creates after authorization; hospital accepts/updates its stage; patient/referrer sees appropriate status. |
| **Information Request** | A specific missing fact/document/test question; requester, clinical/operational reason, due date, response, status. | Belongs to review request and may link records/messages. | Authorized hospital doctor/coordinator/platform creates; patient/referrer answers; all scoped participants read. |
| **Doctor Opinion** | Signed preliminary clinical interpretation; reviewed material, limitations, recommendation/options, required assessment/tests, urgency, author, licence, issue/version date. | Belongs to case and review request; informs proposal/consultation. | Assigned verified doctor authors/signs; hospital and authorized patient/referrer read; only author issues correction version. |
| **Hospital Proposal** | Combined clinical-operational offer; linked opinion, pathway, doctor/location, stay ranges, prerequisites, availability assumptions, consultation, coordinator, validity. | Has quotation and versions; belongs to review request. | Hospital coordinator compiles; clinician approves clinical fields; hospital authorizes; patient/referrer reads if shared. |
| **Quotation** | Indicative financial estimate; range/line items, currency, taxes, inclusions/exclusions, assumptions, deposit/refund terms, validity, version, variance reason. | Belongs to proposal; may relate to payment status/final bill reference. | Hospital finance creates/issues/revises; patient and permitted coordinator read; platform checks completeness only. |
| **Consultation** | Scheduled/held encounter; type, participants, jurisdictional review result, consent, timezones, fee, status, authored note link. | Links case, doctor, hospital, appointment, conversation, opinion. | Hospital schedules; patient confirms; clinician authors clinical note; platform coordinates. |
| **Consent** | Evidence of informed permission or separate optional preference; actor/authority, notice/version/language, purpose, data/recipient scope, date, expiry, withdrawal, evidence. | Governs case processing, grants, consultations, referrer/family/travel/marketing access. | Patient/authorized representative grants/revokes; platform records; recipients can read scope, never expand it. |
| **Case Access Grant** | Effective authorization for a role/person/organization to access a case/document set for purpose and period. | Derived from consent, relationship, membership, and assignment; links audit. | System/platform creates from valid authority; patient can view/request revocation; admins cannot self-grant without controlled policy. |
| **Appointment** | Confirmed or tentative clinical/administrative event; location/link, timezone, participants, purpose, preparation, status, cancellation reason. | Links case, hospital, doctor, consultation/admission. | Hospital proposes/confirms; patient accepts/requests change; coordinator manages logistics. |
| **Visa Case** | Coordination record, not government application; visa category under review, official checklist/source/date, invitation status, applicant-reported reference/status, deadlines, exceptions. | Links patient/case/hospital, passport record, invitation, travel plan. | Patient/platform create after selection; hospital issues letter; patient updates official status; only evidence-backed status shown. |
| **Travel Plan** | Opted-in logistics; party, itinerary, accommodation/transport/interpreter/accessibility needs, providers, confirmations, contingency contacts. | Links case, visa, appointments, partner service requests. | Patient/case manager create; assigned partner sees/updates only its service; hospital sees relevant arrival details. |
| **Case Coordinator/Assignment** | Named accountable owner for a case or review request; role, organization, start/end, backup, SLA. | Links user to case/tasks. | Authorized manager assigns/reassigns; participants see current contact; history retained. |
| **Case Task/Checklist Item** | Next action, owner, due date, prerequisite, completion evidence, escalation state. | Belongs to case/review/journey. | Authorized coordinators/system create; assigned actor updates; scoped participants see relevant tasks. |
| **Conversation/Message** | Case-bound communication; sender, recipients/audience, content classification, attachments, translation, delivery/read state, escalation, immutable history. | Links case and optionally request/proposal/appointment. | Authorized participants create/read in audience; corrections append; admin access limited to support/compliance need. |
| **Payment Record** | Visibility of requested/paid/refunded/disputed amount and recipient/reference; not proof beyond attached hospital/processor evidence. | Links quote, hospital, case, invoice/final bill. | Hospital finance/platform records evidence; patient reads/disputes; no MVP platform custody. |
| **Discharge Summary/Pack** | Hospital-authored continuity package; signed summary, procedure report, medication, results, warning signs, follow-up, fit-to-travel and local-doctor handoff as applicable. | Links case, treatment, records, follow-ups, consent. | Hospital/treating clinician creates; patient reads; referrer reads if permitted; corrections versioned. |
| **Follow-up** | Planned or completed post-discharge contact; date, participants, questions, local results, response, escalation, closure. | Links case, doctors, consultation, messages, records. | Hospital schedules; patient/referrer submits; clinician responds; coordinator tracks SLA. |
| **Complaint/Safety Incident** | Reported service, conduct, clinical, billing, fraud, privacy, or safety concern; severity, parties, evidence, owner, actions, communications, resolution. | Links case/users/organizations/audit events. | Any participant reports; restricted responders investigate/update; complainant sees acknowledgement and appropriate status, not privileged internal material. |
| **Audit Event** | Attributable record of access, download, share, grant/revoke, issue/revision, transition, export, admin action, and security event. | Links actor, subject, case/entity, purpose, time, result, source. | System creates; cannot be edited by ordinary users; compliance can search/export; patient receives appropriate access report. |

---

# 10. MEDICAL DOCUMENT MANAGEMENT

## Upload and format

- MVP supports PDF and common still-image formats. Other formats, archives, DICOM studies, audio/video, and physical-media ingestion require a separately reviewed assisted path.
- Support multi-file and mobile-camera upload, interruption recovery, file count/size guidance, duplicate detection, and a visible processing state.
- Reject executable content, password-protected/unscannable content that cannot be safely handled, corrupt files, mismatched extensions, and unsupported types with a reason and recovery instruction.
- Large diagnostic imaging is not an ordinary image-upload problem. For MVP, use hospital-approved secure transfer/reference procedures; native DICOM viewing and PACS integration are later.

## Categories and metadata

Minimum categories: referral letter, clinical summary, discharge summary, consultation note, laboratory, pathology, radiology report, radiology image/reference, cardiology test, operative/procedure report, medication/prescription, allergy, vaccination, identity/travel, consent/authority, hospital opinion, quotation, visa invitation, payment/billing, translation, other.

Required metadata where applicable: patient/case, source/uploader, document category, document/report date, service date range, author/facility, language, original/translation, page count, upload timestamp, sensitivity/restriction, related request, supersedes/is superseded by, quality/readability status, and integrity identifier.

## Medical-record timeline and versions

- Timeline defaults to clinical/report date, with upload date shown separately.
- Original file is immutable. Rotation, compression, OCR text, redaction, and translation are derived versions visibly linked to the original.
- Metadata corrections retain before/after values, actor, reason, and timestamp.
- A corrected clinical report from its issuer is a new record/version, never a platform edit.
- Users can flag wrong-patient, disputed, duplicate, or obsolete documents. Removal from ordinary view does not silently destroy audit evidence.

## Missing-document requests

- Requests identify exact item, reason, requester role, urgency, due date, acceptable date range/quality, whether an existing document can satisfy it, and whether review is paused.
- The patient/referrer can upload, link an existing document, state “not available,” or ask for clarification.
- Only an authorized clinician may characterize a test as clinically required; coordinators can request administrative documents or relay an attributed clinician request.

## Sharing and secure access

- Sharing is case-, recipient-, purpose-, document-, and time-bound. A hospital receives only the manifest approved for its review request.
- Newly uploaded documents are not automatically shared with every prior recipient unless the active consent/grant explicitly covers future documents of that category and the user is shown this behavior.
- Highly restricted items (for example, passport, genetic, reproductive, mental-health, or HIV-related records where relevant) can require separate sharing confirmation based on policy and jurisdictional review.
- Access uses authenticated, expiring, role-scoped sessions; public links and email attachments containing medical records are prohibited by default.
- Downloads can be disabled by policy or limited to authorized roles, but the product must not promise technical prevention once an authorized recipient legitimately receives a copy. Every view/download/export is auditable.
- On access removal, new access stops immediately; already downloaded copies are governed by recipient agreements, law, and deletion instructions.

## Translation

- Optional translation is a separate derived artifact with language pair, translator/provider, machine/human method, completion date, review state, and disclaimer.
- Medical decisions cannot rely on unreviewed machine translation when mistranslation could materially affect care.
- The original is always available alongside the translation to authorized clinical reviewers.
- Interpreter/translator access is document- or assignment-specific and expires.

## Security and audit requirements

- Encrypt content in transit and storage; isolate production from test; use least privilege, strong authentication, session controls, malware detection, safe previewing, backup, and monitored access.
- Do not place sensitive content in filenames, URLs, notification text, analytics payloads, support tools, or general application logs.
- Record uploader, viewers, downloads, shares, grant changes, transformations, translations, deletion/restriction requests, and administrative overrides.
- Define retention by record class, participant role, contract, and launch jurisdiction. Deletion requests produce `deleted`, `restricted`, `retained_due_to_obligation`, or `pending_review` outcomes with reasons; no universal instant-delete promise.

---

# 11. COMMUNICATION SYSTEM

## Communication relationships

| Relationship | Appropriate communication | Guardrails |
|---|---|---|
| Patient ↔ case manager | Intake help, missing records, status, decision support, logistics, escalation. | Case manager must identify non-clinical role; clinical questions are routed, not answered. |
| Patient ↔ Indian doctor | Clarification, consultation, opinion questions, follow-up. | Only after hospital assignment/authorization; attributable clinician; no emergency monitoring promise. |
| Referring doctor ↔ Indian doctor | Referral question, record interpretation, handoff, follow-up. | Both verified; patient-authorized; clear private/shared audience and record policy. |
| Hospital ↔ patient | Information requests, proposal, quote, appointment, administrative instructions, admission/discharge. | Named hospital users; commercial versus clinical authorship clear; no competitor visibility. |
| Hospital ↔ referring doctor | Clarification and continuity documents. | Patient-authorized, clinically relevant scope; no referral commission solicitation. |
| Admin ↔ all parties | Verification, support, SLA, safety, complaints, privacy rights. | Admin role and purpose shown; sensitive access is case-assigned or incident-authorized and audited. |

## Channel decisions

| Channel | MVP | Later / conditions |
|---|---|---|
| **Internal case messaging** | **Must have.** Case-bound threads, explicit recipients/audience, attachments from the secure record store, delivery/read state, timestamps, escalation, and immutable history. Separate clinical, operational, finance, and internal hospital threads. | Structured multidisciplinary threads, e-sign acknowledgements, advanced routing. |
| **Email** | **Must have for notifications and low-sensitivity support.** Send “action required”/status notices with a secure deep link; no medical record attachments or diagnosis in subject/body by default. Inbound email may be manually captured with consent and classification. | Controlled email ingestion and organization archiving after security/privacy review. |
| **WhatsApp/SMS** | **Optional constrained MVP fallback** for opt-in reminders, contact verification, and logistics notices with no sensitive clinical content. It must never be the sole record of a clinical decision. | Approved business integration, template governance, regional consent/retention rules, and secure deep links. Avoid personal staff accounts. |
| **Video consultation** | Use the hospital's reviewed workflow/link and store appointment plus resulting clinician-authored note. Do not build native video. | Native consultation only after cross-border licensure, consent, recording, accessibility, security, and prescribing rules are resolved. |
| **In-app notifications** | **Must have.** Missing item, new response, approaching/changed appointment, access change, expiring quote, travel task, and support update. | Preference center and advanced digesting. |
| **Automatic status updates** | **Must have where evidence-backed.** Notify attributable transitions and next owner. | External system synchronization; never infer clinical outcomes or official visa status from engagement data. |
| **Voice calls** | Human case manager may call through an approved operational process and log date, participants, purpose, and summary confirmed when material. | Recorded calls/transcription only after explicit consent and jurisdiction review. |

## Communication behavior

- Every message belongs to a case or support/verification context, identifies sender role/organization, recipients, and whether it is visible to patient/referrer.
- Users cannot add a new participant to a thread as a workaround to sharing controls.
- Clinician-to-clinician messages that influence care must be preserved as part of the case record according to reviewed policy.
- Translation shows original and translated content and method; urgent/clinical translation requires qualified human support.
- Edits after sending are not silent; corrections are appended and linked.
- Safety phrases suggesting an emergency trigger an immediate on-screen instruction to contact local emergency services and a human escalation queue, not an automated clinical conclusion.
- Marketing consent and channels are entirely separate from care-coordination communications.

---

# 12. MATCHING / ROUTING

## MVP principle

Matching is a **rules-based eligibility filter plus trained-human selection**, not an AI recommendation and not a provider auction.

## Inputs

- Primary/secondary specialty and treatment capability needed, confirmed administratively or by a qualified clinician when ambiguous.
- Specific disease/pathway only as documented by patient/referrer/reports.
- Doctor expertise and hospital capability/privileges.
- Current provider and organization verification status.
- Accreditation by exact facility and relevant service scope, with expiry.
- Patient's approved cities/hospitals, willingness to consider alternatives, and travel constraints.
- Budget range as a feasibility preference, never a reason to hide clinically appropriate lower-revenue options.
- Language/interpreter capability and accessibility needs.
- Declared urgency and whether the platform is appropriate for the timeframe.
- Provider capacity, response SLA performance, clinician availability, and known treatment timing.
- Country-specific restrictions, sanctions/export/payment issues, age, and special-pathway safeguards.
- Conflict of interest and contractual eligibility.

## Routing sequence

1. **Hard safety/eligibility filters:** active verified hospital; active assigned clinician/department; required specialty/capability; source-country service eligibility; no suspension/conflict block; feasible review deadline.
2. **Preference fit:** location, language, accessibility, budget band, timing, requested doctor/hospital, attendant needs.
3. **Operational quality:** recent response completeness, SLA reliability, unresolved serious complaint status, and capacity. Do not use paid tier as a clinical-fit factor.
4. **Human shortlist:** case manager records why each candidate fits, why another was excluded, and any uncertainty.
5. **Patient consent:** approve named hospitals or a clearly defined recipient class, depending on reviewed consent design.
6. **Separate shares:** send one isolated review request per hospital; never expose competitors, quote amounts, or recipient list.
7. **Monitor and reroute:** on decline/SLA breach, obtain any necessary consent and offer the next suitable provider without selling the case to the highest bidder.

## What the routing output means

“Matched” means the hospital appears operationally eligible to review the submitted case. It does **not** mean clinically recommended, best, guaranteed to accept, or certain to provide the proposed treatment.

## AI later—only where useful

Potentially valuable after a high-quality labeled operating history:

- OCR and document-type/date extraction, always reviewable against the original.
- Draft chronology and missing-document checklist for case-manager confirmation.
- Translation assistance with explicit machine status and human review for material clinical use.
- Suggested specialty/capability tags with confidence and mandatory human confirmation.
- Duplicate-document/case candidates for human resolution.
- SLA-risk and workload forecasting.
- Conversation summarization with source links and human sign-off.

Do not use AI to diagnose, prescribe, determine clinical suitability, rank “best” clinicians, generate unsupervised medical opinions, infer prognosis, promise outcomes, approve visas, or deny access to care.

---

# 13. COMPARISON EXPERIENCE

## Objective

Help the patient and their trusted clinician understand **differences, assumptions, and unanswered questions**, not reduce treatment to a product card.

## Comparison structure

Each response column shows:

- Exact hospital facility/location and verified accreditation scope/date.
- Named reviewing doctor, verified registration source/date, specialty, hospital association, and attributable experience facts.
- Records reviewed and material records not available.
- Proposed pathway in clinician-authored language plus a standardized phase outline.
- Alternatives or “not addressed.”
- Required remote consultation or further tests before/after arrival.
- Expected hospital stay and expected India stay as ranges, with basis/uncertainty.
- Indicative hospital cost range and currency.
- Included/excluded items, taxes, implants/consumables, medicines, complications, ICU, blood products, attendant costs, travel/accommodation, and follow-up as applicable.
- Deposit, cancellation/refund terms, quote validity, and what may change it.
- Tentative availability and response/issue date.
- Languages/interpreter availability and accessibility.
- Questions still unanswered.
- Commercial relationship/conflict disclosure and whether the hospital paid to participate.

## Fairness controls

- Present user-selected or clinically relevant factors; never default-sort by commission, lead price, hospital payment tier, or predicted revenue.
- Do not label a higher-cost proposal worse or a lower-cost proposal better.
- Do not calculate a single quality score or treatment “value score.”
- Do not compare pathways as equivalent when diagnoses, assumptions, techniques, facilities, or inclusions differ.
- Show missing information prominently rather than treating absence as zero/no.
- Show quote revisions and reasons side by side; never replace old promises silently.
- Let the patient export a question list and discuss options with their referring doctor.
- Case managers may explain fields and inconsistencies but must not recommend a treatment or clinician.

## Information that must not be ranked or gamified

- Claimed success rates without comparable definitions, risk adjustment, cohort, period, and independent verification.
- Mortality/complication outcomes as consumer leaderboards.
- Doctor popularity, volume, response speed, or star ratings as proxies for clinical quality.
- Patient reviews/testimonials as a clinical ranking.
- Procedure aggressiveness, shortest stay, or lowest price.
- “Best doctor,” “best hospital,” guaranteed cure, or guaranteed outcome claims.
- Clinician-to-clinician disagreement as a win/loss contest.

---

# 14. TRUST, SAFETY, AND VERIFICATION

## Verification design

### Patient identity and authority

- Verify email/phone at registration; use risk-based identity checks before sensitive sharing.
- Collect legal identity/passport only when needed for recipient verification, hospital registration, or visa documentation.
- Match patient, account holder, guardian, and traveler explicitly; never assume the submitter is the patient.
- For minors/incapacitated patients, verify guardian/legal authority and capture age/capacity-appropriate assent where applicable.
- High-risk changes to identity, contact, passport, beneficiary/bank details, or delegate require step-up verification and human review.

### Indian doctor

- Check identity, NMC and relevant state-council registration, registration number/name match, current status, qualification/specialty evidence as relevant, sanctions/blacklist sources, hospital affiliation, and privileges confirmation.
- Record the exact source URL/document, date, reviewer, result, scope, expiry/recheck, and discrepancies.
- Reverify periodically and on complaint, affiliation change, bounced official contact, or regulator update.
- Public/case profile says “evidence checked as of [date]” and never implies guaranteed competence or outcomes.

### International/referring doctor

- Use the authoritative regulator(s) for the declared practice jurisdiction, plus identity and professional contact verification.
- Confirm whether the licence is active and the role/specialty claim is within available evidence.
- Country-by-country policy decides whether the doctor can refer, consult, receive records, or only act as a patient-authorized adviser.

### Hospital

- Verify legal entity and exact facility; official address/domain/contact; applicable establishment licences; authorized IPD signatory; bank beneficiary; clinical service/capability and doctor affiliation; complaints contact; and accreditation by site, scope, issue/expiry.
- NABH/JCI or another accreditation is displayed precisely, not as a general guarantee. Suspended/expired accreditation is immediately reflected.
- Execute service, data-protection, security, conduct, transparency, response-SLA, records, complaint, and termination agreements before live cases.

### Platform and partners

- The platform should assess NABH MVTF empanelment and design its operations to the applicable standard even before certification claims are made.
- Travel/interpreter partners require legal identity, ownership/contact, insurance/licence where applicable, staff checks appropriate to service, service-area proof, data-processing terms, confidentiality, incident process, bank verification, and ongoing performance review.

## Fraud prevention

- No provider can self-publish a verified status.
- Verify official-domain communications and named signatories out-of-band for onboarding and bank-detail changes.
- Detect duplicate identities, shared credentials, impossible access, unusual bulk downloads, mass case solicitation, altered quotations/letters, and off-platform payment redirection.
- Watermark downloadable sensitive case copies with recipient/case/date where appropriate, without obscuring clinical content.
- Rate-limit invitations/uploads/messages; quarantine suspicious files and accounts.
- Show a prominent warning that the platform/hospital will not request payment to a changed account without verified notice.
- Maintain suspend, revoke access, preserve evidence, notify affected parties, and reinstatement procedures.

## Transparency and safety controls

- **Consent records:** versioned, purpose- and recipient-scoped, understandable, withdrawable prospectively, and available to the patient.
- **Permissions:** default deny; explicit case assignment; least privilege; separation of clinical, finance, partner, support, and compliance access.
- **Audit:** views, downloads, shares, exports, messages, grants, revisions, transitions, and admin overrides are attributable and tamper-evident.
- **Conflict disclosure:** identify who pays the platform, referral-source relationships, sponsored placement if ever permitted, travel commissions, ownership relationships, and provider limitation. A patient must see material conflicts before selection.
- **Referral transparency:** show whether a route came from patient preference, referring clinician request, rule-based eligibility, case-manager shortlist, or commercial relationship. Do not pay doctors per patient without specific legal/ethical clearance; default policy is no such payment.
- **Quote transparency:** author, version, validity, range, currency, assumptions, inclusions/exclusions, clinical-change warning, deposit/refund terms, and change rationale.
- **Disclaimers:** contextual and plain-language, never a blanket waiver. They cannot cure misleading workflows or unsafe conduct.
- **Emergency handling:** persistent local-emergency direction, no emergency response promise, rapid human escalation for safety reports, and documented handoff.

## Complaint and escalation workflow

1. Any participant submits a complaint or staff records one from another channel.
2. System acknowledges receipt, category, case reference, expected next update, and emergency direction.
3. Restricted staff triage severity: immediate safety, privacy/security, fraud/payment, clinician conduct, clinical-care complaint, service/logistics, or billing.
4. Preserve relevant evidence and prevent routine deletion; restrict/suspend access where necessary.
5. Assign responsible organization and independent platform owner; disclose conflicts.
6. Communicate factual progress without adjudicating clinical negligence beyond competence.
7. Escalate to hospital clinical governance, regulator, insurer, law enforcement, data authority, embassy/consulate, or emergency services where legally required/advised.
8. Record resolution, corrective action, appeal/contact route, and trend category.

## High-risk areas requiring professional review before a real case

- Whether the platform/founder entity is a medical-value-travel facilitator, healthcare provider, intermediary, controller/fiduciary, processor, business associate, travel agent, or another regulated role in each jurisdiction.
- Indian central/state healthcare, clinical-establishment, telemedicine, professional-conduct, medical-advertising, consumer-protection, and record rules.
- Source-country licensure, referral, patient-abandonment, informed-consent, medical-record, malpractice, and cross-border consultation rules.
- Referral commissions, success fees, lead fees, doctor benefits, travel commissions, sponsored ordering, and anti-kickback/anti-bribery rules.
- India DPDP implementation plus any still-applicable information-security/privacy rules; source-country privacy and cross-border transfer mechanisms.
- Hosting/subprocessor locations, government/law-enforcement access requests, breach notification, retention/deletion, and data-subject rights.
- Minors, impaired capacity, guardianship, reproductive/genetic/mental-health/HIV data, and other specially protected records.
- Organ/tissue transplant, surrogacy/fertility, controlled medicines, experimental care, and other high-risk treatment pathways; exclude until separately approved.
- Medical visa/invitation assistance, immigration representations, sanctions, nationality restrictions, and use of passport data.
- Payment collection, foreign exchange, taxes, refunds, financing, insurance claims, and chargebacks.
- Professional liability, clinical indemnity, facilitator liability, partner insurance, adverse outcomes, and death/repatriation.
- Contract language, governing law, dispute resolution, accessibility, translations, consumer cancellation, testimonial/claim substantiation, and records ownership.

---

# 15. PRIVACY AND PERMISSION MODEL

## Principles

1. Default deny and minimum necessary access.
2. A verified identity does not itself grant case access.
3. Consent, organizational membership, case assignment, purpose, and current status must all support access.
4. Organization-level access does not mean every employee can browse every shared case.
5. Sharing a case with Hospital A does not expose it to Hospital B, and neither sees the other's response.
6. Clinical, coordination, finance, logistics, support, compliance, and analytics data scopes remain separable.
7. Consent is not bundled with marketing, testimonials, research, or optional partners.
8. Revocation stops future access/sharing where feasible but does not falsify history or automatically erase records another party must lawfully retain.

## Roles and scopes

| Role | Default case scope | Document scope | Special limits |
|---|---|---|---|
| Patient | Own active and historical cases. | All patient-accessible records; may be exceptions only where legally/clinically reviewed and explained. | Controls delegates and elective sharing; cannot alter issued artifacts/audit. |
| Family/delegate | Invited case(s) only. | Explicit categories/actions in delegation. | Cannot expand own scope or impersonate patient. |
| Referring doctor | Cases created by or shared with them while authorization remains. | Referral/clinical records and returned clinical documents selected by consent. | No general commercial, logistics, or family-chat access. |
| Indian doctor | Hospital-assigned review/treatment/follow-up cases with active membership. | Clinical subset required for assigned purpose. | No competitor data; access ends/reduces after assignment unless follow-up/retention justifies it. |
| Hospital coordinator | Cases explicitly shared with hospital and assigned/queued by role. | Clinical summary/records needed for coordination plus hospital artifacts. | Cannot edit signed opinion; internal notes remain governed. |
| Hospital finance | Selected/authorized hospital cases requiring finance action. | Quote/invoice/payment and minimum identity; clinical detail only if specifically needed and permitted. | No broad medical-record browsing. |
| Hospital organization admin | Membership, configuration, aggregate operational data. | No clinical access by default; case access requires separate role/assignment. | Cannot self-authorize hidden access. |
| Platform case manager | Assigned cases. | Minimum records needed for completeness/routing/coordination. | Cannot issue clinical content; assignment/access monitored. |
| Verifier/compliance | Verification subjects and assigned incidents. | Raw identity/credential evidence; clinical records only if incident requires. | Stronger access approval and logging. |
| Support | Assigned ticket and limited case summary. | Attachments explicitly included in ticket. | Temporary elevation only through controlled escalation. |
| Travel/interpreter partner | Accepted service request only. | Logistics/session-specific data. | No diagnosis or general medical documents; expires after service. |
| Analyst | De-identified/aggregated approved datasets. | No direct identifiers or raw records by default. | Re-identification prohibited and access reviewed. |

## Consent model

Separate records are required for:

- platform processing needed to provide the requested coordination service;
- sharing a defined record set with named hospitals or a clearly explained recipient class;
- referring-doctor access and return of clinical documentation;
- family/delegate authority and permitted actions;
- remote consultation and any recording (recording off by default);
- passport/visa-document processing;
- interpreter/translation and travel-partner disclosure;
- optional marketing, testimonials, product research, or de-identified secondary use.

Every consent record includes the patient/representative, authority basis, clear purpose, data categories, recipient/recipient class, actions, duration/expiry, geographic transfer information as reviewed, notice/version/language, evidence, grant time, withdrawal route/time, and consequences of refusal/withdrawal.

## Case- and document-level access behavior

- A provider review request contains an explicit share manifest. Recipient acceptance does not widen it.
- Access to future uploads follows a clearly displayed rule and category scope; sensitive categories may require fresh confirmation.
- Users see an “Access” view listing people/organizations, purpose, scope, granted date, last access where appropriate, expiry, and revoke/request-change action.
- When a staff member leaves or changes role, organization membership ends, sessions are revoked, assigned work is transferred, and historical authorship remains.
- When a doctor changes hospital, old-hospital cases do not follow the doctor automatically; the patient/hospital decides any new lawful care relationship.
- Break-glass access is not an ordinary MVP feature. If required for safety/support, it needs named eligible roles, reason, time limit, alert, after-the-fact review, and patient notification where appropriate.

## Revocation, export, restriction, and deletion

- Revocation is effective for future platform access promptly and propagates to relevant recipients with documented acknowledgement where required.
- The system preserves proof of prior consent, authored clinical records, and audit events according to reviewed retention obligations.
- Patient export includes accessible structured case data, documents, consent history, recipients, and material status history in understandable form.
- Correction appends accurate information and provenance; it does not rewrite another clinician's signed record.
- A deletion/restriction request enters a tracked review, identifies controllers/holders, pauses nonessential processing, and returns a scoped decision and appeal/contact route.
- Cross-border handling, onward transfers, recipient retention, and deletion enforceability require country- and contract-specific review; UI wording must not promise more control than can be delivered.
