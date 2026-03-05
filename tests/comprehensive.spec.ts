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
  status?: string;
  message?: string;
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
  const res = await fetch(`${API}/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({}),
  });
  if (res.status !== 201)
    throw new Error(`create session failed: ${res.status}`);
  const body = await res.json();
  return body.session_id;
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

// ---------------------------------------------------------------------------
// 1. Session Lifecycle (API)
// ---------------------------------------------------------------------------
test.describe("Session Lifecycle", () => {
  test("create session returns valid structure", async () => {
    const res = await fetch(`${API}/sessions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    expect(res.status).toBe(201);
    const body = await res.json();
    expect(body).toHaveProperty("session_id");
    expect(body.status).toBe("active");
    expect(body).toHaveProperty("created_at");
    expect(body).toHaveProperty("last_activity_at");
    // cleanup
    await deleteSessionViaAPI(body.session_id);
  });

  test("get session returns messages array", async () => {
    const sid = await createSessionViaAPI();
    const res = await fetch(`${API}/sessions/${sid}`);
    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.session_id).toBe(sid);
    expect(Array.isArray(body.messages)).toBe(true);
    await deleteSessionViaAPI(sid);
  });

  test("delete session then get returns 404", async () => {
    const sid = await createSessionViaAPI();
    const del = await fetch(`${API}/sessions/${sid}`, { method: "DELETE" });
    expect(del.status).toBe(204);
    const get = await fetch(`${API}/sessions/${sid}`);
    expect(get.status).toBe(404);
  });

  test("get nonexistent session returns 404", async () => {
    const res = await fetch(`${API}/sessions/nonexistent_session_xyz`);
    expect(res.status).toBe(404);
  });

  test("delete nonexistent session returns 404 or 204", async () => {
    const res = await fetch(`${API}/sessions/nonexistent_session_xyz`, {
      method: "DELETE",
    });
    // Without Cosmos, delete always returns 204; with Cosmos, returns 404
    expect([204, 404]).toContain(res.status);
  });
});

// ---------------------------------------------------------------------------
// 2. File Upload & Listing (API)
// ---------------------------------------------------------------------------
test.describe.serial("File Upload & Listing", () => {
  let sessionId: string;

  test.beforeAll(async () => {
    sessionId = await createSessionViaAPI();
  });

  test.afterAll(async () => {
    if (sessionId) await deleteSessionViaAPI(sessionId);
  });

  test("upload .txt returns valid response", async () => {
    const res = await uploadFileViaAPI(
      sessionId,
      "requirements.txt",
      "Budget: $500,000\nDeadline: March 2026\nScope: Full system replacement",
      "text/plain",
    );
    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.filename).toBe("requirements.txt");
    expect(body.size).toBeGreaterThan(0);
    expect(body).toHaveProperty("path");
  });

  test("file listing includes uploaded file with correct fields", async () => {
    const res = await fetch(`${API}/sessions/${sessionId}/files`);
    expect(res.status).toBe(200);
    const body = await res.json();
    const file = body.files.find(
      (f: any) => f.filename === "requirements.txt",
    );
    expect(file).toBeTruthy();
    expect(file.size).toBeGreaterThan(0);
    expect(file).toHaveProperty("modified_at");
    expect(file).toHaveProperty("has_markdown");
  });

  test("upload .csv and listing shows both files", async () => {
    const csv = "Name,Value\nItem1,100\nItem2,200";
    const res = await uploadFileViaAPI(sessionId, "data.csv", csv, "text/csv");
    expect(res.status).toBe(200);

    const list = await fetch(`${API}/sessions/${sessionId}/files`);
    const body = await list.json();
    const filenames = body.files.map((f: any) => f.filename);
    expect(filenames).toContain("requirements.txt");
    expect(filenames).toContain("data.csv");
  });

  test("reject .exe upload", async () => {
    const res = await uploadFileViaAPI(
      sessionId,
      "malware.exe",
      "fake exe",
      "application/octet-stream",
    );
    expect(res.status).toBe(400);
  });

  test("reject .sh upload", async () => {
    const res = await uploadFileViaAPI(
      sessionId,
      "script.sh",
      "#!/bin/bash\necho hello",
      "application/x-sh",
    );
    expect(res.status).toBe(400);
  });

  test("upload to nonexistent session returns 404", async () => {
    const res = await uploadFileViaAPI(
      "nonexistent_session_xyz",
      "test.txt",
      "hello",
      "text/plain",
    );
    expect(res.status).toBe(404);
  });

  test("list files on nonexistent session returns 404", async () => {
    const res = await fetch(
      `${API}/sessions/nonexistent_session_xyz/files`,
    );
    expect(res.status).toBe(404);
  });
});

// ---------------------------------------------------------------------------
// 3. Content Understanding Conversion (API) — skip if CU disabled
// ---------------------------------------------------------------------------
test.describe.serial("Content Understanding Conversion", () => {
  let sessionId: string;
  let cuEnabled = false;

  test.beforeAll(async () => {
    const health = await getHealth();
    cuEnabled = health.content_processing_enabled === true;
    if (cuEnabled) {
      sessionId = await createSessionViaAPI();
    }
  });

  test.afterAll(async () => {
    if (sessionId) await deleteSessionViaAPI(sessionId);
  });

  test("upload file and poll until has_markdown is true", async () => {
    test.skip(!cuEnabled, "Content Understanding not enabled");
    const res = await uploadFileViaAPI(
      sessionId,
      "proposal.txt",
      "This is a test proposal document with detailed budget information and project scope.",
      "text/plain",
    );
    expect(res.status).toBe(200);

    const files = await pollFiles(
      sessionId,
      (f) =>
        f.some(
          (file: any) =>
            file.filename === "proposal.txt" && file.has_markdown === true,
        ),
      60_000,
      3_000,
    );
    const file = files.find((f: any) => f.filename === "proposal.txt");
    expect(file.has_markdown).toBe(true);
  });

  test("markdown sibling exists in listing with size > 0", async () => {
    test.skip(!cuEnabled, "Content Understanding not enabled");
    const res = await fetch(`${API}/sessions/${sessionId}/files`);
    const body = await res.json();
    const mdFile = body.files.find(
      (f: any) => f.filename === "proposal.txt.md",
    );
    expect(mdFile).toBeTruthy();
    expect(mdFile.size).toBeGreaterThan(0);
  });

  test("markdown content is non-trivial", async () => {
    test.skip(!cuEnabled, "Content Understanding not enabled");
    const res = await fetch(`${API}/sessions/${sessionId}/files`);
    const body = await res.json();
    const mdFile = body.files.find(
      (f: any) => f.filename === "proposal.txt.md",
    );
    expect(mdFile.size).toBeGreaterThan(10);
  });
});

// ---------------------------------------------------------------------------
// 4. SSE Message Streaming (API)
// ---------------------------------------------------------------------------
test.describe("SSE Message Streaming", () => {
  let sessionId: string;

  test.beforeAll(async () => {
    sessionId = await createSessionViaAPI();
  });

  test.afterAll(async () => {
    if (sessionId) await deleteSessionViaAPI(sessionId);
  });

  test("send message returns well-formed SSE stream ending with done", async () => {
    const { events, text } = await sendMessageViaAPI(
      sessionId,
      "What is 2 + 2? Answer in one sentence.",
    );

    // Stream contains data: lines
    expect(text).toContain("data: ");

    // Events have type field
    expect(events.length).toBeGreaterThan(0);
    for (const e of events) {
      expect(typeof e.type).toBe("string");
    }

    // Ends with done event
    expect(events[events.length - 1].type).toBe("done");

    // Has a message event with non-empty content
    const messageEvent = events.find((e) => e.type === "message");
    expect(messageEvent).toBeTruthy();
    expect(messageEvent!.content!.length).toBeGreaterThan(0);
  });

  test("no status events appear after message event", async () => {
    const { events } = await sendMessageViaAPI(
      sessionId,
      "Say hello briefly.",
    );
    const messageIdx = events.findIndex((e) => e.type === "message");
    if (messageIdx >= 0) {
      const afterMessage = events.slice(messageIdx + 1);
      const statusAfter = afterMessage.filter((e) => e.type === "status");
      expect(statusAfter.length).toBe(0);
    }
  });

  test("multi-turn context is preserved across messages", async () => {
    // First turn: establish context
    await sendMessageViaAPI(
      sessionId,
      "Remember this code word: PINEAPPLE. Just acknowledge you will remember it.",
    );

    // Second turn: ask about it
    const { events } = await sendMessageViaAPI(
      sessionId,
      "What was the code word I just told you?",
    );
    const messageEvent = events.find((e) => e.type === "message");
    expect(messageEvent).toBeTruthy();
    expect(messageEvent!.content!.length).toBeGreaterThan(5);
    expect(messageEvent!.content!.toUpperCase()).toContain("PINEAPPLE");
  });

  test("send to nonexistent session returns 404", async () => {
    const res = await fetch(
      `${API}/sessions/nonexistent_session_xyz/messages`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: "hello" }),
      },
    );
    expect(res.status).toBe(404);
  });
});

// ---------------------------------------------------------------------------
// 5. Agent + Uploaded Files (API)
// ---------------------------------------------------------------------------
test.describe("Agent + Uploaded Files", () => {
  let sessionId: string;

  test.beforeAll(async () => {
    sessionId = await createSessionViaAPI();

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
    const res = await uploadFileViaAPI(
      sessionId,
      "rfp-document.txt",
      rfpContent,
      "text/plain",
    );
    expect(res.status).toBe(200);
  });

  test.afterAll(async () => {
    if (sessionId) await deleteSessionViaAPI(sessionId);
  });

  test("agent references specific details from uploaded document", async () => {
    const { events } = await sendMessageViaAPI(
      sessionId,
      "Read the rfp-document.txt file in the workspace and tell me the budget and deadline mentioned in it.",
    );
    const msg = events.find((e) => e.type === "message");
    expect(msg).toBeTruthy();
    const content = msg!.content!;
    expect(content.length).toBeGreaterThan(50);

    // Agent should reference at least one specific detail from the file
    const mentionsBudget =
      content.includes("2,500,000") ||
      content.includes("2.5") ||
      content.includes("$2.5M");
    const mentionsDeadline =
      content.includes("September") || content.includes("2026");
    expect(mentionsBudget || mentionsDeadline).toBe(true);
  });

  test("agent summarizes uploaded file without claiming no files exist", async () => {
    const { events } = await sendMessageViaAPI(
      sessionId,
      "Summarize the key requirements from rfp-document.txt.",
    );
    const msg = events.find((e) => e.type === "message");
    expect(msg).toBeTruthy();
    const content = msg!.content!;
    expect(content.length).toBeGreaterThan(50);

    // Should not claim no files exist
    const lower = content.toLowerCase();
    const claimsNoFiles =
      lower.includes("no files found") ||
      lower.includes("no files were found") ||
      lower.includes("cannot find any files");
    expect(claimsNoFiles).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// 6. Health Endpoint (API)
// ---------------------------------------------------------------------------
test.describe("Health Endpoint", () => {
  test("returns all required fields with correct types", async () => {
    const health = await getHealth();
    expect(health.status).toBe("ok");
    expect(typeof health.active_sessions).toBe("number");
    expect(typeof health.cosmos_connected).toBe("boolean");
    expect(typeof health.content_processing_enabled).toBe("boolean");
    expect(health).toHaveProperty("timestamp");
  });
});

// ---------------------------------------------------------------------------
// 7. Browser Chat Flow (E2E)
// ---------------------------------------------------------------------------
test.describe("Browser Chat Flow", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTestId("chat-input")).toBeVisible({
      timeout: 30_000,
    });
  });

  test("page loads with empty state and input enabled", async ({ page }) => {
    const input = page.getByTestId("chat-input");
    await expect(input).toBeEnabled();
    // No initializing spinner visible
    await expect(page.getByTestId("initializing")).toBeHidden();
  });

  test("send message and receive non-empty assistant response", async ({
    page,
  }) => {
    const input = page.getByTestId("chat-input");
    const send = page.getByTestId("send-button");

    await input.fill("What is the capital of France? Answer in one word.");
    await send.click();

    // User message appears
    await expect(
      page.locator("text=What is the capital of France"),
    ).toBeVisible();

    // Wait for streaming to finish
    await expect(input).toBeEnabled({ timeout: 120_000 });

    // Page should contain substantive response
    const body = await page.locator("body").textContent();
    expect(body!.length).toBeGreaterThan(50);
  });

  test("multi-turn conversation preserves context", async ({ page }) => {
    const input = page.getByTestId("chat-input");
    const send = page.getByTestId("send-button");

    await input.fill("Remember the number 7777.");
    await send.click();
    await expect(input).toBeEnabled({ timeout: 120_000 });

    await input.fill("What number did I just ask you to remember?");
    await send.click();
    await expect(input).toBeEnabled({ timeout: 120_000 });

    await expect(page.locator("body")).toContainText("7777");
  });
});

// ---------------------------------------------------------------------------
// 8. Browser File Upload (E2E)
// ---------------------------------------------------------------------------
test.describe("Browser File Upload", () => {
  const tmpDir = path.join(__dirname, ".tmp-comprehensive");
  const tmpFile = path.join(tmpDir, "test-upload.txt");

  test.beforeAll(() => {
    fs.mkdirSync(tmpDir, { recursive: true });
    fs.writeFileSync(tmpFile, "Test document content for comprehensive suite.");
  });

  test.afterAll(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTestId("chat-input")).toBeVisible({
      timeout: 30_000,
    });
  });

  test("upload shows chip, sends, and document panel appears with filename", async ({
    page,
  }) => {
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(tmpFile);

    // File chip in input bar
    await expect(
      page.locator("form").getByText("test-upload.txt"),
    ).toBeVisible();

    const send = page.getByTestId("send-button");
    await send.click();

    // Uploaded message appears
    await expect(page.locator("text=Uploaded")).toBeVisible({
      timeout: 30_000,
    });

    // Document panel with filename (use filter — shared workspace may have other files)
    await expect(page.getByTestId("document-panel")).toBeVisible({
      timeout: 10_000,
    });
    await expect(
      page.getByTestId("document-name").getByText("test-upload.txt"),
    ).toBeVisible();
  });

  test("conversion badge exists (done or pending)", async ({ page }) => {
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(tmpFile);
    await page.getByTestId("send-button").click();

    await expect(page.getByTestId("document-panel")).toBeVisible({
      timeout: 10_000,
    });

    // Either conversion-done or conversion-pending badge should exist
    const done = page.getByTestId("conversion-done");
    const pending = page.getByTestId("conversion-pending");
    const hasBadge = (await done.count()) > 0 || (await pending.count()) > 0;
    expect(hasBadge).toBe(true);
  });

  test("toggle collapse hides items, re-expand shows them", async ({
    page,
  }) => {
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(tmpFile);
    await page.getByTestId("send-button").click();

    await expect(page.getByTestId("document-panel")).toBeVisible({
      timeout: 10_000,
    });

    const toggle = page.getByTestId("document-panel-toggle");

    // Collapse
    await toggle.click();
    await expect(page.getByTestId("document-item").first()).toBeHidden();

    // Re-expand
    await toggle.click();
    await expect(page.getByTestId("document-item").first()).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// 9. CU in Document Panel (E2E) — skip if CU disabled
// ---------------------------------------------------------------------------
test.describe("CU in Document Panel", () => {
  let cuEnabled = false;
  const tmpDir = path.join(__dirname, ".tmp-cu-panel");
  const tmpFile = path.join(tmpDir, "cu-panel-test.txt");

  test.beforeAll(async () => {
    const health = await getHealth();
    cuEnabled = health.content_processing_enabled === true;
    if (cuEnabled) {
      fs.mkdirSync(tmpDir, { recursive: true });
      fs.writeFileSync(tmpFile, "Content for CU conversion panel testing.");
    }
  });

  test.afterAll(() => {
    if (fs.existsSync(tmpDir)) {
      fs.rmSync(tmpDir, { recursive: true, force: true });
    }
  });

  test("conversion-pending badge becomes conversion-done", async ({
    page,
  }) => {
    test.skip(!cuEnabled, "Content Understanding not enabled");
    await page.goto("/");
    await expect(page.getByTestId("chat-input")).toBeVisible({
      timeout: 30_000,
    });

    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(tmpFile);
    await page.getByTestId("send-button").click();

    await expect(page.getByTestId("document-panel")).toBeVisible({
      timeout: 10_000,
    });

    // Wait for conversion to complete (DocumentPanel polls every 10s)
    // Use .first() — shared workspace may have multiple converted files
    await expect(page.getByTestId("conversion-done").first()).toBeVisible({
      timeout: 90_000,
    });
  });

  test("markdown sibling is not shown in document panel", async ({
    page,
  }) => {
    test.skip(!cuEnabled, "Content Understanding not enabled");
    await page.goto("/");
    await expect(page.getByTestId("chat-input")).toBeVisible({
      timeout: 30_000,
    });

    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(tmpFile);
    await page.getByTestId("send-button").click();

    await expect(page.getByTestId("document-panel")).toBeVisible({
      timeout: 10_000,
    });

    // Wait for conversion to complete
    await expect(page.getByTestId("conversion-done").first()).toBeVisible({
      timeout: 90_000,
    });

    // The .md sibling should NOT appear in the panel (DocumentPanel filters them)
    const names = page.getByTestId("document-name");
    const count = await names.count();
    for (let i = 0; i < count; i++) {
      const text = await names.nth(i).textContent();
      expect(text).not.toMatch(/\.txt\.md$/);
    }
  });
});

// ---------------------------------------------------------------------------
// 10. New Chat Reset (E2E)
// ---------------------------------------------------------------------------
test.describe("New Chat Reset", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTestId("chat-input")).toBeVisible({
      timeout: 30_000,
    });
  });

  test("new chat clears messages and restores empty state", async ({
    page,
  }) => {
    const input = page.getByTestId("chat-input");
    const send = page.getByTestId("send-button");

    await input.fill("Hello from comprehensive test");
    await send.click();
    await expect(input).toBeEnabled({ timeout: 120_000 });
    await expect(
      page.locator("text=Hello from comprehensive test"),
    ).toBeVisible();

    // Click new chat
    await page.getByTestId("new-chat-button").click();
    await expect(input).toBeVisible({ timeout: 30_000 });

    // Old message should be gone
    await expect(
      page.locator("text=Hello from comprehensive test"),
    ).toBeHidden();
  });

  test("new session has no context from previous session", async ({
    page,
  }) => {
    const input = page.getByTestId("chat-input");
    const send = page.getByTestId("send-button");

    // First session: establish unique context
    await input.fill("The secret code word is STARFISH.");
    await send.click();
    await expect(input).toBeEnabled({ timeout: 120_000 });

    // New chat
    await page.getByTestId("new-chat-button").click();
    await expect(input).toBeVisible({ timeout: 30_000 });

    // Second session: ask about previous context
    await input.fill(
      "What was the secret code word I told you? If you do not know, say UNKNOWN.",
    );
    await send.click();
    await expect(input).toBeEnabled({ timeout: 120_000 });

    // Agent should NOT know STARFISH from the previous session
    // Check only the last assistant message, not the full page (which includes user input text)
    const lastAssistant = page
      .locator('[class*="justify-start"] [class*="prose"]')
      .last();
    const reply = await lastAssistant.textContent();
    expect(reply!.toUpperCase()).not.toContain("STARFISH");
  });
});

// ---------------------------------------------------------------------------
// 11. ADLS + Content Understanding Full Pipeline (API) — skip if CU disabled
// ---------------------------------------------------------------------------
test.describe("ADLS + CU Full Pipeline", () => {
  let cuEnabled = false;
  let sessionId: string;

  test.beforeAll(async () => {
    const health = await getHealth();
    cuEnabled = health.content_processing_enabled === true;
    if (cuEnabled) sessionId = await createSessionViaAPI();
  });

  test.afterAll(async () => {
    if (sessionId) await deleteSessionViaAPI(sessionId);
  });

  test("upload triggers full pipeline: markdown sibling appears in listing", async () => {
    test.skip(!cuEnabled, "Content Understanding not enabled");
    const content =
      "Full pipeline test: budget of $1M for cloud migration by Q3 2026.";
    const res = await uploadFileViaAPI(
      sessionId,
      "pipeline-test.txt",
      content,
      "text/plain",
    );
    expect(res.status).toBe(200);

    // Poll until .md sibling appears
    const files = await pollFiles(
      sessionId,
      (f) => f.some((file: any) => file.filename === "pipeline-test.txt.md"),
      60_000,
      3_000,
    );
    const mdFile = files.find(
      (f: any) => f.filename === "pipeline-test.txt.md",
    );
    expect(mdFile).toBeTruthy();
    expect(mdFile.size).toBeGreaterThan(0);
  });
});

// ---------------------------------------------------------------------------
// 12. Edge Cases (API)
// ---------------------------------------------------------------------------
test.describe("Edge Cases", () => {
  let sessionId: string;

  test.beforeAll(async () => {
    sessionId = await createSessionViaAPI();
  });

  test.afterAll(async () => {
    if (sessionId) await deleteSessionViaAPI(sessionId);
  });

  test("path traversal filename is sanitized or rejected", async () => {
    const res = await uploadFileViaAPI(
      sessionId,
      "../../../etc/passwd.txt",
      "not a real passwd file",
      "text/plain",
    );
    if (res.status === 200) {
      // Server sanitized the filename — should strip path components
      const body = await res.json();
      expect(body.filename).not.toContain("..");
      expect(body.filename).toBe("passwd.txt");
    } else {
      // Server rejected outright
      expect(res.status).toBe(400);
    }
  });

  test("concurrent sends: one succeeds, other gets busy or also succeeds", async () => {
    // Fire two requests nearly simultaneously
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

    // At least one should have completed successfully with a done event
    const r1Done = result1.events.some((e) => e.type === "done");
    const r2Done = result2.events.some((e) => e.type === "done");
    expect(r1Done || r2Done).toBe(true);

    // The other should either also succeed or have a "busy" error
    if (!r1Done && result1.events.length > 0) {
      const hasError = result1.events.some(
        (e) =>
          e.type === "error" &&
          typeof e.message === "string" &&
          e.message.toLowerCase().includes("busy"),
      );
      expect(hasError).toBe(true);
    }
    if (!r2Done && result2.events.length > 0) {
      const hasError = result2.events.some(
        (e) =>
          e.type === "error" &&
          typeof e.message === "string" &&
          e.message.toLowerCase().includes("busy"),
      );
      expect(hasError).toBe(true);
    }
  });
});
