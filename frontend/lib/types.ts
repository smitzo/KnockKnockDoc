export type RolePreview = "patient" | "referrer" | "hospital" | "coordinator";

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
    role_switch_is_authorization: false;
  };
  case: ReferralCase;
}
