import type { FileInfo } from "./types";

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

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

export async function createSession(): Promise<SessionMetadata> {
  const res = await fetch(`${API_BASE}/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({}),
  });
  if (!res.ok) throw new Error(`Failed to create session: ${res.status}`);
  return res.json();
}

export async function getSession(
  sessionId: string,
): Promise<SessionWithMessages> {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}`);
  if (!res.ok) throw new Error(`Failed to get session: ${res.status}`);
  return res.json();
}

export async function deleteSession(sessionId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}`, {
    method: "DELETE",
  });
  if (!res.ok && res.status !== 404)
    throw new Error(`Failed to delete session: ${res.status}`);
}

export async function uploadFile(
  sessionId: string,
  file: File,
): Promise<{ path: string; filename: string; size: number }> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}/sessions/${sessionId}/upload`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`Upload failed (${res.status}): ${detail}`);
  }
  return res.json();
}

export async function listFiles(
  sessionId: string,
): Promise<{ files: FileInfo[] }> {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}/files`);
  if (!res.ok) throw new Error(`Failed to list files: ${res.status}`);
  return res.json();
}
