import { PublicClientApplication, SilentRequest } from "@azure/msal-browser";

const clientId = process.env.NEXT_PUBLIC_ENTRA_CLIENT_ID ?? "";
const tenantId = process.env.NEXT_PUBLIC_ENTRA_TENANT_ID ?? "";
const backendClientId = process.env.NEXT_PUBLIC_ENTRA_BACKEND_CLIENT_ID ?? "";
const redirectUri = process.env.NEXT_PUBLIC_ENTRA_REDIRECT_URI ?? "";

/** True when all MSAL env vars are configured. */
export const authEnabled = !!(clientId && tenantId && backendClientId);

export const msalInstance: PublicClientApplication | null = authEnabled
  ? new PublicClientApplication({
      auth: {
        clientId,
        authority: `https://login.microsoftonline.com/${tenantId}`,
        redirectUri,
      },
      cache: { cacheLocation: "sessionStorage" },
    })
  : null;

export const loginRequest = {
  scopes: [`api://${backendClientId}/.default`],
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
    return response.accessToken;
  } catch {
    // Silent renewal failed — trigger interactive redirect
    await msalInstance.acquireTokenRedirect(loginRequest);
    return null; // redirect will navigate away
  }
}
