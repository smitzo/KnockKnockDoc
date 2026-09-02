import type { Metadata } from "next";
import Link from "next/link";

import { Icon } from "@/components/icons";
import { PrototypeBanner, SiteFooter, SiteHeader } from "@/components/site-header";
import styles from "@/styles/public-pages.module.css";

export const metadata: Metadata = { title: "About" };

export default function AboutPage() {
  return <><PrototypeBanner /><SiteHeader /><main className={styles.page}>
    <section className={styles.hero}><div className="page-shell"><div><span className={styles.eyebrow}>Why Knock Knock Doc exists</span><h1>Cross-border referrals should begin with trusted doctors—not anonymous lead forms.</h1><p>We are prototyping infrastructure for professional discovery, accountable introductions, structured referrals, and visible handback. The goal is continuity: the home doctor stays connected while a named specialist contributes.</p><div className={styles.heroActions}><Link className="button" href="/how-to">See the product flow <Icon name="arrow" /></Link><Link className="button button--ghost" href="/join">Join the network</Link></div></div></div></section>
    <section className={`${styles.content} page-shell`}>
      <div className={styles.sectionHeading}><span>Design principles</span><h2>Simple for a busy clinician. Understandable for a patient. Strict at every trust boundary.</h2></div>
      <div className={styles.valueGrid}>
        <article><span><Icon name="people" /></span><h3>Relationship first</h3><p>Doctors discover and connect with peers before starting any patient-specific referral.</p></article>
        <article><span><Icon name="shield" /></span><h3>Claims need provenance</h3><p>Credential, capacity, rating, and affiliation fields need a source, review state, and correction path.</p></article>
        <article><span><Icon name="document" /></span><h3>One accountable handoff</h3><p>Questions, responses, access, decisions, and handback remain attributable to named participants.</p></article>
      </div>
      <section className={styles.boundary}><div><span className={styles.eyebrow}>Operating boundary</span><h2>Coordination is not diagnosis, treatment, ranking, or an outcome promise.</h2></div><ul><li><strong>Doctors remain clinically responsible.</strong> The platform does not replace independent medical judgment.</li><li><strong>Collaboration ratings are narrowly defined.</strong> They do not measure clinical quality, suitability, or outcomes.</li><li><strong>No emergency support.</strong> Urgent symptoms belong with local emergency services and treating professionals.</li><li><strong>Prototype V0 is synthetic-only.</strong> Real identities, credentials, and health information are prohibited until launch gates pass.</li></ul></section>
    </section>
  </main><SiteFooter /></>;
}
