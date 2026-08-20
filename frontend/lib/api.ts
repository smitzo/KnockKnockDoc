import { fallbackWorkspace } from "./demo-data";
import type { DemoWorkspaceResponse, ReferralCase } from "./types";

const serverApiUrl = process.env.BACKEND_INTERNAL_URL ?? "http://localhost:8000";

export async function getDemoWorkspace(): Promise<{
  data: DemoWorkspaceResponse;
  source: "api" | "fallback";
}> {
  try {
    const response = await fetch(`${serverApiUrl}/api/v1/demo/workspace/`, {
      cache: "no-store",
      signal: AbortSignal.timeout(2500),
      headers: { Accept: "application/json" },
    });
    if (!response.ok) {
      throw new Error(`Workspace API returned ${response.status}`);
    }
    const data = (await response.json()) as DemoWorkspaceResponse;
    if (data.prototype?.mode !== "synthetic-only" || !data.case?.reference) {
      throw new Error("Workspace API boundary did not validate");
    }
    return { data, source: "api" };
  } catch {
    return { data: fallbackWorkspace, source: "fallback" };
  }
}

export async function createSyntheticReferral(
  payload: Record<string, string | boolean>,
): Promise<ReferralCase> {
  const response = await fetch("/api/backend/cases/", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(payload),
  });
  const body = (await response.json()) as unknown;
  if (!response.ok) {
    const detail = flattenApiError(body);
    throw new Error(detail || "The synthetic referral could not be created.");
  }
  return body as ReferralCase;
}

function flattenApiError(body: unknown): string {
  if (!body || typeof body !== "object") return "";
  const values = Object.values(body).flatMap((value) => {
    if (Array.isArray(value)) return value.map(String);
    if (typeof value === "string") return [value];
    if (value && typeof value === "object") {
      return Object.values(value as Record<string, unknown>).flatMap((nested) =>
        Array.isArray(nested) ? nested.map(String) : [String(nested)],
      );
    }
    return [];
  });
  return values.join(" ");
}
