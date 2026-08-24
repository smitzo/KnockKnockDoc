import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";

import { Icon } from "@/components/icons";
import { PrototypeBanner, SiteHeader } from "@/components/site-header";
import styles from "@/styles/guide.module.css";

export const metadata: Metadata = { title: "How to use Knock Knock Doc" };

const steps = [
  { number: "01", owner: "Referring doctor", title: "Start with one bounded question", copy: "Sign in, create a fictional planned-care referral, preserve the patient alias and the home doctor’s exact question.", action: "Rehearse a referral", href: "/refer" },
  { number: "02", owner: "Patient", title: "Review purpose and people", copy: "See who is named, why they need access, what scope is represented, and what information remains missing before deciding to share.", action: "Open assigned workspace", href: "/workspace" },
  { number: "03", owner: "Coordinator", title: "Make the packet understandable", copy: "Track metadata, source, readiness and requests. Upload remains disabled until the secure-record release gates exist.", action: "Understand the boundary", href: "#safety-boundary" },
  { number: "04", owner: "Receiving team", title: "Return an attributable response", copy: "Keep the named clinician’s preliminary opinion separate from coordination and any indicative commercial proposal.", action: "See response anatomy", href: "#response" },
  { number: "05", owner: "Patient + home doctor", title: "Choose without pressure", copy: "Proceed, pause, ask for clarification or decline. A response is not a diagnosis, guarantee, visa approval or obligation to travel.", action: "Read planning evidence", href: "/blog" },
  { number: "06", owner: "Care teams", title: "Close the loop with handback", copy: "Record what happened, what changed, which source is authoritative, and who owns follow-up in the home system.", action: "View the full loop", href: "#flow" },
];

export default function HowToPage() {
  return <><PrototypeBanner /><SiteHeader /><main className={styles.page}>
    <section className="guide-heading page-shell"><span className="eyebrow">How to use the product</span><h1>One referral. Named people. A visible next step.</h1><p>Follow the arrows from the trusted home-doctor question to an attributable response and handback. Every screen in this guide uses fictional data.</p></section>
    <figure className="annotated-figure page-shell"><Image alt="Illustrative referral flow from patient and home doctor through a secure case to an Indian specialist and coordinator" height={900} priority sizes="(max-width: 1200px) 100vw, 1180px" src="/images/referral-guide-hero.png" width={1600} /><span className="figure-marker figure-marker--one"><b>1</b> Home question</span><span className="figure-marker figure-marker--two"><b>2</b> Scoped case</span><span className="figure-marker figure-marker--three"><b>3</b> Named response</span><i className="figure-arrow figure-arrow--one" /><i className="figure-arrow figure-arrow--two" /><figcaption>Illustrative AI-generated scene; no real patient, clinician, hospital or outcome is shown.</figcaption></figure>
    <section className="guide-steps page-shell" id="flow">{steps.map((step, index) => <article key={step.number}><span className="guide-step__number">{step.number}</span><div><small>{step.owner}</small><h2>{step.title}</h2><p>{step.copy}</p><Link href={step.href}>{step.action} <Icon name="arrow" /></Link></div>{index < steps.length - 1 && <span className="guide-step__arrow"><Icon name="arrow" /></span>}</article>)}</section>
    <section className="guide-boundaries page-shell" id="safety-boundary"><div><Icon name="shield" /><span>Safety and access boundary</span><h2>Authentication is working. Real health data is still not allowed.</h2></div><ul><li><strong>Case access is server-enforced.</strong> Active identity, organization membership, assignment, current grant and scope are all required.</li><li><strong>Records are metadata only.</strong> File upload stays disabled until private storage, scanning, category authorization and audit gates pass.</li><li><strong>No emergency or medical decision support.</strong> Urgent concerns belong with local emergency services and treating clinicians.</li><li><strong>No outcome or travel promise.</strong> Responses are bounded and visas, capacity, price and suitability remain independently confirmed.</li></ul></section>
    <section className="guide-cta"><div className="page-shell"><div><span className="eyebrow">Choose your next rehearsal</span><h2>Sign in with a fictional role and follow only what that role is allowed to see.</h2></div><Link className="button button--light button--large" href="/login">Sign in <Icon name="arrow" /></Link></div></section>
  </main></>;
}
