import { test, expect, Page } from "@playwright/test";
import * as path from "path";
import * as fs from "fs";
import {
  ensureScreenshotDir,
  getScreenshotPath,
  SCREENSHOT_DIR,
} from "./e2e-screenshot-utils";
import {
  cleanupBrowserSession,
  gotoAndUpload,
  startNewChat,
  waitForStreamingDone,
} from "./localhost-ui-helpers";

const STARTER_PROMPTS = [
  {
    label: "Bid/No-Bid analysis",
    prompt: "Run a bid/no-bid analysis and score this opportunity across six dimensions. Provide a final recommendation and do not ask any follow-up questions.",
    keyword: "score",
  },
  {
    label: "Extract requirements",
    prompt: "Extract all requirements from the RFP and build a prioritized requirements matrix with section and page references. Do not ask any follow-up questions.",
    keyword: "requirements",
  },
  {
    label: "Executive summary",
    prompt: "Draft a one-page executive summary with our key win themes, clear value and no follow-up questions.",
    keyword: "summary",
  },
  {
    label: "Response strategy",
    prompt: "Develop a response strategy with win themes, competitive positioning, and a pricing approach. Do not ask follow-up questions.",
    keyword: "win",
  },
];

function slugifyLabel(label: string): string {
  return label
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

async function waitForNewAssistantMessage(page: Page, previousCount: number, timeoutMs = 30_000) {
  const end = Date.now() + timeoutMs;
  while (Date.now() < end) {
    const count = await page.locator(".message-row-assistant").count();
    if (count > previousCount) return;
    await page.waitForTimeout(500);
  }
  throw new Error(`No new assistant message appeared within ${timeoutMs}ms`);
}

test.describe("Starter prompts in UI", () => {
  const tmpDir = path.join(__dirname, ".tmp-starters");
  const rfpPath = path.join(tmpDir, "starter-rfp.md");
  test.setTimeout(1_200_000);

  test.beforeAll(() => {
    ensureScreenshotDir();
    fs.mkdirSync(tmpDir, { recursive: true });
    fs.writeFileSync(
      rfpPath,
      [
        "# Request for Proposal",
        "REQUEST FOR PROPOSAL",
        "Title: Cloud Transformation Project",
        "Budget: $2,750,000",
        "Deadline: December 31, 2026",
        "Requirements:",
        "- Multi-cloud migration",
        "- SOC 2 Type II compliance",
        "- 24x7 support with 99.95% SLA",
      ].join("\n"),
    );
    console.log(`Saving screenshots to: ${SCREENSHOT_DIR}`);
  });

  test.afterAll(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  test.afterEach(async ({ page }) => {
    await cleanupBrowserSession(page);
  });

  test("Run all four starter prompts after upload (UI only)", async ({ page }) => {
    for (let i = 0; i < STARTER_PROMPTS.length; i++) {
      const { label, prompt, keyword } = STARTER_PROMPTS[i];

      if (i === 0) {
        await gotoAndUpload(page, rfpPath);
      } else {
        await startNewChat(page);
        await gotoAndUpload(page, rfpPath);
      }

      const screenshotBase = `starter-${i + 1}-${slugifyLabel(label)}`;

      await page.screenshot({ path: getScreenshotPath(`${screenshotBase}-ready.png`), fullPage: true });

      const beforeAssistantCount = await page.locator(".message-row-assistant").count();

      await page.locator('[data-testid="chat-input"]').fill(prompt);
      await page.locator('[data-testid="send-button"]').click();

      await waitForNewAssistantMessage(page, beforeAssistantCount);

      await waitForStreamingDone(page, 420_000);

      const assistantRows = page.locator(".message-row-assistant");
      await waitForNewAssistantMessage(page, beforeAssistantCount, 30_000);

      const lastAssistant = assistantRows.last();
      const replyText = (await lastAssistant.textContent())?.trim() ?? "";

      expect(replyText.length).toBeGreaterThan(20);
      expect(replyText.toLowerCase()).toContain(keyword);
      expect(replyText.toLowerCase()).not.toContain("agent turn failed");

      await page.screenshot({
        path: getScreenshotPath(`${screenshotBase}-done.png`),
        fullPage: true,
      });

      console.log(`PASS: ${label}`);
    }
  });
});
