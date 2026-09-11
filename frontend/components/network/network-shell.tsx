"use client";

import { FormEvent, useMemo, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { Icon } from "@/components/icons";
import { Brand } from "@/components/site-header";
import {
  createProfessionalConnection,
  getProfessionalConversations,
  getProfessionalMessages,
  logoutSession,
  searchProfessionalDoctors,
  sendProfessionalMessage,
  transitionProfessionalConnection,
} from "@/lib/api";
import type {
  ProfessionalCard,
  ProfessionalConnection,
  ProfessionalConversation,
  ProfessionalDoctorFilters,
  ProfessionalMessage,
  ProfessionalNetworkData,
  SessionResponse,
} from "@/lib/types";
import styles from "@/styles/network.module.css";

type NetworkTab = "discover" | "connections" | "messages" | "referrals";

const tabs: { id: NetworkTab; label: string; icon: "search" | "people" | "message" | "document" }[] = [
  { id: "discover", label: "Discover", icon: "search" },
  { id: "connections", label: "My network", icon: "people" },
  { id: "messages", label: "Messages", icon: "message" },
  { id: "referrals", label: "Referrals", icon: "document" },
];

const purposes = [
  ["referral_collaboration", "Referral collaboration"],
  ["second_opinion_pathway", "Second-opinion pathway"],
  ["handback_coordination", "Home-doctor handback"],
  ["professional_introduction", "Professional introduction"],
];

const emptyDoctorFilters: Required<ProfessionalDoctorFilters> = {
  query: "",
  specialty: "",
  city: "",
  minimumExperience: "",
  language: "",
  ordering: "recommended",
};

function uniqueValues(values: string[]) {
  return [...new Set(values)].sort((left, right) => left.localeCompare(right));
}

function displayDate(value: string) {
  return new Intl.DateTimeFormat("en", {
    day: "numeric",
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  }).format(new Date(value));
}

function DoctorAvatar({ doctor }: { doctor: ProfessionalCard }) {
  return <Image alt="" height={58} src={doctor.avatar_url} unoptimized width={58} />;
}

export function NetworkShell({
  adminPreview,
  data,
  demoModeEnabled,
  session,
}: {
  adminPreview: boolean;
  data: ProfessionalNetworkData;
  demoModeEnabled: boolean;
  session: SessionResponse;
}) {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<NetworkTab>("discover");
  const [doctors, setDoctors] = useState(data.doctors);
  const [connections, setConnections] = useState(data.connections);
  const [conversations, setConversations] = useState(data.conversations);
  const [filters, setFilters] = useState(emptyDoctorFilters);
  const [searching, setSearching] = useState(false);
  const [selectedDoctor, setSelectedDoctor] = useState<string | null>(null);
  const [connectionBusy, setConnectionBusy] = useState<string | null>(null);
  const [selectedConversation, setSelectedConversation] = useState<string | null>(null);
  const [messages, setMessages] = useState<ProfessionalMessage[]>([]);
  const [messagesLoading, setMessagesLoading] = useState(false);
  const [messageBody, setMessageBody] = useState("");
  const [messageConfirmed, setMessageConfirmed] = useState(false);
  const [sendingMessage, setSendingMessage] = useState(false);
  const [error, setError] = useState("");
  const [signingOut, setSigningOut] = useState(false);

  const membership = session.memberships[0];
  const visibleTabs = adminPreview ? tabs.filter((tab) => tab.id === "discover") : tabs;
  const connectionByPeer = useMemo(
    () => new Map(connections.map((connection) => [connection.peer.id, connection])),
    [connections],
  );
  const acceptedConnections = connections.filter((connection) => connection.status === "accepted");
  const activeConversation = conversations.find((item) => item.id === selectedConversation) ?? null;
  const filterOptions = useMemo(() => ({
    specialties: uniqueValues(data.doctors.map((doctor) => doctor.specialty)),
    cities: uniqueValues(data.doctors.map((doctor) => doctor.city)),
    languages: uniqueValues(data.doctors.flatMap((doctor) => doctor.languages)),
  }), [data.doctors]);
  const activeFilterCount = [
    filters.query,
    filters.specialty,
    filters.city,
    filters.minimumExperience,
    filters.language,
  ].filter(Boolean).length;

  function updateFilter<Key extends keyof typeof filters>(key: Key, value: (typeof filters)[Key]) {
    setFilters((current) => ({ ...current, [key]: value }));
  }

  async function searchDoctors(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSearching(true);
    setError("");
    try {
      setDoctors(await searchProfessionalDoctors(filters));
    } catch (searchError) {
      setError(searchError instanceof Error ? searchError.message : "Search failed.");
    } finally {
      setSearching(false);
    }
  }

  async function resetDoctorFilters() {
    setFilters(emptyDoctorFilters);
    setSearching(true);
    setError("");
    try {
      setDoctors(await searchProfessionalDoctors(emptyDoctorFilters));
    } catch (searchError) {
      setError(searchError instanceof Error ? searchError.message : "Directory could not be reset.");
    } finally {
      setSearching(false);
    }
  }

  async function requestConnection(event: FormEvent<HTMLFormElement>, doctor: ProfessionalCard) {
    event.preventDefault();
    setConnectionBusy(doctor.id);
    setError("");
    const formData = new FormData(event.currentTarget);
    try {
      const connection = await createProfessionalConnection({
        recipient_profile_id: doctor.id,
        purpose: String(formData.get("purpose")),
        note: String(formData.get("note")),
      });
      setConnections((current) => [connection, ...current]);
      setSelectedDoctor(null);
    } catch (connectionError) {
      setError(connectionError instanceof Error ? connectionError.message : "Request failed.");
    } finally {
      setConnectionBusy(null);
    }
  }

  async function updateConnection(
    connection: ProfessionalConnection,
    action: "accept" | "decline" | "withdraw",
  ) {
    setConnectionBusy(connection.id);
    setError("");
    try {
      const updated = await transitionProfessionalConnection(connection.id, action);
      setConnections((current) => current.map((item) => item.id === updated.id ? updated : item));
      if (action === "accept") setConversations(await getProfessionalConversations());
    } catch (connectionError) {
      setError(connectionError instanceof Error ? connectionError.message : "Update failed.");
    } finally {
      setConnectionBusy(null);
    }
  }

  async function openConversation(conversation: ProfessionalConversation) {
    setSelectedConversation(conversation.id);
    setMessagesLoading(true);
    setError("");
    try {
      setMessages(await getProfessionalMessages(conversation.id));
    } catch (messageError) {
      setError(messageError instanceof Error ? messageError.message : "Messages could not be loaded.");
    } finally {
      setMessagesLoading(false);
    }
  }

  async function sendMessage(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!activeConversation || !messageConfirmed || !messageBody.trim()) return;
    setSendingMessage(true);
    setError("");
    try {
      const message = await sendProfessionalMessage(activeConversation.id, messageBody.trim());
      setMessages((current) => [...current, message]);
      setConversations((current) => current.map((item) => item.id === activeConversation.id ? { ...item, last_message: message, updated_at: message.created_at } : item));
      setMessageBody("");
      setMessageConfirmed(false);
    } catch (messageError) {
      setError(messageError instanceof Error ? messageError.message : "Message could not be sent.");
    } finally {
      setSendingMessage(false);
    }
  }

  async function signOut() {
    setSigningOut(true);
    try {
      await logoutSession();
      router.replace("/login");
      router.refresh();
    } finally {
      setSigningOut(false);
    }
  }

  return (
    <div className={styles.app}>
        <aside className={styles.sidebar}>
          <Brand />
          <nav aria-label="Doctor workspace">
            {visibleTabs.map((tab) => <button aria-current={activeTab === tab.id ? "page" : undefined} key={tab.id} onClick={() => setActiveTab(tab.id)} type="button"><Icon name={tab.icon} />{tab.label}{tab.id === "messages" && conversations.length > 0 && <span>{conversations.length}</span>}</button>)}
          </nav>
          <div className={styles.sidebarBoundary}><Icon name="shield" /><p><strong>{demoModeEnabled ? "Demo data active" : "Professional privacy"}</strong>{demoModeEnabled ? "Profiles and activity on this screen are sample data." : "Keep patient details inside an authorized referral."}</p></div>
          <div className={styles.sidebarAccount}><span>{session.profile.display_name.slice(0, 2).toUpperCase()}</span><div><strong>{session.profile.display_name}</strong><small>{membership?.organization.name ?? "Professional account"}</small></div><button aria-label="Sign out" disabled={signingOut} onClick={signOut} type="button">{signingOut ? "…" : "↗"}</button></div>
        </aside>

        <main className={styles.main}>
          <header className={styles.mobileHeader}><Brand /><button onClick={signOut} type="button">Sign out</button></header>
          <nav className={styles.mobileTabs} aria-label="Doctor workspace sections">{visibleTabs.map((tab) => <button aria-current={activeTab === tab.id ? "page" : undefined} key={tab.id} onClick={() => setActiveTab(tab.id)} type="button"><Icon name={tab.icon} /><span>{tab.label}</span></button>)}</nav>
          {error && <div className={styles.error} role="alert"><Icon name="shield" /><span><strong>That action did not complete.</strong>{error}</span><button aria-label="Dismiss error" onClick={() => setError("")} type="button">×</button></div>}

          {activeTab === "discover" && <section className={styles.view}>
            {adminPreview && <div className={styles.ratingBoundary}><Icon name="lock" /><p><strong>Read-only administrator preview.</strong> You can inspect demo doctor cards, but administrator status does not let you connect, read conversations, or open referral contents.</p></div>}
            <div className={styles.catalogueHero}>
              <div className={styles.viewHeading}><div><span>India specialist catalogue</span><h1>Find the right doctor for a professional referral</h1><p>Search reviewed profiles by specialty, experience, location, language, doctor, or hospital—then connect with a clear purpose.</p></div><span className={styles.resultCount}>{doctors.length} matching profiles</span></div>
              <form className={styles.directoryFilters} onSubmit={searchDoctors}>
                <label className={styles.keywordSearch}><span>Doctor, specialty or hospital</span><div><Icon name="search" /><input maxLength={80} onChange={(event) => updateFilter("query", event.target.value)} placeholder="Try oncology or a hospital name" type="search" value={filters.query} /></div></label>
                <label><span>Specialty</span><select onChange={(event) => updateFilter("specialty", event.target.value)} value={filters.specialty}><option value="">All specialties</option>{filterOptions.specialties.map((specialty) => <option key={specialty} value={specialty}>{specialty}</option>)}</select></label>
                <label><span>Location</span><select onChange={(event) => updateFilter("city", event.target.value)} value={filters.city}><option value="">All Indian locations</option>{filterOptions.cities.map((city) => <option key={city} value={city}>{city}</option>)}</select></label>
                <label><span>Experience</span><select onChange={(event) => updateFilter("minimumExperience", event.target.value)} value={filters.minimumExperience}><option value="">Any experience</option><option value="10">10+ years</option><option value="15">15+ years</option><option value="20">20+ years</option><option value="25">25+ years</option></select></label>
                <label><span>Language</span><select onChange={(event) => updateFilter("language", event.target.value)} value={filters.language}><option value="">Any language</option>{filterOptions.languages.map((language) => <option key={language} value={language}>{language}</option>)}</select></label>
                <label><span>Sort by</span><select onChange={(event) => updateFilter("ordering", event.target.value as Required<ProfessionalDoctorFilters>["ordering"])} value={filters.ordering}><option value="recommended">Recommended</option><option value="experience_desc">Most experienced</option><option value="experience_asc">Experience: low to high</option><option value="name">Doctor name</option></select></label>
                <div className={styles.filterActions}><button className="button" disabled={searching} type="submit">{searching ? "Searching…" : "Show doctors"} <Icon name="arrow" /></button><button disabled={searching || activeFilterCount === 0} onClick={resetDoctorFilters} type="button">Clear {activeFilterCount > 0 ? `${activeFilterCount} filters` : "filters"}</button></div>
              </form>
              <div className={styles.specialtyShortcuts}><span>Popular specialties</span>{filterOptions.specialties.slice(0, 6).map((specialty) => <button aria-pressed={filters.specialty === specialty} key={specialty} onClick={() => updateFilter("specialty", filters.specialty === specialty ? "" : specialty)} type="button">{specialty}</button>)}</div>
            </div>
            <div className={styles.ratingBoundary}><Icon name="shield" /><p><strong>Collaboration ratings are not clinical quality scores.</strong> {demoModeEnabled ? "Demo ratings summarize sample peer feedback about communication, collaboration, and handback." : "They cover professional communication, collaboration, and handback only."} Always verify suitability independently.</p></div>
            {doctors.length === 0 ? <div className={styles.empty}><Icon name="search" /><h2>{demoModeEnabled ? "No matching professionals" : "No doctor profiles are published yet"}</h2><p>{demoModeEnabled ? "Try a specialty, location, hospital, or a shorter search." : "Reviewed professional profiles will appear here when the network opens in your corridor."}</p></div> : <div className={styles.doctorGrid}>{doctors.map((doctor) => {
              const connection = connectionByPeer.get(doctor.id);
              const isSelected = selectedDoctor === doctor.id;
              return <article className={styles.doctorCard} key={doctor.id}>
                <div className={styles.doctorTop}><DoctorAvatar doctor={doctor} /><div><span>{doctor.specialty}</span><h2>{doctor.display_name}</h2><p>{doctor.professional_role_label}</p></div><span className={styles.verified}><Icon name="shield" /> {doctor.verification_label}</span></div>
                <div className={styles.cardHighlights}><span><strong>{doctor.experience_years}+</strong> years experience</span><span><Icon name="location" /> {doctor.city}, {doctor.country}</span></div>
                <p className={styles.summary}>{doctor.professional_summary}</p>
                <dl className={styles.doctorFacts}><div><dt>Works at</dt><dd>{doctor.organization_name}</dd></div><div><dt>Location</dt><dd>{doctor.city}, {doctor.country}</dd></div><div><dt>Languages</dt><dd>{doctor.languages.join(", ")}</dd></div></dl>
                <div className={styles.rating}><div><strong>{doctor.rating_average ?? "—"}<small>/5</small></strong><span>{doctor.rating_count} peer reviews</span></div><dl><div><dt>Communication</dt><dd>{doctor.rating_breakdown?.communication ?? "—"}</dd></div><div><dt>Collaboration</dt><dd>{doctor.rating_breakdown?.collaboration ?? "—"}</dd></div><div><dt>Handback</dt><dd>{doctor.rating_breakdown?.handback ?? "—"}</dd></div></dl></div>
                <details className={styles.profileDetails}><summary>Professional profile details <Icon name="arrow" /></summary><div><p><strong>Specialist focus</strong>{doctor.specialty}</p><p><strong>Professional setting</strong>{doctor.organization_name}</p><p><strong>Languages</strong>{doctor.languages.join(", ")}</p><small>This synthetic catalogue demonstrates discovery and referral collaboration. It does not establish clinical suitability or treatment outcomes.</small></div></details>
                {adminPreview ? <span className={styles.verified}><Icon name="lock" /> Preview only</span> : connection ? <div className={styles.connectionState}><Icon name={connection.status === "accepted" ? "check" : "timeline"} /><span><strong>{connection.status_label}</strong>{connection.purpose_label}</span>{connection.status === "accepted" && <button onClick={() => setActiveTab("messages")} type="button">Message</button>}</div> : <button className="button button--ghost" disabled={!doctor.accepts_connections} onClick={() => setSelectedDoctor(isSelected ? null : doctor.id)} type="button">{isSelected ? "Cancel" : "Connect"} {!isSelected && <Icon name="plus" />}</button>}
                {!adminPreview && isSelected && !connection && <form className={styles.connectForm} onSubmit={(event) => requestConnection(event, doctor)}><h3>Why do you want to connect?</h3><label><span>Purpose</span><select defaultValue="referral_collaboration" name="purpose">{purposes.map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label><label><span>Short introduction <small>(optional)</small></span><textarea maxLength={400} name="note" placeholder="Introduce your professional collaboration interest." rows={3} /></label><p><Icon name="lock" /> Keep patient details inside an approved referral.</p><button className="button" disabled={connectionBusy === doctor.id} type="submit">{connectionBusy === doctor.id ? "Sending…" : "Send request"}</button></form>}
              </article>;
            })}</div>}
          </section>}

          {activeTab === "connections" && <section className={styles.view}>
            <div className={styles.viewHeading}><div><span>Professional relationships</span><h1>My network</h1><p>Review incoming requests, sent introductions, and accepted connections.</p></div><button className="button" onClick={() => setActiveTab("discover")} type="button"><Icon name="plus" /> Find doctors</button></div>
            {connections.length === 0 ? <div className={styles.empty}><Icon name="people" /><h2>Your network is empty</h2><p>Discover a professional and send a purpose-bound connection request.</p><button className="button" onClick={() => setActiveTab("discover")} type="button">Discover doctors</button></div> : <div className={styles.connectionList}>{connections.map((connection) => <article key={connection.id}><DoctorAvatar doctor={connection.peer} /><div className={styles.connectionMain}><span>{connection.viewer_relation === "recipient" ? "Request from" : "Connection with"}</span><h2>{connection.peer.display_name}</h2><p>{connection.peer.specialty} · {connection.peer.organization_name}</p>{connection.note && <blockquote>“{connection.note}”</blockquote>}<small>{connection.purpose_label} · {displayDate(connection.created_at)}</small></div><div className={styles.connectionActions}><span data-status={connection.status}>{connection.status_label}</span>{connection.status === "pending" && connection.viewer_relation === "recipient" && <><button className="button" disabled={connectionBusy === connection.id} onClick={() => updateConnection(connection, "accept")} type="button">Accept</button><button className="button button--ghost" disabled={connectionBusy === connection.id} onClick={() => updateConnection(connection, "decline")} type="button">Decline</button></>}{connection.status === "pending" && connection.viewer_relation === "requester" && <button className="button button--ghost" disabled={connectionBusy === connection.id} onClick={() => updateConnection(connection, "withdraw")} type="button">Withdraw</button>}{connection.status === "accepted" && <button className="button button--ghost" onClick={() => setActiveTab("messages")} type="button"><Icon name="message" /> Message</button>}</div></article>)}</div>}
          </section>}

          {activeTab === "messages" && <section className={`${styles.view} ${styles.messageView}`}>
            <div className={styles.viewHeading}><div><span>Connection-scoped chat</span><h1>Messages</h1><p>Professional introductions only. Patient-specific discussion belongs in an authorized referral.</p></div></div>
            {conversations.length === 0 ? <div className={styles.empty}><Icon name="message" /><h2>No conversations yet</h2><p>A conversation opens automatically after a connection request is accepted.</p><button className="button" onClick={() => setActiveTab("connections")} type="button">Review connections</button></div> : <div className={styles.messaging}>
              <aside aria-label="Conversations">{conversations.map((conversation) => <button aria-current={selectedConversation === conversation.id ? "true" : undefined} key={conversation.id} onClick={() => openConversation(conversation)} type="button"><DoctorAvatar doctor={conversation.connection.peer} /><span><strong>{conversation.connection.peer.display_name}</strong><small>{conversation.last_message?.body ?? "Connection accepted—say hello."}</small></span><time>{displayDate(conversation.updated_at)}</time></button>)}</aside>
              <section className={styles.thread}>{!activeConversation ? <div className={styles.threadEmpty}><Icon name="message" /><h2>Choose a conversation</h2><p>Messages are visible only to the two accepted connection participants.</p></div> : <><header><DoctorAvatar doctor={activeConversation.connection.peer} /><div><strong>{activeConversation.connection.peer.display_name}</strong><span>{activeConversation.connection.peer.specialty} · {activeConversation.connection.peer.organization_name}</span></div><span><Icon name="lock" /> Participant only</span></header><div className={styles.messages} aria-live="polite">{messagesLoading ? <p>Loading messages…</p> : messages.length === 0 ? <div className={styles.firstMessage}><Icon name="message" /><strong>Start the conversation.</strong><span>Discuss professional collaboration before opening a referral.</span></div> : messages.map((message) => <article data-mine={message.is_mine} key={message.id}><span>{message.sender_name}</span><p>{message.body}</p><time>{displayDate(message.created_at)}</time></article>)}</div><form className={styles.messageForm} onSubmit={sendMessage}><label><span className={styles.srOnly}>Message</span><textarea maxLength={1200} onChange={(event) => setMessageBody(event.target.value)} placeholder="Write a professional message…" required rows={3} value={messageBody} /></label><label className={styles.messageConfirm}><input checked={messageConfirmed} onChange={(event) => setMessageConfirmed(event.target.checked)} required type="checkbox" /><span>This message contains no patient identifiers or contact details.</span></label><button className="button" disabled={sendingMessage || !messageConfirmed || !messageBody.trim()} type="submit">{sendingMessage ? "Sending…" : "Send message"} <Icon name="arrow" /></button></form></>}</section>
            </div>}
          </section>}

          {activeTab === "referrals" && <section className={styles.view}>
            <div className={styles.viewHeading}><div><span>Relationship to handoff</span><h1>Start from an accepted connection</h1><p>Only accepted peers are shown here. A professional connection never grants case access by itself.</p></div></div>
            <div className={styles.referralBoundary}><Icon name="shield" /><div><strong>Connections and case access are separate</strong><p>Starting a referral does not automatically share it. The patient and each care-team member receive their own approved access.</p></div></div>
            {acceptedConnections.length === 0 ? <div className={styles.empty}><Icon name="document" /><h2>No accepted specialist connection</h2><p>Connect with a doctor and wait for acceptance before starting a referral.</p><button className="button" onClick={() => setActiveTab("discover")} type="button">Find a specialist</button></div> : <div className={styles.referralList}>{acceptedConnections.map((connection) => <article key={connection.id}><DoctorAvatar doctor={connection.peer} /><div><span>Accepted connection</span><h2>{connection.peer.display_name}</h2><p>{connection.peer.specialty} · {connection.purpose_label}</p></div><Link className="button" href="/refer">Create referral <Icon name="arrow" /></Link></article>)}</div>}
          </section>}
        </main>
      </div>
  );
}
