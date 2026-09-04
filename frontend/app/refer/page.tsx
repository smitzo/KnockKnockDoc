import type { Metadata } from "next";
import { redirect } from "next/navigation";

import { ReferralComposer } from "@/components/referral-composer";
import { SiteHeader } from "@/components/site-header";
import { getProductMode, getServerSession } from "@/lib/api";
import { getServerCookieHeader } from "@/lib/server-cookies";
import accessStyles from "@/styles/access.module.css";

export const metadata: Metadata = { title: "Create a referral" };

export default async function ReferPage() {
  const cookieHeader = await getServerCookieHeader();
  const [session, productMode] = await Promise.all([
    getServerSession(cookieHeader),
    getProductMode(),
  ]);
  if (!session) redirect("/login?next=/refer");
  const referrer = session.memberships.find((membership) => membership.role === "referrer");
  return (
    <>
      <SiteHeader />
      <main className="refer-page">
        {!productMode.demo_data_enabled ? (
          <section className={`${accessStyles.page} page-shell`}>
            <span className={accessStyles.code}>Referral workspace</span>
            <h1>Referral creation is not open in this environment.</h1>
            <p>Your professional network remains available. Referral intake will open only after the required consent and record-security controls are active.</p>
          </section>
        ) : referrer ? (
          <ReferralComposer
            referrerName={session.profile.display_name}
            referrerOrganization={referrer.organization.name}
          />
        ) : (
          <section className={`${accessStyles.page} page-shell`}>
            <span className={accessStyles.code}>Referrer access required</span>
            <h1>This account cannot create a referral.</h1>
            <p>Referral creation is available only to an active, verified referring-doctor membership.</p>
          </section>
        )}
      </main>
    </>
  );
}
