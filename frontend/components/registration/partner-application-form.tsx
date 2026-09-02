"use client";

import { FormEvent, useRef, useState } from "react";
import Link from "next/link";

import { Icon } from "@/components/icons";
import { submitPartnerApplication } from "@/lib/api";
import type { PartnerApplicationPayload } from "@/lib/types";
import styles from "@/styles/registration.module.css";

const TERMS_VERSION = "prototype-2026-08-11" as const;

function listValue(formData: FormData, name: string) {
  return String(formData.get(name) ?? "")
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean);
}

function Field({
  label,
  name,
  ...inputProps
}: {
  label: string;
  name: string;
} & React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <label className={styles.field}>
      <span>{label}</span>
      <input name={name} {...inputProps} />
    </label>
  );
}

function ListField({ label, name, example }: { label: string; name: string; example: string }) {
  return (
    <Field
      autoComplete="off"
      label={label}
      name={name}
      placeholder={example}
      required
      type="text"
    />
  );
}

export function PartnerApplicationForm({ kind }: { kind: "doctor" | "hospital" }) {
  const formRef = useRef<HTMLFormElement>(null);
  const [step, setStep] = useState(1);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const isDoctor = kind === "doctor";

  function validateCurrentStep() {
    const fieldset = formRef.current?.querySelector<HTMLFieldSetElement>(
      `fieldset[data-step="${step}"]`,
    );
    const fields = fieldset?.querySelectorAll<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >("input, textarea, select");
    if (!fields) return false;
    for (const field of fields) {
      if (!field.checkValidity()) {
        field.reportValidity();
        return false;
      }
    }
    return true;
  }

  function nextStep() {
    if (!validateCurrentStep()) return;
    setError("");
    setStep((current) => Math.min(3, current + 1));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (step < 3) {
      nextStep();
      return;
    }
    setSubmitting(true);
    setError("");
    const formData = new FormData(event.currentTarget);
    const details: PartnerApplicationPayload["details"] = isDoctor
      ? {
          professional_role: String(formData.get("professional_role")),
          primary_specialty: String(formData.get("primary_specialty")),
          subspecialties: listValue(formData, "subspecialties"),
          current_designation: String(formData.get("current_designation")),
          experience_start_year: Number(formData.get("experience_start_year")),
          council_jurisdiction: String(formData.get("council_jurisdiction")),
          synthetic_registration_number: String(
            formData.get("synthetic_registration_number"),
          ),
          qualifications: listValue(formData, "qualifications"),
          languages: listValue(formData, "languages"),
        }
      : {
          organization_type: String(formData.get("organization_type")),
          representative_title: String(formData.get("representative_title")),
          website_url: String(formData.get("website_url")),
          establishment_year: Number(formData.get("establishment_year")),
          departments: listValue(formData, "departments"),
          accreditation_labels: listValue(formData, "accreditation_labels"),
          bed_count: Number(formData.get("bed_count")),
          capacity_as_of: String(formData.get("capacity_as_of")),
          international_patient_services: listValue(
            formData,
            "international_patient_services",
          ),
          languages: listValue(formData, "languages"),
        };

    try {
      await submitPartnerApplication({
        application_type: kind,
        email: String(formData.get("email")),
        password: String(formData.get("password")),
        legal_name: String(formData.get("legal_name")),
        display_name: String(formData.get("display_name")),
        country: String(formData.get("country")),
        city: String(formData.get("city")),
        timezone: String(formData.get("timezone")),
        preferred_language: String(formData.get("preferred_language")),
        organization_name: String(formData.get("organization_name")),
        professional_summary: String(formData.get("professional_summary")),
        terms_version: TERMS_VERSION,
        accepts_synthetic_only: true,
        details,
      });
      setSubmitted(true);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (applicationError) {
      setError(
        applicationError instanceof Error
          ? applicationError.message
          : "The application could not be submitted.",
      );
    } finally {
      setSubmitting(false);
    }
  }

  if (submitted) {
    return (
      <section className={styles.success} aria-live="polite">
        <span><Icon name="check" /></span>
        <p className={styles.kicker}>Application received</p>
        <h1>Your fictional profile is waiting for review.</h1>
        <p>
          The account is inactive. It cannot sign in, appear in search, message a doctor,
          or open a referral until a platform reviewer verifies and approves it.
        </p>
        <div className={styles.successActions}>
          <Link className="button" href="/">Return home</Link>
          <Link className="button button--ghost" href="/about">See how verification works</Link>
        </div>
      </section>
    );
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit} ref={formRef}>
      <div className={styles.formHeader}>
        <div>
          <span className={styles.kicker}>Step {step} of 3</span>
          <h1>{isDoctor ? "Create your doctor application" : "Register a hospital representative"}</h1>
          <p>No access is granted until verification. Use fictional prototype details only.</p>
        </div>
        <ol className={styles.progress} aria-label="Application progress">
          {["Account", "Profile", "Review"].map((label, index) => (
            <li aria-current={step === index + 1 ? "step" : undefined} data-complete={step > index + 1} key={label}>
              <span>{step > index + 1 ? "✓" : index + 1}</span>{label}
            </li>
          ))}
        </ol>
      </div>

      <fieldset data-step="1" hidden={step !== 1}>
        <legend>Secure account</legend>
        <p className={styles.sectionHelp}>Use a made-up <strong>.test</strong> email. Real identities are rejected in V0.</p>
        <div className={styles.grid}>
          <Field autoComplete="email" label="Fictional email" name="email" placeholder="arun@care-network.test" required type="email" />
          <Field autoComplete="new-password" label="Password (14+ characters)" minLength={14} name="password" required type="password" />
          <Field autoComplete="name" label="Fictional legal name" maxLength={120} minLength={2} name="legal_name" required />
          <Field autoComplete="nickname" label="Public display name" maxLength={120} minLength={2} name="display_name" required />
        </div>
        <div className={styles.notice}><Icon name="lock" /><p>The password is hashed by the backend. The application creates an inactive account with no product permissions.</p></div>
      </fieldset>

      <fieldset data-step="2" hidden={step !== 2}>
        <legend>Professional context</legend>
        <p className={styles.sectionHelp}>These details help a reviewer understand the intended network profile.</p>
        <div className={styles.grid}>
          <Field autoComplete="country-name" label="Country" maxLength={80} minLength={2} name="country" placeholder="Fictional country" required />
          <Field autoComplete="address-level2" label="City" maxLength={80} minLength={2} name="city" placeholder="Fictional city" required />
          <Field autoComplete="off" label="Timezone" maxLength={64} minLength={3} name="timezone" placeholder="Asia/Kolkata" required />
          <Field autoComplete="language" label="Preferred language" maxLength={40} minLength={2} name="preferred_language" placeholder="English" required />
          <Field autoComplete="organization" label={isDoctor ? "Current organization" : "Hospital name"} maxLength={140} minLength={2} name="organization_name" required />
          {isDoctor ? (
            <label className={styles.field}>
              <span>Network role</span>
              <select defaultValue="" name="professional_role" required>
                <option disabled value="">Choose a role</option>
                <option value="referrer">Referring doctor</option>
                <option value="specialist">Receiving specialist</option>
              </select>
            </label>
          ) : (
            <label className={styles.field}>
              <span>Organization type</span>
              <select defaultValue="" name="organization_type" required>
                <option disabled value="">Choose a type</option>
                <option value="multi_specialty">Multi-specialty hospital</option>
                <option value="single_specialty">Single-specialty hospital</option>
                <option value="clinic">Clinic</option>
                <option value="hospital_group">Hospital group</option>
              </select>
            </label>
          )}
          <label className={`${styles.field} ${styles.fullWidth}`}>
            <span>Professional summary</span>
            <textarea maxLength={500} minLength={30} name="professional_summary" placeholder="Describe a fictional practice focus, collaboration style, and referral interests." required rows={4} />
            <small>30–500 characters. Do not include patient information.</small>
          </label>
        </div>
      </fieldset>

      <fieldset data-step="3" hidden={step !== 3}>
        <legend>{isDoctor ? "Credentials for prototype review" : "Hospital details for prototype review"}</legend>
        <p className={styles.sectionHelp}>These values remain private application data and do not become a public listing.</p>
        <div className={styles.grid}>
          {isDoctor ? (
            <>
              <Field label="Primary specialty" maxLength={80} minLength={2} name="primary_specialty" placeholder="Cardiology" required />
              <Field label="Current designation" maxLength={100} minLength={2} name="current_designation" placeholder="Consultant" required />
              <ListField example="Interventional cardiology, Heart failure" label="Subspecialties (comma separated)" name="subspecialties" />
              <Field label="Experience start year" max={2026} min={1950} name="experience_start_year" placeholder="2012" required type="number" />
              <Field label="Council jurisdiction" maxLength={100} minLength={2} name="council_jurisdiction" placeholder="Synthetic Medical Council" required />
              <Field label="Fictional registration ID" name="synthetic_registration_number" pattern="SYN-[A-Za-z0-9-]{4,40}" placeholder="SYN-KKD-2048" required />
              <ListField example="MBBS, MD Cardiology" label="Qualifications (comma separated)" name="qualifications" />
              <ListField example="English, Hindi" label="Languages (comma separated)" name="languages" />
            </>
          ) : (
            <>
              <Field label="Representative title" maxLength={100} minLength={2} name="representative_title" placeholder="Clinical partnerships lead" required />
              <Field label="Fictional website" name="website_url" placeholder="https://hospital.example" required type="url" />
              <Field label="Establishment year" max={2026} min={1900} name="establishment_year" required type="number" />
              <Field label="Bed count" max={10000} min={1} name="bed_count" required type="number" />
              <Field label="Capacity data as of" max="2026-08-11" name="capacity_as_of" required type="date" />
              <ListField example="Cardiology, Oncology" label="Departments (comma separated)" name="departments" />
              <ListField example="Synthetic accreditation" label="Accreditations (comma separated)" name="accreditation_labels" />
              <ListField example="Care coordination, Interpreter support" label="International services (comma separated)" name="international_patient_services" />
              <ListField example="English, Hindi" label="Languages (comma separated)" name="languages" />
            </>
          )}
        </div>
        <label className={styles.confirmation}>
          <input name="synthetic_confirmation" required type="checkbox" />
          <span><strong>I confirm every value is fictional.</strong> I understand submission grants no access and is governed by prototype terms {TERMS_VERSION}.</span>
        </label>
      </fieldset>

      {error && <div className={styles.error} role="alert"><Icon name="shield" /><span><strong>Check the application.</strong>{error}</span></div>}
      <div className={styles.actions}>
        {step > 1 && <button className="button button--ghost" disabled={submitting} onClick={() => setStep((current) => current - 1)} type="button">Back</button>}
        <button className="button" disabled={submitting} type="submit">
          {step < 3 ? "Continue" : submitting ? "Submitting…" : "Submit for review"}
          {!submitting && <Icon name="arrow" />}
        </button>
      </div>
    </form>
  );
}
