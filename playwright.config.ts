import { defineConfig } from "@playwright/test";

const APP_URL = process.env.APP_URL ?? "http://localhost:3000";

export default defineConfig({
  testDir: "./tests",
  timeout: 180_000, // LLM responses + tool execution can be slow
  expect: { timeout: 60_000 },
  retries: 0,
  workers: 1, // sequential — shared backend state

  projects: [
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
