import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";

import { AdminLabShell } from "@/components/admin-lab-shell";
import { Brand } from "@/components/site-header";
import { ApiRequestError, getAdminLab, getServerSession } from "@/lib/api";
import { getServerCookieHeader } from "@/lib/server-cookies";
import accessStyles from "@/styles/access.module.css";

export const metadata: Metadata = { title: "Admin data control" };
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
  if (accessDenied || !data) return <main className={`${accessStyles.page} page-shell`}><Brand /><span className={accessStyles.code}>Platform admin only</span><h1>This data control center is not visible to your role.</h1><p>Only an active platform administrator can manage demo data or inspect its operational coverage.</p><Link className="button" href="/workspace">Open my workspace</Link></main>;
  return <AdminLabShell data={data} />;
}
