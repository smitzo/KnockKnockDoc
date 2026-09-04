"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { loginWithPassword } from "@/lib/api";
import { getSessionHomePath } from "@/lib/session-navigation";

import { Icon } from "./icons";

const ALLOWED_NEXT_PATHS = new Set(["/network", "/workspace", "/refer", "/admin/lab", "/hospital"]);

export function LoginForm({
  localAdminEnabled,
  nextPath,
}: {
  localAdminEnabled: boolean;
  nextPath: string;
}) {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      const session = await loginWithPassword(email, password);
      const roleHome = getSessionHomePath(session);
      const safeNext = ALLOWED_NEXT_PATHS.has(nextPath) ? nextPath : roleHome;
      router.replace(roleHome === "/admin/lab" ? roleHome : safeNext);
      router.refresh();
    } catch (loginError) {
      setError(loginError instanceof Error ? loginError.message : "Sign-in failed.");
    } finally {
      setSubmitting(false);
    }
  }

  function useLocalAdmin() {
    setEmail("admin");
    setPassword("admin");
    setError("");
  }

  return (
    <form className="login-card" onSubmit={handleSubmit}>
      <div className="login-card__heading">
        <span className="login-card__mark"><Icon name="lock" /></span>
        <div><span>Account access</span><h1>Sign in to Knock Knock Doc</h1></div>
      </div>
      <p>Enter your account details to continue.</p>
      {localAdminEnabled && <div className="login-demo"><div><span>Local admin demo</span><strong>Username: admin</strong><strong>Password: admin</strong></div><button onClick={useLocalAdmin} type="button">Use admin login</button></div>}
      <label>
        <span>Email or username</span>
        <input
          autoComplete="username"
          maxLength={254}
          onChange={(event) => setEmail(event.target.value)}
          required
          type="text"
          value={email}
        />
      </label>
      <label>
        <span>Password</span>
        <input
          autoComplete="current-password"
          maxLength={256}
          onChange={(event) => setPassword(event.target.value)}
          required
          type="password"
          value={password}
        />
      </label>
      {error && <div className="form-error" role="alert"><Icon name="shield" /><span><strong>We could not sign you in.</strong>{error}</span></div>}
      <button className="button button--large" disabled={submitting} type="submit">
        {submitting ? "Signing in…" : "Sign in securely"} {!submitting && <Icon name="arrow" />}
      </button>
      <small>Secure session · Automatic sign-out after inactivity</small>
    </form>
  );
}
