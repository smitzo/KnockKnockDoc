import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";

import { NetworkShell } from "@/components/network/network-shell";
import { Brand } from "@/components/site-header";
import { ApiRequestError, getProductMode, getProfessionalNetwork, getServerSession } from "@/lib/api";
import { getServerCookieHeader } from "@/lib/server-cookies";
import { getSessionHomePath } from "@/lib/session-navigation";
import accessStyles from "@/styles/access.module.css";

export const metadata: Metadata = { title: "Doctor network" };
export const dynamic = "force-dynamic";

export default async function NetworkPage() {
  const cookieHeader = await getServerCookieHeader();
  const [session, productMode] = await Promise.all([
    getServerSession(cookieHeader),
    getProductMode(),
  ]);
  if (!session) redirect("/login?next=/network");
  const isAdmin = session.memberships.some((membership) => membership.role === "admin");
  if (session.profile.account_type !== "professional" && !isAdmin) {
    redirect(getSessionHomePath(session));
  }

  let data = null;
  let accessDenied = false;
  try {
    data = await getProfessionalNetwork(cookieHeader, isAdmin);
  } catch (error) {
    if (!(error instanceof ApiRequestError) || ![403, 404].includes(error.status)) throw error;
    accessDenied = true;
  }
  if (accessDenied || !data) return <main className={`${accessStyles.page} page-shell`}><Brand /><span className={accessStyles.code}>Professional profile required</span><h1>Your account cannot open the doctor network yet.</h1><p>An active professional identity, reviewed application, and eligible doctor membership are required. An application alone does not grant access.</p><div><Link className="button" href="/">Return home</Link><Link className="button button--ghost" href="/join">Review the application path</Link></div></main>;
  return <NetworkShell adminPreview={isAdmin} data={data} demoModeEnabled={productMode.demo_data_enabled} session={session} />;
}
