import type { Metadata } from "next";
import Link from "next/link";

import { Icon } from "@/components/icons";
import { SiteFooter, SiteHeader } from "@/components/site-header";
import styles from "@/styles/public-pages.module.css";

export const metadata: Metadata = { title: "Explore hospitals" };

export default function HospitalsPage() {
  return <><SiteHeader /><main className={styles.page}>
    <section className={styles.hero}><div className="page-shell"><div><span className={styles.eyebrow}>Provider organizations</span><h1>Understand the hospital behind the specialist.</h1><p>Published hospital profiles will separate verified organizational facts from dated capacity statements and self-reported services. Nothing is ranked or guaranteed.</p></div></div></section>
    <section className={`${styles.content} page-shell`}>
      <div className={styles.directoryPanel}><div><span><Icon name="home" /></span><h2>Hospital partnerships begin with a reviewed profile.</h2><p>Hospitals can present departments, services, languages, and dated capacity information to connected doctors.</p><div><Link className="button" href="/register/hospital">Register a hospital <Icon name="arrow" /></Link><Link className="button button--ghost" href="/about">About Knock Knock Doc</Link></div></div></div>
      <section className={styles.fieldPreview}><div className={styles.sectionHeading}><span>What a reviewed profile will show</span><h2>Organization details without marketplace hype.</h2></div><div className={styles.directoryGrid}><article><small>Organization</small><h3>Departments and location</h3><p>Provider type, establishment context, departments, address, and verified affiliations.</p></article><article><small>Dated operations</small><h3>Capacity with an as-of date</h3><p>Bed and service claims are time-bound, sourced, and never presented as live availability.</p></article><article><small>Patient support</small><h3>Services and languages</h3><p>Coordination services, languages, accessibility, and approved media with clear provenance.</p></article></div></section>
    </section>
  </main><SiteFooter /></>;
}
