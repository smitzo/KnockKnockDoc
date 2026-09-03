import type { Metadata } from "next";
import Link from "next/link";

import { Icon } from "@/components/icons";
import { SiteFooter, SiteHeader } from "@/components/site-header";
import styles from "@/styles/public-pages.module.css";

export const metadata: Metadata = { title: "Join the professional network" };

export default function JoinPage() {
  return <><SiteHeader /><main className={styles.page}>
    <section className={styles.hero}><div className="page-shell"><div><span className={styles.eyebrow}>Join Knock Knock Doc</span><h1>Grow your professional referral network.</h1><p>Choose the path that fits you. Doctor and hospital applications follow a short review before the account becomes active.</p></div></div></section>
    <section className={`${styles.content} page-shell`}>
      <div className={styles.choiceGrid}>
        <article className={styles.choiceCard}><span><Icon name="people" /></span><small>For individual clinicians</small><h2>Register as a doctor</h2><p>Join as a referring doctor or receiving specialist and describe how you want to collaborate.</p><ul><li>Build your professional profile</li><li>Connect by specialty and location</li><li>Manage referrals with trusted peers</li></ul><Link className="button" href="/register/doctor">Start doctor application <Icon name="arrow" /></Link></article>
        <article className={styles.choiceCard}><span><Icon name="home" /></span><small>For provider organizations</small><h2>Register a hospital</h2><p>Introduce your organization, departments, services, and professional partnership team.</p><ul><li>Create a hospital profile</li><li>Present departments and services</li><li>Connect with referring doctors</li></ul><Link className="button" href="/register/hospital">Start hospital application <Icon name="arrow" /></Link></article>
      </div>
      <section className={styles.boundary}><div><span className={styles.eyebrow}>What happens next</span><h2>A short review keeps the network useful.</h2></div><ul><li><strong>1. Send your application.</strong> Complete the three-step form.</li><li><strong>2. We review the profile.</strong> Identity, professional role, and organization details are checked.</li><li><strong>3. Start connecting.</strong> Approved members can discover doctors and build their network.</li></ul></section>
    </section>
  </main><SiteFooter /></>;
}
