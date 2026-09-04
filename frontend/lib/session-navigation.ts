import type { SessionResponse } from "./types";

export function getSessionHomePath(session: SessionResponse) {
  if (session.memberships.some((membership) => membership.role === "admin")) {
    return "/admin/lab";
  }
  if (session.profile.account_type === "professional") return "/network";
  if (session.memberships.some((membership) => membership.role === "hospital_coordinator")) {
    return "/hospital";
  }
  return "/workspace";
}
