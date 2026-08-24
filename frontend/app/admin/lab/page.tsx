import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";

import { AdminLabShell } from "@/components/admin-lab-shell";
import { Brand } from "@/components/site-header";
import { ApiRequestError, getAdminLab, getServerSession } from "@/lib/api";
import { getServerCookieHeader } from "@/lib/server-cookies";
import accessStyles from "@/styles/access.module.css";

export const metadata: Metadata = { title: "Admin synthetic data lab" };
export const dynamic = "force-dynamic";

export default async function AdminLabPage() {
  const cookieHeader = await getServerCookieHeader();
  const session = await getServerSession(cookieHeader);
  if (!session) redirect("/login?next=/admin/lab");
  let data = null;
  let accessDenied = false;
  try {
    data = await getAdminLab(cookieHeader);
  } catch (error) {
    if (error instanceof ApiRequestError && [403, 404].includes(error.status)) {
      accessDenied = true;
    } else {
      throw error;
    }
  }
  if (accessDenied || !data) return <main className={`${accessStyles.page} page-shell`}><Brand /><span className={accessStyles.code}>Platform admin only</span><h1>This synthetic data lab is not visible to your role.</h1><p>Doctor, patient, specialist, hospital, and coordinator accounts are denied by the API. No catalog rows were returned.</p><Link className="button" href="/workspace">Open my workspace</Link></main>;
  return <AdminLabShell data={data} />;
}
