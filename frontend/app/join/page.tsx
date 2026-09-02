import type { Metadata } from "next";
import Link from "next/link";

import { Icon } from "@/components/icons";
import { PrototypeBanner, SiteFooter, SiteHeader } from "@/components/site-header";
import styles from "@/styles/public-pages.module.css";

export const metadata: Metadata = { title: "Join the professional network" };

export default function JoinPage() {
  return <><PrototypeBanner /><SiteHeader /><main className={styles.page}>
    <section className={styles.hero}><div className="page-shell"><div><span className={styles.eyebrow}>Choose your partner path</span><h1>Join a referral network built around professional trust.</h1><p>Doctor and hospital applications are reviewed before activation. This V0 accepts fictional details only, so you can test the flow without exposing a real identity or credential.</p></div></div></section>
    <section className={`${styles.content} page-shell`}>
      <div className={styles.choiceGrid}>
        <article className={styles.choiceCard}><span><Icon name="people" /></span><small>For individual clinicians</small><h2>Register as a doctor</h2><p>Apply as a referring doctor or receiving specialist and describe how you want to collaborate.</p><ul><li>Professional profile details</li><li>Fictional credential rehearsal</li><li>Human review before access</li></ul><Link className="button" href="/register/doctor">Start doctor application <Icon name="arrow" /></Link></article>
        <article className={styles.choiceCard}><span><Icon name="home" /></span><small>For provider organizations</small><h2>Register a hospital</h2><p>Submit an organization representative application with departments, capacity context, and services.</p><ul><li>Hospital and representative details</li><li>Capacity date and provenance fields</li><li>No listing before review</li></ul><Link className="button" href="/register/hospital">Start hospital application <Icon name="arrow" /></Link></article>
      </div>
      <section className={styles.boundary}><div><span className={styles.eyebrow}>What happens next</span><h2>Submission is the beginning of verification—not instant membership.</h2></div><ul><li><strong>1. Application received.</strong> The account is created inactive and cannot sign in.</li><li><strong>2. Evidence reviewed.</strong> A platform reviewer must verify identity, professional standing, and organization authority.</li><li><strong>3. Access assigned deliberately.</strong> Approval, role, organization membership, and publication remain separate actions.</li><li><strong>4. Periodic re-verification.</strong> A real release also needs correction, suspension, appeal, and expiry operations.</li></ul></section>
    </section>
  </main><SiteFooter /></>;
}
