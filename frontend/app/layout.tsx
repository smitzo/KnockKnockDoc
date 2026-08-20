import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "Knock Knock Doc · Care referrals, kept connected",
    template: "%s · Knock Knock Doc",
  },
  description:
    "A synthetic prototype of a consent-led cross-border healthcare referral workspace.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
