"use client";

import { createContext, useContext } from "react";

import type { ProductModeResponse } from "@/lib/types";
import styles from "@/styles/product-mode.module.css";

const ProductModeContext = createContext<ProductModeResponse>({
  mode: "standard",
  demo_data_enabled: false,
});

export function ProductModeProvider({
  children,
  value,
}: {
  children: React.ReactNode;
  value: ProductModeResponse;
}) {
  return <ProductModeContext.Provider value={value}>{children}</ProductModeContext.Provider>;
}

export function useProductMode() {
  return useContext(ProductModeContext);
}

export function DemoModeBanner() {
  const mode = useProductMode();
  if (!mode.demo_data_enabled) return null;
  return (
    <div className={styles.banner} role="status">
      <span aria-hidden="true" />
      <strong>Demo data is on</strong>
      <span>People, organizations, ratings, messages, and referrals shown in demo areas are samples.</span>
    </div>
  );
}
