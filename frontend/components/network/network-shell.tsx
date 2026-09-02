"use client";

import { FormEvent, useMemo, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { Icon } from "@/components/icons";
import { Brand, PrototypeBanner } from "@/components/site-header";
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
  data,
  session,
}: {
  data: ProfessionalNetworkData;
  session: SessionResponse;
}) {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<NetworkTab>("discover");
  const [doctors, setDoctors] = useState(data.doctors);
  const [connections, setConnections] = useState(data.connections);
  const [conversations, setConversations] = useState(data.conversations);
  const [query, setQuery] = useState("");
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
  const connectionByPeer = useMemo(
    () => new Map(connections.map((connection) => [connection.peer.id, connection])),
    [connections],
  );
  const acceptedConnections = connections.filter((connection) => connection.status === "accepted");
  const activeConversation = conversations.find((item) => item.id === selectedConversation) ?? null;

  async function searchDoctors(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSearching(true);
    setError("");
    try {
      setDoctors(await searchProfessionalDoctors(query));
    } catch (searchError) {
      setError(searchError instanceof Error ? searchError.message : "Search failed.");
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
    <>
      <PrototypeBanner />
      <div className={styles.app}>
        <aside className={styles.sidebar}>
          <Brand />
          <nav aria-label="Doctor workspace">
            {tabs.map((tab) => <button aria-current={activeTab === tab.id ? "page" : undefined} key={tab.id} onClick={() => setActiveTab(tab.id)} type="button"><Icon name={tab.icon} />{tab.label}{tab.id === "messages" && conversations.length > 0 && <span>{conversations.length}</span>}</button>)}
          </nav>
          <div className={styles.sidebarBoundary}><Icon name="shield" /><p><strong>Synthetic professional space</strong>No real identities, patient details, links, or contact information.</p></div>
          <div className={styles.sidebarAccount}><span>{session.profile.display_name.slice(0, 2).toUpperCase()}</span><div><strong>{session.profile.display_name}</strong><small>{membership?.organization.name ?? "Professional account"}</small></div><button aria-label="Sign out" disabled={signingOut} onClick={signOut} type="button">{signingOut ? "…" : "↗"}</button></div>
        </aside>

        <main className={styles.main}>
          <header className={styles.mobileHeader}><Brand /><button onClick={signOut} type="button">Sign out</button></header>
          <nav className={styles.mobileTabs} aria-label="Doctor workspace sections">{tabs.map((tab) => <button aria-current={activeTab === tab.id ? "page" : undefined} key={tab.id} onClick={() => setActiveTab(tab.id)} type="button"><Icon name={tab.icon} /><span>{tab.label}</span></button>)}</nav>
          {error && <div className={styles.error} role="alert"><Icon name="shield" /><span><strong>That action did not complete.</strong>{error}</span><button aria-label="Dismiss error" onClick={() => setError("")} type="button">×</button></div>}

          {activeTab === "discover" && <section className={styles.view}>
            <div className={styles.viewHeading}><div><span>Professional discovery</span><h1>Find a specialist</h1><p>Compare verified fictional profiles and peer-collaboration signals before you connect.</p></div><span className={styles.resultCount}>{doctors.length} profiles</span></div>
            <form className={styles.search} onSubmit={searchDoctors}><Icon name="search" /><label><span className={styles.srOnly}>Search professionals</span><input maxLength={80} onChange={(event) => setQuery(event.target.value)} placeholder="Search specialty, doctor, city, or hospital" type="search" value={query} /></label><button className="button" disabled={searching} type="submit">{searching ? "Searching…" : "Search"}</button></form>
            <div className={styles.ratingBoundary}><Icon name="shield" /><p><strong>Collaboration ratings are not clinical quality scores.</strong> They summarize fictional peer feedback about communication, collaboration, and handback. Always verify suitability independently.</p></div>
            {doctors.length === 0 ? <div className={styles.empty}><Icon name="search" /><h2>No matching professionals</h2><p>Try a specialty, location, hospital, or a shorter search.</p></div> : <div className={styles.doctorGrid}>{doctors.map((doctor) => {
              const connection = connectionByPeer.get(doctor.id);
              const isSelected = selectedDoctor === doctor.id;
              return <article className={styles.doctorCard} key={doctor.id}>
                <div className={styles.doctorTop}><DoctorAvatar doctor={doctor} /><div><span>{doctor.professional_role_label}</span><h2>{doctor.display_name}</h2><p>{doctor.specialty} · {doctor.experience_years} years</p></div><span className={styles.verified}><Icon name="shield" /> {doctor.verification_label}</span></div>
                <p className={styles.summary}>{doctor.professional_summary}</p>
                <dl className={styles.doctorFacts}><div><dt>Works at</dt><dd>{doctor.organization_name}</dd></div><div><dt>Location</dt><dd>{doctor.city}, {doctor.country}</dd></div><div><dt>Languages</dt><dd>{doctor.languages.join(", ")}</dd></div></dl>
                <div className={styles.rating}><div><strong>{doctor.rating_average ?? "—"}<small>/5</small></strong><span>{doctor.rating_count} peer reviews</span></div><dl><div><dt>Communication</dt><dd>{doctor.rating_breakdown?.communication ?? "—"}</dd></div><div><dt>Collaboration</dt><dd>{doctor.rating_breakdown?.collaboration ?? "—"}</dd></div><div><dt>Handback</dt><dd>{doctor.rating_breakdown?.handback ?? "—"}</dd></div></dl></div>
                {connection ? <div className={styles.connectionState}><Icon name={connection.status === "accepted" ? "check" : "timeline"} /><span><strong>{connection.status_label}</strong>{connection.purpose_label}</span>{connection.status === "accepted" && <button onClick={() => setActiveTab("messages")} type="button">Message</button>}</div> : <button className="button button--ghost" disabled={!doctor.accepts_connections} onClick={() => setSelectedDoctor(isSelected ? null : doctor.id)} type="button">{isSelected ? "Cancel" : "Connect"} {!isSelected && <Icon name="plus" />}</button>}
                {isSelected && !connection && <form className={styles.connectForm} onSubmit={(event) => requestConnection(event, doctor)}><h3>Why do you want to connect?</h3><label><span>Purpose</span><select defaultValue="referral_collaboration" name="purpose">{purposes.map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label><label><span>Short introduction <small>(optional)</small></span><textarea maxLength={400} name="note" placeholder="Describe a fictional professional collaboration—never a patient." rows={3} /></label><p><Icon name="lock" /> No patient names, record numbers, contact details, or links.</p><button className="button" disabled={connectionBusy === doctor.id} type="submit">{connectionBusy === doctor.id ? "Sending…" : "Send request"}</button></form>}
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
              <section className={styles.thread}>{!activeConversation ? <div className={styles.threadEmpty}><Icon name="message" /><h2>Choose a conversation</h2><p>Messages are visible only to the two accepted connection participants.</p></div> : <><header><DoctorAvatar doctor={activeConversation.connection.peer} /><div><strong>{activeConversation.connection.peer.display_name}</strong><span>{activeConversation.connection.peer.specialty} · {activeConversation.connection.peer.organization_name}</span></div><span><Icon name="lock" /> Participant only</span></header><div className={styles.messages} aria-live="polite">{messagesLoading ? <p>Loading messages…</p> : messages.length === 0 ? <div className={styles.firstMessage}><Icon name="message" /><strong>Start the professional conversation.</strong><span>Keep it fictional, bounded, and free of patient information.</span></div> : messages.map((message) => <article data-mine={message.is_mine} key={message.id}><span>{message.sender_name}</span><p>{message.body}</p><time>{displayDate(message.created_at)}</time></article>)}</div><form className={styles.messageForm} onSubmit={sendMessage}><label><span className={styles.srOnly}>Message</span><textarea maxLength={1200} onChange={(event) => setMessageBody(event.target.value)} placeholder="Write a fictional professional message…" required rows={3} value={messageBody} /></label><label className={styles.messageConfirm}><input checked={messageConfirmed} onChange={(event) => setMessageConfirmed(event.target.checked)} required type="checkbox" /><span>No patient identifiers, contact details, links, or record numbers.</span></label><button className="button" disabled={sendingMessage || !messageConfirmed || !messageBody.trim()} type="submit">{sendingMessage ? "Sending…" : "Send message"} <Icon name="arrow" /></button></form></>}</section>
            </div>}
          </section>}

          {activeTab === "referrals" && <section className={styles.view}>
            <div className={styles.viewHeading}><div><span>Relationship to handoff</span><h1>Start from an accepted connection</h1><p>Only accepted peers are shown here. A professional connection never grants case access by itself.</p></div></div>
            <div className={styles.referralBoundary}><Icon name="shield" /><div><strong>V0 release boundary</strong><p>The referral rehearsal is authenticated and case access is server-enforced, but the composer is not yet cryptographically bound to the selected connection. Do not treat this screen as a production referral pathway.</p></div></div>
            {acceptedConnections.length === 0 ? <div className={styles.empty}><Icon name="document" /><h2>No accepted specialist connection</h2><p>Connect with a doctor and wait for acceptance before rehearsing a referral.</p><button className="button" onClick={() => setActiveTab("discover")} type="button">Find a specialist</button></div> : <div className={styles.referralList}>{acceptedConnections.map((connection) => <article key={connection.id}><DoctorAvatar doctor={connection.peer} /><div><span>Accepted connection</span><h2>{connection.peer.display_name}</h2><p>{connection.peer.specialty} · {connection.purpose_label}</p></div><Link className="button" href="/refer">Rehearse referral <Icon name="arrow" /></Link></article>)}</div>}
          </section>}
        </main>
      </div>
    </>
  );
}
