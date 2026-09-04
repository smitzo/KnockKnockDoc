import type { Metadata } from "next";
import { redirect } from "next/navigation";

import { LoginForm } from "@/components/login-form";
import { SiteFooter, SiteHeader } from "@/components/site-header";
import { getProductMode, getServerSession } from "@/lib/api";
import { getServerCookieHeader } from "@/lib/server-cookies";
import { getSessionHomePath } from "@/lib/session-navigation";
import styles from "@/styles/login.module.css";

export const metadata: Metadata = { title: "Sign in" };
export const dynamic = "force-dynamic";

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string }>;
}) {
  const cookieHeader = await getServerCookieHeader();
  const [session, productMode] = await Promise.all([
    getServerSession(cookieHeader),
    getProductMode(),
  ]);
  if (session) redirect(getSessionHomePath(session));
  const { next = "" } = await searchParams;
  const localAdminEnabled = process.env.LOCAL_DEMO_ADMIN_UI === "true";
  return (
    <>
      <SiteHeader />
      <main className={styles.page}>
        <div className="login-layout page-shell">
          <section className="login-context">
            <span className="eyebrow"><IconShield /> Account access</span>
            {productMode.demo_data_enabled ? <><h2>Demo data is active.</h2><p>Sign in to explore doctor profiles, connections, messages, and referrals.</p><ol><li><span>1</span><div><strong>Sign in</strong><small>Use an account created for this demo.</small></div></li><li><span>2</span><div><strong>Explore the network</strong><small>Compare doctors and professional signals.</small></div></li><li><span>3</span><div><strong>Follow a referral</strong><small>Review the connected workflow.</small></div></li></ol></> : <><h2>Welcome back.</h2><p>Sign in to manage professional connections, referrals, and hospital collaboration.</p></>}
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
