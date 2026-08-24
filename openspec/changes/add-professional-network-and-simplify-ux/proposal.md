# Add a bounded professional network and simplify the product UX

## Why

The authenticated prototype is visually polished but cognitively expensive. It explains access-control concepts before the user understands the product, uses oversized editorial typography, exposes too many parallel concepts, and lacks a clear place for a doctor to discover or contact another doctor. A user should be able to answer “what can I do here?” in seconds.

Professional discovery and communication can support the referral loop, but an unrestricted global social network or generic chat would create spam, clinical-boundary, privacy, moderation, and cold-start risk. The product needs the smallest safe interaction: verified professionals find a relevant professional, send a purpose-bound connection request, exchange synthetic professional messages after acceptance, and move patient-specific work into a referral case.

## What changes

- Replace jargon-first navigation and oversized serif typography with a plain sans-serif task hierarchy.
- Present three primary jobs: find a doctor, discuss a professional connection, and manage an assigned referral.
- Add a professional-only, synthetic directory distinct from the admin-only detailed data lab.
- Add purpose-bound connection requests with explicit accept/decline/withdraw states.
- Add accepted-connection messaging with no attachments and a strict synthetic/no-patient-data boundary.
- Add a simple authenticated application shell for directory, connections, messages, and referrals.
- Record network and chat risks, commercial value, failure criteria, and open founder decisions.

## Non-goals

- Public social feeds, followers, popularity counts, reviews, endorsements, or paid ranking.
- Patient-to-doctor cold messaging, unsolicited bulk outreach, lead resale, or referral commission.
- Patient-specific information in professional chat.
- File, image, voice, video, link-preview, or group-chat support.
- Medical advice, diagnosis, prescription, emergency support, or AI-generated clinical messages.
- WebSocket infrastructure before observed use proves real-time delivery is necessary.

## Impact

The modular monolith gains a `professional_network` app, additive tables, session-authenticated APIs, synthetic seed profiles, and security events. The frontend gains a simpler app shell and task-first public explanation. The admin lab remains the only surface that exposes rich synthetic account/operational fixture fields.
