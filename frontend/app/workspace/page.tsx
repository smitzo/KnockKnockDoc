import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";

import { Brand } from "@/components/site-header";
import { WorkspaceShell } from "@/components/workspace-shell";
import { ApiRequestError, getDemoWorkspace, getServerSession } from "@/lib/api";
import { getServerCookieHeader } from "@/lib/server-cookies";
import accessStyles from "@/styles/access.module.css";

export const metadata: Metadata = { title: "Synthetic case workspace" };
export const dynamic = "force-dynamic";

export default async function WorkspacePage() {
  const cookieHeader = await getServerCookieHeader();
  const session = await getServerSession(cookieHeader);
  if (!session) redirect("/login?next=/workspace");
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
