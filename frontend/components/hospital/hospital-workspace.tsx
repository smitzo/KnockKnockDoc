"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { Icon } from "@/components/icons";
import { Brand } from "@/components/site-header";
import { logoutSession } from "@/lib/api";
import type { SessionMembership, SessionResponse } from "@/lib/types";
import styles from "@/styles/hospital-workspace.module.css";

export function HospitalWorkspace({
  demoModeEnabled,
  membership,
  session,
}: {
  demoModeEnabled: boolean;
  membership: SessionMembership;
  session: SessionResponse;
}) {
  const router = useRouter();
  const [signingOut, setSigningOut] = useState(false);

  async function signOut() {
    setSigningOut(true);
    await logoutSession();
    router.replace("/login");
    router.refresh();
  }

  return (
    <div className={styles.app}>
      <header className={styles.header}>
        <Brand />
        <nav aria-label="Hospital workspace"><a aria-current="page" href="#overview">Overview</a><a href="#profile">Organization profile</a><a href="#referrals">Referrals</a></nav>
        <button className="button button--ghost button--small" disabled={signingOut} onClick={signOut} type="button">{signingOut ? "Signing out…" : "Sign out"}</button>
      </header>
      <main className={`${styles.main} page-shell`}>
        <section className={styles.welcome} id="overview"><div><span className="eyebrow">Hospital workspace</span><h1>Welcome, {session.profile.display_name}.</h1><p>Manage how {membership.organization.name} participates in professional referrals and keeps the handoff accountable.</p></div><span className={styles.accessState}><Icon name="check" /> Active coordinator</span></section>
        {demoModeEnabled && <div className={styles.demoNotice}><Icon name="shield" /><p><strong>Synthetic activation</strong>This local approval proves the workflow only; it is not evidence that a real hospital, mailbox, accreditation, or representative was verified.</p></div>}
        <section className={styles.metrics} aria-label="Hospital workspace summary"><article><span>Published doctors</span><strong>0</strong><small>Addition requires individual professional review.</small></article><article><span>Open referrals</span><strong>0</strong><small>No patient or case access was granted at activation.</small></article><article><span>Pending responses</span><strong>0</strong><small>Assigned referrals will appear here.</small></article></section>
        <div className={styles.grid}>
          <section className={styles.card} id="profile"><header><span><Icon name="home" /></span><div><small>Organization profile</small><h2>{membership.organization.name}</h2></div></header><dl><div><dt>Organization role</dt><dd>{membership.role_label}</dd></div><div><dt>Workspace status</dt><dd>Active</dd></div><div><dt>Profile visibility</dt><dd>Private until publication review</dd></div></dl><div className={styles.progress}><div><span>Activation foundation</span><strong>3 of 6</strong></div><i><b /></i></div><ul><li><Icon name="check" /> Coordinator account activated</li><li><Icon name="check" /> Organization boundary created</li><li><Icon name="check" /> No automatic patient access</li><li><Icon name="timeline" /> Credential evidence review pending</li><li><Icon name="timeline" /> Public profile review pending</li><li><Icon name="timeline" /> Doctor affiliations pending</li></ul></section>
          <section className={styles.card} id="referrals"><header><span><Icon name="document" /></span><div><small>Referral inbox</small><h2>No referrals assigned</h2></div></header><p className={styles.cardCopy}>A professional connection and hospital membership are not enough to open a case. Each referral needs a named assignment, patient sharing decision, and bounded grant.</p><div className={styles.empty}><Icon name="lock" /><p><strong>Your inbox is private and empty.</strong>Authorized referrals will appear with their question, due date, and accountable participants.</p></div><Link className="button button--ghost" href="/how-to">Review the referral flow <Icon name="arrow" /></Link></section>
        </div>
      </main>
    </div>
  );
}
