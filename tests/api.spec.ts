import { test, expect } from "@playwright/test";

const API = process.env.API_URL ?? "http://localhost:8000";

test.describe("Health", () => {
  test("GET /health returns ok", async ({ request }) => {
    const res = await request.get(`${API}/health`);
    expect(res.status()).toBe(200);
    const body = await res.json();
    expect(body.status).toBe("ok");
    expect(body).toHaveProperty("active_sessions");
    expect(body).toHaveProperty("cosmos_connected");
  });
});

test.describe("Session CRUD", () => {
  let sessionId: string;

  test("POST /sessions creates a session", async ({ request }) => {
    const res = await request.post(`${API}/sessions`, {
      data: {},
    });
    expect(res.status()).toBe(201);
    const body = await res.json();
    expect(body).toHaveProperty("session_id");
    expect(body.status).toBe("active");
    sessionId = body.session_id;
  });

  test("GET /sessions/:id returns the session", async ({ request }) => {
    // ensure we have a session from the previous test
    if (!sessionId) {
      const create = await request.post(`${API}/sessions`, { data: {} });
      sessionId = (await create.json()).session_id;
    }

    const res = await request.get(`${API}/sessions/${sessionId}`);
    expect(res.status()).toBe(200);
    const body = await res.json();
    expect(body.session_id).toBe(sessionId);
    expect(body).toHaveProperty("messages");
  });

  test("DELETE /sessions/:id removes the session", async ({ request }) => {
    if (!sessionId) {
      const create = await request.post(`${API}/sessions`, { data: {} });
      sessionId = (await create.json()).session_id;
    }

    const res = await request.delete(`${API}/sessions/${sessionId}`);
    expect(res.status()).toBe(204);

    // confirm it's gone
    const get = await request.get(`${API}/sessions/${sessionId}`);
    expect(get.status()).toBe(404);
  });
});

test.describe("Message SSE", () => {
  test("POST /sessions/:id/messages streams SSE events", async ({
    request,
  }) => {
    // create a fresh session
    const create = await request.post(`${API}/sessions`, { data: {} });
    expect(create.status()).toBe(201);
    const { session_id } = await create.json();

    // Playwright's request context buffers the full response, which doesn't
    // work with SSE streams. Use native fetch + manual stream reading instead.
    const res = await fetch(
      `${API}/sessions/${session_id}/messages`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: "Say hello in one sentence." }),
      },
    );
    expect(res.status).toBe(200);

    // Read SSE stream manually to handle connection close gracefully
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
      // Stream may close abruptly after final event — that's fine
    }
    // SSE stream should contain data: lines
    expect(text).toContain("data: ");

    // parse events — look for at least a delta or message event
    const events = text
      .split("\n")
      .filter((l) => l.startsWith("data: "))
      .map((l) => {
        try {
          return JSON.parse(l.slice(6));
        } catch {
          return null;
        }
      })
      .filter(Boolean);

    expect(events.length).toBeGreaterThan(0);

    // verify we received valid SSE event objects with a type field
    const types = events.map((e: { type: string }) => e.type);
    expect(types.length).toBeGreaterThan(0);
    for (const t of types) {
      expect(typeof t).toBe("string");
    }

    // cleanup
    await request.delete(`${API}/sessions/${session_id}`);
  });
});
