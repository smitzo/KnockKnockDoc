import type {
  AdminLabData,
  AdminLabSummary,
  DeleteDemoFixtureResponse,
  DemoFixtureStatus,
  DemoWorkspaceResponse,
  PaginatedResponse,
  PartnerApplicationPayload,
  PartnerApplicationResponse,
  ProfessionalCard,
  ProfessionalConnection,
  ProfessionalConversation,
  ProfessionalMessage,
  ProfessionalNetworkData,
  ReferralCase,
  SessionResponse,
  SyntheticDoctor,
  SyntheticPatient,
} from "./types";

const serverApiUrl = process.env.BACKEND_INTERNAL_URL ?? "http://localhost:8000";

export class ApiRequestError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
  }
}

async function serverGet<T>(path: string, cookieHeader: string): Promise<T> {
  const response = await fetch(`${serverApiUrl}${path}`, {
    cache: "no-store",
    signal: AbortSignal.timeout(5000),
    headers: { Accept: "application/json", Cookie: cookieHeader },
  });
  if (!response.ok) {
    throw new ApiRequestError(`API request returned ${response.status}`, response.status);
  }
  return (await response.json()) as T;
}

export async function getServerSession(cookieHeader: string): Promise<SessionResponse | null> {
  try {
    return await serverGet<SessionResponse>("/api/v1/auth/session/", cookieHeader);
  } catch (error) {
    if (error instanceof ApiRequestError && [401, 403].includes(error.status)) return null;
    throw error;
  }
}

export async function getDemoWorkspace(cookieHeader: string): Promise<DemoWorkspaceResponse> {
  const data = await serverGet<DemoWorkspaceResponse>(
    "/api/v1/demo/workspace/",
    cookieHeader,
  );
  if (
    data.prototype?.mode !== "synthetic-only" ||
    !data.prototype.authorization_enforced ||
    !data.case?.reference
  ) {
    throw new ApiRequestError("Workspace security boundary did not validate", 502);
  }
  return data;
}

export async function getAdminLab(cookieHeader: string): Promise<AdminLabData> {
  const [summary, doctors, patients] = await Promise.all([
    serverGet<AdminLabSummary>("/api/v1/admin/lab/summary/", cookieHeader),
    serverGet<PaginatedResponse<SyntheticDoctor>>(
      "/api/v1/admin/lab/doctors/?page_size=60",
      cookieHeader,
    ),
    serverGet<PaginatedResponse<SyntheticPatient>>(
      "/api/v1/admin/lab/patients/?page_size=60",
      cookieHeader,
    ),
  ]);
  return { summary, doctors: doctors.results, patients: patients.results };
}

export async function getProfessionalNetwork(
  cookieHeader: string,
): Promise<ProfessionalNetworkData> {
  const [doctors, connections, conversations] = await Promise.all([
    serverGet<PaginatedResponse<ProfessionalCard>>(
      "/api/v1/network/doctors/?page_size=50",
      cookieHeader,
    ),
    serverGet<ProfessionalConnection[]>("/api/v1/network/connections/", cookieHeader),
    serverGet<ProfessionalConversation[]>("/api/v1/network/conversations/", cookieHeader),
  ]);
  return { doctors: doctors.results, connections, conversations };
}

export async function getCsrfToken(): Promise<string> {
  const response = await fetch("/api/backend/auth/csrf", {
    credentials: "same-origin",
    headers: { Accept: "application/json" },
  });
  if (!response.ok) throw new Error("A secure form token could not be issued.");
  const body = (await response.json()) as { csrf_token: string };
  return body.csrf_token;
}

export async function loginWithPassword(email: string, password: string): Promise<SessionResponse> {
  const csrfToken = await getCsrfToken();
  const normalizedLogin = email.trim().toLowerCase() === "admin"
    ? "admin.demo@knocknockdoc.test"
    : email;
  const response = await fetch("/api/backend/auth/login", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ email: normalizedLogin, password }),
  });
  const body = (await response.json()) as unknown;
  if (!response.ok) {
    throw new Error(flattenApiError(body) || "Email or password is incorrect.");
  }
  return body as SessionResponse;
}

export async function logoutSession(): Promise<void> {
  const csrfToken = await getCsrfToken();
  const response = await fetch("/api/backend/auth/logout", {
    method: "POST",
    credentials: "same-origin",
    headers: { Accept: "application/json", "X-CSRFToken": csrfToken },
  });
  if (!response.ok && response.status !== 403) {
    throw new Error("The session could not be closed safely.");
  }
}

export async function loadDemoFixtures(): Promise<DemoFixtureStatus> {
  const csrfToken = await getCsrfToken();
  const response = await fetch("/api/backend/admin/lab/fixtures/", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: "{}",
  });
  const body = (await response.json()) as unknown;
  if (!response.ok) {
    throw new Error(flattenApiError(body) || "The demo data could not be loaded.");
  }
  return body as DemoFixtureStatus;
}

export async function deleteDemoFixtures(): Promise<DeleteDemoFixtureResponse> {
  const csrfToken = await getCsrfToken();
  const response = await fetch("/api/backend/admin/lab/fixtures/", {
    method: "DELETE",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ confirmation: "DELETE SYNTHETIC DEMO DATA" }),
  });
  const body = (await response.json()) as unknown;
  if (!response.ok) {
    throw new Error(flattenApiError(body) || "The demo data could not be deleted.");
  }
  return body as DeleteDemoFixtureResponse;
}

export async function createSyntheticReferral(
  payload: Record<string, string | boolean>,
): Promise<ReferralCase> {
  const csrfToken = await getCsrfToken();
  const response = await fetch("/api/backend/cases/", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify(payload),
  });
  const body = (await response.json()) as unknown;
  if (!response.ok) {
    const detail = flattenApiError(body);
    throw new Error(detail || "The synthetic referral could not be created.");
  }
  return body as ReferralCase;
}

export async function submitPartnerApplication(
  payload: PartnerApplicationPayload,
): Promise<PartnerApplicationResponse> {
  const csrfToken = await getCsrfToken();
  const response = await fetch("/api/backend/onboarding/applications/", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify(payload),
  });
  const body = (await response.json()) as unknown;
  if (!response.ok) {
    throw new Error(flattenApiError(body) || "The application could not be submitted.");
  }
  return body as PartnerApplicationResponse;
}

export async function searchProfessionalDoctors(query: string): Promise<ProfessionalCard[]> {
  const params = new URLSearchParams({ page_size: "50" });
  if (query.trim()) params.set("q", query.trim());
  const response = await fetch(`/api/backend/network/doctors/?${params}`, {
    credentials: "same-origin",
    headers: { Accept: "application/json" },
  });
  const body = (await response.json()) as unknown;
  if (!response.ok) {
    throw new Error(flattenApiError(body) || "The doctor directory could not be loaded.");
  }
  return (body as PaginatedResponse<ProfessionalCard>).results;
}

export async function createProfessionalConnection(payload: {
  recipient_profile_id: string;
  purpose: string;
  note: string;
}): Promise<ProfessionalConnection> {
  const csrfToken = await getCsrfToken();
  const response = await fetch("/api/backend/network/connections/", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ ...payload, accepts_synthetic_only: true }),
  });
  const body = (await response.json()) as unknown;
  if (!response.ok) {
    throw new Error(flattenApiError(body) || "The connection request could not be sent.");
  }
  return body as ProfessionalConnection;
}

export async function transitionProfessionalConnection(
  connectionId: string,
  action: "accept" | "decline" | "withdraw",
): Promise<ProfessionalConnection> {
  const csrfToken = await getCsrfToken();
  const response = await fetch(
    `/api/backend/network/connections/${encodeURIComponent(connectionId)}/${action}/`,
    {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: "{}",
    },
  );
  const body = (await response.json()) as unknown;
  if (!response.ok) {
    throw new Error(flattenApiError(body) || "The connection could not be updated.");
  }
  return body as ProfessionalConnection;
}

export async function getProfessionalConversations(): Promise<ProfessionalConversation[]> {
  const response = await fetch("/api/backend/network/conversations/", {
    credentials: "same-origin",
    headers: { Accept: "application/json" },
  });
  const body = (await response.json()) as unknown;
  if (!response.ok) {
    throw new Error(flattenApiError(body) || "Conversations could not be loaded.");
  }
  return body as ProfessionalConversation[];
}

export async function getProfessionalMessages(
  conversationId: string,
): Promise<ProfessionalMessage[]> {
  const response = await fetch(
    `/api/backend/network/conversations/${encodeURIComponent(conversationId)}/messages/`,
    { credentials: "same-origin", headers: { Accept: "application/json" } },
  );
  const body = (await response.json()) as unknown;
  if (!response.ok) {
    throw new Error(flattenApiError(body) || "Messages could not be loaded.");
  }
  return body as ProfessionalMessage[];
}

export async function sendProfessionalMessage(
  conversationId: string,
  message: string,
): Promise<ProfessionalMessage> {
  const csrfToken = await getCsrfToken();
  const response = await fetch(
    `/api/backend/network/conversations/${encodeURIComponent(conversationId)}/messages/`,
    {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ body: message, accepts_synthetic_only: true }),
    },
  );
  const body = (await response.json()) as unknown;
  if (!response.ok) {
    throw new Error(flattenApiError(body) || "The message could not be sent.");
  }
  return body as ProfessionalMessage;
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
