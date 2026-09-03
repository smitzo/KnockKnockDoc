import type { Metadata } from "next";
import Link from "next/link";

import { Icon } from "@/components/icons";
import { SiteFooter, SiteHeader } from "@/components/site-header";
import styles from "@/styles/public-pages.module.css";

export const metadata: Metadata = { title: "Discover doctors" };

export default function DoctorsPage() {
  return <><SiteHeader /><main className={styles.page}>
    <section className={styles.hero}><div className="page-shell"><div><span className={styles.eyebrow}>Professional discovery</span><h1>Find a doctor you can trust enough to call a colleague.</h1><p>Search by specialty, location, language, experience, and professional focus. Review the context behind every profile before you connect.</p><div className={styles.heroActions}><Link className="button" href="/login?next=/network">Sign in to search <Icon name="arrow" /></Link><Link className="button button--ghost" href="/register/doctor">Join as a doctor</Link></div></div></div></section>
    <section className={`${styles.content} page-shell`}>
      <div className={styles.directoryPanel}><div><span><Icon name="search" /></span><h2>The doctor directory is available after sign-in.</h2><p>Professional profiles, collaboration ratings, connection requests, and messages stay inside the secure doctor workspace.</p><div><Link className="button" href="/login?next=/network">Open doctor network <Icon name="arrow" /></Link><Link className="button button--ghost" href="/how-to">How it works</Link></div></div></div>
      <section className={styles.fieldPreview}><div className={styles.sectionHeading}><span>What a reviewed profile will show</span><h2>Useful professional facts, with context.</h2><p>Private contact, credential evidence, reviewer notes, and patient information will never appear in the public read model.</p></div><div className={styles.directoryGrid}><article><small>Professional focus</small><h3>Specialty and subspecialties</h3><p>Current designation, experience start year, clinical focus, and languages.</p></article><article><small>Trust context</small><h3>Verified affiliation</h3><p>Organization, location, credential review date, and the provenance of published claims.</p></article><article><small>Peer collaboration</small><h3>Transparent feedback</h3><p>Category aggregates, response count, and a clear warning that feedback is not an outcome score.</p></article></div></section>
    </section>
  </main><SiteFooter /></>;
}
