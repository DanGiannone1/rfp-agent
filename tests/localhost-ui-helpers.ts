import { expect, Page } from "@playwright/test";

export const API = process.env.API_URL ?? "http://localhost:8000";

export async function createSessionViaAPI(): Promise<string> {
  const res = await fetch(`${API}/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({}),
  });
  if (!res.ok) throw new Error(`create session failed: ${res.status}`);
  const body = await res.json();
  return body.session_id;
}

export async function deleteSessionViaAPI(sessionId: string): Promise<void> {
  await fetch(`${API}/sessions/${sessionId}`, { method: "DELETE" });
}

export async function cleanupBrowserSession(page: Page): Promise<void> {
  try {
    const sid = await page.evaluate(() => sessionStorage.getItem("rfp_agent_session_id"));
    if (sid) await deleteSessionViaAPI(sid);
  } catch {
    // best-effort cleanup
  }
}

export async function gotoFreshIntake(page: Page): Promise<void> {
  await page.goto("/", { waitUntil: "domcontentloaded", timeout: 30_000 });
  await page.evaluate(() => sessionStorage.clear());
  await page.goto("/", { waitUntil: "domcontentloaded", timeout: 30_000 });

  const retryBtn = page.locator('[data-testid="intake-retry-button"]');
  if (await retryBtn.isVisible().catch(() => false)) {
    await retryBtn.click();
  }

  await expect(page.locator('[data-testid="intake-upload-input"]')).toBeAttached({ timeout: 30_000 });
  await page.waitForFunction(
    () => {
      const el = document.querySelector('[aria-label="Upload RFP file"]');
      return el?.getAttribute("aria-disabled") === "false";
    },
    { timeout: 30_000 },
  );
}

export async function gotoAndUpload(page: Page, filePath: string): Promise<void> {
  await gotoFreshIntake(page);
  await page.locator('[data-testid="intake-upload-input"]').setInputFiles(filePath);
  await expect(page.locator('[data-testid="chat-input"]')).toBeVisible({ timeout: 30_000 });
  await expect(page.locator('[data-testid="chat-input"]')).toBeEnabled({ timeout: 30_000 });
}

export async function startNewChat(page: Page): Promise<void> {
  await page.locator('[data-testid="new-chat-button"]').click();
  await page.getByRole("button", { name: "Start new chat" }).click();
  await expect(page.locator('[data-testid="intake-upload-input"]')).toBeAttached({ timeout: 30_000 });
}

export async function waitForStreamingDone(page: Page, timeoutMs = 180_000): Promise<void> {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const sendVisible = await page.locator('[data-testid="send-button"]').isVisible().catch(() => false);
    const chatEnabled = await page.locator('[data-testid="chat-input"]').isEnabled().catch(() => false);
    if (sendVisible && chatEnabled) return;

    const intakeVisible = await page.locator('[data-testid="intake-upload-input"]').isVisible().catch(() => false);
    if (intakeVisible) throw new Error("Page navigated back to intake during streaming");

    await page.waitForTimeout(500);
  }
  throw new Error(`Streaming did not finish within ${timeoutMs}ms`);
}
