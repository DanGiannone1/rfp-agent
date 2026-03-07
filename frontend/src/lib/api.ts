import type { FileInfo } from "./types";

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface SessionMetadata {
  session_id: string;
  status: string;
}

export async function getSession(sessionId: string): Promise<SessionMetadata | null> {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}`);
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(`Session check failed: ${res.status}`);
  return res.json();
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

export async function uploadFile(
  sessionId: string,
  file: File,
): Promise<{ path: string; filename: string; size: number; markdown_ready: boolean }> {
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

export interface FileContentResponse {
  filename: string;
  size: number;
  mime_type: string;
  content: string;
}

export async function getFileContent(
  sessionId: string,
  filename: string,
): Promise<FileContentResponse> {
  const params = new URLSearchParams({ filename });
  const res = await fetch(`${API_BASE}/sessions/${sessionId}/files/content?${params.toString()}`);
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`Failed to load file content (${res.status}): ${detail}`);
  }
  return res.json();
}
