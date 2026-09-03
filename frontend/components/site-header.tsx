import Link from "next/link";

import styles from "@/styles/site-shell.module.css";

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
    <header className={styles.header}>
      <div className={`${styles.headerInner} page-shell`}>
        <Brand />
        <nav className={styles.desktopNav} aria-label="Main navigation">
          <Link href="/doctors">Doctors</Link>
          <Link href="/hospitals">Hospitals</Link>
          <Link href="/how-to">How it works</Link>
          <Link href="/blog">Blogs</Link>
          <Link href="/about">About</Link>
        </nav>
        <div className={styles.headerActions}>
          <Link className={styles.signIn} href="/login">Sign in</Link>
          <Link className="button button--small" href="/join">
            Join network <Icon name="arrow" />
          </Link>
        </div>
        <Link className={styles.mobileJoin} href="/join">Join</Link>
        <details className={styles.mobileMenu}>
          <summary>Menu</summary>
          <nav aria-label="Mobile navigation">
            <Link href="/doctors">Doctors</Link>
            <Link href="/hospitals">Hospitals</Link>
            <Link href="/how-to">How it works</Link>
            <Link href="/blog">Blogs</Link>
            <Link href="/about">About</Link>
            <Link href="/login">Sign in</Link>
            <Link href="/join">Join network</Link>
          </nav>
        </details>
      </div>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className={styles.footer}>
      <div className={`${styles.footerGrid} page-shell`}>
        <div className={styles.footerBrand}>
          <Brand />
          <p>Doctor-to-doctor relationships for clearer cross-border referrals.</p>
          <small>Built for trusted professional collaboration.</small>
        </div>
        <div>
          <strong>Explore</strong>
          <Link href="/doctors">Doctors</Link>
          <Link href="/hospitals">Hospitals</Link>
          <Link href="/how-to">How it works</Link>
        </div>
        <div>
          <strong>Company</strong>
          <Link href="/about">About</Link>
          <Link href="/blog">Blogs</Link>
          <Link href="/join">Join network</Link>
        </div>
        <div>
          <strong>Account</strong>
          <Link href="/login">Sign in</Link>
          <Link href="/register/doctor">Register as a doctor</Link>
          <Link href="/register/hospital">Register a hospital</Link>
        </div>
      </div>
      <div className={`${styles.footerBottom} page-shell`}>
        <span>© 2026 Knock Knock Doc</span>
        <span>Professional coordination only · Not emergency support</span>
      </div>
    </footer>
  );
}
