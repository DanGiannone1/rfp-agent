import fs from "fs";
import path from "path";

const RUN_ID_KEY = "__rfp_e2e_run_id";

function generateRunId() {
  return `run-${new Date().toISOString().replace(/[:.]/g, "-")}`;
}

const g = globalThis as typeof globalThis & { [RUN_ID_KEY]?: string };

export const E2E_SCREENSHOT_RUN_ID =
  process.env.E2E_SCREENSHOT_RUN_ID ??
  (g[RUN_ID_KEY] ?? (g[RUN_ID_KEY] = generateRunId()));

export const SCREENSHOT_ROOT = path.join(process.cwd(), "screenshots");
export const SCREENSHOT_DIR = path.join(SCREENSHOT_ROOT, E2E_SCREENSHOT_RUN_ID);

export function ensureScreenshotDir() {
  if (!fs.existsSync(SCREENSHOT_ROOT)) {
    fs.mkdirSync(SCREENSHOT_ROOT, { recursive: true });
  }
  if (!fs.existsSync(SCREENSHOT_DIR)) {
    fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
  }
}

export function getScreenshotPath(fileName: string) {
  ensureScreenshotDir();
  return path.join(SCREENSHOT_DIR, fileName);
}
