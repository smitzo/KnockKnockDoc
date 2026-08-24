# Adversarial review: global doctors and chat

## Verdict

Build a bounded synthetic professional network to test the workflow; do not declare “global network” product-market fit. Chat is commodity infrastructure and provides no moat by itself. It is valuable only if it increases trusted connection-to-referral conversion or keeps the home clinician in the loop.

## Business challenges

- A global directory has a severe cold-start problem: empty corridors are worse than a focused network.
- Doctors already use WhatsApp, email, LinkedIn, hospital portals, and personal referrals. A new inbox must earn repeat attention.
- Free doctor accounts can create support and verification cost without revenue.
- Connection count is a vanity metric unless connections create qualified, completed, closed-loop referrals.
- Hospital-paid distribution can compromise neutrality if ranking or outreach is influenced by payment.
- Unrestricted chat invites spam, patient solicitation, unlicensed cross-border advice, and off-platform leakage.

## Recommended commercial position

- corridor-limited verified professional network, free to participating clinicians;
- hospitals pay for measured referral workflow and operations, not access to vulnerable leads;
- no paid ranking or hidden commission;
- measure accepted connections that lead to appropriate referrals, response, and handback;
- stop expanding the directory if fewer than 20% of qualified connection requests are accepted or accepted connections do not create repeat workflow use.

## Technical challenges

- Production verification and re-verification are unsolved.
- Moderation, reporting, blocking, retention, legal hold, export/deletion, notification preference, and abuse operations are missing.
- Real-time delivery needs WebSocket authorization refresh and delivery semantics; polling is intentionally chosen now.
- Generic chat must never become an authorization shortcut into referral data.
- Message encryption at rest, key management, tamper evidence, backup/restore, and cross-border data roles require production decisions.

## Questions that gate expansion

1. Which corridor supplies the first 20 actively referring doctors and 5 receiving teams?
2. What professional verification evidence is authoritative in both jurisdictions?
3. Why will a doctor open this inbox instead of WhatsApp?
4. Which message must become a case, and how is that transition explained?
5. Who handles spam, harassment, solicitation, and clinical-boundary reports?
6. What network metric predicts paid hospital value?
7. Will hospitals accept a directory whose ordering cannot be purchased?

Recommended default: prove one corridor with connection-to-referral behavior before using the word “global” in customer-facing claims.
