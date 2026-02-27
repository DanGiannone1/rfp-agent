"use client";

import { useEffect, useState, type ReactNode } from "react";
import { MsalProvider } from "@azure/msal-react";
import { msalInstance, authEnabled } from "@/lib/auth";

export default function Providers({ children }: { children: ReactNode }) {
  const [ready, setReady] = useState(!authEnabled);

  useEffect(() => {
    const instance = msalInstance;
    if (instance) {
      instance.initialize().then(() => {
        // Handle redirect promise (completes login after redirect back)
        instance.handleRedirectPromise().then(() => setReady(true));
      });
    }
  }, []);

  if (!ready) return null;

  if (msalInstance) {
    return <MsalProvider instance={msalInstance}>{children}</MsalProvider>;
  }

  return <>{children}</>;
}
