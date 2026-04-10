import { defineConfig } from "@playwright/test";

const APP_URL = process.env.APP_URL ?? "http://localhost:3000";
if (!process.env.E2E_SCREENSHOT_RUN_ID) {
  process.env.E2E_SCREENSHOT_RUN_ID = `run-${new Date().toISOString().replace(/[:.]/g, "-")}`;
}

export default defineConfig({
  testDir: "./tests",
  timeout: 180_000, // LLM responses + tool execution can be slow
  expect: { timeout: 60_000 },
  retries: 0,
  workers: 1, // sequential — shared backend state

  projects: [
    // visual and debug run first — they need few sessions and are sensitive
    // to pool exhaustion. comprehensive runs last and cleans up API sessions.
    {
      name: "visual",
      testMatch: "visual-verification.spec.ts",
      use: {
        baseURL: APP_URL,
        browserName: "chromium",
        headless: true,
        viewport: { width: 1440, height: 900 },
      },
    },
    {
      name: "debug",
      testMatch: "artifact_debug.spec.ts",
      use: {
        baseURL: APP_URL,
        browserName: "chromium",
        headless: true,
        viewport: { width: 1440, height: 900 },
      },
    },
    {
      name: "starter-prompts",
      testMatch: "starter-prompts-ui.spec.ts",
      use: {
        baseURL: APP_URL,
        browserName: "chromium",
        headless: true,
        viewport: { width: 1440, height: 900 },
      },
    },
    {
      name: "comprehensive",
      testMatch: "comprehensive.spec.ts",
      use: {
        baseURL: APP_URL,
        browserName: "chromium",
        headless: true,
        viewport: { width: 1280, height: 720 },
      },
    },
  ],
});
