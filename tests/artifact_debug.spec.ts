import { test, expect } from "@playwright/test";
import path from "path";
import fs from "fs";
import { SCREENSHOT_DIR, getScreenshotPath, ensureScreenshotDir } from "./e2e-screenshot-utils";
import {
  cleanupBrowserSession,
  gotoFreshIntake,
} from "./localhost-ui-helpers";

const SCREENSHOTS = SCREENSHOT_DIR;
const RFP_FILE = path.join(SCREENSHOTS, "test-rfp-c.txt");

test.beforeAll(() => {
  ensureScreenshotDir();
  console.log(`Saving artifact debug screenshots to: ${SCREENSHOTS}`);

  if (!fs.existsSync(RFP_FILE)) {
    fs.writeFileSync(RFP_FILE, [
      "REQUEST FOR PROPOSAL",
      "Title: Cloud Infrastructure Modernization",
      "Budget: $3,000,000",
      "Deadline: Q4 2026",
      "Requirements:",
      "- Multi-cloud deployment across AWS and Azure",
      "- SOC 2 Type II compliance",
      "- 99.99% uptime SLA",
      "- Zero-downtime migration capability",
    ].join("\n"));
  }
});

test.afterEach(async ({ page }) => {
  await cleanupBrowserSession(page);
});

test("Executive summary skill produces response and check artifact rendering", async ({ page }) => {
  test.setTimeout(300_000);

  // Step 1: Navigate, clear sessionStorage, reload
  await gotoFreshIntake(page);

  // Step 2: Upload RFP file
  const intakeInput = page.getByTestId("intake-upload-input");
  await intakeInput.setInputFiles(RFP_FILE);
  await expect(page.getByTestId("chat-input")).toBeVisible({ timeout: 30_000 });
  await page.screenshot({ path: getScreenshotPath("exec-summary-01-chat-ready.png"), fullPage: true });
  console.log("Screenshot 1: Chat ready after upload");

  // Step 3: Look for skill cards or type the prompt
  const input = page.getByTestId("chat-input");
  const send = page.getByTestId("send-button");
  await expect(input).toBeEnabled({ timeout: 30_000 });

  // Try to find and click executive summary skill card
  let usedSkillCard = false;
  try {
    const skillCard = page.locator('text=/executive summary/i').first();
    const visible = await skillCard.isVisible({ timeout: 5_000 }).catch(() => false);
    if (visible) {
      await skillCard.click();
      usedSkillCard = true;
      console.log("Clicked executive summary skill card");
    }
  } catch {
    // fall through to typing
  }

  if (!usedSkillCard) {
    await input.fill("Generate an executive summary for this RFP");
    console.log("Typed executive summary prompt");
  }

  await page.screenshot({ path: getScreenshotPath("exec-summary-02-before-send.png"), fullPage: true });
  console.log("Screenshot 2: Before sending");

  // Send if we typed (skill card may auto-send)
  if (!usedSkillCard) {
    await send.click();
  }

  // Wait for input to become disabled (message being processed)
  await expect(input).toBeDisabled({ timeout: 15_000 }).catch(() => {
    console.log("Input did not become disabled - may have already been processed");
  });

  // Take a mid-stream screenshot
  await page.waitForTimeout(5_000);
  await page.screenshot({ path: getScreenshotPath("exec-summary-03-streaming.png"), fullPage: true });
  console.log("Screenshot 3: During streaming");

  // Wait for response to complete (input re-enabled) - skills with gpt-4.1 can take 4+ minutes
  await expect(input).toBeEnabled({ timeout: 280_000 });
  await page.screenshot({ path: getScreenshotPath("exec-summary-04-complete.png"), fullPage: true });
  console.log("Screenshot 4: Response complete");

  // Step 4: Check for agent response
  const assistantMessages = page.locator('.message-row-assistant .prose');
  const count = await assistantMessages.count();
  console.log(`Found ${count} assistant message(s)`);
  expect(count).toBeGreaterThan(0);

  const lastReply = await assistantMessages.last().textContent();
  console.log(`Last reply length: ${lastReply?.length ?? 0} chars`);
  console.log(`Last reply preview: ${lastReply?.substring(0, 300)}`);

  // Verify no "agent turn failed" error
  const lowerReply = (lastReply ?? "").toLowerCase();
  expect(lowerReply).not.toContain("agent turn failed");
  expect(lowerReply).not.toContain("error");

  // Verify substantive content (should mention something from the RFP)
  expect(lastReply!.length).toBeGreaterThan(50);

  // Step 5: Check for artifact/canvas panel
  const artifactsPanel = page.getByTestId("artifacts-panel");
  const artifactVisible = await artifactsPanel.isVisible().catch(() => false);
  console.log(`Artifacts panel visible: ${artifactVisible}`);

  if (artifactVisible) {
    await expect
      .poll(async () => (await artifactsPanel.textContent()) || "", { timeout: 15_000 })
      .not.toContain("No deliverables");

    const artifactContent = await artifactsPanel.textContent();
    console.log(`Artifacts panel content preview: ${artifactContent?.substring(0, 200)}`);
    const generatedDoc = artifactsPanel
      .locator('[data-testid="document-name"]')
      .filter({ hasText: /^executive_summary\.md$/ })
      .first();
    await expect(generatedDoc).toBeVisible({ timeout: 15_000 });
    await page.screenshot({ path: getScreenshotPath("exec-summary-05-artifacts.png"), fullPage: true });
    console.log("Screenshot 5: Artifacts panel");
  }

  // Step 6: Open the generated artifact in the current UI
  if (artifactVisible) {
    await artifactsPanel
      .locator('[data-testid="document-name"]')
      .filter({ hasText: /^executive_summary\.md$/ })
      .first()
      .click();
    console.log("Clicked generated executive summary");
    await page.waitForTimeout(3_000);
    await page.screenshot({ path: getScreenshotPath("exec-summary-06-canvas-opened.png"), fullPage: true });
    console.log("Screenshot 6: Canvas opened");

    const errorEl = page.locator('text=/could not load artifact/i');
    const hasError = await errorEl.isVisible().catch(() => false);
    console.log(`Canvas error visible: ${hasError}`);
    expect(hasError).toBe(false);

    await expect(page.getByText("Executive Summary").first()).toBeVisible({ timeout: 15_000 });
    const allContent = await page.textContent("body");
    const hasContent = (allContent ?? "").toLowerCase().includes("executive summary");
    console.log(`Page has executive summary content: ${hasContent}`);
    expect(hasContent).toBe(true);
  }

  // Final full-page screenshot
  await page.screenshot({ path: getScreenshotPath("exec-summary-07-final.png"), fullPage: true });
  console.log("Screenshot 7: Final state");
});
