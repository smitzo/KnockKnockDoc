import Link from "next/link";

import { Icon } from "./icons";

export function Brand() {
  return (
    <Link className="brand" href="/" aria-label="Knock Knock Doc home">
      <span className="brand-mark"><Icon name="heart" /></span>
      <span>knock<span>knock</span>doc</span>
    </Link>
  );
}

export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="site-header__inner page-shell">
        <Brand />
        <nav className="site-nav" aria-label="Main navigation">
          <a href="#how-it-works">How it works</a>
          <Link href="/how-to">Product guide</Link>
          <Link href="/blog">Insights</Link>
        </nav>
        <div className="site-header__actions">
          <Link className="text-link hide-mobile" href="/login">Sign in</Link>
          <Link className="button button--small" href="/refer">
            Start a referral <Icon name="arrow" />
          </Link>
        </div>
      </div>
    </header>
  );
}

export function PrototypeBanner() {
  return (
    <div className="prototype-banner" role="note">
      <span className="prototype-banner__dot" aria-hidden="true" />
      Prototype V0 · Fictional data only · Not medical advice or emergency support
    </div>
  );
}
