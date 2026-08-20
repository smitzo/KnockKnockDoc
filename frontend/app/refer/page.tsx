import type { Metadata } from "next";

import { ReferralComposer } from "@/components/referral-composer";
import { PrototypeBanner, SiteHeader } from "@/components/site-header";

export const metadata: Metadata = { title: "Rehearse a referral" };

export default function ReferPage() {
  return (
    <>
      <PrototypeBanner />
      <SiteHeader />
      <main className="refer-page">
        <ReferralComposer />
      </main>
    </>
  );
}
