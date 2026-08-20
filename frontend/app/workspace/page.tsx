import type { Metadata } from "next";

import { WorkspaceShell } from "@/components/workspace-shell";
import { getDemoWorkspace } from "@/lib/api";

export const metadata: Metadata = { title: "Synthetic case workspace" };
export const dynamic = "force-dynamic";

export default async function WorkspacePage() {
  const { data, source } = await getDemoWorkspace();
  return <WorkspaceShell workspace={data} source={source} />;
}
