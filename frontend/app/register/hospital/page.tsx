import type { Metadata } from "next";
import Link from "next/link";

import { Icon } from "@/components/icons";
import { PartnerApplicationForm } from "@/components/registration/partner-application-form";
import { SiteFooter, SiteHeader } from "@/components/site-header";
import styles from "@/styles/public-pages.module.css";

export const metadata: Metadata = { title: "Hospital application" };

export default function HospitalRegistrationPage() {
  return <><SiteHeader /><main className={styles.registrationPage}><div className="page-shell"><div className={styles.registrationIntro}><Link href="/join"><Icon name="arrow" /> All partner paths</Link><p>Hospital application · Three short steps · Review required before access</p></div><PartnerApplicationForm kind="hospital" /></div></main><SiteFooter /></>;
}
