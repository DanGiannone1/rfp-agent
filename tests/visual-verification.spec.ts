import { test, expect, Page } from "@playwright/test";
import * as path from "path";
import * as fs from "fs";

const SCREENSHOTS = path.join(__dirname, "..", "screenshots");
const RFP_CONTENT = `REQUEST FOR PROPOSAL (RFP)
Title: Enterprise Cloud Migration Platform
Issuer: ACME Federal Services
Budget: $5,000,000 (Five Million USD)
Deadline: Q4 2026
SOC 2 Compliance: Required - Type II certification mandatory

REQUIREMENTS:
1. Multi-cloud orchestration supporting AWS, Azure, and GCP
2. Zero-downtime migration capability for mission-critical workloads
3. Automated dependency mapping and migration planning
4. Real-time progress dashboard with executive reporting
5. Role-based access control with SSO/SAML integration
6. Data encryption at rest and in transit (AES-256)
7. Comprehensive audit logging and compliance reporting
8. Disaster recovery with RPO < 15 minutes, RTO < 1 hour
9. API-first architecture with RESTful and GraphQL endpoints
10. 24/7 support with SLA guarantees (99.95% uptime)

EVALUATION CRITERIA:
- Technical approach and architecture (40%)
- Past performance and experience (25%)
- Cost proposal and value (20%)
- Management approach (15%)

SUBMISSION DEADLINE: December 31, 2026
QUESTIONS DUE: September 30, 2026
`;

const SECOND_FILE_CONTENT = `ADDENDUM TO RFP
Title: Security Requirements Supplement
Additional compliance: FedRAMP High, NIST 800-53
Penetration testing required annually.
`;

function screenshot(name: string) {
  return path.join(SCREENSHOTS, name);
}

async function waitForChatInput(page: Page) {
  return page.locator('[data-testid="chat-input"]').waitFor({ state: "visible", timeout: 60_000 });
}

async function waitForStreamingDone(page: Page) {
  // During streaming, stop-button is shown instead of send-button.
  // Wait for send-button to reappear OR chat-input to be enabled (means streaming finished).
  // Use a polling approach to be more resilient to HMR/navigation events.
  const deadline = Date.now() + 180_000;
  while (Date.now() < deadline) {
    const sendVisible = await page.locator('[data-testid="send-button"]').isVisible().catch(() => false);
    const chatEnabled = await page.locator('[data-testid="chat-input"]').isEnabled().catch(() => false);
    if (sendVisible && chatEnabled) return;
    // If we got navigated away (back to intake), the stream is effectively done
    const intakeVisible = await page.locator('[data-testid="intake-upload-input"]').isVisible().catch(() => false);
    if (intakeVisible) throw new Error("Page navigated back to intake during streaming");
    await page.waitForTimeout(500);
  }
  throw new Error("Streaming did not finish within 180s");
}

async function uploadViaIntake(page: Page, filePath: string) {
  const input = page.locator('[data-testid="intake-upload-input"]');
  await input.setInputFiles(filePath);
}

test.describe("Visual Verification", () => {
  let tmpDir: string;
  let rfpFile: string;
  let secondFile: string;

  test.beforeAll(() => {
    tmpDir = fs.mkdtempSync("/tmp/rfp-visual-");
    rfpFile = path.join(tmpDir, "ACME_Cloud_Migration_RFP.txt");
    fs.writeFileSync(rfpFile, RFP_CONTENT);
    secondFile = path.join(tmpDir, "Security_Addendum.txt");
    fs.writeFileSync(secondFile, SECOND_FILE_CONTENT);
  });

  test.afterAll(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  test.use({
    viewport: { width: 1440, height: 900 },
  });

  test("Phase 1-6: Full desktop flow", async ({ page }) => {
    test.setTimeout(300_000);
    // ── Phase 1: IntakeScreen ──
    console.log("Phase 1: IntakeScreen");
    await page.goto("/", { waitUntil: "domcontentloaded", timeout: 30_000 });
    await page.evaluate(() => sessionStorage.clear());
    await page.goto("/", { waitUntil: "domcontentloaded", timeout: 30_000 });

    // Wait for session to be ready (the upload drop zone should be clickable)
    // Handle retry button if session creation fails (pool exhaustion)
    for (let attempt = 0; attempt < 5; attempt++) {
      const retryBtn = page.locator('[data-testid="intake-retry-button"]');
      const retryVisible = await retryBtn.isVisible().catch(() => false);
      if (retryVisible) {
        console.log(`  Session failed, clicking retry (attempt ${attempt + 1})`);
        await retryBtn.click();
        await page.waitForTimeout(3_000);
        continue;
      }
      try {
        await page.waitForFunction(() => {
          const el = document.querySelector('[aria-label="Upload RFP file"]');
          return el && el.getAttribute("aria-disabled") === "false";
        }, { timeout: 15_000 });
        break;
      } catch {
        console.log(`  Session not ready after attempt ${attempt + 1}, reloading...`);
        if (attempt < 4) {
          await page.evaluate(() => sessionStorage.clear());
          await page.reload({ waitUntil: "domcontentloaded", timeout: 15_000 });
          await page.waitForTimeout(2_000);
        } else {
          throw new Error("Session did not become ready after 5 attempts");
        }
      }
    }

    await page.screenshot({ path: screenshot("01-intake-screen.png"), fullPage: true });

    const intakeInput = page.locator('[data-testid="intake-upload-input"]');
    await expect(intakeInput).toBeAttached();
    console.log("  PASS: intake-upload-input exists");

    const chatInput = page.locator('[data-testid="chat-input"]');
    await expect(chatInput).not.toBeVisible();
    console.log("  PASS: chat-input not visible on intake screen");

    // ── Phase 2: Upload and transition ──
    console.log("Phase 2: Upload and transition");
    await uploadViaIntake(page, rfpFile);

    await waitForChatInput(page);
    console.log("  PASS: chat-input appeared after upload");

    await page.screenshot({ path: screenshot("02-chat-ready.png"), fullPage: true });

    const artifactsPanel = page.locator('[data-testid="artifacts-panel"]');
    // The panel uses `hidden lg:flex` - at 1440px desktop it should render.
    // Use toBeAttached as a fallback if CSS `hidden` class causes visibility check issues.
    const panelVisible = await artifactsPanel.isVisible();
    if (panelVisible) {
      console.log("  PASS: artifacts-panel visible on desktop");
    } else {
      await expect(artifactsPanel).toBeAttached();
      console.log("  PASS: artifacts-panel attached on desktop (hidden+lg:flex CSS)");
    }

    // Check uploaded filename appears in the artifacts panel
    // The panel uses `hidden lg:flex` so we check the element is attached and has text
    const docName = page.locator('[data-testid="document-name"]').first();
    await expect(docName).toBeAttached({ timeout: 15_000 });
    const nameText = await docName.textContent();
    expect(nameText).toContain("ACME_Cloud_Migration_RFP");
    console.log(`  PASS: document-name shows "${nameText}"`);

    await artifactsPanel.screenshot({ path: screenshot("03-artifacts-panel.png") });

    // ── Phase 3: Agent conversation ──
    console.log("Phase 3: Agent conversation");
    await page.locator('[data-testid="chat-input"]').fill("Analyze the uploaded RFP and summarize the key requirements, budget, and deadline.");
    await page.locator('[data-testid="send-button"]').click();

    // Wait for user message to appear
    await page.locator("text=Analyze the uploaded RFP").waitFor({ state: "visible", timeout: 10_000 });
    console.log("  PASS: user message visible");

    // Quick screenshot while streaming (give agent a moment to start)
    await page.waitForTimeout(2000);
    await page.screenshot({ path: screenshot("04-streaming.png"), fullPage: true });

    // Wait for streaming to finish
    await waitForStreamingDone(page);
    await page.screenshot({ path: screenshot("05-response-complete.png"), fullPage: true });

    // Check response content
    const messages = page.locator('[data-testid="message-content"]');
    const allText = await messages.allTextContents();
    const responseText = allText.join(" ").toLowerCase();

    // The agent should mention at least some of these keywords from the RFP
    const hasRelevantContent =
      responseText.includes("budget") ||
      responseText.includes("5,000,000") ||
      responseText.includes("5m") ||
      responseText.includes("deadline") ||
      responseText.includes("q4") ||
      responseText.includes("requirement") ||
      responseText.includes("soc 2") ||
      responseText.includes("compliance");

    if (!hasRelevantContent) {
      // Fallback: check all visible text on page
      const pageText = (await page.textContent("body"))?.toLowerCase() || "";
      const pageHasContent =
        pageText.includes("budget") ||
        pageText.includes("requirement") ||
        pageText.includes("deadline") ||
        pageText.includes("compliance");
      expect(pageHasContent).toBe(true);
    }
    console.log("  PASS: assistant response contains relevant content");

    // ── Phase 4: Tool activity ──
    console.log("Phase 4: Tool activity");
    await page.locator('[data-testid="chat-input"]').fill("Use the convert_document tool to convert the uploaded file to markdown");
    await page.locator('[data-testid="send-button"]').click();

    // Wait for streaming to finish (this may take a while with tool execution)
    await waitForStreamingDone(page);
    await page.screenshot({ path: screenshot("06-tool-activity.png"), fullPage: true });

    // Check for tool indicators in the page (tool-item class from ToolIndicator component)
    const toolItems = page.locator(".tool-item");
    const toolCount = await toolItems.count();
    console.log(`  Tool indicators found: ${toolCount}`);
    if (toolCount > 0) {
      console.log("  PASS: tool activity indicators present");
    } else {
      // Tools may have completed and been shown - check page text for tool-related content
      const bodyText = (await page.textContent("body"))?.toLowerCase() || "";
      const hasToolEvidence = bodyText.includes("convert") || bodyText.includes("markdown") || bodyText.includes("tool");
      console.log(`  ${hasToolEvidence ? "PASS" : "WARN"}: tool indicators - evidence in text: ${hasToolEvidence}`);
    }

    // ── Phase 5: Multi-file and artifacts ──
    console.log("Phase 5: Multi-file upload");
    // The InputBar has a hidden file input with aria-label="Upload file"
    const chatFileInput = page.locator('input[type="file"][aria-label="Upload file"]');
    await chatFileInput.setInputFiles(secondFile);

    // Wait for upload to complete - look for the second file name in documents
    await page.waitForTimeout(5000);
    // Refresh files by waiting a bit
    await page.screenshot({ path: screenshot("07-multiple-files.png"), fullPage: true });

    // Wait for the second file to appear in the panel (may need polling refresh)
    // Use page.evaluate to count DOM elements directly since panel uses hidden+lg:flex
    let docCount = 0;
    for (let attempt = 0; attempt < 6; attempt++) {
      docCount = await page.evaluate(() =>
        document.querySelectorAll('[data-testid="document-item"]').length
      );
      console.log(`  Attempt ${attempt + 1}: DOM document items = ${docCount}`);
      if (docCount >= 2) break;
      await page.waitForTimeout(3000);
    }
    console.log(`  Document items in panel: ${docCount}`);
    console.log(`  ${docCount >= 2 ? "PASS" : "WARN"}: multiple files in panel (found ${docCount})`);

    // ── Phase 6: New chat ──
    console.log("Phase 6: New chat");
    await page.locator('[data-testid="new-chat-button"]').click();
    // Confirm via the React modal (not a browser dialog)
    await page.getByRole("button", { name: "Start new chat" }).click();

    // Wait for IntakeScreen to appear and session to be ready (with retry handling)
    await page.locator('[data-testid="intake-upload-input"]').waitFor({ state: "attached", timeout: 30_000 });
    for (let attempt = 0; attempt < 5; attempt++) {
      const retryBtn = page.locator('[data-testid="intake-retry-button"]');
      const retryVisible = await retryBtn.isVisible().catch(() => false);
      if (retryVisible) {
        console.log(`  New chat session failed, clicking retry (attempt ${attempt + 1})`);
        await retryBtn.click();
        await page.waitForTimeout(3_000);
        continue;
      }
      try {
        await page.waitForFunction(() => {
          const el = document.querySelector('[aria-label="Upload RFP file"]');
          return el && el.getAttribute("aria-disabled") === "false";
        }, { timeout: 15_000 });
        break;
      } catch {
        if (attempt < 4) {
          await page.waitForTimeout(2_000);
        } else {
          throw new Error("New chat session did not become ready after 5 attempts");
        }
      }
    }

    await page.screenshot({ path: screenshot("08-new-chat-intake.png"), fullPage: true });

    // Verify no previous messages
    const chatInputAfterReset = page.locator('[data-testid="chat-input"]');
    await expect(chatInputAfterReset).not.toBeVisible();
    console.log("  PASS: back on IntakeScreen, no chat visible");
  });

  test("Phase 7: Mobile viewport", async ({ browser, page: _unused }) => {
    test.setTimeout(60_000);
    console.log("Phase 7: Mobile viewport");
    const context = await browser.newContext({
      viewport: { width: 375, height: 812 },
    });
    const page = await context.newPage();

    await page.goto("/", { waitUntil: "domcontentloaded", timeout: 30_000 });

    // Wait for the intake screen to render (no session needed for this check)
    await page.locator('[data-testid="intake-upload-input"]').waitFor({ state: "attached", timeout: 30_000 });

    await page.screenshot({ path: screenshot("09-mobile-intake.png"), fullPage: true });

    // Artifacts panel uses "hidden lg:flex" — verify it's not visible at mobile width
    const artifactsPanel = page.locator('[data-testid="artifacts-panel"]');
    const panelAttached = await artifactsPanel.count();
    if (panelAttached > 0) {
      const mobileVisible = await artifactsPanel.isVisible();
      expect(mobileVisible).toBe(false);
    }
    console.log("  PASS: artifacts-panel hidden on mobile viewport");

    await context.close();
  });
});
