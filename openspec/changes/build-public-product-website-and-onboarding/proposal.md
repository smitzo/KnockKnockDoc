# Build the public product website and verified partner onboarding

## Why

Knock Knock Doc currently looks like a prototype route collection, not a coherent product website. A doctor cannot understand the company, browse the provider model, inspect a hospital, register an identity, or see why the platform should be trusted from one stable navigation system. The five existing evidence articles also exist without enough prominence in the main product journey.

The public surface must establish trust before asking for an account. The authenticated product remains doctor-first: a referring doctor discovers a specialist, compares bounded professional information, connects, communicates, and starts a referral. Patients may read public educational content, but the home page and onboarding must not silently turn into an unqualified patient lead marketplace.

## Benchmark and product decision

Vaidam was reviewed on 2026-08-11 as an information-architecture benchmark. Its public surface exposes doctors, hospitals, treatments/cost, knowledge, patient stories, About, partner services, and medical-travel support. Its doctor listings emphasize specialty, location, experience, designation, hospital, qualifications, and availability actions; hospital pages emphasize accreditation, departments, doctors, infrastructure, facilities, location, and galleries.

Knock Knock Doc will adopt the useful discoverability pattern, not Vaidam's claims, copy, ranking language, open patient-enquiry funnel, WhatsApp-first interactions, or unverified success/outcome framing. The differentiator remains an accountable doctor-to-doctor relationship and closed-loop referral.

Sources reviewed:

- https://www.vaidam.com/
- https://www.vaidam.com/about-us
- https://www.vaidam.com/doctors/oncology-and-oncosurgery/cancer-treatment/india
- https://www.vaidam.com/hospitals/
- https://www.vaidam.com/vaidam-doctor-services
- https://www.vaidam.com/vaidam-hospital-services

## What changes

- Introduce one responsive public header/footer and a clear sitemap: Home, Doctors, Hospitals, How it works, Insights, About, Sign in, and Join.
- Reframe the home page around the doctor-first `Discover -> Compare -> Connect -> Refer` job.
- Add public doctor and hospital list/detail route contracts with publication and verification gates.
- Keep synthetic admin-lab patient/account fields outside every public representation.
- Add separate doctor and hospital registration paths with complete, role-specific fields and explicit review states.
- Preserve secure session login; registration never grants active professional or organization privileges immediately.
- Make all five reusable evidence articles reachable from the header, home page, footer, and stable `/blog` routes.
- Add About, trust, service boundaries, contact, privacy, terms, accessibility, and medical/emergency disclaimers.

## Non-goals

- Copying another company's visual design, prose, rankings, testimonials, metrics, or provider claims.
- Open publication of self-entered credentials, accreditations, outcomes, prices, or success rates.
- Patient cold-messaging, instant booking, medical advice, emergency triage, treatment recommendation, payment, visa fulfillment, or travel booking in this phase.
- Social login, public passwords, weak default credentials, or automatic activation after registration.
- Search-engine publication of synthetic admin-lab records.

## Impact

The frontend gains a stable public information architecture and reusable provider/content components. The backend gains application records and verification/publication states distinct from active identities and memberships. Existing identity, organization, professional-network, and admin-lab boundaries remain authoritative; the new public read models expose only explicitly published fields.
