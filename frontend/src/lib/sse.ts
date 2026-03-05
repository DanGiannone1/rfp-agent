import { SSEEvent } from "./types";

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function* streamSSE(
  prompt: string,
  signal: AbortSignal,
  sessionId: string,
): AsyncGenerator<SSEEvent> {
  const url = `${API_BASE}/sessions/${sessionId}/messages`;

  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
    signal,
  });

  if (!res.ok) {
    yield { type: "error", message: `HTTP ${res.status}: ${res.statusText}` };
    return;
  }

  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    const lines = buffer.split("\n");
    buffer = lines.pop()!;

    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed.startsWith("data: ")) continue;
      const data = trimmed.slice(6);
      try {
        const event = JSON.parse(data) as SSEEvent;
        yield event;
      } catch {
        // skip malformed lines
      }
    }
  }

  // process any remaining buffer
  if (buffer.trim().startsWith("data: ")) {
    const data = buffer.trim().slice(6);
    try {
      const event = JSON.parse(data) as SSEEvent;
      yield event;
    } catch {
      // skip
    }
  }
}
