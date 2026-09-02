import type { Metadata } from "next";

import "./tailwind.css";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "Knock Knock Doc · Doctor connections, clearer referrals",
    template: "%s · Knock Knock Doc",
  },
  description:
    "A doctor-first professional network for trusted cross-border referral relationships.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
