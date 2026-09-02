import type { Metadata } from "next";
import Link from "next/link";

import { Icon } from "@/components/icons";
import { PartnerApplicationForm } from "@/components/registration/partner-application-form";
import { PrototypeBanner, SiteFooter, SiteHeader } from "@/components/site-header";
import styles from "@/styles/public-pages.module.css";

export const metadata: Metadata = { title: "Doctor application" };

export default function DoctorRegistrationPage() {
  return <><PrototypeBanner /><SiteHeader /><main className={styles.registrationPage}><div className="page-shell"><div className={styles.registrationIntro}><Link href="/join"><Icon name="arrow" /> All partner paths</Link><p>Doctor application · Fictional prototype details only · Review required before access</p></div><PartnerApplicationForm kind="doctor" /></div></main><SiteFooter /></>;
}
