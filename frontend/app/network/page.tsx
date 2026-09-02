import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";

import { NetworkShell } from "@/components/network/network-shell";
import { Brand } from "@/components/site-header";
import { ApiRequestError, getProfessionalNetwork, getServerSession } from "@/lib/api";
import { getServerCookieHeader } from "@/lib/server-cookies";
import accessStyles from "@/styles/access.module.css";

export const metadata: Metadata = { title: "Doctor network" };
export const dynamic = "force-dynamic";

export default async function NetworkPage() {
  const cookieHeader = await getServerCookieHeader();
  const session = await getServerSession(cookieHeader);
  if (!session) redirect("/login?next=/network");
  if (session.profile.account_type !== "professional") redirect("/workspace");

  let data = null;
  let accessDenied = false;
  try {
    data = await getProfessionalNetwork(cookieHeader);
  } catch (error) {
    if (!(error instanceof ApiRequestError) || ![403, 404].includes(error.status)) throw error;
    accessDenied = true;
  }
  if (accessDenied || !data) return <main className={`${accessStyles.page} page-shell`}><Brand /><span className={accessStyles.code}>Professional profile required</span><h1>Your account cannot open the doctor network yet.</h1><p>An active professional identity and verified synthetic directory profile are both required. A submitted application does not grant either.</p><div><Link className="button" href="/">Return home</Link><Link className="button button--ghost" href="/join">Review the application path</Link></div></main>;
  return <NetworkShell data={data} session={session} />;
}
