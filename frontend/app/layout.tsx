import type { Metadata } from "next";

import { DemoModeBanner, ProductModeProvider } from "@/components/product-mode-provider";
import { getProductMode } from "@/lib/api";

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

export default async function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const productMode = await getProductMode();
  return (
    <html lang="en">
      <body data-product-mode={productMode.mode}>
        <ProductModeProvider value={productMode}>
          <DemoModeBanner />
          {children}
        </ProductModeProvider>
      </body>
    </html>
  );
}
