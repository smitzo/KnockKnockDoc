import type { Metadata } from "next";
import { redirect } from "next/navigation";

import { HospitalWorkspace } from "@/components/hospital/hospital-workspace";
import { getProductMode, getServerSession } from "@/lib/api";
import { getServerCookieHeader } from "@/lib/server-cookies";
import { getSessionHomePath } from "@/lib/session-navigation";

export const metadata: Metadata = { title: "Hospital workspace" };
export const dynamic = "force-dynamic";

export default async function HospitalPage() {
  const cookieHeader = await getServerCookieHeader();
  const [session, productMode] = await Promise.all([
    getServerSession(cookieHeader),
    getProductMode(),
  ]);
  if (!session) redirect("/login?next=/hospital");
  const membership = session.memberships.find(
    (item) => item.role === "hospital_coordinator",
  );
  if (!membership) redirect(getSessionHomePath(session));
  return (
    <HospitalWorkspace
      demoModeEnabled={productMode.demo_data_enabled}
      membership={membership}
      session={session}
    />
  );
}
