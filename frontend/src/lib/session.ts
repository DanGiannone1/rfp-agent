import type { ChatMessage } from "./types";

const SESSION_KEY = "rfp_agent_session_id";
const MESSAGES_KEY = "rfp_agent_messages";

export function storeSessionId(id: string): void {
  if (typeof window === "undefined") return;
  sessionStorage.setItem(SESSION_KEY, id);
}

export function clearSessionId(): void {
  if (typeof window === "undefined") return;
  sessionStorage.removeItem(SESSION_KEY);
  sessionStorage.removeItem(MESSAGES_KEY);
}

export function getSessionId(): string | null {
  if (typeof window === "undefined") return null;
  return sessionStorage.getItem(SESSION_KEY);
}

export function getStoredMessages(): ChatMessage[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = sessionStorage.getItem(MESSAGES_KEY);
    return raw ? (JSON.parse(raw) as ChatMessage[]) : [];
  } catch {
    return [];
  }
}

export function storeMessages(messages: ChatMessage[]): void {
  if (typeof window === "undefined") return;
  const completed = messages.filter((m) => !m.isStreaming);
  sessionStorage.setItem(MESSAGES_KEY, JSON.stringify(completed));
}
