import { getAccessToken } from "./auth";

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function authHeaders(): Promise<Record<string, string>> {
  const token = await getAccessToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export interface SessionMetadata {
  session_id: string;
  working_dir: string;
  status: string;
  created_at: string;
  last_activity_at: string;
}

export interface SessionWithMessages extends SessionMetadata {
  messages: Array<{
    session_id: string;
    role: "user" | "assistant";
    content: string;
    tool_activity: Array<{ tool: string; status: "running" | "done" }>;
    timestamp: string;
    turn_index: number;
  }>;
}

export async function createSession(
  workingDir?: string,
): Promise<SessionMetadata> {
  const res = await fetch(`${API_BASE}/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...(await authHeaders()) },
    body: JSON.stringify({ working_dir: workingDir ?? null }),
  });
  if (!res.ok) throw new Error(`Failed to create session: ${res.status}`);
  return res.json();
}

export async function getSession(
  sessionId: string,
): Promise<SessionWithMessages> {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}`, {
    headers: await authHeaders(),
  });
  if (!res.ok) throw new Error(`Failed to get session: ${res.status}`);
  return res.json();
}

export async function deleteSession(sessionId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}`, {
    method: "DELETE",
    headers: await authHeaders(),
  });
  if (!res.ok && res.status !== 404)
    throw new Error(`Failed to delete session: ${res.status}`);
}
