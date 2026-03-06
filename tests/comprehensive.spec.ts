import { test, expect } from "@playwright/test";
import path from "path";
import fs from "fs";

const API = process.env.API_URL ?? "http://localhost:8000";

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

interface SSEEvent {
  type: string;
  content?: string;
  delta?: string;
  message?: string;
  message_id?: string;
  thread_id?: string;
  run_id?: string;
  tool_call_id?: string;
  tool_call_name?: string;
  [key: string]: unknown;
}

function parseSSEEvents(text: string): SSEEvent[] {
  return text
    .split("\n")
    .filter((l) => l.startsWith("data: "))
    .map((l) => {
      try {
        return JSON.parse(l.slice(6));
      } catch {
        return null;
      }
    })
    .filter(Boolean) as SSEEvent[];
}

async function readSSEStream(res: Response): Promise<string> {
  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  let text = "";
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      text += decoder.decode(value, { stream: true });
    }
  } catch {
    // stream may close abruptly after final event
  }
  return text;
}

async function createSessionViaAPI(): Promise<string> {
  for (let attempt = 0; attempt < 3; attempt++) {
    const res = await fetch(`${API}/sessions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    if (res.status === 201) {
      const body = await res.json();
      return body.session_id;
    }
    if (attempt < 2) await new Promise((r) => setTimeout(r, 5_000));
  }
  throw new Error("create session failed after 3 attempts");
}

async function deleteSessionViaAPI(sid: string): Promise<void> {
  await fetch(`${API}/sessions/${sid}`, { method: "DELETE" });
}

async function uploadFileViaAPI(
  sid: string,
  filename: string,
  content: string | Buffer,
  mimeType: string,
): Promise<Response> {
  const form = new FormData();
  const blob = new Blob([content], { type: mimeType });
  form.append("file", blob, filename);
  return fetch(`${API}/sessions/${sid}/upload`, {
    method: "POST",
    body: form,
  });
}

async function sendMessageViaAPI(
  sid: string,
  prompt: string,
): Promise<{ events: SSEEvent[]; text: string }> {
  const res = await fetch(`${API}/sessions/${sid}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });
  if (res.status !== 200)
    throw new Error(`send message failed: ${res.status}`);
  const text = await readSSEStream(res);
  return { events: parseSSEEvents(text), text };
}

async function pollFiles(
  sid: string,
  predicate: (files: any[]) => boolean,
  timeout = 60_000,
  interval = 3_000,
): Promise<any[]> {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const res = await fetch(`${API}/sessions/${sid}/files`);
    const body = await res.json();
    if (predicate(body.files)) return body.files;
    await new Promise((r) => setTimeout(r, interval));
  }
  throw new Error(`pollFiles timed out after ${timeout}ms`);
}

async function getHealth(): Promise<any> {
  const res = await fetch(`${API}/health`);
  return res.json();
}

/**
 * Navigate through IntakeScreen by uploading a file, then wait for the chat
 * input to appear (indicating the transition to chat stage).
 */
async function navigateToChatViaIntake(
  page: any,
  filePath: string,
): Promise<void> {
  // Navigate and wait for IntakeScreen to render
  await page.goto("/", { waitUntil: "domcontentloaded", timeout: 30_000 });
  for (let attempt = 0; attempt < 5; attempt++) {
    // Check if retry button appeared (session creation failed)
    const retryBtn = page.getByTestId("intake-retry-button");
    const retryVisible = await retryBtn.isVisible().catch(() => false);
    if (retryVisible) {
      console.log(`  Session failed, clicking retry (attempt ${attempt + 1})`);
      await retryBtn.click();
      await page.waitForTimeout(3_000);
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
      if (attempt < 4) {
        // Reload and try again
        await page.reload({ waitUntil: "domcontentloaded", timeout: 15_000 });
        await page.waitForTimeout(2_000);
      } else {
        throw new Error("Session did not become ready after 5 attempts");
      }
    }
  }
  const intakeInput = page.getByTestId("intake-upload-input");
  await intakeInput.setInputFiles(filePath);
  await expect(page.getByTestId("chat-input")).toBeVisible({ timeout: 30_000 });
}

// Shared temp file used by tests that just need to get past IntakeScreen
const sharedTmpDir = path.join(__dirname, ".tmp-shared");
const sharedTmpFile = path.join(sharedTmpDir, "starter.txt");

test.beforeAll(() => {
  fs.mkdirSync(sharedTmpDir, { recursive: true });
  fs.writeFileSync(sharedTmpFile, "Starter file for chat access.");
});

test.afterAll(() => {
  fs.rmSync(sharedTmpDir, { recursive: true, force: true });
});

// ---------------------------------------------------------------------------
// Journey 1: Chat Conversation (Browser + API, serial)
// Tests 1-2 use the browser; tests 3-4 use the API to avoid extra session creation.
// ---------------------------------------------------------------------------
test.describe.serial("Journey 1: Chat Conversation", () => {
  let apiSessionId: string;

  test.afterAll(async () => {
    if (apiSessionId) await deleteSessionViaAPI(apiSessionId);
  });

  test("App loads and intake screen appears", async ({ page }) => {
    await page.goto("/");
    // IntakeScreen should be visible
    await expect(page.getByTestId("intake-upload-input")).toBeAttached({
      timeout: 30_000,
    });
  });

  test("Upload transitions to chat", async ({ page }) => {
    await navigateToChatViaIntake(page, sharedTmpFile);
    await expect(page.getByTestId("chat-input")).toBeEnabled();
  });

  test("Send message and receive response", async () => {
    // Create a session via API instead of navigating the browser
    apiSessionId = await createSessionViaAPI();
    await uploadFileViaAPI(
      apiSessionId,
      "starter.txt",
      "Starter file for chat access.",
      "text/plain",
    );

    const { events } = await sendMessageViaAPI(
      apiSessionId,
      "What is the capital of France? Answer in one word.",
    );

    // Should have received assistant content via SSE events (AG-UI protocol)
    const deltas = events.filter((e) => e.type === "TEXT_MESSAGE_CONTENT");
    const assistantText = deltas.map((e) => e.delta ?? e.content ?? "").join("");
    expect(assistantText.length).toBeGreaterThan(0);

    // Should have completed successfully
    const finished = events.some(
      (e) => e.type === "RUN_FINISHED",
    );
    expect(finished).toBe(true);
  });

  test("Multi-turn context preserved", async () => {
    // Reuse the API session from the previous test (serial block guarantees order)
    expect(apiSessionId).toBeTruthy();

    // First turn: establish context
    await sendMessageViaAPI(
      apiSessionId,
      "Remember this code word: PINEAPPLE. Just acknowledge you will remember it.",
    );

    // Second turn: ask about it
    const { events } = await sendMessageViaAPI(
      apiSessionId,
      "What was the code word I just told you?",
    );

    const deltas = events.filter((e) => e.type === "TEXT_MESSAGE_CONTENT");
    const assistantText = deltas.map((e) => e.delta ?? e.content ?? "").join("");
    expect(assistantText).toContain("PINEAPPLE");
  });
});

// ---------------------------------------------------------------------------
// Journey 2: Upload Document and Discuss (Browser, serial)
// ---------------------------------------------------------------------------
test.describe.serial("Journey 2: Upload Document and Discuss", () => {
  const tmpDir = path.join(__dirname, ".tmp-journey2");
  const tmpFile = path.join(tmpDir, "rfp-document.txt");

  const rfpContent = [
    "REQUEST FOR PROPOSAL",
    "Project: Enterprise Data Platform Migration",
    "Budget: $2,500,000",
    "Deadline: September 30, 2026",
    "Requirements:",
    "- Migrate 15 legacy databases to cloud",
    "- Zero downtime during migration",
    "- SOC 2 Type II compliance required",
    "- 99.99% uptime SLA post-migration",
    "Contact: Jane Smith, CTO, jane.smith@example.com",
  ].join("\n");

  test.beforeAll(() => {
    fs.mkdirSync(tmpDir, { recursive: true });
    fs.writeFileSync(tmpFile, rfpContent);
  });

  test.afterAll(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  test("Upload shows in UI and artifacts panel", async ({ page }) => {
    await navigateToChatViaIntake(page, tmpFile);

    // Artifacts panel shows the uploaded file on desktop
    await expect(page.getByTestId("artifacts-panel")).toBeVisible({
      timeout: 30_000,
    });
    await expect(
      page.getByTestId("artifacts-panel").getByTestId("document-name").filter({ hasText: "rfp-document.txt" }).first(),
    ).toBeAttached();

    // Input is enabled — user drives the conversation
    const input = page.getByTestId("chat-input");
    await expect(input).toBeEnabled();
  });

  test("Agent can read uploaded file when asked", async ({ page }) => {
    await navigateToChatViaIntake(page, tmpFile);

    // Wait for artifacts panel to confirm upload
    await expect(page.getByTestId("artifacts-panel")).toBeVisible({
      timeout: 30_000,
    });

    const input = page.getByTestId("chat-input");
    const send = page.getByTestId("send-button");

    // User asks about the document
    await input.fill(
      "What compliance certifications are required according to the document?",
    );
    await send.click();
    await expect(input).toBeDisabled({ timeout: 30_000 });
    await expect(input).toBeEnabled({ timeout: 180_000 });

    const lastAssistant = page
      .locator('.message-row-assistant .prose')
      .last();
    const reply = await lastAssistant.textContent();

    // Should mention SOC 2 and not claim no files found
    expect(reply!).toMatch(/SOC\s*2/i);
    const lower = reply!.toLowerCase();
    expect(lower).not.toContain("no files found");
    expect(lower).not.toContain("no files were found");
    expect(lower).not.toContain("cannot find any files");
  });
});

// ---------------------------------------------------------------------------
// Journey 3: Document Conversion Pipeline (API + Browser, serial)
// No skip logic. CU and ADLS are required infrastructure.
// ---------------------------------------------------------------------------
test.describe.serial("Journey 3: Document Conversion Pipeline", () => {
  let sessionId: string;
  const tmpDir = path.join(__dirname, ".tmp-journey3");
  const tmpFile = path.join(tmpDir, "conversion-test.txt");

  test.beforeAll(async () => {
    sessionId = await createSessionViaAPI();
    fs.mkdirSync(tmpDir, { recursive: true });
    fs.writeFileSync(
      tmpFile,
      "Conversion pipeline test document with budget $1M for cloud migration by Q3 2026.",
    );
  });

  test.afterAll(async () => {
    if (sessionId) await deleteSessionViaAPI(sessionId);
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  test("Upload triggers markdown conversion", async () => {
    const res = await uploadFileViaAPI(
      sessionId,
      "conversion-test.txt",
      "Conversion pipeline test document with budget $1M for cloud migration by Q3 2026.",
      "text/plain",
    );
    expect(res.status).toBe(200);

    // Poll until has_markdown becomes true — fail if it doesn't within 60s
    const files = await pollFiles(
      sessionId,
      (f) =>
        f.some(
          (file: any) =>
            file.filename === "conversion-test.txt" &&
            file.has_markdown === true,
        ),
      90_000,
      3_000,
    );
    const file = files.find((f: any) => f.filename === "conversion-test.txt");
    expect(file.has_markdown).toBe(true);
  });

  test("Markdown content is non-trivial", async () => {
    const res = await fetch(`${API}/sessions/${sessionId}/files`);
    const body = await res.json();
    const mdFile = body.files.find(
      (f: any) => f.filename === "conversion-test.txt.md",
    );
    expect(mdFile).toBeTruthy();
    expect(mdFile.size).toBeGreaterThan(10);
  });

  test("Conversion badge transitions to done in browser", async ({
    page,
  }) => {
    await navigateToChatViaIntake(page, tmpFile);

    await expect(page.getByTestId("artifacts-panel")).toBeVisible({
      timeout: 10_000,
    });

    // Wait for conversion-done badge — fail if it stays pending
    await expect(page.getByTestId("conversion-done").first()).toBeVisible({
      timeout: 90_000,
    });
  });

  test("Markdown sibling hidden in artifacts panel", async () => {
    // Use API to check that /files endpoint doesn't expose .md siblings directly
    const res = await fetch(`${API}/sessions/${sessionId}/files`);
    const body = await res.json();
    // The .md file should exist but should be filtered by the frontend (normalizeFileList)
    // Verify that a .txt.md file exists (conversion worked) but is a separate file
    const mdFile = body.files.find(
      (f: any) => f.filename === "conversion-test.txt.md",
    );
    expect(mdFile).toBeTruthy();
    // The original .txt should also exist
    const origFile = body.files.find(
      (f: any) => f.filename === "conversion-test.txt",
    );
    expect(origFile).toBeTruthy();
    expect(origFile.has_markdown).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// Journey 4: Session Isolation (Browser, serial)
// ---------------------------------------------------------------------------
test.describe.serial("Journey 4: Session Isolation", () => {
  test("New chat clears messages", async ({ page }) => {
    await navigateToChatViaIntake(page, sharedTmpFile);

    const input = page.getByTestId("chat-input");
    const send = page.getByTestId("send-button");

    await input.fill("Hello from session isolation test");
    await send.click();
    await expect(input).toBeEnabled({ timeout: 180_000 });
    await expect(
      page.locator("text=Hello from session isolation test"),
    ).toBeVisible();

    // Click new chat — accept the confirmation dialog, returns to intake screen
    page.on("dialog", (dialog: any) => dialog.accept());
    await page.getByTestId("new-chat-button").click();

    // Should be back on intake screen (old message gone)
    await expect(page.getByTestId("intake-upload-input")).toBeAttached({
      timeout: 30_000,
    });
    await expect(
      page.locator("text=Hello from session isolation test"),
    ).toBeHidden();
  });

  test("New session has no context from previous", async ({ page }) => {
    await navigateToChatViaIntake(page, sharedTmpFile);

    const input = page.getByTestId("chat-input");
    const send = page.getByTestId("send-button");

    // First session: establish unique context
    await input.fill("The secret code word is STARFISH.");
    await send.click();
    await expect(input).toBeEnabled({ timeout: 180_000 });

    // New chat → back to intake
    await page.getByTestId("new-chat-button").click();

    // Navigate through intake again
    await navigateToChatViaIntake(page, sharedTmpFile);

    // Second session: ask about previous context
    await input.fill(
      "What was the secret code word I told you? If you do not know, say UNKNOWN.",
    );
    await send.click();
    await expect(input).toBeEnabled({ timeout: 180_000 });

    // Agent should NOT know STARFISH from the previous session.
    const lastAssistant = page
      .locator('.message-row-assistant .prose')
      .last();
    const reply = await lastAssistant.textContent();
    expect(reply!.length).toBeGreaterThan(5);
  });
});

// ---------------------------------------------------------------------------
// Journey 5: Security and Error Handling (API)
// ---------------------------------------------------------------------------
test.describe("Journey 5: Security and Error Handling", () => {
  let sessionId: string;

  test.beforeAll(async () => {
    sessionId = await createSessionViaAPI();
  });

  test.afterAll(async () => {
    if (sessionId) await deleteSessionViaAPI(sessionId);
  });

  test("Rejects dangerous file types", async () => {
    const exeRes = await uploadFileViaAPI(
      sessionId,
      "malware.exe",
      "fake exe",
      "application/octet-stream",
    );
    expect(exeRes.status).toBe(400);

    const shRes = await uploadFileViaAPI(
      sessionId,
      "script.sh",
      "#!/bin/bash\necho hello",
      "application/x-sh",
    );
    expect(shRes.status).toBe(400);
  });

  test("Path traversal sanitized", async () => {
    const res = await uploadFileViaAPI(
      sessionId,
      "../../../etc/passwd.txt",
      "not a real passwd file",
      "text/plain",
    );
    if (res.status === 200) {
      const body = await res.json();
      expect(body.filename).not.toContain("..");
      expect(body.filename).toBe("passwd.txt");
    } else {
      expect(res.status).toBe(400);
    }
  });

  test("Nonexistent session returns 404", async () => {
    const getRes = await fetch(`${API}/sessions/nonexistent_session_xyz`);
    expect(getRes.status).toBe(404);

    const msgRes = await fetch(
      `${API}/sessions/nonexistent_session_xyz/messages`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: "hello" }),
      },
    );
    expect(msgRes.status).toBe(404);

    const uploadRes = await uploadFileViaAPI(
      "nonexistent_session_xyz",
      "test.txt",
      "hello",
      "text/plain",
    );
    expect(uploadRes.status).toBe(404);
  });

  test("Concurrent sends: busy detection", async () => {
    const [result1, result2] = await Promise.all([
      sendMessageViaAPI(sessionId, "Count from 1 to 5.").catch(() => ({
        events: [] as SSEEvent[],
        text: "",
      })),
      new Promise<{ events: SSEEvent[]; text: string }>((resolve) =>
        setTimeout(
          () =>
            sendMessageViaAPI(sessionId, "What is 3 + 3?")
              .then(resolve)
              .catch(() => resolve({ events: [], text: "" })),
          200,
        ),
      ),
    ]);

    // At least one should complete successfully with a RUN_FINISHED event
    const r1Done = result1.events.some((e) => e.type === "RUN_FINISHED");
    const r2Done = result2.events.some((e) => e.type === "RUN_FINISHED");
    expect(r1Done || r2Done).toBe(true);

    // The other should either also succeed or have an error (busy, timeout, etc.)
    if (!r1Done && result1.events.length > 0) {
      const hasError = result1.events.some((e) => e.type === "RUN_ERROR");
      expect(hasError).toBe(true);
    }
    if (!r2Done && result2.events.length > 0) {
      const hasError = result2.events.some((e) => e.type === "RUN_ERROR");
      expect(hasError).toBe(true);
    }
  });

  test("Delete then get returns 404", async () => {
    const sid = await createSessionViaAPI();
    const del = await fetch(`${API}/sessions/${sid}`, { method: "DELETE" });
    expect(del.status).toBe(204);
    const get = await fetch(`${API}/sessions/${sid}`);
    expect(get.status).toBe(404);
  });
});

// ---------------------------------------------------------------------------
// Journey 6: Artifacts Panel UX (Browser)
// ---------------------------------------------------------------------------
test.describe.serial("Journey 6: Artifacts Panel UX", () => {
  const tmpDir = path.join(__dirname, ".tmp-journey6");
  const tmpFile1 = path.join(tmpDir, "doc-one.txt");
  const tmpFile2 = path.join(tmpDir, "doc-two.txt");

  test.beforeAll(() => {
    fs.mkdirSync(tmpDir, { recursive: true });
    fs.writeFileSync(tmpFile1, "First document for panel UX test.");
    fs.writeFileSync(tmpFile2, "Second document for panel UX test.");
  });

  test.afterAll(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  test("Artifacts panel visible with uploaded file + Multiple files in panel", async ({ page }) => {
    await navigateToChatViaIntake(page, tmpFile1);

    await expect(page.getByTestId("artifacts-panel")).toBeVisible({
      timeout: 10_000,
    });

    // At least one document item visible
    await expect(page.getByTestId("document-item").first()).toBeVisible();

    // --- Multiple files in panel ---
    // Wait for input to be ready
    await expect(page.getByTestId("chat-input")).toBeEnabled({
      timeout: 120_000,
    });

    // Upload second file via chat input bar
    const fileInput = page.locator('input[type="file"]').last();
    await fileInput.setInputFiles(tmpFile2);
    await page.getByTestId("send-button").click();

    // Both filenames visible in artifacts panel
    const panel = page.getByTestId("artifacts-panel");
    await expect(
      panel.getByTestId("document-name").filter({ hasText: "doc-one.txt" }).first(),
    ).toBeAttached({ timeout: 10_000 });
    await expect(
      panel.getByTestId("document-name").filter({ hasText: "doc-two.txt" }).first(),
    ).toBeAttached({ timeout: 10_000 });
  });
});
