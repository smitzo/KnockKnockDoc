import type { Metadata } from "next";
import { redirect } from "next/navigation";

import { LoginForm } from "@/components/login-form";
import { PrototypeBanner, SiteFooter, SiteHeader } from "@/components/site-header";
import { getServerSession } from "@/lib/api";
import { getServerCookieHeader } from "@/lib/server-cookies";
import styles from "@/styles/login.module.css";

export const metadata: Metadata = { title: "Sign in" };
export const dynamic = "force-dynamic";

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string }>;
}) {
  const cookieHeader = await getServerCookieHeader();
  const session = await getServerSession(cookieHeader);
  if (session) {
    const isAdmin = session.memberships.some((membership) => membership.role === "admin");
    const isProfessional = session.profile.account_type === "professional";
    redirect(isAdmin ? "/admin/lab" : isProfessional ? "/network" : "/workspace");
  }
  const { next = "" } = await searchParams;
  return (
    <>
      <PrototypeBanner />
      <SiteHeader />
      <main className={styles.page}>
        <div className="login-layout page-shell">
          <section className="login-context">
            <span className="eyebrow"><IconShield /> Secure professional access</span>
            <h2>Sign in to your doctor network and assigned referrals.</h2>
            <p>Every professional action is checked against your active identity, organization membership, and exact permission on the server.</p>
            <ul><li>HTTP-only session cookie</li><li>CSRF-protected changes</li><li>Connection-scoped messages</li><li>Fictional data only in V0</li></ul>
          </section>
          <LoginForm nextPath={next} />
        </div>
      </main>
      <SiteFooter />
    </>
  );
}

function IconShield() {
  return <span aria-hidden="true">◆</span>;
}
