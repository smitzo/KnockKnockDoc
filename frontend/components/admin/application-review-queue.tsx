"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";

import { Icon } from "@/components/icons";
import { getApplicationReviewDetail, reviewPartnerApplication } from "@/lib/api";
import type {
  PartnerApplicationReview,
  PartnerApplicationReviewAction,
  PartnerApplicationReviewSummary,
  PartnerApplicationStatus,
} from "@/lib/types";
import styles from "@/styles/application-review.module.css";

const statusFilters: { value: "all" | PartnerApplicationStatus; label: string }[] = [
  { value: "all", label: "All" },
  { value: "submitted", label: "New" },
  { value: "under_review", label: "In review" },
  { value: "changes_requested", label: "Changes" },
  { value: "approved", label: "Approved" },
  { value: "rejected", label: "Rejected" },
];

const reasons = [
  ["identity_clarification", "Identity clarification"],
  ["credential_evidence", "Credential evidence"],
  ["organization_authority", "Organization authority"],
  ["profile_correction", "Profile correction"],
  ["not_eligible", "Not eligible"],
  ["duplicate", "Duplicate application"],
  ["other", "Other"],
] as const;

export function ApplicationReviewQueue({
  initialApplications,
}: {
  initialApplications: PartnerApplicationReviewSummary[];
}) {
  const [applications, setApplications] = useState(initialApplications);
  const [filter, setFilter] = useState<(typeof statusFilters)[number]["value"]>("all");
  const [selectedId, setSelectedId] = useState(initialApplications[0]?.id ?? "");
  const [reasonCode, setReasonCode] = useState("");
  const [reviewerNote, setReviewerNote] = useState("");
  const [busyAction, setBusyAction] = useState<PartnerApplicationReviewAction | "">("");
  const [selected, setSelected] = useState<PartnerApplicationReview | null>(null);
  const [detailLoading, setDetailLoading] = useState(Boolean(initialApplications.length));
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const filtered = useMemo(
    () => applications.filter((application) => filter === "all" || application.status === filter),
    [applications, filter],
  );

  useEffect(() => {
    if (!selectedId) return;
    let current = true;
    setDetailLoading(true);
    getApplicationReviewDetail(selectedId)
      .then((application) => {
        if (current) setSelected(application);
      })
      .catch((detailError) => {
        if (current) {
          setSelected(null);
          setError(
            detailError instanceof Error
              ? detailError.message
              : "The application detail could not be loaded.",
          );
        }
      })
      .finally(() => {
        if (current) setDetailLoading(false);
      });
    return () => { current = false; };
  }, [selectedId]);

  async function applyAction(action: PartnerApplicationReviewAction) {
    if (!selected) return;
    if (["request-changes", "reject"].includes(action) && !reasonCode) {
      setError("Choose a reason before requesting changes or rejecting an application.");
      return;
    }
    setBusyAction(action);
    setError("");
    setNotice("");
    try {
      const updated = await reviewPartnerApplication(selected.id, action, {
        reason_code: reasonCode,
        reviewer_note: reviewerNote,
      });
      setApplications((current) => current.map((item) => item.id === updated.id ? updated : item));
      setSelected(updated);
      setReasonCode("");
      setReviewerNote("");
      setNotice(reviewNotice(action));
    } catch (reviewError) {
      setError(reviewError instanceof Error ? reviewError.message : "The review did not complete.");
    } finally {
      setBusyAction("");
    }
  }

  if (applications.length === 0) {
    return (
      <section className={styles.empty}>
        <span><Icon name="document" /></span>
        <h2>No applications are waiting</h2>
        <p>Create a synthetic doctor or hospital application to exercise the private review and activation flow.</p>
        <div>
          <Link className="button" href="/register/doctor">Create doctor application</Link>
          <Link className="button button--ghost" href="/register/hospital">Create hospital application</Link>
        </div>
      </section>
    );
  }

  return (
    <section className={styles.review}>
      <div className={styles.heading}>
        <div><span className="eyebrow">Private reviewer queue</span><h2>Review access before activation</h2><p>Approval projects only the role-specific synthetic identity and membership. It never grants referral or patient access.</p></div>
        <span className={styles.queueCount}>{applications.filter((item) => !["approved", "rejected"].includes(item.status)).length} open</span>
      </div>
      <div className={styles.filters} aria-label="Application status filters">
        {statusFilters.map((item) => <button aria-pressed={filter === item.value} key={item.value} onClick={() => setFilter(item.value)} type="button">{item.label}<span>{item.value === "all" ? applications.length : applications.filter((application) => application.status === item.value).length}</span></button>)}
      </div>
      <div className={styles.layout}>
        <div className={styles.list} aria-label="Applications">
          {filtered.length === 0 ? <p className={styles.noMatch}>No applications have this status.</p> : filtered.map((application) => (
            <button aria-current={selectedId === application.id} key={application.id} onClick={() => { setSelected(null); setDetailLoading(true); setSelectedId(application.id); setError(""); setNotice(""); }} type="button">
              <span className={styles.applicationIcon}><Icon name={application.application_type === "doctor" ? "people" : "home"} /></span>
              <span><small>{application.application_type_label}</small><strong>{application.display_name}</strong><em>{application.organization_name}</em></span>
              <i data-status={application.status}>{application.status_label}</i>
            </button>
          ))}
        </div>
        {detailLoading && <article className={styles.detailLoading}><span /><strong>Loading private application detail…</strong><small>Only the selected record is requested.</small></article>}
        {!detailLoading && !selected && <article className={styles.detailLoading}><Icon name="shield" /><strong>Application detail unavailable</strong><small role="alert">{error}</small></article>}
        {selected && <article className={styles.detail}>
          <header><div><span>{selected.application_type_label} application</span><h3>{selected.display_name}</h3><p>{selected.organization_name} · {selected.city}, {selected.country}</p></div><i data-status={selected.status}>{selected.status_label}</i></header>
          <div className={styles.identityGrid}><dl><div><dt>Login email</dt><dd>{selected.normalized_email}</dd></div><div><dt>Legal name</dt><dd>{selected.legal_name}</dd></div><div><dt>Language</dt><dd>{selected.preferred_language}</dd></div><div><dt>Submitted</dt><dd>{formatDate(selected.created_at)}</dd></div></dl><p>{selected.professional_summary}</p></div>
          <section className={styles.details}><h4>Application evidence</h4><dl>{Object.entries(selected.details).map(([key, value]) => <div key={key}><dt>{humanize(key)}</dt><dd>{Array.isArray(value) ? value.join(", ") : String(value)}</dd></div>)}</dl></section>
          {selected.review_reason_code && <div className={styles.previousDecision}><Icon name="document" /><p><strong>{selected.review_reason_label}</strong>{selected.reviewer_note || "No private reviewer note."}</p></div>}
          {selected.status === "approved" && <div className={styles.activation}><Icon name="check" /><p><strong>Access projection created</strong>{selected.activated_organization?.name} · {selected.application_type === "doctor" ? "professional directory access" : "hospital coordinator access"}. No case grant was created.</p></div>}
          {["submitted", "changes_requested"].includes(selected.status) && <div className={styles.primaryAction}><button className="button" disabled={Boolean(busyAction)} onClick={() => applyAction("start-review")} type="button">{busyAction === "start-review" ? "Starting…" : "Start review"} <Icon name="arrow" /></button></div>}
          {selected.status === "under_review" && <div className={styles.decision}>
            <label><span>Reason <small>required for changes or rejection</small></span><select onChange={(event) => setReasonCode(event.target.value)} value={reasonCode}><option value="">Choose a reason</option>{reasons.map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label>
            <label><span>Private reviewer note <small>never copied into the audit event</small></span><textarea maxLength={500} onChange={(event) => setReviewerNote(event.target.value)} rows={3} value={reviewerNote} /></label>
            <div><button className="button" disabled={Boolean(busyAction)} onClick={() => applyAction("approve")} type="button">{busyAction === "approve" ? "Approving…" : "Approve and activate"}</button><button className="button button--ghost" disabled={Boolean(busyAction)} onClick={() => applyAction("request-changes")} type="button">Request changes</button><button className={styles.reject} disabled={Boolean(busyAction)} onClick={() => applyAction("reject")} type="button">Reject</button></div>
          </div>}
          <div aria-live="polite" className={styles.feedback}>{notice && <p>{notice}</p>}{error && <p role="alert">{error}</p>}</div>
          <footer><Icon name="shield" /><p><strong>Synthetic review basis</strong> Approval in this local environment does not verify a real mailbox, credential, accreditation, or facility.</p></footer>
        </article>}
      </div>
    </section>
  );
}

function reviewNotice(action: PartnerApplicationReviewAction) {
  if (action === "start-review") return "Review started and attributed to your administrator session.";
  if (action === "request-changes") return "Changes requested. No access was granted.";
  if (action === "approve") return "Application approved and its bounded account access activated.";
  return "Application rejected. No access was granted.";
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat("en", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value));
}

function humanize(value: string) {
  return value.replaceAll("_", " ").replace(/^./, (letter) => letter.toUpperCase());
}
