import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";

import { Brand } from "@/components/site-header";
import { WorkspaceShell } from "@/components/workspace-shell";
import { ApiRequestError, getDemoWorkspace, getProductMode, getServerSession } from "@/lib/api";
import { getServerCookieHeader } from "@/lib/server-cookies";
import accessStyles from "@/styles/access.module.css";

export const metadata: Metadata = { title: "Referral workspace" };
export const dynamic = "force-dynamic";

export default async function WorkspacePage() {
  const cookieHeader = await getServerCookieHeader();
  const [session, productMode] = await Promise.all([
    getServerSession(cookieHeader),
    getProductMode(),
  ]);
  if (!session) redirect("/login?next=/workspace");
  if (!productMode.demo_data_enabled) return (
    <main className={`${accessStyles.page} page-shell`}>
      <Brand />
      <span className={accessStyles.code}>Referral workspace</span>
      <h1>No referrals are assigned to you yet.</h1>
      <p>New referrals will appear here after the patient sharing decision and your organization assignment are complete.</p>
      <div><Link className="button" href="/network">Open doctor network</Link><Link className="button button--ghost" href="/how-to">How referrals work</Link></div>
    </main>
  );
  let workspace = null;
  let accessDenied = false;
  try {
    workspace = await getDemoWorkspace(cookieHeader);
  } catch (error) {
    if (error instanceof ApiRequestError && [403, 404].includes(error.status)) {
      accessDenied = true;
    } else {
      throw error;
    }
  }
  if (accessDenied || !workspace) return (
    <main className={`${accessStyles.page} page-shell`}>
      <Brand />
      <span className={accessStyles.code}>Access not assigned</span>
      <h1>This account has no active grant for the demo case.</h1>
      <p>Knowing a case reference or belonging to a hospital is not enough. Ask a platform coordinator to assign this exact membership and scope.</p>
      <div><Link className="button" href="/">Return home</Link><Link className="button button--ghost" href="/how-to">Understand access</Link></div>
    </main>
  );
  return <WorkspaceShell workspace={workspace} />;
}
