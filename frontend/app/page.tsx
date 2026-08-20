import Link from "next/link";

import { Icon } from "@/components/icons";
import { PrototypeBanner, SiteHeader } from "@/components/site-header";

const referralSteps = [
  ["1", "Your doctor prepares the referral", "One clear clinical question and an organized record summary."],
  ["2", "You choose what is shared", "See the people, purpose, and information before the case moves."],
  ["3", "A named specialist team responds", "Questions and responses stay attributable—never a mystery inbox."],
  ["4", "Your home doctor stays connected", "The decision and later handback return to the care relationship you trust."],
];

export default function HomePage() {
  return (
    <>
      <PrototypeBanner />
      <SiteHeader />
      <main>
        <section className="hero page-shell">
          <div className="hero__copy">
            <div className="eyebrow"><Icon name="shield" /> Planned cross-border care, thoughtfully coordinated</div>
            <h1>A safer handoff, from your doctor to the right hospital team.</h1>
            <p className="hero__lead">
              One calm, shared place for a referral, its records, the people involved,
              and the next decision—without losing your home doctor along the way.
            </p>
            <div className="hero__actions">
              <Link className="button button--large" href="/workspace">
                Explore the demo case <Icon name="arrow" />
              </Link>
              <Link className="button button--ghost button--large" href="/refer">
                Rehearse a referral
              </Link>
            </div>
            <div className="hero__promise" aria-label="Product promises">
              <span><Icon name="check" /> Named care team</span>
              <span><Icon name="check" /> Visible sharing</span>
              <span><Icon name="check" /> Clear next step</span>
            </div>
          </div>

          <div className="hero-card" aria-label="Synthetic referral preview">
            <div className="hero-card__top">
              <div>
                <span className="hero-card__kicker">Referral journey</span>
                <strong>Every handoff stays visible</strong>
              </div>
              <span className="status-pill status-pill--live"><span /> On track</span>
            </div>
            <div className="care-path">
              <article className="care-person care-person--complete">
                <span className="care-person__avatar care-person__avatar--sage">LA</span>
                <div><strong>Dr. Lena A.</strong><span>Home doctor · Referral sent</span></div>
                <span className="care-person__check"><Icon name="check" /></span>
              </article>
              <div className="care-path__line"><span /></div>
              <article className="care-person care-person--complete">
                <span className="care-person__avatar care-person__avatar--blue">AM</span>
                <div><strong>Ama K.</strong><span>Patient · Sharing approved</span></div>
                <span className="care-person__check"><Icon name="check" /></span>
              </article>
              <div className="care-path__line"><span /></div>
              <article className="care-person care-person--active">
                <span className="care-person__avatar care-person__avatar--gold">AR</span>
                <div><strong>Dr. Arun Mehta</strong><span>Receiving specialist · Responded</span></div>
                <span className="care-person__pulse" />
              </article>
            </div>
            <div className="hero-card__next">
              <span className="icon-tile"><Icon name="spark" /></span>
              <div><span>Next step</span><strong>Review the response together</strong></div>
              <Icon name="chevron" />
            </div>
            <p className="synthetic-caption">Illustrative people and care only. No real health data.</p>
          </div>
        </section>

        <section className="trust-strip" aria-label="Core service boundaries">
          <div className="page-shell trust-strip__inner">
            <div><Icon name="lock" /><span><strong>Consent-led</strong>Nothing moves silently</span></div>
            <div><Icon name="people" /><span><strong>Human-owned</strong>A named coordinator follows through</span></div>
            <div><Icon name="document" /><span><strong>Attributable</strong>Every request and response has an author</span></div>
            <div><Icon name="timeline" /><span><strong>Closed-loop</strong>Your home doctor remains informed</span></div>
          </div>
        </section>

        <section className="section page-shell" id="how-it-works">
          <div className="section-heading section-heading--center">
            <span className="eyebrow eyebrow--quiet">A referral, not a maze</span>
            <h2>Four moments. One accountable journey.</h2>
            <p>Designed around what people need to understand when a healthcare decision crosses borders.</p>
          </div>
          <div className="steps-grid">
            {referralSteps.map(([number, title, body]) => (
              <article className="step-card" key={number}>
                <span className="step-card__number">{number}</span>
                <h3>{title}</h3>
                <p>{body}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="care-section" id="built-for-care">
          <div className="page-shell care-section__grid">
            <div className="section-heading">
              <span className="eyebrow eyebrow--quiet">Built around both sides of care</span>
              <h2>Clear enough for a worried patient. Precise enough for a busy doctor.</h2>
              <p>
                The same referral is explained differently to each person, while its source,
                scope, and ownership stay consistent.
              </p>
              <Link className="text-cta" href="/workspace">
                See the role-aware workspace <Icon name="arrow" />
              </Link>
            </div>
            <div className="perspective-stack">
              <article className="perspective-card perspective-card--patient">
                <span className="perspective-card__icon"><Icon name="heart" /></span>
                <div>
                  <span className="perspective-card__label">For the patient</span>
                  <h3>“What happens next, and who can see my case?”</h3>
                  <p>A single next action, plain-language response, and visible participant access.</p>
                </div>
              </article>
              <article className="perspective-card perspective-card--doctor">
                <span className="perspective-card__icon"><Icon name="document" /></span>
                <div>
                  <span className="perspective-card__label">For the doctor</span>
                  <h3>“Was my question answered, and will the care loop return?”</h3>
                  <p>Structured records, attributable specialist review, and a clear handback path.</p>
                </div>
              </article>
            </div>
          </div>
        </section>

        <section className="section page-shell" id="safety">
          <div className="boundary-card">
            <div className="boundary-card__mark"><Icon name="shield" /></div>
            <div>
              <span className="eyebrow eyebrow--quiet">An important boundary</span>
              <h2>Coordination stays separate from clinical judgment.</h2>
              <p>
                Knock Knock Doc helps the right people receive, understand, and act on a referral.
                Licensed clinicians remain responsible for diagnosis and treatment. This prototype
                uses fictional data and is not an emergency, diagnostic, or medical-advice service.
              </p>
            </div>
            <Link className="button button--ghost" href="/workspace">See it in the demo</Link>
          </div>
        </section>

        <section className="closing-cta">
          <div className="page-shell closing-cta__inner">
            <div><span className="eyebrow">Prototype V0</span><h2>Walk through the first referral loop.</h2></div>
            <Link className="button button--light button--large" href="/workspace">
              Open the synthetic case <Icon name="arrow" />
            </Link>
          </div>
        </section>
      </main>
      <footer className="site-footer">
        <div className="page-shell site-footer__inner">
          <div><strong>knock<span>knock</span>doc</strong><p>Care referrals, kept connected.</p></div>
          <p>Prototype V0 · Fictional data only · © 2026</p>
        </div>
      </footer>
    </>
  );
}
