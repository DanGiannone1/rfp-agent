import { test, expect } from "@playwright/test";
import path from "path";
import fs from "fs";

const RFP_FILE = "/tmp/test-rfp-c.txt";

test.beforeAll(() => {
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

test("Executive summary skill produces response and check artifact rendering", async ({ page }) => {
  test.setTimeout(300_000);

  // Step 1: Navigate, clear sessionStorage, reload
  await page.goto("/", { waitUntil: "domcontentloaded", timeout: 30_000 });
  await page.evaluate(() => sessionStorage.clear());
  await page.goto("/", { waitUntil: "domcontentloaded", timeout: 30_000 });

  // Wait for upload button to be ready (with retry for session creation)
  // Session pool cooldown is 300s so we retry patiently (15 attempts × ~15s = ~225s max)
  for (let attempt = 0; attempt < 15; attempt++) {
    const retryBtn = page.getByTestId("intake-retry-button");
    const retryVisible = await retryBtn.isVisible().catch(() => false);
    if (retryVisible) {
      console.log(`Session failed, clicking retry (attempt ${attempt + 1}/15)`);
      await retryBtn.click();
      await page.waitForTimeout(10_000);
      continue;
    }
    try {
      await page.waitForFunction(
        () => {
          const el = document.querySelector('[aria-label="Upload RFP file"]');
          return el && el.getAttribute("aria-disabled") === "false";
        },
        { timeout: 15_000 },
      );
      break;
    } catch {
      if (attempt < 14) {
        console.log(`Session not ready, retrying (attempt ${attempt + 1}/15)`);
        await page.evaluate(() => sessionStorage.clear());
        await page.reload({ waitUntil: "domcontentloaded", timeout: 15_000 });
        await page.waitForTimeout(5_000);
      } else {
        throw new Error("Session did not become ready after 15 attempts");
      }
    }
  }

  // Step 2: Upload RFP file
  const intakeInput = page.getByTestId("intake-upload-input");
  await intakeInput.setInputFiles(RFP_FILE);
  await expect(page.getByTestId("chat-input")).toBeVisible({ timeout: 30_000 });
  await page.screenshot({ path: "/tmp/exec-summary-01-chat-ready.png", fullPage: true });
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

  await page.screenshot({ path: "/tmp/exec-summary-02-before-send.png", fullPage: true });
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
  await page.screenshot({ path: "/tmp/exec-summary-03-streaming.png", fullPage: true });
  console.log("Screenshot 3: During streaming");

  // Wait for response to complete (input re-enabled) - skills with gpt-4.1 can take 4+ minutes
  await expect(input).toBeEnabled({ timeout: 280_000 });
  await page.screenshot({ path: "/tmp/exec-summary-04-complete.png", fullPage: true });
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
    // Check for any artifact content beyond uploaded files
    const artifactContent = await artifactsPanel.textContent();
    console.log(`Artifacts panel content preview: ${artifactContent?.substring(0, 200)}`);
    await page.screenshot({ path: "/tmp/exec-summary-05-artifacts.png", fullPage: true });
    console.log("Screenshot 5: Artifacts panel");
  }

  // Step 6: Click "Open" on the generated artifact to open canvas
  if (artifactVisible) {
    const openButtons = artifactsPanel.locator('button', { hasText: /^Open$/ });
    const openCount = await openButtons.count();
    console.log(`Open buttons found: ${openCount}`);

    if (openCount > 0) {
      await openButtons.last().click();
      console.log("Clicked Open on generated artifact");
      await page.waitForTimeout(3_000);
      await page.screenshot({ path: "/tmp/exec-summary-06-canvas-opened.png", fullPage: true });
      console.log("Screenshot 6: Canvas opened");

      // Check for error state
      const errorEl = page.locator('text=/could not load artifact/i');
      const hasError = await errorEl.isVisible().catch(() => false);
      console.log(`Canvas error visible: ${hasError}`);
      expect(hasError).toBe(false);

      // Verify canvas rendered meaningful content
      const allContent = await page.textContent("body");
      const hasContent = (allContent ?? "").toLowerCase().includes("executive summary") ||
                         (allContent ?? "").length > 5000;
      console.log(`Page has executive summary content: ${hasContent}`);
      expect(hasContent).toBe(true);
    }
  }

  // Final full-page screenshot
  await page.screenshot({ path: "/tmp/exec-summary-07-final.png", fullPage: true });
  console.log("Screenshot 7: Final state");
});
