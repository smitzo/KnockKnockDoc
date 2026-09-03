import type { Metadata } from "next";
import { redirect } from "next/navigation";

import { LoginForm } from "@/components/login-form";
import { SiteFooter, SiteHeader } from "@/components/site-header";
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
  const localAdminEnabled = process.env.LOCAL_DEMO_ADMIN_UI === "true";
  return (
    <>
      <SiteHeader />
      <main className={styles.page}>
        <div className="login-layout page-shell">
          <section className="login-context">
            <span className="eyebrow"><IconShield /> Product demo</span>
            <h2>See the full product in three simple steps.</h2>
            <p>Start as the administrator, load the sample data, then explore the doctor and patient flows.</p>
            <ol><li><span>1</span><div><strong>Sign in as admin</strong><small>Use the local demo credentials.</small></div></li><li><span>2</span><div><strong>Load demo data</strong><small>Create 30 doctors and 30 patients.</small></div></li><li><span>3</span><div><strong>Explore the product</strong><small>Review profiles, connections, chat, and referrals.</small></div></li></ol>
          </section>
          <LoginForm localAdminEnabled={localAdminEnabled} nextPath={next} />
        </div>
      </main>
      <SiteFooter />
    </>
  );
}

function IconShield() {
  return <span aria-hidden="true">◆</span>;
}
