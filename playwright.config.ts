import { defineConfig } from "@playwright/test";

const API_URL = process.env.API_URL ?? "http://localhost:8000";
const APP_URL = process.env.APP_URL ?? "http://localhost:3000";

export default defineConfig({
  testDir: "./tests",
  timeout: 120_000, // LLM responses can be slow
  expect: { timeout: 60_000 },
  retries: 0,
  workers: 1, // sequential — shared backend state

  projects: [
    {
      name: "api",
      testMatch: "api.spec.ts",
      use: { baseURL: API_URL },
    },
    {
      name: "e2e",
      testMatch: "e2e.spec.ts",
      use: {
        baseURL: APP_URL,
        browserName: "chromium",
        headless: true,
        viewport: { width: 1280, height: 720 },
      },
    },
  ],
});
