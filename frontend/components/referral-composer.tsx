"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";

import { createSyntheticReferral } from "@/lib/api";
import styles from "@/styles/authenticated.module.css";

import { Icon } from "./icons";

const initialForm = {
  patient_alias: "Patient B · synthetic",
  patient_country: "Kenya",
  patient_age_band: "45–59",
  specialty: "Oncology",
  clinical_question: "Please review this fictional planned-care referral for specialist fit.",
  summary: "A fully fictional, stable planned-care scenario created only to rehearse the referral workflow.",
  is_planned_care: true,
  accepts_synthetic_only: false,
};

export function ReferralComposer({
  referrerName,
  referrerOrganization,
}: {
  referrerName: string;
  referrerOrganization: string;
}) {
  const [form, setForm] = useState(initialForm);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [createdReference, setCreatedReference] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      const created = await createSyntheticReferral(form);
      setCreatedReference(created.reference);
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "The rehearsal could not be created.");
    } finally {
      setSubmitting(false);
    }
  }

  if (createdReference) {
    return (
      <section className="refer-success page-shell">
        <span className="refer-success__mark"><Icon name="check" /></span>
        <span className="eyebrow eyebrow--quiet">Rehearsal created</span>
        <h1>The synthetic referral is ready for patient review.</h1>
        <p>Reference <strong>{createdReference}</strong> was written with a pending synthetic consent step. No real person or clinical record was submitted.</p>
        <div><Link className="button button--large" href="/workspace">Open the guided demo workspace <Icon name="arrow" /></Link><button className="button button--ghost button--large" onClick={() => setCreatedReference("")} type="button">Create another rehearsal</button></div>
      </section>
    );
  }

  return (
    <div className="refer-layout page-shell">
      <aside className="refer-intro">
        <span className="eyebrow"><Icon name="document" /> Referral rehearsal</span>
        <h1>Prepare one clear question for one named care path.</h1>
        <p>This V0 form demonstrates the doctor-created start of a referral. It accepts fictional text only and never medical files.</p>
        <ol className="refer-checklist">
          <li className="is-current"><span>1</span><div><strong>Referral context</strong><small>Question and synthetic summary</small></div></li>
          <li><span>2</span><div><strong>Patient review</strong><small>Purpose, people, and sharing</small></div></li>
          <li><span>3</span><div><strong>Case completeness</strong><small>Handled in the workspace</small></div></li>
        </ol>
        <div className="refer-boundary"><Icon name="shield" /><p><strong>Stable planned care only.</strong> This is not an emergency or triage service. For urgent concerns, contact local emergency services or a treating clinician.</p></div>
      </aside>

      <form className="refer-form" onSubmit={handleSubmit}>
        <div className="refer-form__heading"><span>Step 1 of 3</span><h2>Tell the receiving team what is being asked</h2><p>Use invented names and facts. Do not paste a real medical history.</p></div>
        <fieldset>
          <legend>Fictional patient context</legend>
          <div className="form-grid form-grid--two">
            <label><span>Patient alias</span><input maxLength={80} required value={form.patient_alias} onChange={(event) => setForm({ ...form, patient_alias: event.target.value })}/><small>No name, email, or phone number</small></label>
            <label><span>Country</span><input maxLength={80} required value={form.patient_country} onChange={(event) => setForm({ ...form, patient_country: event.target.value })}/></label>
            <label><span>Age band</span><select value={form.patient_age_band} onChange={(event) => setForm({ ...form, patient_age_band: event.target.value })}><option>child</option><option>18–29</option><option>30–44</option><option>45–59</option><option>60–74</option><option>75+</option></select></label>
            <label><span>Specialty</span><select value={form.specialty} onChange={(event) => setForm({ ...form, specialty: event.target.value })}><option>Oncology</option><option>Cardiac sciences</option><option>Complex surgery</option><option>Neurology</option><option>Other</option></select></label>
          </div>
        </fieldset>
        <fieldset>
          <legend>Referral question</legend>
          <label><span>What should the receiving specialist review?</span><textarea minLength={20} maxLength={500} required rows={3} value={form.clinical_question} onChange={(event) => setForm({ ...form, clinical_question: event.target.value })}/><small>{form.clinical_question.length}/500 · Preserve the referring doctor&apos;s wording</small></label>
          <label><span>Brief sourced context</span><textarea minLength={30} maxLength={2000} required rows={4} value={form.summary} onChange={(event) => setForm({ ...form, summary: event.target.value })}/><small>Describe a fictional, stable planned-care scenario. Do not diagnose.</small></label>
        </fieldset>
        <div className={styles.authenticatedReferrer}><Icon name="shield" /><div><span>Creating as</span><strong>{referrerName}</strong><small>{referrerOrganization} · identity supplied by the server</small></div></div>
        <div className="confirmation-list">
          <label><input checked={form.is_planned_care} onChange={(event) => setForm({ ...form, is_planned_care: event.target.checked })} type="checkbox"/><span><strong>This is a stable, planned-care rehearsal</strong><small>Not an urgent or emergency concern</small></span></label>
          <label><input checked={form.accepts_synthetic_only} onChange={(event) => setForm({ ...form, accepts_synthetic_only: event.target.checked })} type="checkbox"/><span><strong>Everything entered here is fictional</strong><small>I have not included real personal or health data</small></span></label>
        </div>
        {error && <div className="form-error" role="alert"><Icon name="shield" /><span><strong>We could not create this rehearsal.</strong>{error}</span></div>}
        <div className="refer-form__actions"><p><Icon name="lock" /> JSON metadata only · Uploads disabled</p><button className="button button--large" disabled={submitting} type="submit">{submitting ? "Creating rehearsal…" : "Create synthetic referral"} {!submitting && <Icon name="arrow" />}</button></div>
      </form>
    </div>
  );
}
