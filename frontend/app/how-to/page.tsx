import type { Metadata } from "next";
import Link from "next/link";

import { Icon } from "@/components/icons";
import { SiteFooter, SiteHeader } from "@/components/site-header";
import styles from "@/styles/guide.module.css";

export const metadata: Metadata = { title: "How it works" };

const steps = [
  {
    number: "01",
    owner: "Discover",
    title: "Find the right specialist",
    copy: "Search doctors by specialty, location, language, experience, and professional focus.",
  },
  {
    number: "02",
    owner: "Connect",
    title: "Introduce yourself",
    copy: "Send a connection request with a clear professional reason. The other doctor chooses whether to accept.",
  },
  {
    number: "03",
    owner: "Discuss",
    title: "Confirm referral fit",
    copy: "Use private professional chat to align on expertise, process, and handback expectations.",
  },
  {
    number: "04",
    owner: "Refer",
    title: "Start a structured referral",
    copy: "Once connected, create the referral, name the care team, and keep the next action visible.",
  },
];

export default function HowToPage() {
  return <><SiteHeader /><main className={styles.page}>
    <section className="guide-heading page-shell"><span className="eyebrow">How it works</span><h1>From first search to trusted referral.</h1><p>Knock Knock Doc helps doctors build the relationship before moving a referral forward.</p><div className="guide-heading__actions"><Link className="button button--large" href="/login?next=/network">Sign in to start <Icon name="arrow" /></Link><Link className="button button--ghost button--large" href="/doctors">Explore doctor profiles</Link></div></section>
    <section className="guide-steps page-shell" id="flow">{steps.map((step, index) => <article key={step.number}><span className="guide-step__number">{step.number}</span><div><small>{step.owner}</small><h2>{step.title}</h2><p>{step.copy}</p></div>{index < steps.length - 1 && <span className="guide-step__arrow"><Icon name="arrow" /></span>}</article>)}</section>
    <section className="guide-note page-shell"><Icon name="shield" /><div><strong>A clear safety boundary</strong><p>Patient access remains separate from professional connections. Share information only inside an authorized referral, and use local emergency services for urgent care.</p></div></section>
    <section className="guide-cta"><div className="page-shell"><div><span className="eyebrow">Ready to begin?</span><h2>Find a colleague, make a connection, and build a clearer referral.</h2></div><Link className="button button--light button--large" href="/login?next=/network">Sign in <Icon name="arrow" /></Link></div></section>
  </main><SiteFooter /></>;
}
