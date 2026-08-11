# Verified Cross-Border Healthcare Referral Network

## Refined Product, Business, and Functional Specification

**Status:** Founder decision document; pre-architecture and pre-build
**Version:** 1.0
**Date:** 11 August 2026
**Planning target:** Close and safely coordinate the first 10 legitimate cross-border referrals, not acquire a large directory audience.

This document retains the earlier work on consent, cases, provider review requests, hospital/doctor workflows, medical records, permissions, verification, lifecycle, coordination, and professional-review boundaries. It deliberately does not repeat that material except where it changes product scope, adoption, or economics.

## Executive conclusion

The product is **not a medical-tourism marketplace with a doctor community attached**. It is a **closed-loop professional referral network** whose initial transaction happens to be planned treatment in India.

The core product unit is not a profile, message, lead, or quotation. It is a **completed referral loop**:

`verified referring doctor → consented structured case → verified receiving specialist/hospital → attributable response → patient decision/care → discharge and follow-up returned`

The commercial wedge is equally specific:

- Hospitals do not need another generic dashboard. They may pay for **qualified cases from a hard-to-build referring-doctor channel**, plus workflow that turns those cases into timely, measurable responses and arrivals.
- Doctors should join free. They return only if the product gives them reliable specialist access, saves coordination time, protects their patient relationship, and closes the loop after treatment.
- Patients receive a controlled case workspace and coordinator, but direct-to-patient marketplace traffic is not the launch engine.
- The first product is a software-assisted managed network. Human operators verify, match, chase, normalize, and coordinate until repeatable patterns earn automation.

The initial monetization should be a **paid hospital corridor pilot**: a fixed quarterly/annual platform-and-operations fee for access to a defined verified referral corridor, an international case workspace, response-SLA operations, and measurable funnel reporting. Do not begin with percentage commissions, doctor payments, hidden patient markups, or a broad self-serve SaaS promise.

## The thesis in five statements

1. **Demand before dashboard:** A hospital pays first for credible, qualified international demand and repeatable referrer relationships; workflow makes that demand convert and remain attributable.
2. **Referral before social:** A doctor profile exists to complete a referral, not to accumulate followers.
3. **Relationship before lead:** A referring doctor who receives a useful response and a proper handback can send the next patient; a purchased lead usually does not compound.
4. **Corridor before globe:** One source-country × specialty × India corridor creates density, operating knowledge, and credible response promises.
5. **Service before automation:** The first moat is reliable execution and relationship data; software captures and scales it after the team understands the work.

---

# 1. WHAT THE ACTUAL PRODUCT IS

## Product definition

### One sentence

A verified professional referral network that lets doctors and patients send consented cross-border cases to appropriate Indian specialists and hospitals, receive attributable treatment responses, and close the care loop back to the home doctor.

### One paragraph

The product combines a verified specialist directory, professional relationship layer, structured referral workflow, patient case workspace, hospital international-patient CRM, and a human operations console. A foreign doctor can find a verified Indian specialist, create a consented referral, share organized records, receive questions and a preliminary opinion, and remain informed through treatment and follow-up. A hospital receives a qualified, complete case, assigns a doctor, issues a structured response and quotation, tracks conversion, and retains the referring relationship. The platform coordinates; licensed clinicians make clinical decisions.

### What it is not

- Not “find cheap treatment in India.”
- Not a hospital listing or pay-to-rank marketplace.
- Not LinkedIn with medical job/news/social features.
- Not a generic CRM sold without a demand advantage.
- Not an AI diagnostic or treatment-recommendation product.
- Not a travel marketplace with healthcare branding.
- Not an agent network that pays doctors for patient procurement.

## The product's four connected surfaces

1. **Professional Doctor Network:** Verified professional identity, focused discovery, relationship requests, bounded messaging, and referral initiation.
2. **Patient Case Workspace:** The consented case, records, participants, questions, responses, next actions, and handback.
3. **Hospital International Patient CRM:** Case qualification, assignment, response, proposal/quote, pipeline, conversion, and referring-doctor relationship management.
4. **Platform Operations:** Verification, completeness, matching, SLA chasing, coordination, exceptions, and commercial measurement.

Each surface is incomplete without the other three. A standalone directory has no transaction; a standalone patient portal has no supply; a standalone hospital CRM has no differentiated demand; a managed service without software does not accumulate a reusable network or workflow history.

## What makes users repeatedly use it

### Referring doctors return when

- named specialists respond reliably;
- the structured referral takes less time than email/WhatsApp chasing;
- they can reuse their verified identity and professional relationships;
- the patient is not silently taken away from their care;
- opinion, discharge, and follow-up documents return to them where authorized;
- past collaboration makes the next referral faster and more predictable;
- participation is free and does not depend on ethically problematic referral payments.

### Indian specialists return when

- incoming cases are relevant, organized, and answer a clear clinical question;
- administrative coordination stays with hospital/platform staff;
- authorship and boundaries are clear;
- repeated referrers learn what information the specialist needs;
- the tool produces professional relationships, not spam or vanity engagement.

### Hospitals stay when

- the network produces qualified cases they would not otherwise receive or helps recover cases currently lost in manual channels;
- response time, completeness, conversion, arrival, and source can be measured;
- referrer relationships belong to an institutional workflow rather than an employee's private phone;
- coordinators spend less time chasing documents and status;
- international-market decisions use actual corridor/referral evidence;
- the system becomes the operating record for cross-border pre-arrival work even if the hospital EHR remains the clinical record.

### Patients use it when

- a trusted doctor introduces it, or the platform can establish equivalent trust;
- they submit once, know who has access, and receive a named, attributable response;
- a real human owns the next step;
- uncertainty and cost assumptions are clearer than in informal agent channels.

---

# 2. MARKET WEDGE: ONE CORRIDOR, NOT GLOBAL HEALTHCARE

## Corridor definition

A launch corridor is:

`one source country or tightly similar pair + one defined referrer segment + one or two planned-care specialties + two to five Indian hospital partners + one operating playbook`

“Africa,” “GCC,” or “international oncology” is not a corridor. A usable example is “independent oncologists and internal-medicine referrers in two Kenyan cities sending selected adult solid-tumour cases to three Indian cancer centres.” The final corridor must come from evidence, not this document.

## Characteristics of a good first corridor

### Patient and clinical characteristics

- Existing, observable patient movement to India rather than hypothetical demand.
- Planned, non-emergency cases that tolerate a structured remote review window.
- Meaningful specialist/capability or affordability gap in the source country.
- Records can support a responsible preliminary review before travel.
- Treatment value is high enough that the hospital cares about conversion, while coordination cost is a reasonable fraction of value.
- A local clinician is needed after return, strengthening the closed-loop value.
- A reasonably repeatable minimum document set and care pathway.
- Excludes or tightly controls pathways with exceptional ethical/regulatory complexity in V0.

### Distribution characteristics

- Referring doctors can be identified and reached through credible institutions or relationships.
- Some already refer abroad but lack reliable Indian relationships or closed-loop status.
- Two to five Indian hospitals actively want this exact source market and specialty.
- A local clinical/association champion can establish trust.
- Competition is fragmented or transactional enough that relationship continuity is a meaningful wedge.

### Operating characteristics

- Language and medical translation can be served by the small team.
- Travel route and visa process are workable for planned cases.
- Source-country and Indian professional/privacy/referral rules can be responsibly operationalized.
- Payment, sanctions, insurance, and currency frictions do not make the corridor impractical.
- Expected response SLA is achievable with the chosen hospital departments.

## Corridor scorecard

Score each candidate from 1–5 using evidence, multiply by the weight, and do not launch unless it clears a founder-set threshold and has no legal/safety stop.

| Criterion | Weight | Evidence required before scoring |
|---|---:|---|
| Existing patient movement to India | 15 | Hospital origin data, interviews, official/industry evidence, recent cases. |
| Reachable referring-doctor channel | 15 | Named doctors/associations, response rates, pilot commitments. |
| Indian hospital demand and capacity | 15 | Named service-line/IPD champions, review SLA, pilot terms. |
| Clinical/cost gap and willingness to travel | 10 | Referrer and patient interviews; alternative destinations/local care. |
| Planned case value and hospital economics | 10 | Real anonymized quote ranges and contribution logic from hospitals. |
| Need for home-doctor continuity | 10 | Workflow interviews and evidence of current handback failures. |
| Visa/travel/payment feasibility | 10 | Current official rules and actual recent journeys. |
| Language and operating fit | 5 | Required staffing/translation and document-language mix. |
| Regulatory/ethical tractability | 5 | Counsel review; no unresolved launch-stopping issue. |
| Competitive space for a relationship wedge | 5 | Mystery shopping, hospital/referrer interviews, incumbent response quality. |

## Illustrative corridor hypotheses—not selections

| Corridor hypothesis | Why it could work | Why it could fail | What to validate first |
|---|---|---|---|
| **Kenya → India → oncology** | English professional communication; high need for specialist opinions; complex cases benefit from records and home-doctor continuity; hospitals value oncology cases. | Time-sensitive disease, pathology/imaging complexity, financial barriers, existing facilitators and direct hospital channels, and variable ability to travel. | Ten oncology/internal-medicine referrer interviews; three hospital oncology/IPD SLAs; five recent patient journey reconstructions; payment and follow-up reality. |
| **Oman → India → cardiac care** | Geographic proximity, potential institutional referrers/payers, high-value planned interventions, and hospitals may invest in the corridor. | Strong regional alternatives; Arabic service needs; insurer/government pathways; established bilateral relationships; cross-border consultation rules. | Who controls referral decisions, payer authorization, doctor incentives, hospital gap, and whether independent doctors can originate cases. |
| **Bangladesh → India → complex surgery** | Existing travel habit, geographic/cultural proximity, substantial provider awareness, and potentially high case volume. | Intense hospital/broker competition, direct relationships already strong, visa/political variability, price sensitivity, and weak differentiation. | Whether doctors lack a closed-loop tool, whether hospitals will pay for incremental rather than existing demand, and whether a narrow subspecialty creates a genuine gap. |

## Specialty selection guardrails

Favour specialties with planned timelines, interpretable pre-arrival records, high coordination value, a meaningful local capacity gap, and feasible home-doctor follow-up. Do not start with a specialty merely because treatment values are high.

- **Potential:** selected oncology pathways, planned cardiac interventions, complex orthopaedic/spine surgery, selected neurosurgical pathways.
- **Treat cautiously:** clinically urgent oncology/cardiac cases that cannot tolerate platform delay.
- **Do not include in V0 without a dedicated reviewed programme:** transplant procurement/listing, fertility/surrogacy, experimental treatment, emergency transfer, organ/tissue matching, and other pathways with exceptional legal/ethical complexity.

## Corridor selection gate

Select the first corridor only when all are true:

1. At least 20 reachable relevant foreign doctors are named, 10 interviewed, and 5 willing to test the referral workflow.
2. At least two Indian hospitals commit named clinical/IPD owners and a written preliminary-review SLA.
3. Five recent patient journeys demonstrate the same material coordination failure.
4. At least one hospital agrees to a paid or contractually committed pilot tied to measurable value.
5. Counsel finds no unresolved stop around referral conduct, data transfer, telemedicine, marketing, or commercial terms.

---

# 3. BUSINESS MODEL AND RECOMMENDATION

## Revenue-model evaluation

| Model | Who pays | What they pay for | Why pay / measurable value | Likely sales friction | Incentive conflicts | Timing verdict |
|---|---|---|---|---|---|---|
| **A. International Patient CRM SaaS** | Hospital group, facility, or international-patient department. | Seats/facilities/case capacity for referral intake, case pipeline, documents, assignment, SLA, proposal/quote, source/referrer relationship, conversion, and follow-up. | Reduced time to complete case; faster response; fewer lost cases; coordinator capacity; attributable conversion; institutional retention of referral relationships. | Existing CRM/email; integration/procurement/security reviews; no budget for another point tool; switching costs; hospitals may want customization. | Hospital priorities may favour conversion over neutrality; usage can become sales surveillance. | **EARLY/MVP only when bundled into a corridor pilot.** Pure self-serve SaaS is not the first sell. |
| **B1. Fixed successful-case fee** | Hospital, under a reviewed services/marketing/coordination agreement. | A fixed amount when a precisely defined milestone occurs, such as verified arrival/admission—not a percentage of treatment. | Hospital pays for attributable acquired demand and coordination only after value occurs. Measure selected/arrived cases and incremental source. | Attribution disputes, cancellations, long cycles, delayed reporting/payment, procurement, and hospitals pushing fee risk downstream. | Can bias routing toward payer/provider revenue and create pressure to mark success; may be treated as problematic referral economics. | **LATER/conditional.** Only after legal/ethical review, transparent disclosure, and neutral routing controls. |
| **B2. Qualified-case/lead fee** | Hospital. | Each case meeting agreed completeness, consent, specialty, geography, and intent criteria, regardless of treatment. | Predictable acquisition price; platform paid for genuine work. Measure accepted-for-review rate and completeness. | Hospitals resist paying for non-conversion; disputes over “qualified”; encourages volume over fit. | Incentivizes oversharing/multiple sale and low-quality routing; especially poor for patient trust. | **DO NOT USE initially.** Revisit only with strict exclusivity/quality rules. |
| **B3. Platform access/marketing fee** | Hospital. | Participation in a corridor/network, profile, review capacity, and campaign access. | Budget-compatible for international business development; predictable cost. | Looks like listing/advertising; hard to prove value; incumbents already sell visibility. | Pay-to-play can influence discovery and undermine verification. | **MVP only as the fixed corridor contract—not sponsored ranking.** |
| **C. Enterprise network access** | Hospital group/enterprise international business team. | Verified referrer graph, relationship CRM, corridor coverage, institutional referral history, analytics, multi-facility routing, governance, and SLAs. | Builds an owned repeat-referral channel, reduces relationship loss when staff leave, and informs country investment. | Requires network density and proof; enterprise security/integration; long sales cycle; buyers may try to build. | Hospitals may pressure exclusive referrals or surveillance of doctors. | **LATER**, after a corridor has active relationships and repeat referrals. |
| **D. Patient concierge** | Patient/family pays a disclosed fixed fee; optionally hospital sponsors it. | Defined non-clinical package: interpreter, ground transport, accommodation shortlist/booking assistance, dedicated admin support. | Convenience, language support, one accountable coordinator. Measure service completion and satisfaction. | Patients expect facilitation free; refund/service failures; local partner quality; support burden. | Hidden markups, steering, tying care access to payment, confusing facilitator and provider roles. | **EARLY/LATER, not core MVP revenue.** Start with pass-through or hospital-provided options; charge only after demand and terms are clear. |
| **Doctor membership/premium networking** | Doctor. | Profile/discovery/messaging/referral tools. | Possible professional productivity value. | Doctors resist paying without dense network and guaranteed responses. | Paid visibility and two-tier patient access damage trust. | **DO NOT USE initially.** Doctors join free. |
| **Advertising/sponsored placement** | Hospitals, pharma, recruiters, others. | Attention/ranking/content placement. | Scalable in a large network. | Requires audience scale; contaminates product focus. | Serious conflict with neutral routing and professional trust. | **DO NOT USE.** |
| **Travel-partner commission** | Travel/accommodation/transport partner. | Introduction or booking. | Small ancillary revenue. | Low revenue relative to oversight burden; attribution and refunds. | Biased recommendations and hidden markup. | **LATER at most**, disclosed with equivalent non-commission options. |

## Recommended initial monetization: the paid corridor operating pilot

Sell one thing:

> **A fixed-fee, 90–180 day hospital corridor pilot that combines access to a recruited/verified referrer cohort, structured international case intake, managed response-SLA operations, and a shared conversion/relationship record.**

The pilot includes a defined source country, specialty, facilities, named hospital users, expected case capacity, response SLA, coordinator support, reporting, and a jointly agreed success review. It does not sell ranking, promise patient volume, pay doctors, or charge a percentage of treatment.

Why this is the best starting model:

- It sells the outcome hospitals care about—new and better-managed international demand—not software theatre.
- Fixed pricing avoids early commission ambiguity and lets the team learn true operating cost.
- The hospital has skin in the game: named staff, response commitments, and a real budget owner.
- It produces evidence for later annual SaaS/network contracts and, if cleared, fixed case-coordination fees.
- It exposes the thesis quickly: if no hospital will fund a tightly scoped pilot after seeing named referrers and workflow, the product probably does not yet create enough commercial value.

Do not offer a permanently free hospital pilot. A discounted design-partner price is acceptable, but at least one partner must pay money or make a binding procurement commitment before major build-out.

## What must exist before a hospital pays recurring SaaS

1. A material number of cases arrive through or are recovered by the platform.
2. Hospital staff actually work the queue rather than forwarding everything back to WhatsApp/email.
3. Median time from complete case to attributable response improves.
4. Source/referrer attribution survives staff handoffs.
5. The system shows accepted, declined, quoted, selected, arrived, lost, and follow-up outcomes.
6. A coordinator can manage more cases or fewer cases are lost/stalled.
7. The network has repeat referrers or a credible path to them.
8. Implementation and security burden is lower than configuring the same workflow in the hospital's existing CRM.

---

# 4. WHY AN INDIAN HOSPITAL WOULD PAY

## The honest answer

A hospital will not pay because the interface is cleaner. It may pay if the platform creates an **incremental, attributable, repeatable international referral channel** and measurably improves the conversion of those cases. The CRM is the delivery mechanism and retention layer, not the original reason to buy.

Hospitals already advertise many of the journey services contemplated here. For example, [Apollo's international patient programme](https://www.apollohospitals.com/international-patient-services/plan-your-visit) describes expert opinions, cost explanations, visa invitation letters, accommodation, interpretation, and airport assistance. [Max](https://www.maxhealthcare.in/hospitals-in-india) and [Fortis](https://www.fortishealthcare.com/international-patients) also describe international coordinators and second-opinion/coordination services. Therefore duplicating concierge functions creates little leverage.

## Willingness-to-pay ranking

| Rank | Value source | Likely willingness to pay | Why |
|---:|---|---|---|
| 1 | **Qualified international demand** | Very high if demonstrably incremental | Direct revenue opportunity; the hospital can compare acquisition cost and realised treatment value. |
| 2 | **Better conversion** | High | Faster, complete, trusted responses can convert more existing and sourced inquiries into selected/arrived cases. |
| 3 | **Verified referring-doctor network** | High once active | A repeat professional channel is more defensible and lower-churn than anonymous leads or individual agents. |
| 4 | **Shorter response times** | High when tied to conversion | Slow clinical/quote response loses cases; SLA evidence can change departmental behaviour. |
| 5 | **Better case completeness** | Medium-high | Clinicians review faster and coordinators avoid repeated chasing; value is measurable in touches and elapsed time. |
| 6 | **Less manual document chasing** | Medium | Real labour savings, but alone may not justify a new system or enterprise sale. |
| 7 | **Referral relationship management** | Medium initially; high with repeats | Becomes valuable when relationships and referral history would otherwise sit on personal phones or leave with staff. |
| 8 | **International pipeline visibility** | Medium | Useful to managers, but generic CRMs can provide dashboards if data is entered consistently. |
| 9 | **Country/source analytics** | Low initially; medium at scale | Ten cases do not produce strategic intelligence; hundreds of attributable cases might. |
| 10 | **Continuity with home-country doctor** | Clinically high, direct WTP initially low | Supports trust, outcomes, and repeat referrals, but needs evidence that it improves acquisition/retention or strategic brand value. |

## The hospital ROI equation

The pilot business case should be expressed without invented outcomes:

`Incremental gross contribution from arrived cases`

`+ coordinator time saved`

`+ value of recovered/stalled cases`

`+ value of retained repeat-referrer relationships`

`− platform fee`

`− implementation and staff time`

`− any added coordination/service cost`

A hospital renewal requires the left side to be credibly positive. “Leads generated” is not an ROI measure.

## Proof required in the pilot

- Unique, consented referrals attributable to the corridor/network.
- Percentage accepted for review and reasons for decline.
- Completeness at first hospital review and number of information-request loops.
- Time to accept, ask, issue opinion, and issue quote.
- Proposal sent → selected → arrived/admitted conversion.
- Lost reasons and cases recovered by intervention.
- Active/referring/repeat doctor count.
- Coordinator touches and approximate handling time.
- Hospital-user adoption inside the workflow.

---

# 5. WHY FOREIGN DOCTORS PARTICIPATE

## The job to be done

“Help me get my patient to a trustworthy specialist I can reach, without wasting my time or losing continuity.”

## Participation value

- Free verified professional identity and visibility to relevant peers.
- Access to a curated set of Indian specialists with known hospital affiliation and response path.
- A concise structured referral instead of repeated messages and attachments.
- Acknowledgement that a named human owns the case.
- Ability to ask a clear clinical question and receive an attributable response.
- Visibility into whether records are missing, review has begun, and handoff is complete.
- Discharge/follow-up return to the home doctor where the patient permits.
- Relationship memory: the next referral goes to a known collaborator with prior context.
- No expectation to sell, promote, pay membership, or accept patient-referral compensation.

## What destroys doctor adoption

- Unsolicited patient lead spam or hospital sales outreach.
- A social feed, vanity metrics, or pressure to create content.
- Slow/no specialist response after the doctor spends time preparing a case.
- Patient poaching or failure to return follow-up information.
- Profiles that look “verified” without credible evidence.
- Unclear professional responsibility or cross-border consultation scope.
- Re-entering data the patient/hospital already provided.
- Hidden commissions or routing incentives.

## The required service promise

For the first corridor, the platform should promise only operational behavior it can control:

- acknowledge a complete referral within a defined business window;
- tell the referrer who owns it;
- provide an accept/decline/information-needed response within the partner SLA;
- return issued opinion/discharge materials where authorized;
- explain delay or closure rather than allow silent failure.

Do not promise a clinical opinion by a fixed deadline unless partner doctors have contractually committed capacity.

---

# 6. NETWORK EFFECT AND DEFENSIBILITY

## Is there a genuine network effect?

Potentially—but not from profile count.

A weak network is a directory: more doctors create more search results, but little additional value and low switching cost. A strong network forms when each completed referral creates a useful professional edge and makes the next referral more likely and easier.

The primary graph is:

`Doctor ↔ professional relationship ↔ Doctor`

`Doctor → Referral → Patient Case → Provider Review → Doctor/Hospital`

`Hospital → response/coordination → treatment milestone → follow-up → Referring Doctor`

## Data that makes the network more valuable as it grows

Only operational, permissioned, non-outcome-ranking data should drive early value:

- Verified identities, licence jurisdictions, specialties, subspecialties, languages, and current hospital affiliations.
- Explicit professional connections and introductions.
- Which corridors and case types a doctor/hospital is willing and able to review.
- Structured referral requirements learned by specialty and receiving team.
- Prior collaboration between particular doctors and institutions.
- Referral acknowledgement, acceptance, response, and follow-up completion.
- Typical response intervals and reliability, with minimum sample sizes and internal context.
- Repeated referral relationships and last interaction.
- Hospital/department capacity declarations and coordinator ownership.
- Case stage, closure reason, and whether handback occurred.
- Patient preferences and outcomes only in lawful, appropriately aggregated forms—not public clinician scoreboards.

## Why a competitor cannot win by copying the UI

They can copy every screen. They cannot instantly copy:

- verified active relationships with source-country doctors;
- trust earned by reliably closing prior referrals;
- hospital departments that have committed named reviewers and SLAs;
- structured history of who responds well to which referral type;
- corridor-specific operations, language, documents, escalation paths, and local champions;
- embedded referrer relationship records used by hospital teams;
- proof that the platform returns the patient to the home doctor rather than acting as a one-time broker.

These assets become defensible only through real use. A database of scraped profiles is not a moat.

## Return and retention mechanisms

### What makes doctors return after the first case?

- The prior specialist relationship appears first for relevant future referrals.
- Referral templates remember the receiving team's required information.
- The doctor can see all active/closed referrals and outstanding handbacks.
- The platform reliably reaches a human when a case stalls.
- The next case avoids re-verification and repetitive administrative setup.
- Collaboration produces professional recognition inside a relevant closed network, not public popularity.

### What makes hospitals stay?

- Continued access to an active referrer cohort.
- Historical referral relationships and source attribution embedded in team workflow.
- Repeat referrers and conversion evidence unavailable in generic lead channels.
- Coordinator and department behavior organized around response SLAs.
- Cases, messages, and next actions do not disappear when staff leave.
- Corridor analytics improve recruitment, outreach, language staffing, and service-line investment.

### What creates liquidity?

Liquidity is not “doctors registered.” It is the probability that an eligible referral receives a useful, attributable response quickly enough to influence the patient's decision.

Measure liquidity by:

- active verified referrers with a case in the last 90/180 days;
- referral coverage by target specialty;
- partner departments with current review capacity;
- accepted-for-review rate;
- complete-case-to-opinion time;
- percentage of referrals receiving a usable response;
- repeat-referral and handback rates.

## Cold-start problem

Doctors will not join an empty network; hospitals will not pay without cases; patients will not trust unknown providers; and cases will not close if specialists do not respond. A broad launch makes every segment look empty.

## Manual cold-start plan for the first 50–100 doctors

1. Select one corridor and build a list of 100 high-fit referrers, not 10,000 generic physicians.
2. Recruit 10–20 anchor referrers through existing hospital relationships, personal introductions, associations, and small clinical roundtables.
3. Onboard two to five hospital partners with named IPD and specialty champions before asking doctors to refer.
4. Manually verify every doctor and pre-populate only evidence-backed profile facts for their review.
5. Conduct concierge onboarding calls; capture which specialists/pathways each referrer actually needs.
6. Offer facilitated introductions to a small receiving-specialist roster.
7. Personally operate the first referrals and enforce response/handback promises.
8. Ask each satisfied referrer for one peer introduction—not a public follower campaign.
9. Hold small case-process reviews (using appropriately de-identified or consented material), not content-feed engagement campaigns.
10. Remove inactive/unresponsive supply from discovery until capacity returns.

The first network metric is not signups. It is **number of verified referrers who completed one closed-loop referral and indicated intent to use the same relationship again**.

---

# 7. SURFACE 1 — PROFESSIONAL DOCTOR NETWORK

## Doctor profile prioritization

| Tier | Profile information/function | Product decision |
|---|---|---|
| **Fundamental** | Professional name; country/city; current specialty/subspecialty; regulator and licence/registration verification state/date; current hospital affiliation; core qualifications; languages; defined clinical interests/procedures; accepts cross-border referrals; case-review/remote-consult availability as a declared state; contact through platform. | Enough to determine identity, relevance, current institutional context, and whether a referral can be attempted. |
| **Useful / early** | Professional photo; years of practice with basis; prior affiliations; appointment/review preferences; required referral documents; referral response expectation; concise biography; selected leadership/teaching roles. | Improves trust and case completeness after the basic loop works. |
| **Bonus** | Publications imported from authoritative identifiers; research interests; trials/research collaboration; peer introductions; corridor experience; professional events. | Valuable to a mature professional network, not required to close V0 referrals. |
| **Do not build yet** | Followers, public endorsements, star ratings, popularity, badges for activity, “top doctor” awards, posts, reels, news feed, patient testimonials as ranking, sponsored expertise. | Creates noise, gaming, solicitation, moderation cost, and misleading quality signals. |

“Verified” must always mean a specific claim was checked against a source on a date. The [NMC register](https://www.nmc.org.in/information-desk/indian-medical-register/) itself notes updating limitations, so V0 verification remains manual and evidence-based rather than a permanent automated badge.

## Doctor discovery V1

### Required search/filter

- Name.
- Specialty.
- Subspecialty or controlled procedure/case-interest tag.
- Current hospital/facility.
- Country/city.
- Language.
- Currently accepts international referral review.

### Search result behavior

- Show only verified/approved professionals to referral users.
- Display why a result matches the selected criteria.
- Default order by explicit relevance and availability rules, not payment or popularity.
- Allow a case manager to present a curated shortlist.
- Make clear that discoverability is not a treatment recommendation.

### Not V1

Free-form symptom search, outcomes ranking, live calendar inventory, distance maps, insurance-network search, price filter, reviews, followers, and opaque “smart” ranking.

## Professional connections: decision by action

| Action | Decision | Rationale |
|---|---|---|
| **Connect / accept / decline** | **Fundamental but lightweight.** | Creates an explicit professional relationship and permission for limited non-case communication. |
| **View own connections** | **Fundamental.** | Makes past collaborators reusable for future referrals. |
| **Introduce doctor** | **Early.** | High-trust growth mechanism, but a case manager can perform it manually in V0. |
| **Follow** | **Do not build.** | No feed or content model exists; following adds no core value. |
| **Endorse skills** | **Do not build.** | Easy to game and unsafe as a quality signal. |
| **Recommend doctor publicly** | **Do not build.** | Risks misleading claims and social-pressure dynamics. Private referral history is more useful. |
| **Remove/mute/report connection** | **Fundamental.** | Required to control spam, harassment, and unwanted solicitation. |

## Doctor messaging

### Product decision

Most clinical communication must be **case-bound**. Generic doctor-to-doctor messaging should exist only in a constrained form after a connection is accepted.

### V0 rules

- A doctor may send a connection request with one short professional note.
- Before connection, no open inbox chat and no attachment/patient data.
- After connection, limited non-case professional messaging supports introduction, capability clarification, and invitation to create a referral.
- Any patient-specific discussion must move into a consented referral case.
- Case messages identify the patient case, participants, sender role, and audience; clinical responses stay attributable.
- Rate limits, block/report, organization policy, and admin review control spam.
- Hospitals cannot bulk-message foreign doctors or scrape/export the directory for sales.
- Patient solicitation, referral-payment offers, and requests to move sensitive records to personal channels violate network rules.

## Core specialist-referral workflow

1. **Find:** Referrer searches by specialty/subspecialty/procedure, language, hospital, and current international-review status.
2. **Assess:** Referrer views verified facts, hospital affiliation, declared focus, response route, and any existing relationship.
3. **Connect or refer:** An existing connection is helpful but not mandatory. A referrer may send a referral request directly to a specialist/hospital under platform controls.
4. **Name the clinical question:** Referrer states what review is requested and the known/uncertain diagnosis, without the platform rewriting it.
5. **Identify patient and authority:** Patient receives an invitation to verify contact, see the notice, authorize the referral and record sharing, and optionally invite a family member. Approved exceptions require a reviewed operating rule.
6. **Build referral packet:** Patient/referrer supplies structured summary, relevant history, prior treatment, medication/allergy context, and categorized records.
7. **Submit:** Referrer confirms accuracy/source, patient consent is active, and the packet is sent to platform review—not automatically to every hospital.
8. **Completeness review:** Case manager checks readability, chronology, required fields, duplicates, and corridor fit; the referrer answers administrative gaps.
9. **Route:** Case manager sends a distinct provider review request to an eligible partner hospital/specialist with an SLA.
10. **Acknowledge:** Hospital accepts, declines, or requests information; referrer and patient see the attributed status.
11. **Clarify:** Assigned specialist asks case-bound questions. Referrer/patient answers or provides records.
12. **Respond:** Specialist issues an attributable preliminary opinion; hospital adds a separate proposal and indicative quotation.
13. **Discuss:** Referrer and patient review the response; a permitted consultation can be scheduled using the hospital's process.
14. **Decide and hand off:** Patient selects, declines, or requests another route. If proceeding, hospital/platform coordinates pre-travel.
15. **Close the loop:** Treatment milestones remain high-level; discharge/follow-up documents return to patient and referring doctor where authorized; the professional relationship remains for future cases.

### Referral success condition

A referral is not “successful” when sent. It is operationally closed-loop when it has a final provider disposition, the patient/referrer received the attributable response, any treatment handoff is recorded, and promised follow-up documents are returned or a documented reason explains why not.

---

# 8. SURFACE 2 — PATIENT CASE WORKSPACE

## Fundamental for the first real cases

| Capability | Minimum functional behavior | Can human operations supplement it? |
|---|---|---|
| Patient and case identity | Distinguish patient, submitter, referrer, and family delegate; show case reference and source. | Exceptions and identity review are manual. |
| Clinical/referral summary | Structured reason for referral, known diagnosis/history as sourced, treatment sought, and clinical question. | Case manager helps complete but does not diagnose. |
| Participants and access | Show patient, referrer, receiving hospital/team, case manager, and current sharing scope. | Case manager resolves permission exceptions. |
| Consent | Patient-facing approval for case processing and named/defined sharing; record state and revocation. | Language/capacity assistance is manual. |
| Medical records | PDF/image upload, categories/dates, original preservation, download/view based on access. | Staff classify, chase, rotate, translate externally, and handle large imaging separately. |
| Information requests | Named requester asks for a specific item; patient/referrer answers, links, or marks unavailable. | Staff relays and clarifies. |
| Case-bound messaging | Patient/referrer/case manager/hospital communicate with visible author and audience. | Calls and approved off-platform contact are summarized manually. |
| Status and next action | Current simple stage, owner, due/expected date, and latest material event. | Case manager drives every transition. |
| Specialist response | Display/download signed or attributable preliminary opinion and limitations. | Hospital may upload a document rather than use a complex builder. |
| Proposal and quote | Show pathway, stay assumptions, indicative cost, inclusions/exclusions, validity, and author/version. | Case manager checks and normalizes manually. |
| Patient decision | Proceed, need clarification, not proceeding, or pause; attributable confirmation. | Case manager confirms offline decisions. |
| Pre-travel readiness | Simple checklist/status and secure invitation-document area after selection. | Visa, travel, accommodation, transport, and interpreter work is mostly manual. |
| Discharge/follow-up handback | Hospital uploads discharge/follow-up documents; patient authorizes/receives; referrer receives where permitted. | Case manager chases and confirms handback. |

## Important but not required before case #1

- Side-by-side multi-hospital comparison.
- Appointment self-scheduling.
- Structured travel itinerary/partner portal.
- Payment reconciliation inside the platform.
- Native translation workflow.
- Patient mobile app.
- Self-service access/deletion administration beyond a supported request path.

## Case-workspace product rule

The workspace should answer five questions on one page:

1. What is this case asking?
2. Who currently has it and is allowed to see it?
3. What information is missing?
4. What response has been issued?
5. Who must do what next, by when?

Anything else is secondary in V0.

---

# 9. SURFACE 3 — HOSPITAL INTERNATIONAL PATIENT CRM

## Minimal viable CRM thesis

The hospital interface must turn a structured referral into a timely response and measurable outcome. It is not a replacement EHR, full billing system, or general hospital CRM.

## Practical pipeline

| Stage | What happens | Primary owner | Action that moves it forward | Required data | Common blockers |
|---|---|---|---|---|---|
| **NEW CASE** | Shared referral arrives and is acknowledged. | IPD intake/coordinator. | Accept for qualification, decline, or request admin correction. | Source, country, specialty, consent/share, summary, documents, received time. | Wrong facility, duplicate, missing authority, unowned inbox. |
| **ACCEPTED FOR REVIEW** | Hospital commits to evaluate within SLA. | IPD coordinator. | Assign verified specialist and case coordinator. | Acceptance, SLA, assigned department, owner. | No specialist/capacity, unclear commercial ownership. |
| **INFORMATION REQUIRED** | Specific missing record/question blocks or qualifies review. | Assigned specialist for clinical items; coordinator for admin items. | Issue structured request; patient/referrer responds or marks unavailable. | Item, reason, requester, due date, blocking state. | Unavailable tests, poor scans, translation, no patient response. |
| **MEDICAL REVIEW** | Assigned specialist reviews the authorized packet. | Indian specialist. | Issue opinion, decline as unsuitable, or ask another question. | Reviewed-document set, clinical question, author, start time. | Incomplete data, wrong specialty, competing clinical workload. |
| **OPINION READY** | Attributable preliminary response is complete. | Specialist; coordinator checks delivery. | Approve/issue response and start proposal. | Opinion, limitations, suggested pathway/tests, author/date. | Unsigned response, ambiguous pathway, clinician delay. |
| **QUOTE READY** | Hospital turns pathway into operational proposal and estimate. | IPD + finance; clinician owns clinical fields. | Authorize version for sending. | Facility/doctor, stay, timing, range, currency, assumptions, inclusions/exclusions, validity. | Implant/consumable uncertainty, finance delay, missing package rules. |
| **SENT** | Patient/referrer receives the response. | Coordinator. | Confirm delivery and set decision follow-up. | Sent version, recipients, date, questions contact. | Channel failure, language, incomplete response. |
| **PATIENT DECIDING** | Clarifications/consultation occur. | Patient; coordinator facilitates. | Record proceed/not proceed/pause or schedule consultation. | Decision due/next touch, questions, competitor unknown, quote expiry. | Price, trust, financing, second opinion, no response. |
| **SELECTED** | Patient chooses this hospital, provisionally. | IPD coordinator. | Hospital confirms capacity/conditions and opens pre-arrival. | Patient confirmation, selected proposal, tentative timing, conditions. | Doctor/date changed, deposit, clinical change. |
| **PRE-ARRIVAL** | Invitation, visa, appointment, travel readiness, and pre-arrival instructions are coordinated. | Hospital coordinator + platform case manager. | Confirm visa/itinerary/readiness and appointment. | Passport only as needed, hospital letter, self-reported visa status, arrival plan, contact. | Visa refusal/delay, changed dates, fitness concern, funding. |
| **ARRIVED** | Arrival/hospital handoff is confirmed. | Hospital coordinator. | Confirm first appointment/check-in. | Arrival confirmation, location/contact, exception. | Missed flight/pickup, deterioration, identity mismatch. |
| **ADMITTED** | Hospital completes its own registration and in-person assessment. | Hospital admissions/clinical team. | Confirm admission or revised plan; record hospital reference. | Admission confirmation and high-level variance. | New clinical findings, bed, deposit, consent. |
| **TREATMENT** | Care is delivered in hospital systems; platform tracks only agreed milestones. | Treating team/IPD. | Record high-level progress or material coordination change. | Current milestone, revised estimate/proposal if communicated. | Complication, changed procedure, longer stay, dispute. |
| **DISCHARGED** | Hospital issues discharge pack and final coordination instructions. | Treating team + coordinator. | Upload/share permitted documents and schedule handback. | Discharge date, summary, medication/instructions, follow-up, billing status. | Unsigned/missing reports, translation, balance dispute. |
| **FOLLOW-UP** | Patient/home doctor and Indian team complete agreed handback/review. | Hospital clinician/coordinator. | Respond to follow-up, confirm local handover, or escalate. | Follow-up due, recipients, returned documents, unresolved question. | Home doctor absent, lost patient, clinical deterioration. |
| **CLOSED** | Referral outcome and relationship record are finalized. | Coordinator/manager. | Select closure/lost reason and next referrer action. | Final outcome, dates, lost reason, next relationship task. | Missing handback, open complaint/payment, no outcome evidence. |

Declined, not selected, patient unresponsive, visa not obtained, transferred, and deceased are outcome reasons/branches rather than normal progress stages. Multiple hospital review requests remain separate; a decline by one hospital does not close the patient case.

## Hospital capability prioritization

### Fundamental

1. Incoming case queue.
2. Case/referral source, country, specialty, and completeness.
3. Authorized document view.
4. Accept/decline/request information.
5. Assign verified doctor and coordinator.
6. Case-bound questions/messages.
7. Upload/issue attributable opinion.
8. Create/upload structured proposal and quote.
9. Stage, next action, owner, timestamp, and SLA due state.
10. Patient decision/selected/lost reason.
11. Pre-arrival through follow-up high-level tracking.
12. Referring-doctor identity and relationship history for that hospital.
13. Staff role/access administration and audit trail.

### Useful / early

- Reusable specialty document checklists.
- Proposal/quotation templates and version comparison.
- Pipeline filters and manager dashboard.
- Coordinator workload and SLA escalation.
- Appointment and travel checklists.
- Basic source-country/referrer conversion reports.
- Repeat-referrer tasks and relationship notes.
- Multi-facility routing within one hospital group.
- Final estimate-versus-actual reconciliation fields.

### Bonus

- Existing CRM/EHR/document-system integrations.
- Capacity/availability feeds.
- Advanced cohort and corridor analytics.
- Configurable automation and risk alerts.
- Proposal translation assistance.
- Hospital-group portfolio routing.
- Referrer engagement campaigns with strict consent/governance.

### Do not build yet

- Full EHR/EMR, clinical orders, medication, nursing, or inpatient chart.
- Full hospital billing/payment/refund system.
- Generic domestic lead CRM.
- Marketing automation suite.
- Call centre/telephony platform.
- Dozens of custom hospital integrations.
- AI clinical prioritization or diagnosis.

---

# 10. SURFACE 4 — PLATFORM OPERATIONS

## Smallest console for 10–100 cases

| Capability | Needs product functionality in V0? | What remains manual |
|---|---|---|
| Doctor verification | **Yes:** evidence upload, status, source/date, approve/reject/suspend, visible result. | Regulator search, identity comparison, affiliation call, recheck. |
| Hospital verification | **Yes:** organization/facility status and authorized users. | Contracts, licence/accreditation review, bank/signatory verification. |
| Patient/case review | **Yes:** queue, case view, completeness state, owner, notes. | Contact call, judgement, exception resolution. |
| Case completeness | **Yes:** required/missing list and request action. | Decide relevance/readability and chase records. |
| Provider routing | **Yes:** select recipient and create isolated provider review request. | All matching and conflict/capacity confirmation. |
| Hospital response tracking | **Yes:** SLA timestamps, status, owner, escalation flag. | Call/message hospital, negotiate deadline, reroute. |
| Communications | **Yes:** case-bound messaging and material call-note capture. | Phone/approved external channel use and human translation. |
| Consent/access overview | **Yes:** who can see case/documents and why; revoke future access. | Capacity/guardian and legal exceptions. |
| Status/next action | **Yes:** controlled stages, owner, due date, history. | Decide and execute the next step. |
| Proposal normalization | **Minimal:** structured fields and original attachment/version. | Check assumptions, query omissions, prepare human explanation. |
| Visa/travel | **Minimal:** selected-case checklist and document status. | Rule checking, letter chase, itinerary/accommodation/transport coordination. |
| Escalations/complaints | **Minimal:** flag, owner, notes, status, evidence link. | Triage, investigation, external escalation, resolution. |
| Commercial tracking | **Yes:** hospital, source, case milestone, pilot attribution, fee status. | Invoicing/reconciliation can remain existing finance process. |
| Audit history | **Yes:** access/share/status/artifact events. | Periodic review and evidence export. |
| Analytics | **Minimal:** case counts, response time, conversion stages, referrer activity. | Analysis in controlled exports for early pilots. |

## Operating doctrine

- One named platform case manager owns each active case.
- One named hospital coordinator owns each accepted provider request.
- Every case has one explicit next action, owner, and expected date.
- The team may use approved phone/email/WhatsApp for convenience, but material facts return to the case record.
- Operators never create clinician-authored opinions or alter hospital quotations.
- The operating team is part of the V0 product, not a temporary embarrassment. Automation comes only after the team measures repetition, error, and volume.

---

# 11. FEATURE PRIORITIZATION

These are exactly four tiers. “Fundamental” means the end-to-end referral fails without it; it does not mean every edge case receives custom software.

## TIER 1 — FUNDAMENTAL

1. **Role-based account and organization membership:** doctor, patient/delegate, hospital user, and platform operator.
2. **Manual-verification workflow and status:** doctor identity/licence/affiliation and hospital/facility/team approval.
3. **Focused verified doctor profile:** enough evidence and scope to decide whether to refer.
4. **Doctor discovery:** name, specialty/subspecialty/procedure tag, hospital, country, language, and accepting-referrals status.
5. **Lightweight professional connection:** request, accept/decline, view, remove/report.
6. **Referral and patient case creation:** clinical question, sourced summary, patient identity, referrer, corridor/specialty.
7. **Patient consent/activation:** patient can authorize the referral, participants, and sharing.
8. **Medical document upload and controlled case sharing:** categorized PDF/images, recipient-specific provider request.
9. **Hospital case inbox and qualification:** accept, decline, or request information.
10. **Hospital doctor/coordinator assignment:** named verified reviewer and operational owner.
11. **Case-bound information requests and messaging:** all patient-specific collaboration happens in the case.
12. **Attributable specialist opinion:** issued by named verified clinician, with document/version support.
13. **Hospital proposal and indicative quotation:** structured essential fields plus original document/version.
14. **Status, next action, owner, SLA timestamp, and history:** visible to the appropriate participants.
15. **Patient decision, selected-case pre-travel status, and discharge/follow-up handback:** simple tracking and document return, backed by human coordination.

## TIER 2 — IMPORTANT / EARLY

1. Doctor introductions by existing trusted connections.
2. Connection-only non-case professional messages.
3. Reusable specialty-specific referral templates and document checklists.
4. Side-by-side proposal comparison for two or three responses.
5. Structured remote-consultation request and appointment tracking.
6. Proposal/quote builder, approvals, and revision comparison.
7. Coordinator workload and SLA escalation dashboard.
8. Referring-doctor relationship history and next relationship task.
9. Repeat referral flow that reuses connection and provider requirements.
10. Structured visa invitation/readiness checklist.
11. Travel/arrival/admission checklist.
12. Translation request and provenance tracking.
13. Basic hospital source, stage, response-time, conversion, and lost-reason analytics.
14. Scoped patient case export and self-service access overview.
15. Multi-facility routing within a contracted hospital group.

## TIER 3 — BONUS / DIFFERENTIATORS

1. Evidence-backed specialist recommendations based on case requirements and availability, with human confirmation.
2. Referral relationship graph and corridor coverage analytics.
3. AI-assisted document classification, dates, and chronology with source-linked review.
4. AI-assisted missing-document suggestions with human approval.
5. Assisted translation with clinical human-review states.
6. SLA and capacity prediction.
7. Case-message summarization with citations to source events.
8. Advanced hospital performance and cohort analytics with minimum sample sizes.
9. Publications/research profile imports from authoritative identifiers.
10. Multidisciplinary case-conference workflow.
11. Hospital CRM/EHR/document-system integrations where proven valuable.
12. Referrer cohort tools for approved educational events—not a content feed.
13. Patient concierge partner workspace.
14. Configurable hospital-group workflow and reporting.
15. De-identified corridor-demand forecasting after sufficient data and governance.

## TIER 4 — DO NOT BUILD YET

1. **Social feed:** does not close referrals; creates moderation and engagement theatre.
2. **Likes, reactions, follower counts, streaks, badges:** vanity signals invite gaming and can be confused with professional quality.
3. **Doctor influencer content, reels, and creator tools:** attracts the wrong behavior and buyer.
4. **Generic medical news feed:** crowded, non-differentiated, and irrelevant to the referral wedge.
5. **Public endorsements, star ratings, and “top doctor” rankings:** unsafe quality proxies and commercially corruptible.
6. **Job board/recruiting marketplace:** a separate network monetization problem.
7. **General discussion groups/forums:** diffuse use case, heavy moderation, low corridor liquidity.
8. **Open pre-connection chat:** invites spam, hospital solicitation, and patient-data leakage.
9. **Full flight/hotel/transport marketplace:** operationally broad and already served elsewhere.
10. **Insurance marketplace or claims adjudication:** different regulation, integrations, and buyer.
11. **Medical lending/financing:** high-risk consumer finance and conflict burden.
12. **Native video calling/recording:** hospital links are sufficient until consultation volume proves need.
13. **AI diagnosis, prognosis, treatment recommendation, or autonomous clinical triage:** violates the coordination boundary and creates unacceptable risk.
14. **AI/public doctor ranking:** lacks valid outcome methodology and invites bias.
15. **Percentage-of-treatment commission engine:** legal/ethical and neutrality risk before counsel and evidence.
16. **Patient payment custody/wallet:** reconciliation, refunds, FX, fraud, and regulatory scope distract from referrals.
17. **Dozens of hospital integrations:** V0 partners can use the portal; integration before workflow proof slows learning.
18. **Native mobile apps:** responsive web is enough for workflow validation.
19. **Global/all-specialty launch:** destroys density, verification quality, and service promises.
20. **Transplant/fertility/emergency marketplace:** exceptional clinical, legal, ethical, and operational risk needs a separate programme.

---

# 12. MINIMUM PAGE / SCREEN SPECIFICATION

## Public

| Screen name | Primary user | Purpose | Core information | Primary action | Secondary actions | Tier |
|---|---|---|---|---|---|---|
| **Corridor landing page** | Foreign doctor, patient, hospital buyer | Explain the exact corridor, service, roles, boundaries, and response process. | Supported countries/specialties, partner model, how referral works, coordination boundary, support contact. | Start doctor application or patient case. | Hospital enquiry; sign in; emergency direction. | **Fundamental** |
| **Verified specialist search** | Verified/eligible doctor; limited public view optional | Find relevant Indian specialists/hospital teams. | Search/filter, verified status/date, specialty, facility, languages, accepts referrals. | View specialist profile. | Request assisted match. | **Fundamental** |
| **Specialist profile** | Foreign doctor/patient | Establish professional relevance and trust. | Verified claims, speciality/focus, affiliation, languages, referral availability, response route. | Connect or start referral. | Report correction; request introduction. | **Fundamental** |
| **Hospital programme page** | Doctor/patient/buyer | Explain one partner facility's relevant capability without ranking. | Exact facility, service lines, accreditations, participating team, corridor languages/process. | Refer/request review. | Contact coordinator. | **Early** |

## Doctor

| Screen name | Primary user | Purpose | Core information | Primary action | Secondary actions | Tier |
|---|---|---|---|---|---|---|
| **Doctor application and verification** | Foreign or Indian doctor | Establish verified professional identity and scope. | Identity, regulator/licence, specialty, affiliation, evidence, status/issues. | Submit verification. | Save; correct; contact support. | **Fundamental** |
| **Doctor home** | Verified doctor | See work requiring attention and relationship activity. | Active referrals, information requests, responses, handbacks due, connection requests. | Open next referral action. | Find specialist; create referral; edit profile. | **Fundamental** |
| **Specialist discovery** | Referring doctor | Search the curated network by referral need. | Required V1 filters, prior connections, declared availability, verification. | View/select specialist. | Ask case manager; save shortlist. | **Fundamental** |
| **Connections** | Doctor | Reuse trusted professional relationships. | Pending/accepted connections, specialty, last collaboration, block/report state. | Accept/request/open relationship. | Remove/report; introduction request. | **Fundamental** |
| **Create referral** | Referring doctor | Build the clinical question and invite patient consent. | Patient contact, role, question, sourced summary, specialty, candidate recipient, required records. | Invite patient/submit draft. | Save; request assistance. | **Fundamental** |
| **Referral/case detail** | Referring or receiving doctor | Collaborate around one authorized case. | Summary, participants, records, requests, messages, opinion, status/next action, handback. | Complete current action or issue response. | Message; upload; decline; request consultation. | **Fundamental** |
| **Professional inbox** | Connected doctors | Limited non-case professional communication. | Connection-related conversations, report/block controls. | Reply or convert to referral. | Archive; report. | **Early** |

## Patient

| Screen name | Primary user | Purpose | Core information | Primary action | Secondary actions | Tier |
|---|---|---|---|---|---|---|
| **Patient invitation, identity, and consent** | Patient/guardian | Understand and authorize a doctor-created referral. | Referrer identity, purpose, recipient/sharing, records, participant rights, support. | Verify and consent/decline. | Invite delegate; ask case manager. | **Fundamental** |
| **Patient case workspace** | Patient/delegate | See and act on the whole case without navigating many modules. | Summary, participants/access, missing items, records, messages, status, next action. | Complete next action. | Upload; message; change delegate; request help. | **Fundamental** |
| **Response and decision** | Patient/referrer | Review opinion, proposal, quote, assumptions, and questions. | Attributable opinion, hospital/doctor, pathway, estimate, inclusions/exclusions, validity, limitations. | Proceed / clarify / decline / pause. | Download; share with authorized referrer. | **Fundamental** |
| **Journey and handback** | Proceeding patient | Track pre-travel through discharge/follow-up at a simple level. | Checklist, hospital contacts, invitation document, next milestone, discharge/follow-up files. | Complete/confirm next step. | Request support; upload itinerary/local result. | **Fundamental, operationally simple** |
| **Compare responses** | Patient/referrer | Normalize two or more proposals without simplistic ranking. | Differences, assumptions, missing items, ranges, dates, conflicts. | Ask questions or choose. | Export. | **Early** |

## Hospital

| Screen name | Primary user | Purpose | Core information | Primary action | Secondary actions | Tier |
|---|---|---|---|---|---|---|
| **Hospital inbox/pipeline** | IPD team/manager | Own every shared case and see SLA risk. | Stage, age, country, specialty, referrer, completeness, owner, next action, SLA. | Open/assign case. | Filter; accept/decline; export controlled report. | **Fundamental** |
| **Hospital case detail** | Coordinator/doctor/finance by role | Work one referral from review to follow-up. | Authorized summary/records, participants, requests, messages, assignments, status/timeline. | Perform role-specific next action. | Reassign; escalate; mark lost/selected. | **Fundamental** |
| **Clinical response** | Assigned Indian specialist | Ask questions and issue attributable preliminary opinion. | Clinical question, reviewed records, limitations, response fields/document, version. | Request information or issue opinion. | Decline/reroute; propose consultation. | **Fundamental** |
| **Proposal and quote** | Coordinator/finance + clinician approval | Send a complete versioned hospital response. | Pathway, doctor/facility, expected stay, assumptions, range/currency, inclusions/exclusions, validity. | Issue proposal/quote. | Revise with reason; send clarification. | **Fundamental** |
| **Hospital team/programme settings** | Hospital admin | Control approved staff, participating doctors, corridor scope, and basic SLA. | Memberships/roles, facilities, specialties, status, response commitments. | Add/deactivate/assign. | Request profile correction. | **Fundamental** |
| **Hospital performance** | IPD manager/buyer | Measure pilot value. | Funnel, response intervals, lost reasons, referrers, arrivals, user adoption. | Review/export pilot report. | Drill into exceptions. | **Early** |

## Platform admin

| Screen name | Primary user | Purpose | Core information | Primary action | Secondary actions | Tier |
|---|---|---|---|---|---|---|
| **Operations queue** | Platform case manager | See cases/verification/SLA tasks needing action. | Queue type, priority, owner, due, stage, blocker, latest event. | Claim/open next item. | Reassign; filter; escalate. | **Fundamental** |
| **Case operations console** | Platform case manager | Review completeness, route, coordinate, and maintain next action. | Full authorized case, missing list, recipients, grants, provider requests, statuses, messages, notes, SLA. | Route/request/update next action. | Suspend sharing; record call; escalate; close. | **Fundamental** |
| **Verification console** | Verifier/admin | Approve/suspend doctors, affiliations, hospitals, and users. | Claims, evidence, source/date, discrepancies, expiry/recheck, decision history. | Approve/reject/suspend. | Request evidence; schedule recheck. | **Fundamental** |
| **Partner/corridor configuration** | Operations lead | Maintain the narrow operating roster and promises. | Countries, specialties, partner facilities, reviewers, capacity, SLA, checklist versions. | Activate/deactivate capacity. | Update tags/checklists. | **Fundamental, simple** |
| **Pilot/commercial dashboard** | Founder/ops/hospital success | Demonstrate attributable value and economics. | Qualified referrals, SLA, stages, arrivals, repeat referrers, fees, operating effort. | Review pilot. | Export/invoice reconciliation. | **Early** |

---

# 13. CORE USER LOOPS

## LOOP A — DOCTOR NETWORK

`Doctor joins → manually verified → discovers relevant specialist → requests/accepts connection → exchanges bounded professional context → collaborates on a referral → relationship and history persist → future collaboration is faster`

**Value created:** trusted reach and reuse.
**Failure mode:** registrations and connections never result in a referral.
**Core metric:** connected verified referrers who initiate a referral within 90 days, and those who repeat.

## LOOP B — REFERRAL

`Doctor has patient → finds specialist → states clinical question → patient consents → records shared → hospital accepts/assigns → specialist asks/responds → proposal/quote returned → patient decides → treatment/handoff tracked → discharge/follow-up returns`

**Value created:** closed-loop cross-border care handoff.
**Failure mode:** slow response, incomplete records, patient lost, or no handback.
**Core metric:** percentage of complete referrals receiving a usable attributable response within the agreed SLA and closing with a recorded disposition.

## LOOP C — PATIENT

`Patient activates/submits → case becomes complete → appropriate provider reviews → patient receives understandable response → chooses/declines → coordinator executes next steps → patient receives discharge/follow-up`

**Value created:** trust, clarity, and continuity.
**Failure mode:** false certainty, confusing quote, too many handoffs, or coordination promise not delivered.
**Core metric:** complete case → decision, and selected → arrived/treatment-start conversion with patient-reported trust.

## LOOP D — HOSPITAL

`Hospital receives qualified referral → accepts and assigns → responds within SLA → patient decides/arrives → hospital records outcome → referrer receives handback → relationship is retained → more qualified cases`

**Value created:** incremental revenue plus a repeat referral channel and lower leakage.
**Failure mode:** hospital users revert to private channels or do not respond.
**Core metric:** accepted case → timely response → selected/arrived conversion plus repeat referrer count.

## Most important MVP loop

**Loop B—the referral loop—is the only loop the MVP must optimize.**

It activates each other loop: doctors form meaningful connections, the patient receives value, and the hospital has a revenue opportunity. A social connection without a referral is weak evidence; a case without a timely hospital response destroys trust; an arrived patient without handback prevents compounding.

---

# 14. MANUAL VS AUTOMATED

The rule is: **automate only after the team understands the workflow, can define a stable decision, and has measured enough repetition to justify it.**

| Function | MVP method | Future method |
|---|---|---|
| Doctor identity/licence/affiliation verification | Human checks authoritative sources and records evidence/status. | Assisted source lookup, discrepancy alerts, scheduled reverification; human decision remains. |
| Hospital verification and contracting | Founder/compliance checklist and out-of-band confirmation. | Renewal alerts, evidence integrations, multi-facility governance. |
| Doctor recruitment/onboarding | Founder/local champion calls and assisted profile completion. | Self-service onboarding plus risk-based human verification. |
| Specialist discovery | Simple controlled filters and case-manager curated shortlist. | Explainable relationship/capability suggestions using verified data and live capacity. |
| Connection/intro | Direct request; platform team makes high-trust introductions. | Mutual-connection introduction workflow and relationship recommendations. |
| Patient case intake | Structured form plus case-manager call. | Adaptive specialty templates and reuse of prior patient-approved records. |
| Medical document review | Human checks relevance, readability, date/category, and missing items. | OCR/classification/chronology and missing-item suggestions, always reviewed. |
| Matching/routing | Case manager checks corridor roster, capacity, fit, preference, and conflicts. | Rules-assisted shortlist with reasons; human authorizes every share. |
| Hospital acceptance and SLA | Case manager monitors timestamps and personally chases/escalates. | Automated reminders/escalation and capacity-based routing. |
| Clinical opinion | Hospital specialist authors/signs, potentially as uploaded document. | Structured authoring/templates and hospital integration; never platform-generated clinical opinion. |
| Proposal normalization | Case manager maps hospital response into common fields without editing source. | Structured proposal builder and automated completeness checks. |
| Comparison | Case manager explains fields/uncertainty; basic structured display. | Normalized side-by-side view and question generation, no simplistic ranking. |
| Translation | Approved human/external translation and interpreter. | Assisted translation with provenance and required human-review levels. |
| Visa coordination | Human checklist using current official sources; hospital issues letter; patient applies. | Configured checklist/status reminders; still no eligibility/approval promise. |
| Travel/accommodation/transport | Coordinator works with hospital/patient and approved vendors outside platform. | Scoped partner requests and status, only if volume justifies it. |
| Appointment coordination | Coordinator records confirmed time/status. | Hospital scheduling integration after repeat demand. |
| Payment visibility | Quote/document plus manual status; payment occurs directly to stated recipient. | Payment-reference/reconciliation integrations; custody only after separate decision. |
| Discharge/follow-up chase | Case manager reminds hospital, confirms recipient, and records handback. | SLA reminders, document checklist, follow-up task automation. |
| Complaint/escalation | Human triage and documented action. | Rules route category/severity; human ownership remains. |
| Pilot analytics | Simple event capture and controlled spreadsheet/report review. | Self-service corridor, referrer, SLA, conversion, and unit-economics dashboards. |

---

# 15. MVP — FIRST TEN REAL CASES

## MVP objective

Safely facilitate ten legitimate, consented referrals in one selected corridor; obtain timely attributable hospital responses; track patient decisions; coordinate selected cases through the next step; and return discharge/follow-up material where treatment occurs.

It is not an objective to have thousands of profiles, dozens of hospitals, every specialty, organic patient SEO, or automated logistics.

## Assumed operating envelope

- One source country, with a second only if operationally equivalent.
- One specialty, with a second only if the same referrers/hospital teams and document workflow cover it.
- Two to five contracted Indian hospital facilities.
- 20–100 manually verified foreign referrers.
- A small named platform operations team.
- Responsive web product; no native app.

## What needs software

1. Authenticated role-based accounts and hospital memberships.
2. Doctor/hospital verified status and focused profiles.
3. Doctor discovery and simple connection relationship.
4. Referral creation and patient invitation/consent.
5. Case workspace, participant list, records, and controlled hospital share.
6. Hospital inbox, acceptance, assignment, and information requests.
7. Case-bound messages/notifications.
8. Attributable opinion and proposal/quote delivery.
9. Status, owner, next action, SLA timestamps, and outcome.
10. Patient decision and minimal pre-travel/discharge/follow-up tracking.
11. Admin operations/verification queues and essential audit history.
12. Pilot event export/report sufficient to prove response and conversion.

## What can be manual

- All identity/licence/accreditation checks.
- Every specialist/hospital match and capacity confirmation.
- Case-completeness judgement and report chasing.
- Medical image transfer outside ordinary PDFs/images.
- Translation/interpreter sourcing and quality review.
- Proposal normalization and patient explanation.
- Remote consultation scheduling through hospital tools.
- Visa rules/checklist, hospital invitation chase, and status follow-up.
- Travel, accommodation, transport, arrival, and admission coordination.
- Payment handling and reconciliation outside the platform.
- Hospital SLA escalation and referrer relationship management.
- Complaints, exceptional consent, patient deterioration, and other sensitive exceptions.

## Must be ready before the first real patient

- Selected corridor and scope/exclusion policy.
- At least two contracted hospital partners with named IPD/specialty owners and response SLA.
- Verified receiving specialist roster with actual review capacity.
- Verified pilot referrers and onboarding support.
- The complete Tier 1 referral path through response and handback.
- Reviewed patient/referrer consent and data-sharing flow.
- Case isolation, access control, secure record handling, backups, and audit evidence at a level appropriate for real health data.
- Human playbooks for completeness, routing, non-response, emergency redirect, consent withdrawal, access incident, complaint, and death/deterioration.
- Clear commercial terms and no doctor referral payment.
- A case manager available to own the whole journey.

## Can wait until case #10

- Self-service proposal comparison.
- Dedicated professional inbox beyond case/connection messages.
- Reusable specialty templates and provider-required-document presets.
- Structured appointment and travel screens beyond status/checklist.
- Hospital manager dashboards beyond a controlled pilot report.
- Referral relationship history/next-task tooling beyond case history.
- Translation workflow beyond secure manual handling.
- More than one response per case as a standard promise.

## Can wait until case #100

- AI-assisted documents/matching/translation.
- Hospital-system integrations.
- Enterprise multi-facility configuration.
- Capacity forecasting and advanced SLA automation.
- Sophisticated graph analytics and referral recommendations.
- Patient concierge marketplace/partner portal.
- Native mobile apps/video/payment custody.
- Expansion to additional corridors based on measured playbook reuse.

## V0 release gate

Do not onboard a real patient merely because screens work. Release requires one synthetic end-to-end rehearsal, one permission/access test across all roles, one hospital response rehearsal with an actual pilot team, and signed operational ownership for every step from referral receipt to handback.

---

# 16. MVP ACCEPTANCE SCENARIO

The MVP passes when the following can be demonstrated with role-correct users and an auditable synthetic case, followed by an approved real pilot case:

1. A manually verified doctor outside India signs in and appears with accurate verification scope/date.
2. They search the curated Indian specialist roster and view a verified professional profile.
3. They initiate a referral, state the clinical question, add the patient's contact, and select a proposed recipient.
4. The patient verifies their channel, reviews the referrer/recipient/purpose, authorizes case sharing, and can see who will receive it.
5. Patient/referrer uploads relevant categorized records; originals remain attributable.
6. A platform case manager sees the new case, marks missing/complete items, and records the next action.
7. The case manager creates one isolated provider review request to an eligible hospital.
8. The hospital inbox shows the case; an authorized coordinator accepts it and assigns a verified specialist.
9. The specialist sees only the assigned authorized case, asks for a specific additional item, and the patient/referrer responds.
10. The specialist issues an attributable preliminary opinion with limitations.
11. The hospital issues a versioned proposal and indicative quotation with required assumptions, inclusions/exclusions, currency, and validity.
12. The patient and referring doctor can view the permitted response, ask a case-bound question, and record proceed/clarify/decline/pause.
13. If proceeding, the case manager/hospital updates a simple pre-travel next-step checklist and shares the hospital invitation document securely.
14. High-level arrival/treatment/discharge states can be recorded without pretending the platform is the hospital clinical record.
15. The hospital uploads discharge/follow-up information; the patient receives it and the referring doctor receives it only where authorized.
16. Every access, share, assignment, issued response, status change, and decision is attributable; Hospital B cannot see Hospital A's request or response.
17. The pilot report can show source/referrer, completeness, response times, stage/outcome, handback, and operator effort.

Any feature not necessary to make this scenario reliable requires a separate justification before entering V0.

---

# 17. REALISTIC BUSINESS ECONOMICS

## Variable model

Use corridor-specific evidence, not market-size headlines.

| Variable | Meaning |
|---|---|
| `N` | Active participating referring doctors, not merely verified profiles. |
| `R` | Average qualified referrals per active doctor per year. |
| `Q = N × R` | Qualified referrals per year. |
| `C` | Percentage of qualified referrals that become the defined paid/successful treatment milestone. |
| `T = Q × C` | Successful cases per year. |
| `V` | Average hospital treatment value per successful case. This is hospital revenue, not platform revenue. |
| `G` | Hospital contribution-margin rate on that treatment, if the hospital will provide it. |
| `F` | Fixed platform revenue per successful case, only if legally/ethically cleared and contracted. |
| `H` | Paying hospital/facility contracts. |
| `S` | Annual recurring/pilot-equivalent platform revenue per hospital. |
| `Oq` | Direct platform operations cost per qualified referral, including incomplete/non-converting cases. |
| `Ot` | Additional direct coordination cost per successful case. |
| `K` | Annual fixed cost: product, sales, corridor team, verification/compliance, support, and overhead. |

Equations:

- **Platform revenue:** `(T × F) + (H × S)`
- **Direct variable cost:** `(Q × Oq) + (T × Ot)`
- **Contribution before fixed cost:** `Platform revenue − Direct variable cost`
- **Hospital gross treatment value influenced:** `T × V`
- **Hospital economic ceiling:** the platform's hospital cost must be comfortably below truly incremental `T × V × G` plus demonstrated operating savings—not total treatment revenue.

## Illustrative scenario assumptions

These values are **planning hypotheses in INR, not market facts or pricing recommendations**. Replace them with pilot evidence. `F` represents a future fixed coordination fee or allocated per-success revenue; for the recommended initial fixed-fee pilot, set `F = 0` and price `S` to cover the agreed case capacity.

| Scenario | `R` | `C` | `F` | `S` per hospital/year | `Oq` | `Ot` | Hospital counts at `N=50 / 100 / 500` |
|---|---:|---:|---:|---:|---:|---:|---|
| **Conservative** | 0.5 | 15% | ₹30,000 | ₹3.6 lakh | ₹10,000 | ₹20,000 | 2 / 3 / 6 |
| **Base** | 1.0 | 25% | ₹50,000 | ₹6 lakh | ₹8,000 | ₹15,000 | 3 / 4 / 8 |
| **Optimistic** | 2.0 | 35% | ₹75,000 | ₹9 lakh | ₹6,000 | ₹10,000 | 4 / 6 / 12 |

## Doctor-count scenarios

Amounts below are annual and rounded. “Contribution” excludes `K`, taxes, bad debt, refunds, and capital cost.

| Scenario | Active doctors `N` | Qualified referrals `Q` | Successful cases `T` | Platform revenue | Direct variable cost | Contribution before `K` |
|---|---:|---:|---:|---:|---:|---:|
| Conservative | 50 | 25 | 3.8 | ₹8.3 lakh | ₹3.3 lakh | ₹5.1 lakh |
| Conservative | 100 | 50 | 7.5 | ₹13.1 lakh | ₹6.5 lakh | ₹6.6 lakh |
| Conservative | 500 | 250 | 37.5 | ₹32.9 lakh | ₹32.5 lakh | ₹0.4 lakh |
| Base | 50 | 50 | 12.5 | ₹24.3 lakh | ₹5.9 lakh | ₹18.4 lakh |
| Base | 100 | 100 | 25 | ₹36.5 lakh | ₹11.8 lakh | ₹24.8 lakh |
| Base | 500 | 500 | 125 | ₹1.11 crore | ₹58.8 lakh | ₹51.8 lakh |
| Optimistic | 50 | 100 | 35 | ₹62.3 lakh | ₹9.5 lakh | ₹52.8 lakh |
| Optimistic | 100 | 200 | 70 | ₹1.07 crore | ₹19 lakh | ₹87.5 lakh |
| Optimistic | 500 | 1,000 | 350 | ₹3.71 crore | ₹95 lakh | ₹2.76 crore |

### What this table reveals

- Registered-doctor count is meaningless unless `R` is material.
- At low conversion, human processing of non-converting cases can consume almost all revenue even with many doctors.
- A pure fixed case fee is fragile; a pure low-priced SaaS subscription is also fragile before workflow becomes lighter.
- Improving referral quality/completeness and `C` matters more than inflating top-of-funnel profiles.
- Fixed hospital revenue must scale with facilities/case capacity; it cannot remain flat while case operations grow.
- This can begin as a valuable managed service before it becomes scalable software. The founders must be honest about that transition.

## Successful-patients-per-month scenarios

Illustrative base assumptions: `C=25%`, `F=₹50,000`, `S=₹6 lakh/year`, `Oq=₹8,000`, `Ot=₹15,000`; 5, 10, and 20 hospital contracts respectively. These are deliberately transparent hypotheses.

| Successful patients/month | `T`/year | Required `Q`/year | Case revenue | Hospital fixed revenue | Total revenue | Direct variable cost | Contribution before `K` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 120 | 480 | ₹60 lakh | ₹30 lakh | ₹90 lakh | ₹56.4 lakh | ₹33.6 lakh |
| 50 | 600 | 2,400 | ₹3 crore | ₹60 lakh | ₹3.6 crore | ₹2.82 crore | ₹78 lakh |
| 100 | 1,200 | 4,800 | ₹6 crore | ₹1.2 crore | ₹7.2 crore | ₹5.64 crore | ₹1.56 crore |

Interpretation:

- **10 successes/month:** enough to prove a corridor and perhaps support a lean service team, but unlikely to support a substantial standalone company after fixed product, sales, security, legal, and management cost.
- **50/month:** can become a real managed-network business, but the illustrative human cost leaves modest contribution. Stronger conversion, higher fixed hospital revenue, or lower handling cost is necessary.
- **100/month:** meaningful scale, but 400 qualified cases/month at the base conversion rate is an operations machine. Workflow standardization and selective automation are mandatory.

If `F=0` under the initial no-success-fee pilot, five hospitals at the illustrative base `S` produce ₹30 lakh against ₹56.4 lakh in variable work at 10 successes/month. That is underwater before fixed cost. Therefore pilot pricing must include a bounded case capacity/service level, or the workflow must achieve lower `Oq` and higher `C`; “unlimited cases” is economically unsafe.

## Assumptions that matter most

1. **Active referrer productivity (`R`)**, not network registrations.
2. **Qualified-to-success conversion (`C`)** and whether platform cases are incremental.
3. **Operations cost for non-converting cases (`Oq`)**.
4. **Hospital willingness to pay fixed recurring revenue (`S`)** before guaranteed volume.
5. **Lawful, neutral availability and size of any fixed success fee (`F`)**.
6. Hospital response speed and completeness, which influence `C` but are partly outside platform control.
7. Hospital sales cycle, renewal, and implementation burden.
8. Referrer acquisition cost and repeat-referral rate.

---

# 18. GO-TO-MARKET AND PRODUCT IMPLICATIONS

## Foreign doctors: test order

| Rank | Channel | Why test in this order | Product feature that supports it |
|---:|---|---|---|
| 1 | **Warm introductions through trusted clinicians and existing cross-border relationships** | Highest trust and fastest access to doctors who already see relevant cases. Guard against merely digitizing a hospital's existing demand. | Verified profiles, connection/introduction, structured referral, guaranteed operational acknowledgement. |
| 2 | **Founder-led direct outreach to a tightly defined referrer list** | Tests whether the problem exists beyond current hospital networks; produces honest objection data. | Corridor-specific landing, concierge verification/onboarding, clear specialist roster and SLA. |
| 3 | **Medical associations/specialty societies and small CME/case-workflow events** | Institutional trust and concentrated specialty access; slower but scalable if the proposition is educational/professional rather than sales. | Verified closed network, event-linked onboarding, referral templates, no social feed. |
| 4 | **Diaspora physician networks and alumni relationships** | Natural India ties and trusted introductions; corridor fit varies. | Mutual introduction, country/language search, professional relationship history. |
| 5 | **Hospital co-development/outreach to new referrers** | Hospital brand increases trust, but risks making the network feel captive or promotional. | Transparent hospital relationship, named specialists, neutral case routing rules. |
| 6 | **Local representatives** | Can unlock relationships but creates cost, supervision, commission, and conduct risk. | Activity attribution, no bulk export, controlled invitations, complaint/reporting. |
| 7 | **Large conferences and broad digital acquisition** | Expensive, noisy, and likely to produce signups rather than referrals before the message is proven. | Only later with proven case studies and conversion instrumentation. |

### Foreign-doctor acquisition test

Do not ask “Would you join?” Ask the doctor to complete profile verification, identify one specialist need from the last six months, review the referral flow, and commit to using it for the next eligible consenting patient. Measure completion and actual referral, not interview enthusiasm.

## Indian specialists: test order

1. **Hospital-appointed specialty champions and their teams:** ensures capacity, institutional authorization, and proposal handoff.
2. **Peer-to-peer introductions from trusted referrers/Indian leaders:** strengthens the professional rather than sales relationship.
3. **Service-line leadership partnerships:** establishes document requirements and review SLA.
4. **Professional societies/conferences:** later, once a clear corridor use case exists.
5. **Open self-registration:** last; uncurated supply creates verification work and no liquidity.

Product implication: specialist onboarding should be organization-backed, profiles concise, assignment explicit, and review work case-bound. Do not recruit a giant independent directory disconnected from hospital operations.

## Indian hospitals: test order

1. Heads of International Business/IPD at hospitals already targeting the candidate corridor.
2. Medical director/service-line leader plus IPD champion together; either one alone cannot make the pilot work.
3. Hospital groups that can provide two relevant facilities without creating five separate implementations.
4. Smaller specialty hospitals only where verification, capacity, outcomes governance, and corridor trust are strong.

The hospital sell needs a live workflow demonstration using a synthetic case, named referrer pipeline, implementation burden, SLA contract, and pilot ROI scorecard. A generic product deck is insufficient.

## Patients: test order

1. **Referring-doctor introduction:** highest trust and central to the thesis.
2. **Hospital-partner co-referral where the case needs structured intake/handback:** useful but test incrementality.
3. **Diaspora/patient-community introductions with a trusted coordinator:** validate direct-patient path in the same corridor.
4. **Targeted educational/search content for the exact pathway:** only after the team knows what a qualified case looks like.
5. **Broad paid lead generation and hospital listing SEO:** do not prioritize; it drifts into facilitator competition and creates low-quality volume.

## GTM/product alignment test

If doctor relationships are the acquisition engine, product effort must prioritize verified profiles, discovery, referral creation, response reliability, and handback. Public hospital pages, travel inventory, content feeds, and consumer SEO should not receive equivalent investment.

---

# 19. COMPETITIVE DIFFERENTIATION

Competition is significant. The wedge is a particular combination and operating model, not a claim that each component is new.

| Category and examples | What they solve | Overlap | Our proposed wedge | Easy for them to copy | Harder for them to copy |
|---|---|---|---|---|---|
| **1. Medical-tourism facilitators** — [Lyfboat](https://www.lyfboat.com/), [MediGence](https://medigence.com/), Vaidam and others | Hospital/doctor discovery, estimates, patient acquisition, visa/travel/concierge coordination. | Patient intake, records, provider responses, comparison, travel. | Doctor-originated closed-loop referrals, durable professional graph, home-doctor handback, and hospital relationship CRM. | Verified-profile presentation, referral form, messaging, hospital portal. | Active referrer trust, repeat doctor-to-doctor edges, institutional handback behavior, and a non-broker identity. |
| **2. Hospital international-patient programmes** — [Apollo](https://www.apollohospitals.com/international-patient-services), [Max](https://www.maxhealthcare.in/hospitals-in-india), [Fortis](https://www.fortishealthcare.com/international-patients) | Direct expert opinion, hospital conversion, visa letters, appointments, concierge, admission and follow-up. | Almost the entire single-hospital patient journey. | Cross-institution referrer network, one reusable referral relationship, controlled routing, and neutral/transparent multi-provider option where justified. | Better intake portal, referrer login, status updates. | A hospital-neutral cross-border network and relationships that span competing institutions. Hospitals may choose to build a captive version instead. |
| **3. Doctor networking products** — [Doximity](https://www.doximity.com/about/company/), [Docquity](https://docquity.website/), [Sermo](https://support.sermo.com/hc/en-us/articles/15492555632155-How-do-you-know-members-are-actually-physicians) | Verified professional identity, communication, education/content, careers, peer community. | Profiles, verification, search, connections, messages. | A transaction-specific international referral loop tied to patient consent, hospital response, arrival, and handback. | Referral form, case messaging, India specialist segment. | Hospital IPD workflow, corridor operations, case coordination, and commercial hospital contracts—unless they partner/acquire. |
| **4. Healthcare CRMs** — [Salesforce Health Cloud](https://help.salesforce.com/s/articleView?id=ind.hc_referrals_flow.htm&language=en_US&type=5) and configured CRMs | Patient/provider data, referral workflows, service requests, document links, engagement, analytics. | Hospital inbox, pipeline, assignment, relationship management, reporting. | Pre-built cross-border corridor workflow plus verified demand network and operated SLA, not software configuration alone. | Every workflow screen and report. | Referrer acquisition, trust, active graph, corridor playbook, and performance-based operating service. A system integrator could reproduce software for a large hospital. |
| **5. Second-opinion products** — [Teladoc Expert Medical Opinion](https://www.teladochealth.com/individuals/specialty-wellness/medical-experts), [Cleveland Clinic Virtual Second Opinions](https://my.clevelandclinic.org/online-services/virtual-second-opinions) | Record collection, specialist matching, written expert opinion, optional consultation. | Structured case, records, specialist response, coordinator. | Opinion-to-treatment travel pathway across selected Indian hospitals plus referring-doctor relationship and hospital conversion workflow. | Professional referral input and follow-up sharing. | Destination hospital network, on-ground coordination, and repeat corridor economics. They are stronger in opinion quality/brand and could expand. |
| **6. Referral-management software** — [ReferWell](https://engage.referwell.com/our-platform/) and others | Provider search/matching, scheduling, closed-loop referral tracking, care navigation, leakage reduction. | Provider network, referral, case status, handback, human navigator. | Cross-border planned treatment, patient-controlled international sharing, hospital proposals/quotes, visa/pre-arrival, and source-country doctor graph. | International fields, documents, hospital-specific workflow. | Corridor distribution, immigration/arrival operations, India hospital contracts, and cross-border professional trust. This category proves that “software + human navigator” is not itself unique. |

## Competitive implication

The UI and workflow are table stakes. The differentiation must be demonstrated in three facts:

1. We can recruit and retain relevant foreign referrers.
2. Partner hospitals respond better through us and pay for that channel/workflow.
3. Completed cases create repeat professional relationships and handbacks.

If those facts do not emerge, the product is a smaller medical-tourism facilitator or a niche CRM and should be evaluated as such.

---

# 20. WHAT THE MOAT COULD ACTUALLY BE

| Potential moat | Rating | Why |
|---|---|---|
| Verified international doctor graph | **STRONG, if active** | Verification plus real cross-border edges is costly to reproduce; static/scraped profiles are weak. |
| Repeated referral relationships | **VERY STRONG** | Trust and successful handbacks compound, are path-dependent, and make future referrals easier. This is the best potential moat. |
| Cross-border workflow data | **MODERATE → STRONG** | Useful for document requirements, matching, SLA, and funnel learning; needs sufficient clean volume and cannot rely on unrestricted patient-data exploitation. |
| Hospital integrations | **MODERATE** | Create switching cost but are buildable by competitors and expensive to maintain; no moat before usage. |
| Hospital contracts | **MODERATE** | Provide access and temporary exclusivity/stickiness, but renew only with ROI and can be won by incumbents. |
| Country-corridor position | **STRONG** | Local champions, language, referrer density, hospital capacity, and operating knowledge reinforce one another. It weakens if spread too early. |
| Specialist supply | **WEAK → MODERATE** | Famous/qualified doctors are not exclusive; committed review capacity and response reliability are more defensible than profile count. |
| Trusted brand | **MODERATE initially; potentially STRONG** | Trust follows consistent verified behavior and case recovery, not marketing claims. One serious incident can damage it. |
| Operational expertise | **STRONG** | Handling completeness, escalation, handback, and corridor exceptions reliably is hard and learned case by case. It must be codified, not trapped in founders' heads. |
| Case history | **MODERATE** | Makes repeat work easier but is portable/sensitive and should not become a lock-in strategy. Relationship context is more defensible than raw documents. |
| Referral workflow embedded in hospital operations | **STRONG** | Ownership, SLA, and relationship records create habitual and institutional switching cost if staff truly use it. |
| Response-time/SLA reliability | **STRONG** | A reputation for actual response is commercially valuable and operationally hard; it requires supply discipline, not just software. |

The moat sequence is:

`corridor operations → completed referral loops → repeated relationships → embedded hospital/referrer workflow → proprietary network reliability data`

Trying to claim a data or AI moat before completing referrals reverses the sequence.

---

# 21. PRODUCT PRINCIPLES

1. **Doctor relationships before patient leads.** Build a repeat source of trusted referrals, not an anonymous lead funnel.
2. **Referral workflow before social network features.** A profile or connection must help a case move.
3. **Trust before scale.** Curate and verify a small useful roster.
4. **Human operations before premature automation.** Learn decisions and failure modes first.
5. **Hospital revenue value before dashboard vanity.** Every manager view must connect to demand, speed, conversion, effort, or retention.
6. **One corridor before global expansion.** Density beats breadth.
7. **Structured cases before generic chat.** Patient-specific work belongs in a consented case.
8. **Transparent commercial relationships.** The user can understand who pays and what may influence participation.
9. **Clinicians make clinical decisions.** The platform coordinates and attributes.
10. **Every feature must support referral, coordination, trust, or revenue.** If it supports none, it is not on the roadmap.

## Feature decision test

Before accepting any feature, answer:

- Which core loop improves?
- Which measurable bottleneck changes?
- Can a human handle it for the next 100 cases?
- Does it create or protect repeat referral relationships?
- Will a doctor, patient, hospital buyer, or operator change behavior because of it?
- What is the cost in trust, moderation, compliance, training, and operational complexity?

---

# 22. FOUNDER-READY SPECIFICATION

## 1. PRODUCT IN ONE SENTENCE

A verified professional referral network that closes the loop between a home-country doctor, a consenting patient, and an Indian specialist/hospital from structured referral through attributable response and post-treatment handback.

## 2. TARGET MARKET

One evidence-selected source country; one planned, high-coordination specialty; two to five Indian hospital facilities; and 20–100 relevant foreign referrers. The exact corridor is a validation decision, not a product assumption.

## 3. PRIMARY USERS

- Foreign/referring doctor: discovers, refers, collaborates, and receives handback.
- Indian specialist: reviews and responds to assigned structured cases.
- Patient/family delegate: authorizes, supplies information, reviews response, decides, and coordinates.
- Hospital IPD coordinator/manager/finance: qualifies, assigns, responds, converts, and tracks relationships.
- Platform case manager/verifier: makes the network and workflow reliable.

## 4. PAYING CUSTOMER

The Indian hospital or hospital group, initially through its international-patient/business team with medical/service-line sponsorship.

## 5. PRIMARY BUSINESS MODEL

A fixed-fee hospital corridor operating pilot, converting to an annual subscription priced by facility/corridor/case capacity and service level. It bundles network access, referral workflow, managed response SLA, and pilot reporting. Doctors join free. Any future fixed successful-case fee requires separate legal/ethical review and transparency.

## 6. CORE VALUE PROPOSITION

- **Hospital:** obtain/retain qualified international referrals and convert them with faster, more complete, attributable workflow.
- **Referring doctor:** reach a credible specialist, save coordination time, preserve the patient relationship, and get the handback.
- **Patient:** submit once, know who has the case, receive a named response, and have one accountable next step.
- **Indian specialist:** review relevant organized cases without becoming the administrative coordinator.

## 7. DIFFERENTIATION

Not discovery, quotation, or concierge by themselves. The wedge is the combination of:

1. verified foreign-to-Indian professional relationships;
2. consented structured referrals;
3. a hospital response-and-conversion workflow;
4. accountable human coordination; and
5. closed-loop discharge/follow-up back to the referrer.

## 8. CORE NETWORK EFFECT

Every successfully closed referral creates a reusable professional edge, known receiving requirements, response history, and institutional relationship. More active trusted edges improve the probability and speed of the next useful response. Profiles and follower counts do not create this effect.

## 9. FUNDAMENTAL FEATURES

Maximum 15:

1. Role-based accounts and organization membership.
2. Doctor/hospital manual verification status and evidence workflow.
3. Focused verified doctor and hospital profiles.
4. Curated specialist search/filter.
5. Lightweight doctor connection/request relationship.
6. Structured referral and patient case creation.
7. Patient activation, consent, and participants/access view.
8. Medical-record upload and controlled provider sharing.
9. Hospital case inbox and accept/decline/request-information actions.
10. Verified specialist and coordinator assignment.
11. Case-bound messaging and information requests.
12. Attributable preliminary opinion.
13. Versioned hospital proposal and indicative quotation.
14. Case stage, owner, next action, SLA, decision, and history.
15. Simple pre-travel status plus discharge/follow-up handback.

## 10. EARLY FEATURES

Maximum 15:

1. Trusted doctor introductions.
2. Connection-only non-case professional inbox.
3. Reusable specialty referral templates/checklists.
4. Side-by-side proposal comparison.
5. Consultation/appointment tracking.
6. Structured proposal/quote builder and approvals.
7. SLA/workload escalation dashboard.
8. Referrer relationship history and tasks.
9. Fast repeat-referral flow.
10. Visa invitation/readiness workflow.
11. Travel/arrival/admission checklist.
12. Translation request/provenance.
13. Basic hospital/referrer/conversion analytics.
14. Patient export and self-service access overview.
15. Hospital-group multi-facility routing.

## 11. BONUS FEATURES

Maximum 15:

1. Assisted specialist suggestions with human approval.
2. Referral relationship graph/corridor coverage analytics.
3. AI-assisted document classification/chronology.
4. AI-assisted missing-document suggestions.
5. Assisted translation with human-review state.
6. Capacity and SLA prediction.
7. Source-linked case summarization.
8. Advanced hospital cohort/performance analytics.
9. Authoritative publication/research imports.
10. Multidisciplinary case conference.
11. Proven-value hospital system integrations.
12. Approved referrer education/event tools.
13. Concierge partner workspace.
14. Enterprise hospital-group workflow configuration.
15. De-identified corridor forecasting after sufficient evidence.

## 12. DO NOT BUILD YET

- Social/content/news feed.
- Likes, follows, follower counts, activity badges, or streaks.
- Doctor influencer/reel/video publishing.
- Public endorsements, reviews, star ratings, or “top doctor” ranks.
- Jobs/recruiting.
- General discussion forums/groups.
- Open pre-connection chat and bulk hospital outreach.
- Full travel/accommodation booking marketplace.
- Insurance marketplace/claims engine.
- Lending/medical finance.
- Native video platform or call recording.
- AI diagnosis, treatment recommendation, prognosis, or clinician ranking.
- Percentage-of-treatment commission engine.
- Patient payment custody/wallet.
- Dozens of hospital integrations.
- Native mobile apps.
- Global/all-specialty launch.
- Exceptional-risk transplant/fertility/emergency marketplaces.

## 13. FIRST 10-CASE MVP

Operate one corridor with a curated roster and a named case manager. Productize only verified identity/discovery, referral/consent, records/sharing, hospital inbox/assignment, case collaboration, response/proposal, next-action tracking, decision, and handback. Perform verification, matching, completeness, proposal normalization, visa/travel, translation, escalation, and relationship development manually. Measure operator effort as carefully as conversion.

## 14. REQUIRED SCREENS

1. Corridor landing/start page.
2. Doctor application/verification.
3. Doctor home.
4. Specialist search.
5. Specialist profile.
6. Connections.
7. Create referral.
8. Doctor referral/case detail.
9. Patient invitation/consent.
10. Patient case workspace.
11. Response and decision.
12. Simple journey/handback view.
13. Hospital inbox/pipeline.
14. Hospital case detail.
15. Clinical response.
16. Proposal/quote.
17. Hospital team/programme settings.
18. Platform operations queue.
19. Platform case console.
20. Verification console.

These may share layouts and routes; “screen” describes a user job, not a requirement for 20 independent implementations.

## 15. CORE WORKFLOWS

- Doctor verification → discovery → connection.
- Referrer creates case → patient consents → records complete.
- Case manager routes → hospital accepts → assigns specialist.
- Specialist requests information → issues opinion.
- Hospital issues proposal/quote → patient decides.
- Selected case moves through manually coordinated pre-travel and high-level treatment milestones.
- Discharge/follow-up returns to patient and authorized referrer.
- Hospital/platform review response, conversion, operator effort, and repeat relationship.

## 16. MANUAL OPERATIONS REQUIRED

- Corridor recruitment and partner capacity.
- Every verification and match.
- Case completeness/record chase.
- Hospital SLA chase/escalation.
- Proposal normalization and patient navigation.
- Translation/interpreter coordination.
- Consultation, visa, travel, arrival, and admission coordination.
- Payment-status confirmation outside custody.
- Discharge/follow-up chase.
- Complaints, consent exceptions, safety issues, and relationship management.

## 17. REALISTIC MONETIZATION

Sell a bounded paid corridor pilot to hospitals. Price for included facility/corridor/case capacity and human SLA service rather than “unlimited SaaS.” Convert to annual recurring contracts only after showing incremental cases, response improvement, conversion, referrer retention, and workflow usage. Keep doctors free; keep patient concierge optional/fixed/transparent later; do not rely on commissions initially.

## 18. GTM STRATEGY

Recruit the first foreign doctors through warm professional relationships, founder-led outreach, and targeted specialty associations. Recruit Indian specialists through hospital service-line champions. Sell hospitals through a joint IPD + medical sponsor with a synthetic live workflow and corridor ROI scorecard. Acquire patients primarily through referring doctors; defer broad consumer SEO/paid leads.

## 19. TOP 5 BUSINESS RISKS

1. Hospitals value patient volume but will not pay a fixed pilot without guaranteed cases.
2. Foreign doctors express interest but do not submit real referrals because of trust, liability, effort, or existing relationships.
3. Hospital departments fail response SLAs, destroying referrer trust and conversion.
4. Commercial/referral rules prevent or severely constrain attractive revenue models.
5. The business remains a labour-intensive facilitator with weak software margins and no repeat relationship effect.

## 20. TOP 5 PRODUCT RISKS

1. The product tries to serve too many countries, specialties, and actors before achieving corridor liquidity.
2. The referral workflow takes more doctor time than existing messaging and assistants.
3. Hospital staff revert to email/WhatsApp, leaving status incomplete and value unmeasurable.
4. Opinion, proposal, and indicative quote are blurred, creating false patient certainty.
5. A permission, verification, or communication failure damages trust before the network is established.

## 21. TOP 5 ASSUMPTIONS TO VALIDATE

1. At least a small cohort of foreign doctors will use a structured platform for their next eligible patient, without referral payment.
2. Two or more hospital partners will provide named specialist capacity and a dependable response SLA.
3. A hospital will pay a fixed corridor pilot fee for the combined network/workflow proposition.
4. Closing the loop and returning follow-up materially increases referrer repeat behavior.
5. One selected corridor has enough qualified, financially/travel-feasible planned cases to support repeat operations.

## 22. WHAT MAKES THIS A REAL BUSINESS INSTEAD OF A PROJECT?

Three reinforcing, paid behaviors:

1. verified referrers repeatedly originate qualified cases;
2. hospitals reliably respond, convert cases, and renew paid contracts because economics are measurable; and
3. each completed handback increases the probability of another referral through the same relationship.

If cases depend indefinitely on founders finding individual patients, hospitals will not pay recurring fees, or every workflow requires bespoke heroics, it is a project/service—not yet a scalable product business.

## 23. WHAT MUST BE TRUE FOR THIS TO BECOME A LARGE COMPANY?

- One corridor must show repeat referrers, hospital renewal, positive contribution after real operating cost, and reliable handback.
- The corridor playbook must transfer to adjacent countries/specialties faster and more cheaply than starting over.
- Hospital fixed revenue and workflow usage must grow, reducing dependence on ethically sensitive case fees.
- Operations cost per qualified case must fall without reducing trust or response quality.
- The verified active graph must improve referral liquidity and create cross-hospital/network value no single hospital can reproduce.
- The company must become an institutional system of relationship and coordination, not a founder-run agent desk.

## 24. THE FIRST THING WE SHOULD BUILD

Build **one end-to-end referral workbench**, first with a seeded curated specialist roster:

`verified referrer → patient consent → structured case/records → isolated hospital request → assignment/questions → opinion/proposal → decision/next action → handback`

Do not build the broad doctor network first. The network becomes real only when this transaction works.

## 25. THE FIRST THING WE SHOULD SELL

Sell a **paid, bounded corridor pilot** to one Indian hospital partner: named source-country referrer cohort, one specialty, included case capacity, response SLA, managed workflow, and a joint report measuring completeness, speed, conversion, repeat relationships, and operator effort.

The first sale is not “CRM software.” It is “we will stand up and operate a measurable professional referral corridor with you.”

---

# V0 FEATURE MATRIX

| FEATURE | USER | WHY IT EXISTS | FUNDAMENTAL / EARLY / BONUS / NO | MANUAL OR SOFTWARE | DEPENDENCIES | SUCCESS CRITERIA |
|---|---|---|---|---|---|---|
| Role accounts and organization membership | All | Separate doctor, patient, hospital, and operator authority. | **Fundamental** | Software; manual role approval | Pilot organizations and role policy | Each acceptance-scenario user can act only in their role; unauthorized cross-role access fails. |
| Verification record and visible status | Doctors, hospitals, verifier | Make discovery and assignment credible. | **Fundamental** | Hybrid | Authoritative sources, hospital confirmation, verification playbook | Every discoverable/assignable doctor and hospital has approved evidence, source/date, scope, and no unresolved block. |
| Focused doctor/hospital profile | Referrer, patient, hospital | Establish relevance and institutional context. | **Fundamental** | Software content; manually curated | Verification | A referrer can decide whether to open a profile/referral without sales intervention, and claims match evidence. |
| Specialist search | Referring doctor, case manager | Find the small relevant receiving roster. | **Fundamental** | Software filters; human shortlist | Verified roster and controlled taxonomy | A user can find an eligible specialist by specialty/procedure, hospital, country/language, and active availability; no paid ordering. |
| Professional connection | Doctors | Preserve a reusable trusted relationship. | **Fundamental, minimal** | Software; manual introductions | Verified doctor accounts | Request, accept/decline, view, remove/report work; pre-connection users cannot send patient data. |
| Referral creation and patient invitation | Referring doctor | Turn discovery into the core transaction. | **Fundamental** | Software; assisted by case manager | Profile, patient contact, corridor policy | Doctor creates a referral with clinical question/source and patient receives an attributable activation request. |
| Patient activation, consent, and participants | Patient/guardian | Authorize the case and make sharing visible. | **Fundamental** | Software; manual exceptions | Reviewed notices/consent and authority policy | Patient can approve/decline the named purpose/recipient, see participants, and revoke future access through support/workflow. |
| Case summary and medical records | Patient, doctors, hospital, case manager | Give the reviewer one organized packet. | **Fundamental** | Software upload/timeline; human completeness | File policy, secure storage process, document categories | Multiple PDFs/images are categorized and attributable; originals persist; a non-authorized user cannot view/download. |
| Provider review request / controlled share | Case manager, hospital | Isolate each hospital's access and SLA. | **Fundamental** | Software action; fully human matching | Consent, verified hospital, complete case | Only the selected hospital receives the declared record manifest; another hospital sees nothing; recipient and sent time are recorded. |
| Hospital inbox, qualification, and assignment | IPD coordinator | Put a named team behind every received case. | **Fundamental** | Software; human decisions | Hospital membership, provider request, SLA | Hospital accepts/declines/asks; accepted case has verified specialist, coordinator, owner, and response due state. |
| Information requests and case messaging | Case participants | Resolve missing information and collaborate without unsafe generic chat. | **Fundamental** | Software; human communication | Active case access and recipients | Specialist issues a specific request; patient/referrer responds; audience/authorship/time appear in one history. |
| Attributable preliminary opinion | Indian specialist | Deliver the primary clinical response without platform authorship. | **Fundamental** | Software issue/upload; clinician creates content | Assigned verified specialist, adequate records | Only eligible assigned clinician can issue; patient/referrer sees author, date/version, reviewed scope, and limitations. |
| Hospital proposal and indicative quote | Hospital coordinator/finance; clinician owns clinical part | Convert opinion into a decision-ready offer. | **Fundamental** | Minimal structured software; manual preparation/normalization | Issued opinion and hospital authorization | Issued response contains facility/doctor, pathway, estimate/currency, assumptions, inclusions/exclusions, validity, and version. |
| Case stage, next action, owner, SLA, and outcome | All scoped users | Prevent silent failure and measure value. | **Fundamental** | Software; human updates/escalation | Controlled lifecycle | Every active case/provider request has one current stage, owner, next action, and timestamp; material transitions are attributable. |
| Patient response and simple journey/handback | Patient, referrer, hospital, case manager | Record decision and close the referral loop. | **Fundamental** | Software status/documents; human pre-travel and follow-up | Proposal, selected hospital, authorized recipients | Patient records proceed/clarify/decline/pause; selected case tracks next milestone; discharge/follow-up reaches patient and authorized referrer or has a reason. |
| Operations and verification queue with audit | Platform team | Let a small team safely operate 10–100 cases and prove what happened. | **Fundamental** | Software queue/history; human work | All core events and role policy | Team can find unowned/blocked/SLA-risk work; access/share/assignment/issue/status events are searchable and pilot metrics can be exported. |
| Proposal comparison | Patient/referrer | Clarify multiple responses without price ranking. | **Early** | Human-prepared initially; later software | Two comparable issued proposals | Patient can see assumptions/differences/missing items and make a decision without “best/cheapest” ranking. |
| Referral templates and repeat flow | Referring doctor, hospital | Reduce time and improve completeness on the next case. | **Early** | Software after manual pattern evidence | At least 10 cases in one specialty | Repeat referrer submits a complete eligible case with fewer manual touches/time than first referral. |
| Relationship/pilot analytics | Hospital manager, founder | Prove renewal value and network compounding. | **Early** | Controlled export/manual report; later software | Accurate core event capture and definitions | Report reconciles qualified cases, response time, stages, arrivals, lost reasons, active/repeat referrers, and operator effort. |
| AI document/matching/translation | Operators/participants | Potentially reduce repetitive work only after a stable corpus exists. | **Bonus** | No V0; future assisted workflow | Sufficient labeled examples, evaluation, governance, human review | Must beat manual baseline without new material errors; never makes independent clinical decisions. |
| Social feed/ratings/travel marketplace/native app | Various | Does not support the first referral loop. | **No** | Do not build | Proven new strategy would be required | No V0 resources allocated. |

## V0 scope rule

The first release contains the 16 fundamental matrix rows only. The early rows enter work only after the acceptance scenario succeeds and real cases show the manual approach is a measurable bottleneck. Bonus/no rows are outside V0.
