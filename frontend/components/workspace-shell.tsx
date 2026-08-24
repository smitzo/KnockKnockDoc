"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useMemo, useState } from "react";

import type { DemoWorkspaceResponse, RolePreview } from "@/lib/types";
import { logoutSession } from "@/lib/api";
import styles from "@/styles/authenticated.module.css";

import { Icon, type IconName } from "./icons";
import { Brand } from "./site-header";

type WorkspaceTab = "overview" | "records" | "access" | "activity";

const roleGuidance: Record<RolePreview, { heading: string; note: string; action: string }> = {
  patient: {
    heading: "Your decision, without the pressure",
    note: "Take the response back to the doctor you trust. Asking for clarification or pausing is a valid next step.",
    action: "Review the response",
  },
  referrer: {
    heading: "Help your patient interpret the handoff",
    note: "The specialist response is preliminary. Confirm whether it answers your original clinical question and add context if needed.",
    action: "Prepare the patient discussion",
  },
  hospital: {
    heading: "The patient is waiting on a clear handoff",
    note: "The response is issued. Keep clinical authorship separate from coordination and make the next operational step explicit.",
    action: "Review delivery status",
  },
  coordinator: {
    heading: "One person owns the next safe step",
    note: "Confirm the patient and referrer received the response, then record whether they proceed, pause, clarify, or decline.",
    action: "Confirm response receipt",
  },
};

const tabs: { value: WorkspaceTab; label: string; icon: IconName }[] = [
  { value: "overview", label: "Overview", icon: "home" },
  { value: "records", label: "Records", icon: "document" },
  { value: "access", label: "Who has access", icon: "people" },
  { value: "activity", label: "Activity", icon: "timeline" },
];

const journeySteps = ["Referral", "Sharing", "Review", "Response", "Decision"];

function formatDate(value: string | null, options?: Intl.DateTimeFormatOptions) {
  if (!value) return "No date set";
  return new Intl.DateTimeFormat("en", options ?? { day: "numeric", month: "short", year: "numeric" }).format(new Date(value));
}

function roleFromMembership(membershipRole: string): RolePreview {
  if (membershipRole === "patient") return "patient";
  if (membershipRole === "referrer") return "referrer";
  if (["specialist", "hospital_coordinator"].includes(membershipRole)) return "hospital";
  return "coordinator";
}

export function WorkspaceShell({
  workspace,
}: {
  workspace: DemoWorkspaceResponse;
}) {
  const router = useRouter();
  const role = roleFromMembership(workspace.viewer.membership_role);
  const [tab, setTab] = useState<WorkspaceTab>("overview");
  const currentRole = roleGuidance[role];
  const referral = workspace.case;
  const openRequests = useMemo(
    () => referral.information_requests.filter((request) => request.state === "open"),
    [referral.information_requests],
  );
  const readyRecords = referral.records.filter((record) => record.state === "ready").length;

  async function handleLogout() {
    await logoutSession();
    router.replace("/login");
    router.refresh();
  }

  return (
    <div className="workspace-app">
      <div className="workspace-prototype-bar">
        <strong>Synthetic prototype</strong>
        <span>No real patient data. Account, assignment, and scoped grant checks are enforced.</span>
      </div>
      <header className="workspace-header">
        <Brand />
        <div className="workspace-header__case">
          <span>Case</span><strong>{referral.reference}</strong>
        </div>
        <div className={styles.workspaceAccount}>
          <div><span>{workspace.viewer.membership_role_label}</span><strong>{workspace.viewer.display_name}</strong><small>{workspace.viewer.organization_name}</small></div>
          <button className="button button--ghost button--small" onClick={handleLogout} type="button">Sign out</button>
        </div>
      </header>

      <div className="workspace-layout">
        <aside className="workspace-sidebar">
          <nav aria-label="Case workspace">
            {tabs.map((item) => (
              <button
                className={tab === item.value ? "sidebar-link sidebar-link--active" : "sidebar-link"}
                key={item.value}
                onClick={() => setTab(item.value)}
                type="button"
              >
                <Icon name={item.icon} />{item.label}
                {item.value === "records" && <span>{referral.records.length}</span>}
              </button>
            ))}
          </nav>
          <div className="sidebar-support">
            <span className="avatar avatar--coordinator">N</span>
            <div><span>Your coordinator</span><strong>Nila</strong><small>Prototype care team</small></div>
            <button aria-label="Message prototype coordinator" type="button"><Icon name="message" /></button>
          </div>
          <Link className="sidebar-home" href="/"><Icon name="arrow" /> Back to product home</Link>
        </aside>

        <main className="workspace-main">
          <section className="case-heading">
            <div>
              <div className="case-heading__meta">
                <span className="status-pill status-pill--soft"><span /> {referral.status_label}</span>
                <span>{referral.corridor_label}</span>
              </div>
              <h1>{role === "patient" ? "Your referral workspace" : `${workspace.viewer.membership_role_label} workspace`}</h1>
              <p>{referral.patient_alias} · {referral.patient_age_band} · {referral.specialty}</p>
            </div>
            <button className="icon-button" aria-label="Open synthetic case messages" type="button"><Icon name="message" /><span>1</span></button>
          </section>

          <section className="journey-card" aria-label="Referral progress">
            <div className="journey-card__heading"><span>Referral progress</span><strong>{referral.progress_percent}% complete</strong></div>
            <ol className="journey-progress">
              {journeySteps.map((step, index) => {
                const complete = index < 4;
                const active = index === 4;
                return (
                  <li className={complete ? "is-complete" : active ? "is-active" : ""} key={step}>
                    <span>{complete ? <Icon name="check" /> : index + 1}</span><strong>{step}</strong>
                  </li>
                );
              })}
            </ol>
          </section>

          <section className="next-action-card">
            <span className="next-action-card__icon"><Icon name="spark" /></span>
            <div className="next-action-card__copy">
              <span>Your next step</span>
              <h2>{currentRole.heading}</h2>
              <p>{currentRole.note}</p>
              <div className="next-action-card__meta">
                <span><Icon name="calendar" /> Suggested by {formatDate(referral.next_action_due, { weekday: "short", day: "numeric", month: "short" })}</span>
                <span><Icon name="people" /> Owner: {referral.next_action_owner}</span>
              </div>
            </div>
            <button className="button" onClick={() => document.getElementById("response")?.scrollIntoView({ behavior: "smooth" })} type="button">
              {currentRole.action} <Icon name="arrow" />
            </button>
          </section>

          {tab === "overview" && (
            <OverviewTab referral={referral} openRequests={openRequests} readyRecords={readyRecords} />
          )}
          {tab === "records" && <RecordsTab referral={referral} />}
          {tab === "access" && <AccessTab referral={referral} />}
          {tab === "activity" && <ActivityTab referral={referral} />}
        </main>
      </div>
    </div>
  );
}

function OverviewTab({
  referral,
  openRequests,
  readyRecords,
}: {
  referral: DemoWorkspaceResponse["case"];
  openRequests: DemoWorkspaceResponse["case"]["information_requests"];
  readyRecords: number;
}) {
  const clinicalResponse = referral.responses.find((response) => response.response_type === "clinical_opinion");
  return (
    <div className="workspace-content-grid">
      <div className="workspace-content-main">
        <section className="content-card question-card">
          <div className="content-card__heading"><div><span className="card-kicker">The referral question</span><h2>What the receiving team was asked</h2></div><span className="source-chip">From home doctor</span></div>
          <blockquote>{referral.clinical_question}</blockquote>
          <p>{referral.summary}</p>
        </section>

        <section className="content-card" id="response">
          <div className="content-card__heading">
            <div><span className="card-kicker card-kicker--green">Response received</span><h2>{clinicalResponse?.title ?? "No response issued yet"}</h2></div>
            {clinicalResponse && <span className="issued-chip"><Icon name="check" /> Attributable</span>}
          </div>
          {clinicalResponse ? (
            <>
              <div className="response-author">
                <span className="avatar avatar--specialist">AR</span>
                <div><strong>{clinicalResponse.author_name}</strong><span>{clinicalResponse.author_role}</span><small>{clinicalResponse.organization}</small></div>
                <span className="response-author__date">Issued {formatDate(clinicalResponse.issued_at)}</span>
              </div>
              <p className="response-summary">{clinicalResponse.summary}</p>
              <div className="response-boundary"><Icon name="shield" /><div><strong>Important limitation</strong><p>{clinicalResponse.limitations}</p></div></div>
              <div className="response-actions">
                <button className="button" type="button">Ask a case question <Icon name="message" /></button>
                <button className="button button--ghost" type="button">View coordination plan</button>
              </div>
            </>
          ) : <p>A named response will appear here when issued.</p>}
        </section>
      </div>

      <aside className="workspace-content-aside">
        <section className="content-card completeness-card">
          <div className="content-card__heading"><div><span className="card-kicker">Case readiness</span><h2>{readyRecords} of {referral.records.length} records ready</h2></div><span className="ring-progress" style={{ "--progress": `${Math.round((readyRecords / referral.records.length) * 100)}%` } as React.CSSProperties}>{Math.round((readyRecords / referral.records.length) * 100)}%</span></div>
          <div className="mini-progress"><span style={{ width: `${(readyRecords / referral.records.length) * 100}%` }} /></div>
          {openRequests.map((request) => (
            <div className="missing-item" key={request.id}>
              <span><Icon name="document" /></span>
              <div><strong>{request.item}</strong><small>{request.is_blocking ? "Blocks review" : "Does not block this response"}</small></div>
              <Icon name="chevron" />
            </div>
          ))}
          <button className="card-link" type="button">See all record details <Icon name="arrow" /></button>
        </section>

        <section className="content-card access-glance">
          <div className="content-card__heading"><div><span className="card-kicker">Access at a glance</span><h2>{referral.participants.length} named participants</h2></div><Icon name="lock" /></div>
          <div className="avatar-stack" aria-label="Case participant avatars">
            <span className="avatar avatar--patient">AK</span><span className="avatar avatar--referrer">LA</span><span className="avatar avatar--specialist">AR</span><span className="avatar avatar--coordinator">N</span>
          </div>
          <p>Server checks require an active identity, membership, assignment, grant, and case-view scope.</p>
          <button className="card-link" type="button">Review participants and purpose <Icon name="arrow" /></button>
        </section>

        <section className="coordinator-note">
          <span className="avatar avatar--coordinator">N</span>
          <div><span>From Nila · Coordinator</span><p>“I’ll make sure your questions reach the named team. You do not have to decide today.”</p></div>
        </section>
      </aside>
    </div>
  );
}

function RecordsTab({ referral }: { referral: DemoWorkspaceResponse["case"] }) {
  return (
    <section className="content-card tab-panel">
      <div className="content-card__heading"><div><span className="card-kicker">Synthetic metadata only</span><h2>Records shared for this review</h2><p>No files are accepted or stored in Prototype V0.</p></div><button className="button button--disabled" disabled type="button"><Icon name="plus" /> Upload disabled</button></div>
      <div className="record-list">
        {referral.records.map((record) => (
          <article className="record-row" key={record.id}>
            <span className="record-row__icon"><Icon name="document" /></span>
            <div><strong>{record.label}</strong><span>{record.category} · {record.source_label}</span><small>{record.note}</small></div>
            <span>{formatDate(record.clinical_date)}</span>
            <span className={`record-state record-state--${record.state}`}><i />{record.state_label}</span>
          </article>
        ))}
      </div>
    </section>
  );
}

function AccessTab({ referral }: { referral: DemoWorkspaceResponse["case"] }) {
  return (
    <section className="content-card tab-panel">
      <div className="content-card__heading"><div><span className="card-kicker">Visible sharing</span><h2>Who is part of this case</h2><p>Each person has a named purpose. Authentication and case-view scope are enforced; consent and document-category gates remain future work.</p></div><span className="issued-chip"><Icon name="lock" /> Consent: {referral.consent_status_label}</span></div>
      <div className="participant-grid">
        {referral.participants.map((participant, index) => (
          <article className="participant-card" key={participant.id}>
            <span className={`avatar avatar--${participant.role}`}>{index === 3 ? "N" : participant.display_name.split(" ").slice(0, 2).map((part) => part[0]).join("")}</span>
            <div><span>{participant.role_label}</span><h3>{participant.display_name}</h3><p>{participant.organization || "Independent participant"}</p></div>
            <dl><div><dt>Purpose</dt><dd>{participant.purpose}</dd></div><div><dt>Visible scope</dt><dd>{participant.access_scope}</dd></div></dl>
            <span className="access-active"><i /> {participant.access_state_label}</span>
          </article>
        ))}
      </div>
    </section>
  );
}

function ActivityTab({ referral }: { referral: DemoWorkspaceResponse["case"] }) {
  return (
    <section className="content-card tab-panel">
      <div className="content-card__heading"><div><span className="card-kicker">Attributable history</span><h2>Material case activity</h2><p>This operational timeline does not expose private internal notes.</p></div></div>
      <ol className="activity-list">
        {referral.events.map((event, index) => (
          <li key={event.id}>
            <span className={index === 0 ? "activity-list__dot activity-list__dot--latest" : "activity-list__dot"}><Icon name={index === 0 ? "spark" : "check"} /></span>
            <div><strong>{event.summary}</strong><span>{event.actor_label} · {event.actor_role}</span></div>
            <time dateTime={event.occurred_at}>{formatDate(event.occurred_at, { day: "numeric", month: "short", hour: "numeric", minute: "2-digit" })}</time>
          </li>
        ))}
      </ol>
    </section>
  );
}
