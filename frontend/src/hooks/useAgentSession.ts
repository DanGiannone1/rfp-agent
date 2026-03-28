import { useReducer, useRef, useCallback, useEffect, useState } from "react";
import { AGUIEvent, AppFile, ChatMessage, IntakeState, MessagePart } from "@/lib/types";
import { streamSSE } from "@/lib/sse";
import { createSession, getFileContent, getSession, listFiles, uploadFile } from "@/lib/api";
import { clearSessionId, getSessionId, getStoredMessages, storeSessionId, storeMessages } from "@/lib/session";
import { friendlyError } from "@/lib/utils";

type ChatStage = "intake" | "chat";

type Action =
  | { type: "USER_SEND"; content: string }
  | { type: "RUN_STARTED"; runId: string }
  | { type: "ASSISTANT_START"; messageId: string }
  | { type: "DELTA"; delta: string }
  | { type: "MESSAGE_END" }
  | { type: "TOOL_START"; toolCallId: string; toolCallName: string }
  | { type: "TOOL_ARGS"; toolCallId: string; delta: string }
  | { type: "TOOL_END"; toolCallId: string }
  | { type: "DONE" }
  | { type: "ERROR"; message: string }
  | { type: "SET_SESSION_ID"; sessionId: string }
  | { type: "SET_INITIALIZING"; value: boolean }
  | { type: "SET_STAGE"; stage: ChatStage }
  | { type: "RESTORE_SESSION"; sessionId: string; messages: ChatMessage[] }
  | { type: "RESET_FOR_NEW_CHAT" }
  | { type: "FILE_PENDING"; filename: string; size: number }
  | { type: "FILES_LOADED"; files: AppFile[] }
  | { type: "INTAKE_SESSION"; sessionState: "preparing" | "ready" | "error"; error?: string }
  | { type: "INTAKE_UPLOAD"; uploadState: "idle" | "uploading"; filename?: string; error?: string };

interface State {
  messages: ChatMessage[];
  isStreaming: boolean;
  sessionId: string | null;
  isInitializing: boolean;
  stage: ChatStage;
  currentRunId: string | null;
  files: AppFile[];
  intake: IntakeState;
}

const SESSION_TIMEOUT_MS = 12_000;
const UPLOAD_TIMEOUT_MS = 180_000;

function updateLastMessage(msgs: ChatMessage[], updater: (msg: ChatMessage) => ChatMessage): ChatMessage[] {
  if (msgs.length === 0) return msgs;
  const copy = [...msgs];
  copy[copy.length - 1] = updater({ ...copy[copy.length - 1] });
  return copy;
}

function createUserMessage(content: string): ChatMessage {
  return {
    id: crypto.randomUUID(),
    role: "user",
    isStreaming: false,
    parts: [{ type: "text", content }],
  };
}

function createAssistantMessage(id: string, parts: MessagePart[], isStreaming: boolean): ChatMessage {
  return {
    id,
    role: "assistant",
    isStreaming,
    parts,
  };
}

function finalizeAssistantMessage(msg: ChatMessage): ChatMessage {
  if (msg.role !== "assistant") return msg;
  const parts = msg.parts.map((p) =>
    p.type === "tool_call" && p.status === "running"
      ? { ...p, status: "done" as const }
      : p,
  );
  return { ...msg, parts, isStreaming: false };
}

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "SET_SESSION_ID": return { ...state, sessionId: action.sessionId };
    case "SET_INITIALIZING": return { ...state, isInitializing: action.value };
    case "SET_STAGE": return { ...state, stage: action.stage };
    case "RESET_FOR_NEW_CHAT":
      return {
        ...state,
        messages: [],
        isStreaming: false,
        sessionId: null,
        stage: "intake",
        currentRunId: null,
        files: [],
        intake: { sessionState: "preparing", uploadState: "idle", error: null, filename: null },
      };
    case "USER_SEND":
      return {
        ...state,
        isStreaming: true,
        messages: [
          ...state.messages,
          createUserMessage(action.content),
          createAssistantMessage(`pending-${crypto.randomUUID()}`, [], true),
        ],
      };
    case "RUN_STARTED": return { ...state, currentRunId: action.runId };
    case "ASSISTANT_START": {
      if (state.messages.length === 0) return { ...state, messages: [createAssistantMessage(action.messageId, [], true)] };
      const last = state.messages[state.messages.length - 1];
      if (last.role === "assistant" && last.isStreaming && last.id.startsWith("pending-")) {
        return { ...state, messages: updateLastMessage(state.messages, (m) => ({ ...m, id: action.messageId })) };
      }
      if (last.role === "assistant" && last.isStreaming && state.currentRunId) return state;
      return { ...state, messages: [...state.messages, createAssistantMessage(action.messageId, [], true)] };
    }
    case "DELTA": {
      if (state.messages.length === 0) return state;
      return {
        ...state,
        messages: updateLastMessage(state.messages, (m) => {
          const parts = [...m.parts];
          const lastPart = parts[parts.length - 1];
          if (lastPart && lastPart.type === "text") {
            parts[parts.length - 1] = { ...lastPart, content: lastPart.content + action.delta };
          } else {
            parts.push({ type: "text", content: action.delta });
          }
          return { ...m, parts };
        }),
      };
    }
    case "MESSAGE_END": return { ...state, messages: updateLastMessage(state.messages, (m) => finalizeAssistantMessage(m)) };
    case "TOOL_START": {
      if (state.messages.length === 0) return state;
      return {
        ...state,
        messages: updateLastMessage(state.messages, (m) => {
          const parts = [...m.parts, {
            type: "tool_call" as const,
            tool: action.toolCallName,
            toolCallId: action.toolCallId,
            status: "running" as const,
          }];
          return { ...m, parts };
        }),
      };
    }
    case "TOOL_ARGS": {
      if (state.messages.length === 0) return state;
      return {
        ...state,
        messages: updateLastMessage(state.messages, (m) => {
          const parts = m.parts.map((p) =>
            p.type === "tool_call" && p.toolCallId === action.toolCallId
              ? { ...p, args: (p.args || "") + action.delta }
              : p,
          );
          return { ...m, parts };
        }),
      };
    }
    case "TOOL_END": {
      if (state.messages.length === 0) return state;
      return {
        ...state,
        messages: updateLastMessage(state.messages, (m) => {
          const parts = m.parts.map((p) =>
            p.type === "tool_call" && p.toolCallId === action.toolCallId
              ? { ...p, status: "done" as const }
              : p,
          );
          return { ...m, parts };
        }),
      };
    }
    case "DONE": return { ...state, isStreaming: false, currentRunId: null, messages: updateLastMessage(state.messages, (m) => finalizeAssistantMessage(m)) };
    case "ERROR": {
      const msgs = [...state.messages];
      if (msgs.length > 0 && msgs[msgs.length - 1].role === "assistant") {
        return {
          ...state,
          isStreaming: false,
          currentRunId: null,
          messages: updateLastMessage(msgs, (m) => {
            const parts = [...m.parts, { type: "text" as const, content: `\n\n${action.message}` }];
            return { ...m, parts, isStreaming: false };
          }),
        };
      }
      msgs.push(createAssistantMessage(crypto.randomUUID(), [{ type: "text", content: action.message }], false));
      return { ...state, messages: msgs, isStreaming: false, currentRunId: null };
    }
    case "RESTORE_SESSION":
      return {
        ...state,
        sessionId: action.sessionId,
        stage: "chat",
        messages: action.messages,
        isInitializing: false,
        files: [],
        intake: { sessionState: "ready", uploadState: "idle", error: null, filename: null },
      };
    case "FILE_PENDING": {
      const pending: AppFile = {
        filename: action.filename,
        size: action.size,
        modified_at: new Date().toISOString(),
        origin: "uploaded",
        status: "pending",
        has_markdown: false,
      };
      return { ...state, files: [pending, ...state.files.filter(f => f.filename !== action.filename)] };
    }
    case "FILES_LOADED": {
      const serverFilenames = new Set(action.files.map(f => f.filename));
      const stillPending = state.files.filter(f => f.status === "pending" && !serverFilenames.has(f.filename));
      return { ...state, files: [...stillPending, ...action.files] };
    }
    case "INTAKE_SESSION":
      return {
        ...state,
        intake: {
          ...state.intake,
          sessionState: action.sessionState,
          error: action.error ?? (action.sessionState === "error" ? state.intake.error : null),
        },
      };
    case "INTAKE_UPLOAD":
      return {
        ...state,
        intake: {
          ...state.intake,
          uploadState: action.uploadState,
          filename: action.filename ?? state.intake.filename,
          error: action.error ?? (action.uploadState === "idle" ? null : state.intake.error),
        },
      };
    default: return state;
  }
}

const initialState: State = {
  messages: [],
  isStreaming: false,
  sessionId: null,
  isInitializing: true,
  stage: "intake",
  currentRunId: null,
  files: [],
  intake: { sessionState: "preparing", uploadState: "idle", error: null, filename: null },
};

function withTimeout<T>(promise: Promise<T>, timeoutMs: number, timeoutMessage: string): Promise<T> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(timeoutMessage)), timeoutMs);
    promise.then((value) => { clearTimeout(timer); resolve(value); }).catch((error) => { clearTimeout(timer); reject(error); });
  });
}

export function useAgentSession() {
  const [state, dispatch] = useReducer(reducer, initialState);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [chatUploadName, setChatUploadName] = useState<string | null>(null);
  const [isChatUploading, setIsChatUploading] = useState(false);
  const abortRef = useRef<AbortController | null>(null);
  const sessionIdRef = useRef<string | null>(null);
  const streamingRef = useRef(false);

  useEffect(() => { sessionIdRef.current = state.sessionId; }, [state.sessionId]);
  useEffect(() => { streamingRef.current = state.isStreaming; }, [state.isStreaming]);

  const refreshFiles = useCallback(async (sessionId: string) => {
    const data = await listFiles(sessionId);
    const raw = data.files;
    const byName = new Map(raw.map(f => [f.filename, f]));
    const normalized = raw
      .filter(f => {
        if (!f.filename.endsWith(".md")) return true;
        const sourceName = f.filename.slice(0, -3);
        return !byName.has(sourceName);
      })
      .map((f): AppFile => ({
        filename: f.filename,
        size: f.size,
        modified_at: f.modified_at,
        origin: f.origin ?? "generated",
        status: "ready",
        has_markdown: f.has_markdown,
      }))
      .sort((a, b) => Date.parse(b.modified_at) - Date.parse(a.modified_at));
    dispatch({ type: "FILES_LOADED", files: normalized });
  }, []);

  const startSession = useCallback(async () => {
    setStatusMessage(null);
    dispatch({ type: "INTAKE_SESSION", sessionState: "preparing" });
    dispatch({ type: "SET_INITIALIZING", value: true });
    const storedId = getSessionId();
    if (storedId) {
      try {
        const meta = await withTimeout(getSession(storedId), SESSION_TIMEOUT_MS, "Session check timed out");
        if (meta) {
          const msgs = getStoredMessages();
          dispatch({ type: "RESTORE_SESSION", sessionId: meta.session_id, messages: msgs });
          try { await refreshFiles(meta.session_id); } catch (e) { console.warn("Failed to refresh files on restore", e); }
          return;
        }
      } catch { /* session dead or unreachable — fall through to create new */ }
    }
    clearSessionId();
    try {
      const meta = await withTimeout(createSession(), SESSION_TIMEOUT_MS, "Session creation timed out");
      storeSessionId(meta.session_id);
      dispatch({ type: "SET_SESSION_ID", sessionId: meta.session_id });
      dispatch({ type: "INTAKE_SESSION", sessionState: "ready" });
    } catch (err) {
      dispatch({ type: "INTAKE_SESSION", sessionState: "error", error: friendlyError(err, "Could not start a session.") });
    } finally {
      dispatch({ type: "SET_INITIALIZING", value: false });
    }
  }, [refreshFiles]);

  useEffect(() => { startSession(); }, [startSession]);

  useEffect(() => {
    if (!state.isStreaming && state.messages.length > 0) storeMessages(state.messages);
  }, [state.isStreaming, state.messages]);

  useEffect(() => {
    if (state.intake.error) return;
    let timer: ReturnType<typeof setTimeout> | undefined;
    if (state.isInitializing) {
      timer = setTimeout(() => setStatusMessage("Still starting your session. You can retry if this continues."), 9000);
    } else if (state.intake.uploadState === "uploading") {
      timer = setTimeout(() => setStatusMessage("Converting your document — this can take 30–60 seconds."), 8000);
    } else { setStatusMessage(null); }
    return () => { if (timer) clearTimeout(timer); };
  }, [state.isInitializing, state.intake.uploadState, state.intake.error]);

  useEffect(() => {
    if (!state.sessionId || state.stage !== "chat") return;
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout> | undefined;
    const sid = state.sessionId;
    async function tick() {
      try { await refreshFiles(sid); if (cancelled) return; } catch (e) { console.warn("File poll failed", e); }
      if (!cancelled) timer = setTimeout(tick, 10_000);
    }
    tick();
    return () => { cancelled = true; if (timer) clearTimeout(timer); };
  }, [state.sessionId, state.stage, refreshFiles]);

  const handleIntakeUpload = useCallback(async (file: File) => {
    if (!state.sessionId) return;
    setStatusMessage(null);
    dispatch({ type: "INTAKE_UPLOAD", uploadState: "uploading", filename: file.name });
    dispatch({ type: "FILE_PENDING", filename: file.name, size: file.size });
    try {
      await withTimeout(uploadFile(state.sessionId, file), UPLOAD_TIMEOUT_MS, "Upload timed out");
      try { await refreshFiles(state.sessionId); } catch (e) { console.warn("Failed to refresh files after upload", e); }
      dispatch({ type: "INTAKE_UPLOAD", uploadState: "idle" });
      dispatch({ type: "SET_STAGE", stage: "chat" });
    } catch (err) { dispatch({ type: "INTAKE_UPLOAD", uploadState: "idle", error: friendlyError(err, "Upload failed.") }); }
  }, [state.sessionId, refreshFiles]);

  const doNewChat = useCallback(async () => {
    abortRef.current?.abort(); abortRef.current = null;
    clearSessionId(); setStatusMessage(null);
    dispatch({ type: "RESET_FOR_NEW_CHAT" });
    dispatch({ type: "SET_INITIALIZING", value: true });
    await startSession();
  }, [startSession]);

  const handleStop = useCallback(() => {
    if (state.isStreaming) {
      abortRef.current?.abort();
      abortRef.current = null;
      dispatch({ type: "DONE" });
    }
  }, [state.isStreaming]);

  const handleAGUIEvent = useCallback((event: AGUIEvent) => {
    switch (event.type) {
      case "RUN_STARTED": dispatch({ type: "RUN_STARTED", runId: event.run_id }); break;
      case "TEXT_MESSAGE_START": dispatch({ type: "ASSISTANT_START", messageId: event.message_id }); break;
      case "TEXT_MESSAGE_CONTENT": dispatch({ type: "DELTA", delta: event.delta }); break;
      case "TEXT_MESSAGE_END": dispatch({ type: "MESSAGE_END" }); break;
      case "TOOL_CALL_START": dispatch({ type: "TOOL_START", toolCallId: event.tool_call_id, toolCallName: event.tool_call_name }); break;
      case "TOOL_CALL_ARGS": dispatch({ type: "TOOL_ARGS", toolCallId: event.tool_call_id, delta: event.delta }); break;
      case "TOOL_CALL_END": dispatch({ type: "TOOL_END", toolCallId: event.tool_call_id }); break;
      case "RUN_FINISHED": dispatch({ type: "DONE" }); if (sessionIdRef.current) void refreshFiles(sessionIdRef.current).catch(() => {}); break;
      case "RUN_ERROR": dispatch({ type: "ERROR", message: event.message || "Error during generation." }); if (sessionIdRef.current) void refreshFiles(sessionIdRef.current).catch(() => {}); break;
    }
  }, [refreshFiles]);

  const handleSend = useCallback(async (content: string) => {
    if (!state.sessionId || state.isStreaming || streamingRef.current) return;
    dispatch({ type: "USER_SEND", content });
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    try {
      for await (const event of streamSSE(content, controller.signal, state.sessionId)) { handleAGUIEvent(event); }
      dispatch({ type: "DONE" });
    } catch (err: unknown) {
      if (err instanceof Error && err.name === "AbortError") return;
      dispatch({ type: "ERROR", message: friendlyError(err, "Message failed.") });
    } finally { if (abortRef.current === controller) abortRef.current = null; }
  }, [handleAGUIEvent, state.sessionId, state.isStreaming]);

  const handleChatUpload = useCallback(async (file: File) => {
    if (!state.sessionId) return;
    setIsChatUploading(true); setChatUploadName(file.name);
    dispatch({ type: "FILE_PENDING", filename: file.name, size: file.size });
    try {
      await withTimeout(uploadFile(state.sessionId, file), UPLOAD_TIMEOUT_MS, "Upload timed out");
      try { await refreshFiles(state.sessionId); } catch (e) { console.warn("Failed to refresh files after chat upload", e); }
    } catch (err) {
      dispatch({ type: "ERROR", message: friendlyError(err, "File upload failed.") });
    } finally { setIsChatUploading(false); setChatUploadName(null); }
  }, [state.sessionId, refreshFiles]);

  return {
    state,
    statusMessage,
    isChatUploading,
    chatUploadName,
    handleIntakeUpload,
    handleSend,
    handleStop,
    handleChatUpload,
    doNewChat,
    startSession
  };
}
