import Link from "next/link";

import { Icon } from "@/components/icons";
import { PrototypeBanner, SiteFooter, SiteHeader } from "@/components/site-header";
import { getBlogArticles } from "@/lib/blog-content";
import styles from "@/styles/home.module.css";

const networkSteps = [
  { icon: "search" as const, title: "Discover", body: "Search by specialty, location, language, and professional focus." },
  { icon: "shield" as const, title: "Compare", body: "Review verified facts and transparent peer-collaboration feedback." },
  { icon: "people" as const, title: "Connect", body: "Send a purpose-bound request before any case or patient context is shared." },
  { icon: "document" as const, title: "Refer", body: "Create a structured handoff only after the professional connection is accepted." },
];

export default function HomePage() {
  const articles = getBlogArticles().slice(0, 3);

  return (
    <>
      <PrototypeBanner />
      <SiteHeader />
      <main className={styles.page}>
        <section className={`${styles.hero} page-shell`}>
          <div className={styles.heroCopy}>
            <span className={styles.eyebrow}><Icon name="people" /> Built for doctor-to-doctor referrals</span>
            <h1>Find the right specialist before you refer.</h1>
            <p>
              Discover trusted clinicians, understand how they collaborate, connect with a clear
              purpose, and keep the referral loop visible from first question to handback.
            </p>
            <div className={styles.heroActions}>
              <Link className="button button--large" href="/doctors">Discover doctors <Icon name="arrow" /></Link>
              <Link className="button button--ghost button--large" href="/how-to">See how it works</Link>
            </div>
            <ul className={styles.heroAssurances}>
              <li><Icon name="check" /> Verification before visibility</li>
              <li><Icon name="check" /> Connection before referral</li>
              <li><Icon name="check" /> No real health data in V0</li>
            </ul>
          </div>

          <div className={styles.networkPreview} aria-label="Illustrative professional discovery interface">
            <div className={styles.previewTop}>
              <div><span>Professional network</span><strong>Find a specialist</strong></div>
              <span className={styles.previewStatus}>Illustrative</span>
            </div>
            <div className={styles.searchMock}><Icon name="search" /><span>Specialty, city, or clinical focus</span></div>
            <article className={styles.profileAnatomy}>
              <span className={styles.avatar}><Icon name="people" /></span>
              <div>
                <small>Verified profile anatomy</small>
                <strong>Specialty and current designation</strong>
                <p>Experience · affiliation · languages</p>
              </div>
              <span className={styles.verified}><Icon name="shield" /> Verified</span>
            </article>
            <div className={styles.feedbackMock}>
              <div><strong>Peer collaboration</strong><span>Not a clinical outcome score</span></div>
              <dl><div><dt>Communication</dt><dd>Transparent aggregate</dd></div><div><dt>Referral clarity</dt><dd>Count shown</dd></div></dl>
            </div>
            <div className={styles.previewAction}><Icon name="message" /><span><small>Next safe action</small><strong>Connect with a stated purpose</strong></span><Icon name="chevron" /></div>
          </div>
        </section>

        <section className={styles.pathSection}>
          <div className="page-shell">
            <div className={styles.sectionHeading}>
              <span>One understandable workflow</span>
              <h2>Discover → Compare → Connect → Refer</h2>
              <p>The relationship comes first. Patient context enters only after a trusted professional connection exists.</p>
            </div>
            <div className={styles.steps}>
              {networkSteps.map((item, index) => (
                <article key={item.title}>
                  <span className={styles.stepIcon}><Icon name={item.icon} /></span>
                  <small>0{index + 1}</small>
                  <h3>{item.title}</h3>
                  <p>{item.body}</p>
                  {index < networkSteps.length - 1 && <span className={styles.stepArrow} aria-hidden="true">→</span>}
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className={`${styles.roles} page-shell`}>
          <div className={styles.sectionHeading}>
            <span>Useful on both sides of the introduction</span>
            <h2>A professional network with a referral workflow—not a lead marketplace.</h2>
          </div>
          <div className={styles.roleGrid}>
            <article>
              <span><Icon name="search" /></span>
              <div><small>For referring doctors</small><h3>Make a confident first connection.</h3><p>Search a focused directory, understand credentials and collaboration signals, then contact a named peer with a bounded purpose.</p><Link href="/register/doctor">Join as a referring doctor <Icon name="arrow" /></Link></div>
            </article>
            <article>
              <span><Icon name="message" /></span>
              <div><small>For specialists and hospitals</small><h3>Receive clearer, more accountable referrals.</h3><p>Present verified professional facts, set collaboration expectations, and respond within an attributable conversation.</p><Link href="/join">See partner paths <Icon name="arrow" /></Link></div>
            </article>
          </div>
        </section>

        <section className={styles.trustSection}>
          <div className={`${styles.trustGrid} page-shell`}>
            <div>
              <span className={styles.eyebrow}><Icon name="shield" /> Trust is a product surface</span>
              <h2>Ratings describe collaboration—not medical quality or outcomes.</h2>
              <p>Every published signal needs provenance, a visible count, a defined category, and a route to correction. Credentials need human verification before a profile becomes public.</p>
              <Link className="button button--ghost" href="/about">Read our operating boundary</Link>
            </div>
            <ul>
              <li><Icon name="check" /><span><strong>Identity before reach</strong>Applications remain inactive until a reviewer approves them.</span></li>
              <li><Icon name="check" /><span><strong>Purpose before chat</strong>Connection requests state why one doctor wants to collaborate.</span></li>
              <li><Icon name="check" /><span><strong>Consent before case access</strong>A connection never grants automatic access to a referral.</span></li>
              <li><Icon name="check" /><span><strong>Clinical judgment stays human</strong>The product coordinates; licensed clinicians diagnose and treat.</span></li>
            </ul>
          </div>
        </section>

        <section className={`${styles.insights} page-shell`}>
          <div className={styles.insightsHeading}><div className={styles.sectionHeading}><span>Evidence and planning</span><h2>Useful context, with sources and uncertainty.</h2></div><Link href="/blog">View all insights <Icon name="arrow" /></Link></div>
          <div className={styles.articleGrid}>
            {articles.map((article) => (
              <article key={article.slug}>
                <span>{article.category} · {article.readMinutes} min</span>
                <h3><Link href={`/blog/${article.slug}`}>{article.title}</Link></h3>
                <p>{article.dek}</p>
                <Link href={`/blog/${article.slug}`}>Read sourced article <Icon name="arrow" /></Link>
              </article>
            ))}
          </div>
        </section>

        <section className={styles.closing}>
          <div className="page-shell">
            <div><small>Prototype partner applications</small><h2>Build a trusted referral network, one verified relationship at a time.</h2><p>Applications use fictional data in V0 and do not grant immediate access.</p></div>
            <Link className="button button--light button--large" href="/join">Choose how to join <Icon name="arrow" /></Link>
          </div>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
