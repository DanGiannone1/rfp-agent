import { getAccessToken } from "./auth";
import { SSEEvent } from "./types";

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function* streamSSE(
  prompt: string,
  signal: AbortSignal,
  sessionId?: string,
): AsyncGenerator<SSEEvent> {
  const url = sessionId
    ? `${API_BASE}/sessions/${sessionId}/messages`
    : `${API_BASE}/analyze`;

  const token = await getAccessToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(url, {
    method: "POST",
    headers,
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
