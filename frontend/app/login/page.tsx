import type { Metadata } from "next";
import { redirect } from "next/navigation";

import { LoginForm } from "@/components/login-form";
import { Brand, PrototypeBanner } from "@/components/site-header";
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
    redirect(isAdmin ? "/admin/lab" : "/workspace");
  }
  const { next = "/workspace" } = await searchParams;
  return (
    <>
      <PrototypeBanner />
      <main className={styles.page}>
        <div className="login-page__brand"><Brand /></div>
        <div className="login-layout page-shell">
          <section className="login-context">
            <span className="eyebrow"><IconShield /> Case access, not role theatre</span>
            <h2>Only the people assigned to a referral can open it.</h2>
            <p>Your account, organization membership, exact case assignment, and current scoped grant are all checked by the server.</p>
            <ul><li>HTTP-only session cookie</li><li>CSRF-protected changes</li><li>Hospital-to-hospital isolation</li><li>Fictional data only</li></ul>
          </section>
          <LoginForm nextPath={next} />
        </div>
      </main>
    </>
  );
}

function IconShield() {
  return <span aria-hidden="true">◆</span>;
}
