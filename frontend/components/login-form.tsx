"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { loginWithPassword } from "@/lib/api";

import { Icon } from "./icons";

const ALLOWED_NEXT_PATHS = new Set(["/workspace", "/refer", "/admin/lab"]);

export function LoginForm({ nextPath }: { nextPath: string }) {
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
      const isAdmin = session.memberships.some((membership) => membership.role === "admin");
      const safeNext = ALLOWED_NEXT_PATHS.has(nextPath) ? nextPath : "/workspace";
      router.replace(isAdmin ? "/admin/lab" : safeNext);
      router.refresh();
    } catch (loginError) {
      setError(loginError instanceof Error ? loginError.message : "Sign-in failed.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="login-card" onSubmit={handleSubmit}>
      <div className="login-card__heading">
        <span className="login-card__mark"><Icon name="lock" /></span>
        <div><span>Authenticated prototype</span><h1>Sign in to your care workspace</h1></div>
      </div>
      <p>Use only a locally seeded fictional account. Real patient or clinical data is still prohibited.</p>
      <label>
        <span>Email</span>
        <input
          autoComplete="username"
          inputMode="email"
          maxLength={254}
          onChange={(event) => setEmail(event.target.value)}
          required
          type="email"
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
      <small>Session cookies are HTTP-only. Passwords are never stored in this browser.</small>
    </form>
  );
}
