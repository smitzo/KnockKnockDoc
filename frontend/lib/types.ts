export type RolePreview = "patient" | "referrer" | "hospital" | "coordinator";

export interface OrganizationSummary {
  id: string;
  name: string;
  slug: string;
  type: string;
}

export interface SessionMembership {
  id: string;
  role: string;
  role_label: string;
  organization: OrganizationSummary;
}

export interface SessionResponse {
  authenticated: true;
  profile: {
    id: string;
    email: string;
    display_name: string;
    account_type: string;
    account_type_label: string;
  };
  memberships: SessionMembership[];
  session: { expires_at: string };
}

export interface Participant {
  id: string;
  display_name: string;
  role: string;
  role_label: string;
  organization: string;
  access_scope: string;
  access_state: string;
  access_state_label: string;
  purpose: string;
}

export interface RecordItem {
  id: string;
  label: string;
  category: string;
  clinical_date: string | null;
  source_label: string;
  state: "ready" | "needs_update" | "requested" | "unavailable";
  state_label: string;
  note: string;
}

export interface InformationRequest {
  id: string;
  item: string;
  reason: string;
  requester_name: string;
  requester_role: string;
  state: "open" | "answered" | "unavailable";
  state_label: string;
  is_blocking: boolean;
  due_at: string | null;
  response_note: string;
}

export interface ProviderResponse {
  id: string;
  response_type: string;
  response_type_label: string;
  title: string;
  author_name: string;
  author_role: string;
  organization: string;
  summary: string;
  limitations: string;
  state: string;
  state_label: string;
  issued_at: string | null;
  version: number;
}

export interface CaseEvent {
  id: string;
  event_type: string;
  actor_label: string;
  actor_role: string;
  summary: string;
  occurred_at: string;
}

export interface ReferralCase {
  id: string;
  reference: string;
  patient_alias: string;
  patient_country: string;
  patient_age_band: string;
  specialty: string;
  status: string;
  status_label: string;
  consent_status: string;
  consent_status_label: string;
  corridor_label: string;
  clinical_question: string;
  summary: string;
  is_planned_care: boolean;
  is_synthetic: boolean;
  progress_percent: number;
  next_action: string;
  next_action_owner: string;
  next_action_due: string | null;
  participants: Participant[];
  records: RecordItem[];
  information_requests: InformationRequest[];
  responses: ProviderResponse[];
  events: CaseEvent[];
  created_at: string;
  updated_at: string;
}

export interface DemoWorkspaceResponse {
  prototype: {
    mode: "synthetic-only";
    real_patient_data_allowed: false;
    authorization_enforced: true;
  };
  viewer: {
    display_name: string;
    membership_role: string;
    membership_role_label: string;
    organization_name: string;
  };
  case: ReferralCase;
}

export interface SyntheticDoctor {
  id: string;
  fixture_key: string;
  display_name: string;
  login_email: string;
  specialty: string;
  city: string;
  hospital_name: string;
  experience_years: number;
  languages: string[];
  availability: string;
  availability_label: string;
  response_hours: number;
  credential_state: string;
  avatar_url: string;
  profile_summary: string;
  is_synthetic: true;
}

export interface SyntheticPatient {
  id: string;
  fixture_key: string;
  display_alias: string;
  login_email: string;
  home_country: string;
  age_band: string;
  specialty_interest: string;
  journey_stage: string;
  journey_stage_label: string;
  preferred_city: string;
  language: string;
  coordination_need: string;
  avatar_url: string;
  is_synthetic: true;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface AdminLabSummary {
  prototype: { mode: "synthetic-only"; real_people: false; admin_only: true };
  counts: { doctors: number; patients: number };
  fixture: DemoFixtureStatus;
  doctor_specialties: { specialty: string; count: number }[];
  patient_stages: { journey_stage: string; count: number }[];
}

export interface DemoFixtureStatus {
  fixture: {
    id: string;
    schema_version: number;
    synthetic_only: true;
    disclosure: string;
  };
  state: "empty" | "partial" | "loaded";
  loaded: boolean;
  counts: Record<string, { actual: number; expected: number }>;
}

export interface DeleteDemoFixtureResponse {
  fixture_status: DemoFixtureStatus;
  removed: Record<string, number>;
}

export interface AdminLabData {
  summary: AdminLabSummary;
  doctors: SyntheticDoctor[];
  patients: SyntheticPatient[];
}
