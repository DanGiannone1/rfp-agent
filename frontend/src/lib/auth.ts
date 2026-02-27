import { PublicClientApplication, SilentRequest } from "@azure/msal-browser";

const tenantId = process.env.NEXT_PUBLIC_ENTRA_TENANT_ID ?? "";
const backendClientId = process.env.NEXT_PUBLIC_ENTRA_BACKEND_CLIENT_ID ?? "";
const redirectUri = process.env.NEXT_PUBLIC_ENTRA_REDIRECT_URI ?? "";

/** True when all MSAL env vars are configured. */
export const authEnabled = !!(tenantId && backendClientId);

// Use the backend app registration as the SPA client — single app reg,
// no custom API scopes, no consent required.
export const msalInstance: PublicClientApplication | null = authEnabled
  ? new PublicClientApplication({
      auth: {
        clientId: backendClientId,
        authority: `https://login.microsoftonline.com/${tenantId}`,
        redirectUri,
      },
      cache: { cacheLocation: "sessionStorage" },
    })
  : null;

export const loginRequest = {
  scopes: ["openid", "profile"],
};

/**
 * Acquire an access token silently, falling back to redirect.
 * Returns null when auth is disabled (local dev without Entra vars).
 */
export async function getAccessToken(): Promise<string | null> {
  if (!msalInstance) return null;

  // Ensure MSAL is fully initialised before using accounts
  await msalInstance.initialize();

  const accounts = msalInstance.getAllAccounts();
  if (accounts.length === 0) return null;

  const request: SilentRequest = {
    ...loginRequest,
    account: accounts[0],
  };

  try {
    const response = await msalInstance.acquireTokenSilent(request);
    return response.idToken;
  } catch {
    // Silent renewal failed — trigger interactive redirect
    await msalInstance.acquireTokenRedirect(loginRequest);
    return null; // redirect will navigate away
  }
}
