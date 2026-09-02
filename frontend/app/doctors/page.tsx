import type { Metadata } from "next";
import Link from "next/link";

import { Icon } from "@/components/icons";
import { PrototypeBanner, SiteFooter, SiteHeader } from "@/components/site-header";
import styles from "@/styles/public-pages.module.css";

export const metadata: Metadata = { title: "Discover doctors" };

export default function DoctorsPage() {
  return <><PrototypeBanner /><SiteHeader /><main className={styles.page}>
    <section className={styles.hero}><div className="page-shell"><div><span className={styles.eyebrow}>Professional discovery</span><h1>Find a doctor you can trust enough to call a colleague.</h1><p>Searchable public profiles will appear only after identity, credential, affiliation, and publication review. Admin demo doctors are deliberately excluded from this public directory.</p></div></div></section>
    <section className={`${styles.content} page-shell`}>
      <div className={styles.directoryPanel}><div><span><Icon name="search" /></span><h2>No verified public doctor profiles yet.</h2><p>This is an honest V0 empty state. Loadable synthetic records stay inside the authenticated admin lab and never become public listings.</p><div><Link className="button" href="/register/doctor">Apply as a doctor <Icon name="arrow" /></Link><Link className="button button--ghost" href="/how-to">Understand the flow</Link></div></div></div>
      <section className={styles.fieldPreview}><div className={styles.sectionHeading}><span>What a reviewed profile will show</span><h2>Useful professional facts, with context.</h2><p>Private contact, credential evidence, reviewer notes, and patient information will never appear in the public read model.</p></div><div className={styles.directoryGrid}><article><small>Professional focus</small><h3>Specialty and subspecialties</h3><p>Current designation, experience start year, clinical focus, and languages.</p></article><article><small>Trust context</small><h3>Verified affiliation</h3><p>Organization, location, credential review date, and the provenance of published claims.</p></article><article><small>Peer collaboration</small><h3>Transparent feedback</h3><p>Category aggregates, response count, and a clear warning that feedback is not an outcome score.</p></article></div></section>
    </section>
  </main><SiteFooter /></>;
}
