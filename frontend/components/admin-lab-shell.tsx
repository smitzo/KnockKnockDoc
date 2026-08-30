"use client";

import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useMemo, useState } from "react";

import type { AdminLabData } from "@/lib/types";
import { deleteDemoFixtures, loadDemoFixtures, logoutSession } from "@/lib/api";
import styles from "@/styles/admin-lab.module.css";

import { Icon } from "./icons";
import { Brand } from "./site-header";

type LabTab = "doctors" | "patients" | "flow";

export function AdminLabShell({ data }: { data: AdminLabData }) {
  const router = useRouter();
  const [tab, setTab] = useState<LabTab>("doctors");
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState("all");
  const [fixtureBusy, setFixtureBusy] = useState(false);
  const [fixtureNotice, setFixtureNotice] = useState("");
  const [fixtureError, setFixtureError] = useState("");
  const fixtureLoaded = data.summary.fixture.loaded;
  const normalizedQuery = query.trim().toLowerCase();
  const doctors = useMemo(
    () => data.doctors.filter((doctor) => {
      const matchesQuery = [doctor.display_name, doctor.specialty, doctor.city, doctor.hospital_name]
        .some((value) => value.toLowerCase().includes(normalizedQuery));
      return matchesQuery && (filter === "all" || doctor.specialty === filter);
    }),
    [data.doctors, filter, normalizedQuery],
  );
  const patients = useMemo(
    () => data.patients.filter((patient) => {
      const matchesQuery = [patient.display_alias, patient.home_country, patient.specialty_interest]
        .some((value) => value.toLowerCase().includes(normalizedQuery));
      return matchesQuery && (filter === "all" || patient.journey_stage === filter);
    }),
    [data.patients, filter, normalizedQuery],
  );

  function chooseTab(nextTab: LabTab) {
    setTab(nextTab);
    setFilter("all");
    setQuery("");
  }

  async function signOut() {
    await logoutSession();
    router.replace("/login");
    router.refresh();
  }

  async function toggleDemoFixtures() {
    if (fixtureLoaded) {
      const confirmed = window.confirm(
        "Delete all versioned synthetic doctors, patients, ratings, messages, and referral rehearsals? The platform admin account will be kept so you can load them again.",
      );
      if (!confirmed) return;
    }
    setFixtureBusy(true);
    setFixtureError("");
    setFixtureNotice("");
    try {
      if (fixtureLoaded) {
        await deleteDemoFixtures();
        setFixtureNotice("Demo data deleted. The administrator account was preserved.");
        chooseTab("doctors");
      } else {
        await loadDemoFixtures();
        setFixtureNotice("30 doctors, 30 patients, and the referral rehearsal were loaded.");
      }
      router.refresh();
    } catch (error) {
      setFixtureError(error instanceof Error ? error.message : "The demo data action failed.");
    } finally {
      setFixtureBusy(false);
    }
  }

  return (
    <div className={styles.app}>
      <div className="workspace-prototype-bar"><strong>Admin-only synthetic lab</strong><span>{data.summary.counts.doctors + data.summary.counts.patients} fictional people loaded · no real records</span></div>
      <header className="lab-header">
        <Brand />
        <nav aria-label="Admin lab sections">
          <button className={tab === "doctors" ? "is-active" : ""} onClick={() => chooseTab("doctors")} type="button">Doctors <span>{data.summary.counts.doctors}</span></button>
          <button className={tab === "patients" ? "is-active" : ""} onClick={() => chooseTab("patients")} type="button">Patients <span>{data.summary.counts.patients}</span></button>
          <button className={tab === "flow" ? "is-active" : ""} onClick={() => chooseTab("flow")} type="button">Flow map</button>
        </nav>
        <button className="button button--ghost button--small" onClick={signOut} type="button">Sign out</button>
      </header>
      <main className="lab-main page-shell">
        <section className="lab-heading">
          <div><span className="eyebrow">Demo data controls</span><h1>Load the sample network when you need it.</h1><p>The records live in versioned JSON files. Only a platform admin can load, inspect, or delete the complete collection.</p></div>
          <Link className="button button--ghost" href="/how-to">Open product guide <Icon name="arrow" /></Link>
        </section>
        <section className={`fixture-control fixture-control--${data.summary.fixture.state}`} aria-labelledby="fixture-control-title">
          <div>
            <span className="fixture-control__state">{fixtureLoaded ? "Demo data loaded" : data.summary.fixture.state === "partial" ? "Demo data needs repair" : "Demo data is empty"}</span>
            <h2 id="fixture-control-title">{fixtureLoaded ? "Your full rehearsal dataset is ready." : "Create the full rehearsal dataset in one click."}</h2>
            <p>{fixtureLoaded ? "Deleting removes synthetic accounts, directory cards, ratings, chats, and referral rehearsals. Your admin account stays active." : "Loading creates 30 fictional doctors, 30 fictional patients, professional ratings, illustrated avatars, and one complete referral flow."}</p>
            <small>Fixture {data.summary.fixture.fixture.id} · schema {data.summary.fixture.fixture.schema_version} · credentials are never stored in JSON</small>
          </div>
          <button className={`button ${fixtureLoaded ? "button--danger" : ""}`} disabled={fixtureBusy} onClick={toggleDemoFixtures} type="button">
            {fixtureBusy ? "Working…" : fixtureLoaded ? "Delete demo data" : "Load demo data"}
          </button>
        </section>
        <div aria-live="polite" className="fixture-feedback">
          {fixtureNotice && <p className="fixture-feedback__success">{fixtureNotice}</p>}
          {fixtureError && <p className="fixture-feedback__error" role="alert">{fixtureError}</p>}
        </div>
        <section className="lab-stats" aria-label="Synthetic lab summary">
          <article><span>Fictional doctors</span><strong>{data.summary.counts.doctors}</strong><small>All have demo auth; none has a case grant</small></article>
          <article><span>Fictional patients</span><strong>{data.summary.counts.patients}</strong><small>Distributed across seven journey stages</small></article>
          <article><span>Specialties</span><strong>{data.summary.doctor_specialties.length}</strong><small>Balanced for filtering and flow rehearsal</small></article>
          <article><span>Real people</span><strong>0</strong><small>Every name, account, and scenario is synthetic</small></article>
        </section>

        {!fixtureLoaded && (
          <section className="lab-empty">
            <span><Icon name="people" /></span>
            <h2>No demo profiles are loaded</h2>
            <p>Use <strong>Load demo data</strong> above. The admin-only API validates the JSON manifest before creating anything.</p>
          </section>
        )}

        {fixtureLoaded && tab !== "flow" && (
          <section className="lab-toolbar" aria-label="Directory controls">
            <label><Icon name="search" /><span className="sr-only">Search profiles</span><input onChange={(event) => setQuery(event.target.value)} placeholder={tab === "doctors" ? "Search doctor, specialty, city…" : "Search alias, country, specialty…"} type="search" value={query} /></label>
            <select aria-label={tab === "doctors" ? "Filter by specialty" : "Filter by journey stage"} onChange={(event) => setFilter(event.target.value)} value={filter}>
              <option value="all">All {tab === "doctors" ? "specialties" : "stages"}</option>
              {tab === "doctors"
                ? data.summary.doctor_specialties.map((item) => <option key={item.specialty} value={item.specialty}>{item.specialty}</option>)
                : data.summary.patient_stages.map((item) => <option key={item.journey_stage} value={item.journey_stage}>{stageLabel(item.journey_stage)}</option>)}
            </select>
            <span>{tab === "doctors" ? doctors.length : patients.length} profiles shown</span>
          </section>
        )}

        {fixtureLoaded && tab === "doctors" && <DoctorGrid doctors={doctors} />}
        {fixtureLoaded && tab === "patients" && <PatientGrid patients={patients} />}
        {fixtureLoaded && tab === "flow" && <FlowMap data={data} />}
      </main>
    </div>
  );
}

function DoctorGrid({ doctors }: { doctors: AdminLabData["doctors"] }) {
  return <section className="profile-grid" aria-label="Fictional doctor profiles">{doctors.map((doctor) => (
    <article className="profile-card" key={doctor.id}>
      <Image alt={`Generated avatar for ${doctor.display_name}`} className="profile-card__avatar" height={72} src={doctor.avatar_url} unoptimized width={72} />
      <div className="profile-card__identity"><span>{doctor.specialty}</span><h2>{doctor.display_name}</h2><p>{doctor.hospital_name}</p></div>
      <span className={`capacity capacity--${doctor.availability}`}><i />{doctor.availability_label}</span>
      <dl><div><dt>City</dt><dd>{doctor.city}</dd></div><div><dt>Experience</dt><dd>{doctor.experience_years} fictional years</dd></div><div><dt>Response rehearsal</dt><dd>{doctor.response_hours} hours</dd></div><div><dt>Languages</dt><dd>{doctor.languages.join(", ")}</dd></div></dl>
      <p className="profile-card__summary">{doctor.profile_summary}</p>
      <small>{doctor.login_email} · synthetic credential state</small>
    </article>
  ))}</section>;
}

function PatientGrid({ patients }: { patients: AdminLabData["patients"] }) {
  return <section className="profile-grid" aria-label="Fictional patient profiles">{patients.map((patient) => (
    <article className="profile-card profile-card--patient" key={patient.id}>
      <Image alt={`Generated avatar for ${patient.display_alias}`} className="profile-card__avatar" height={72} src={patient.avatar_url} unoptimized width={72} />
      <div className="profile-card__identity"><span>{patient.journey_stage_label}</span><h2>{patient.display_alias}</h2><p>{patient.home_country} · {patient.age_band}</p></div>
      <span className="capacity capacity--patient"><i />Synthetic journey</span>
      <dl><div><dt>Referral interest</dt><dd>{patient.specialty_interest}</dd></div><div><dt>Preferred city</dt><dd>{patient.preferred_city}</dd></div><div><dt>Language</dt><dd>{patient.language}</dd></div><div><dt>Next coordination need</dt><dd>{patient.coordination_need}</dd></div></dl>
      <small>{patient.login_email} · no case grant created</small>
    </article>
  ))}</section>;
}

function FlowMap({ data }: { data: AdminLabData }) {
  const total = Math.max(1, data.summary.counts.patients);
  return (
    <section className="flow-map">
      <div className="flow-map__heading"><span className="eyebrow">Synthetic distribution</span><h2>Where the 30 patient rehearsals sit in the loop</h2><p>These rows help operators inspect queue shape. They are not live cases and contain no diagnosis.</p></div>
      <ol>{data.summary.patient_stages.map((item, index) => (
        <li key={item.journey_stage}><span>{index + 1}</span><div><strong>{stageLabel(item.journey_stage)}</strong><small>{item.count} fictional patients</small><i><b style={{ width: `${(item.count / total) * 100 * 5}%` }} /></i></div>{index < data.summary.patient_stages.length - 1 && <Icon name="arrow" />}</li>
      ))}</ol>
      <div className="flow-map__boundary"><Icon name="shield" /><p><strong>Catalog row ≠ care authorization.</strong> A real workspace query still requires active account, membership, assignment, grant, and scope. This lab can inspect catalog state only.</p></div>
    </section>
  );
}

function stageLabel(value: string) {
  return value.split("_").map((part) => part[0].toUpperCase() + part.slice(1)).join(" ");
}
