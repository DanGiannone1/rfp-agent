"use client";

import { useReducer, useRef, useCallback, useEffect, useState, useMemo } from "react";
import { AGUIEvent, ChatMessage, FileInfo, MessagePart } from "@/lib/types";
import { streamSSE } from "@/lib/sse";
import { createSession, getFileContent, getSession, listFiles, uploadFile } from "@/lib/api";
import { clearSessionId, getSessionId, getStoredMessages, storeSessionId, storeMessages } from "@/lib/session";
import MessageList from "./MessageList";
import InputBar from "./InputBar";
import IntakeScreen from "./IntakeScreen";
import DocumentsDrawer from "./DocumentsDrawer";
import ArtifactsPanel from "./ArtifactsPanel";
import ArtifactCanvas from "./ArtifactCanvas";

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
  | { type: "FILES_CHANGED" }
  | { type: "APPEND_ASSISTANT"; content: string; id?: string }
  | { type: "UPDATE_ASSISTANT"; id: string; content: string }
  | { type: "RESTORE_SESSION"; sessionId: string; messages: ChatMessage[] }
  | { type: "RESET_FOR_NEW_CHAT" };

interface State {
  messages: ChatMessage[];
  isStreaming: boolean;
  sessionId: string | null;
  isInitializing: boolean;
  fileRefreshKey: number;
  stage: ChatStage;
  currentRunId: string | null;
}

const SESSION_TIMEOUT_MS = 12_000;
const UPLOAD_TIMEOUT_MS = 180_000; // covers file transfer + CU conversion (large PDFs can take 2+ min)

function normalizeFileList(files: FileInfo[]): FileInfo[] {
  const byName = new Map(files.map((f) => [f.filename, f]));
  return files
    .filter((f) => {
      if (!f.filename.endsWith(".md")) return true;
      const sourceName = f.filename.slice(0, -3);
      return !byName.has(sourceName);
    })
    .sort((a, b) => Date.parse(b.modified_at || "") - Date.parse(a.modified_at || ""));
}

function pendingFileFromUpload(file: File): FileInfo {
  return {
    filename: file.name,
    size: file.size,
    modified_at: new Date().toISOString(),
    has_markdown: false,
  };
}

function mergeVisibleFiles(serverFiles: FileInfo[], pendingFiles: FileInfo[]): FileInfo[] {
  const map = new Map<string, FileInfo>();
  for (const file of pendingFiles) {
    map.set(file.filename, file);
  }
  for (const file of serverFiles) {
    const existing = map.get(file.filename);
    map.set(file.filename, existing ? { ...existing, ...file, has_markdown: file.has_markdown || existing.has_markdown } : file);
  }
  return Array.from(map.values()).sort((a, b) => Date.parse(b.modified_at || "") - Date.parse(a.modified_at || ""));
}

/** Helper: update the last message in a messages array. */
function updateLastMessage(msgs: ChatMessage[], updater: (msg: ChatMessage) => ChatMessage): ChatMessage[] {
  if (msgs.length === 0) return msgs;
  const copy = [...msgs];
  copy[copy.length - 1] = updater({ ...copy[copy.length - 1] });
  return copy;
}

/** Derive flat content and toolActivity from parts for backward compat. */
function syncFromParts(msg: ChatMessage): ChatMessage {
  const content = msg.parts
    .filter((p): p is MessagePart & { type: "text" } => p.type === "text")
    .map((p) => p.content)
    .join("");
  const toolActivity = msg.parts
    .filter((p): p is MessagePart & { type: "tool_call" } => p.type === "tool_call")
    .map((p) => ({ tool: p.tool, toolCallId: p.toolCallId, status: p.status, args: p.args }));
  return { ...msg, content, toolActivity };
}

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "SET_SESSION_ID":
      return { ...state, sessionId: action.sessionId };

    case "SET_INITIALIZING":
      return { ...state, isInitializing: action.value };

    case "SET_STAGE":
      return { ...state, stage: action.stage };

    case "RESET_FOR_NEW_CHAT":
      return {
        ...state,
        messages: [],
        isStreaming: false,
        sessionId: null,
        stage: "intake",
        fileRefreshKey: 0,
        currentRunId: null,
      };

    case "USER_SEND":
      return {
        ...state,
        isStreaming: true,
        messages: [
          ...state.messages,
          {
            id: crypto.randomUUID(),
            role: "user",
            content: action.content,
            isStreaming: false,
            toolActivity: [],
            parts: [{ type: "text", content: action.content }],
          },
          {
            id: `pending-${crypto.randomUUID()}`,
            role: "assistant",
            content: "",
            isStreaming: true,
            toolActivity: [],
            parts: [],
          },
        ],
      };

    case "RUN_STARTED":
      return { ...state, currentRunId: action.runId };

    case "ASSISTANT_START": {
      if (state.messages.length === 0) {
        return {
          ...state,
          messages: [{
            id: action.messageId,
            role: "assistant",
            content: "",
            isStreaming: true,
            toolActivity: [],
            parts: [],
          }],
        };
      }
      const last = state.messages[state.messages.length - 1];
      // Replace pending message ID
      if (last.role === "assistant" && last.isStreaming && last.id.startsWith("pending-")) {
        return {
          ...state,
          messages: updateLastMessage(state.messages, (m) => ({ ...m, id: action.messageId })),
        };
      }
      // Same run — continuation after tool call, stay in same message
      if (last.role === "assistant" && last.isStreaming && state.currentRunId) {
        return state;
      }
      return {
        ...state,
        messages: [
          ...state.messages,
          {
            id: action.messageId,
            role: "assistant",
            content: "",
            isStreaming: true,
            toolActivity: [],
            parts: [],
          },
        ],
      };
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
          return syncFromParts({ ...m, parts });
        }),
      };
    }

    case "MESSAGE_END":
      return {
        ...state,
        messages: updateLastMessage(state.messages, (m) => {
          if (m.role !== "assistant") return m;
          const parts = m.parts.map((p) =>
            p.type === "tool_call" && p.status === "running"
              ? { ...p, status: "done" as const }
              : p,
          );
          return syncFromParts({ ...m, parts, isStreaming: false });
        }),
      };

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
          return syncFromParts({ ...m, parts });
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
          return syncFromParts({ ...m, parts });
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
          return syncFromParts({ ...m, parts });
        }),
      };
    }

    case "DONE": {
      return {
        ...state,
        isStreaming: false,
        currentRunId: null,
        messages: updateLastMessage(state.messages, (m) => {
          if (m.role !== "assistant") return m;
          const parts = m.parts.map((p) =>
            p.type === "tool_call" && p.status === "running"
              ? { ...p, status: "done" as const }
              : p,
          );
          return syncFromParts({ ...m, parts, isStreaming: false });
        }),
      };
    }

    case "ERROR": {
      const msgs = [...state.messages];
      if (msgs.length > 0 && msgs[msgs.length - 1].role === "assistant") {
        return {
          ...state,
          isStreaming: false,
          currentRunId: null,
          messages: updateLastMessage(msgs, (m) => {
            const parts = [...m.parts, { type: "text" as const, content: `\n\n${action.message}` }];
            return syncFromParts({ ...m, parts, isStreaming: false });
          }),
        };
      }
      msgs.push({
        id: crypto.randomUUID(),
        role: "assistant",
        content: action.message,
        isStreaming: false,
        toolActivity: [],
        parts: [{ type: "text", content: action.message }],
      });
      return { ...state, messages: msgs, isStreaming: false, currentRunId: null };
    }

    case "RESTORE_SESSION":
      return {
        ...state,
        sessionId: action.sessionId,
        stage: "chat",
        messages: action.messages,
        isInitializing: false,
      };

    case "APPEND_ASSISTANT":
      return {
        ...state,
        messages: [
          ...state.messages,
          {
            id: action.id ?? crypto.randomUUID(),
            role: "assistant",
            content: action.content,
            isStreaming: false,
            toolActivity: [],
            parts: [{ type: "text", content: action.content }],
          },
        ],
      };

    case "UPDATE_ASSISTANT":
      return {
        ...state,
        messages: state.messages.map((m) =>
          m.id === action.id
            ? { ...m, content: action.content, parts: [{ type: "text", content: action.content }] }
            : m,
        ),
      };

    case "FILES_CHANGED":
      return { ...state, fileRefreshKey: state.fileRefreshKey + 1 };

    default:
      return state;
  }
}

const initialState: State = {
  messages: [],
  isStreaming: false,
  sessionId: null,
  isInitializing: true,
  fileRefreshKey: 0,
  stage: "intake",
  currentRunId: null,
};

function withTimeout<T>(promise: Promise<T>, timeoutMs: number, timeoutMessage: string): Promise<T> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(timeoutMessage)), timeoutMs);
    promise
      .then((value) => {
        clearTimeout(timer);
        resolve(value);
      })
      .catch((error) => {
        clearTimeout(timer);
        reject(error);
      });
  });
}

function friendlyError(err: unknown, fallback: string): string {
  if (!(err instanceof Error)) return fallback;
  const msg = err.message.toLowerCase();
  if (msg.includes("timeout") || msg.includes("timed out")) return "The request took too long. Please try again.";
  if (msg.includes("failed to fetch") || msg.includes("network")) return "Network issue. Check your connection and try again.";
  if (msg.includes("413") || msg.includes("too large")) return "The file is too large. Please upload a smaller file.";
  if (msg.includes("415") || msg.includes("unsupported")) return "This file type is not supported.";
  if (msg.includes("404")) return "Artifact not found. It may still be generating — please try again in a moment.";
  return fallback;
}

export default function Chat() {
  const [state, dispatch] = useReducer(reducer, initialState);
  const [uploadedFileNames, setUploadedFileNames] = useState<string[]>([]);
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [sessionError, setSessionError] = useState<string | null>(null);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadState, setUploadState] = useState<"idle" | "uploading">("idle");
  const [sessionState, setSessionState] = useState<"preparing" | "ready" | "error">("preparing");
  const [chatUploadName, setChatUploadName] = useState<string | null>(null);
  const [isChatUploading, setIsChatUploading] = useState(false);
  const [hasFetchedFiles, setHasFetchedFiles] = useState(false);
  const [serverFiles, setServerFiles] = useState<FileInfo[]>([]);
  const [pendingFiles, setPendingFiles] = useState<FileInfo[]>([]);
  const [documentsOpen, setDocumentsOpen] = useState(false);
  const [selectedArtifact, setSelectedArtifact] = useState<string | null>(null);
  const [confirmNewChat, setConfirmNewChat] = useState(false);
  const [artifactContent, setArtifactContent] = useState<string>("");
  const [artifactMimeType, setArtifactMimeType] = useState<string | undefined>();
  const [artifactLoading, setArtifactLoading] = useState(false);
  const [artifactError, setArtifactError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  const lastAutoOpenedGenerated = useRef<string | null>(null);
  const fileRetryTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const files = useMemo(() => mergeVisibleFiles(serverFiles, pendingFiles), [serverFiles, pendingFiles]);
  const uploadedNameSet = useMemo(
    () => new Set([...uploadedFileNames, ...pendingFiles.map((f) => f.filename)]),
    [uploadedFileNames, pendingFiles],
  );
  const hasOriginMetadata = useMemo(() => files.some((f) => f.origin === "uploaded" || f.origin === "generated"), [files]);
  const uploadedFiles = useMemo(
    () => hasOriginMetadata
      ? files.filter((f) => f.origin === "uploaded")
      : files.filter((f) => uploadedNameSet.has(f.filename)),
    [files, hasOriginMetadata, uploadedNameSet],
  );
  const generatedFiles = useMemo(
    () => hasOriginMetadata
      ? files.filter((f) => f.origin === "generated")
      : files.filter((f) => !uploadedNameSet.has(f.filename)),
    [files, hasOriginMetadata, uploadedNameSet],
  );
  const filesLoading = !hasFetchedFiles && pendingFiles.length === 0;

  const addPendingFile = useCallback((file: File) => {
    const pending = pendingFileFromUpload(file);
    setPendingFiles((prev) => [pending, ...prev.filter((item) => item.filename !== pending.filename)]);
  }, []);

  const clearPendingFile = useCallback((filename: string) => {
    setPendingFiles((prev) => prev.filter((item) => item.filename !== filename));
  }, []);

  const markUploadedFile = useCallback((filename: string) => {
    setUploadedFileNames((prev) => (prev.includes(filename) ? prev : [...prev, filename]));
  }, []);

  const refreshFiles = useCallback(async (sessionId: string) => {
    const data = await listFiles(sessionId);
    const normalized = normalizeFileList(data.files);
    setServerFiles(normalized);
    setPendingFiles((prev) => prev.filter((file) => !normalized.some((server) => server.filename === file.filename)));
    setHasFetchedFiles(true);
  }, []);

  const startSession = useCallback(async () => {
    setSessionError(null);
    setUploadError(null);
    setStatusMessage(null);
    setSessionState("preparing");
    dispatch({ type: "SET_INITIALIZING", value: true });

    // Attempt to restore an existing session from sessionStorage
    const storedId = getSessionId();
    if (storedId) {
      try {
        const meta = await getSession(storedId);
        if (meta) {
          const msgs = getStoredMessages();
          dispatch({ type: "RESTORE_SESSION", sessionId: meta.session_id, messages: msgs });
          setSessionState("ready");
          try { await refreshFiles(meta.session_id); } catch { /* non-blocking */ }
          return;
        }
      } catch {
        // Fall through to create a new session
      }
    }

    // No stored session or restore failed — create fresh
    clearSessionId();
    setServerFiles([]);
    setPendingFiles([]);
    setHasFetchedFiles(false);
    setUploadedFileNames([]);

    try {
      const meta = await withTimeout(createSession(), SESSION_TIMEOUT_MS, "Session creation timed out");
      storeSessionId(meta.session_id);
      dispatch({ type: "SET_SESSION_ID", sessionId: meta.session_id });
      setSessionState("ready");
    } catch (err) {
      setSessionError(friendlyError(err, "Could not start a session. Please retry."));
      setSessionState("error");
    } finally {
      dispatch({ type: "SET_INITIALIZING", value: false });
    }
  }, [refreshFiles]);

  useEffect(() => {
    startSession();
  }, [startSession]);

  useEffect(() => {
    return () => { if (fileRetryTimerRef.current) clearTimeout(fileRetryTimerRef.current); };
  }, []);

  useEffect(() => {
    if (!state.isStreaming && state.messages.length > 0) {
      storeMessages(state.messages);
    }
  }, [state.isStreaming, state.messages]);

  useEffect(() => {
    if (sessionError || uploadError) return;
    let timer: ReturnType<typeof setTimeout> | undefined;

    if (state.isInitializing) {
      timer = setTimeout(() => {
        setStatusMessage("Still starting your session. You can retry if this continues.");
      }, 9000);
    } else if (isUploading) {
      timer = setTimeout(() => {
        setStatusMessage("Converting your document with Azure Content Understanding — this can take 30–60 seconds for large files.");
      }, 8000);
    } else {
      setStatusMessage(null);
    }

    return () => {
      if (timer) clearTimeout(timer);
    };
  }, [state.isInitializing, isUploading, sessionError, uploadError]);

  useEffect(() => {
    if (!state.sessionId || state.stage !== "chat") return;
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout> | undefined;
    const sid = state.sessionId;

    async function tick() {
      try {
        await refreshFiles(sid);
        if (cancelled) return;
      } catch {
        // non-blocking
      }
      if (!cancelled) timer = setTimeout(tick, 10_000);
    }

    tick();
    return () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
    };
  }, [state.sessionId, state.stage, state.fileRefreshKey, refreshFiles]);

  const handleIntakeUpload = useCallback(
    async (file: File) => {
      if (!state.sessionId) {
        setSessionError("Session is not ready yet. Please retry session setup.");
        setSessionState("error");
        return;
      }

      setSelectedFileName(file.name);
      setUploadError(null);
      setStatusMessage(null);
      setIsUploading(true);
      setUploadState("uploading");
      addPendingFile(file);

      try {
        // Single request: file transfer + CU conversion happen server-side before response
        await withTimeout(uploadFile(state.sessionId, file), UPLOAD_TIMEOUT_MS, "Upload timed out");
        dispatch({ type: "FILES_CHANGED" });
        setUploadedFileName(file.name);
        markUploadedFile(file.name);
        try {
          await refreshFiles(state.sessionId);
        } catch {
          // non-blocking; optimistic pending file remains visible
        }
        dispatch({ type: "SET_STAGE", stage: "chat" });
        setUploadState("idle");
      } catch (err) {
        clearPendingFile(file.name);
        setUploadError(friendlyError(err, "Upload failed. Please try again."));
        setUploadState("idle");
      } finally {
        setIsUploading(false);
      }
    },
    [state.sessionId, addPendingFile, clearPendingFile, markUploadedFile, refreshFiles],
  );

  const doNewChat = useCallback(async () => {
    abortRef.current?.abort();
    abortRef.current = null;

    clearSessionId();
    setUploadedFileName(null);
    setSelectedFileName(null);
    setUploadError(null);
    setSessionError(null);
    setStatusMessage(null);
    setUploadState("idle");
    setServerFiles([]);
    setPendingFiles([]);
    setHasFetchedFiles(false);
    setUploadedFileNames([]);
    setDocumentsOpen(false);
    setSelectedArtifact(null);
    setArtifactContent("");
    setArtifactMimeType(undefined);
    setArtifactError(null);
    setArtifactLoading(false);
    lastAutoOpenedGenerated.current = null;
    dispatch({ type: "RESET_FOR_NEW_CHAT" });

    await startSession();
  }, [startSession]);

  const handleNewChat = useCallback(() => {
    const hasActiveContext = state.messages.length > 0 || Boolean(uploadedFileName) || files.length > 0;
    if (hasActiveContext) {
      setConfirmNewChat(true);
      return;
    }
    void doNewChat();
  }, [state.messages.length, uploadedFileName, files.length, doNewChat]);

  const handleStop = useCallback(() => {
    if (!state.isStreaming) return;
    abortRef.current?.abort();
    abortRef.current = null;
    dispatch({ type: "DONE" });
    dispatch({ type: "APPEND_ASSISTANT", content: "_Generation stopped by user._" });
  }, [state.isStreaming]);

  const handleAGUIEvent = useCallback((event: AGUIEvent) => {
    switch (event.type) {
      case "RUN_STARTED":
        dispatch({ type: "RUN_STARTED", runId: event.run_id });
        break;
      case "TEXT_MESSAGE_START":
        dispatch({ type: "ASSISTANT_START", messageId: event.message_id });
        break;
      case "TEXT_MESSAGE_CONTENT":
        dispatch({ type: "DELTA", delta: event.delta });
        break;
      case "TEXT_MESSAGE_END":
        dispatch({ type: "MESSAGE_END" });
        break;
      case "TOOL_CALL_START":
        dispatch({ type: "TOOL_START", toolCallId: event.tool_call_id, toolCallName: event.tool_call_name });
        break;
      case "TOOL_CALL_ARGS":
        dispatch({ type: "TOOL_ARGS", toolCallId: event.tool_call_id, delta: event.delta });
        break;
      case "TOOL_CALL_END":
        dispatch({ type: "TOOL_END", toolCallId: event.tool_call_id });
        break;
      case "RUN_FINISHED":
        dispatch({ type: "DONE" });
        dispatch({ type: "FILES_CHANGED" });
        if (state.sessionId) {
          const sid = state.sessionId;
          void refreshFiles(sid).catch(() => {});
          if (fileRetryTimerRef.current) clearTimeout(fileRetryTimerRef.current);
          fileRetryTimerRef.current = setTimeout(() => void refreshFiles(sid).catch(() => {}), 1500);
        }
        break;
      case "RUN_ERROR":
        dispatch({ type: "ERROR", message: event.message || "Something went wrong while generating the response. Please retry." });
        dispatch({ type: "FILES_CHANGED" });
        if (state.sessionId) {
          const sid = state.sessionId;
          void refreshFiles(sid).catch(() => {});
          if (fileRetryTimerRef.current) clearTimeout(fileRetryTimerRef.current);
          fileRetryTimerRef.current = setTimeout(() => void refreshFiles(sid).catch(() => {}), 1500);
        }
        break;
    }
  }, [refreshFiles, state.sessionId]);

  const handleSend = useCallback(
    async (content: string) => {
      if (!state.sessionId || state.isStreaming) return;

      dispatch({ type: "USER_SEND", content });

      abortRef.current?.abort();
      const controller = new AbortController();
      abortRef.current = controller;

      try {
        for await (const event of streamSSE(content, controller.signal, state.sessionId)) {
          handleAGUIEvent(event);
        }
        // Fallback: ensure streaming is closed if RUN_FINISHED was not received
        dispatch({ type: "DONE" });
      } catch (err: unknown) {
        if (err instanceof Error && err.name === "AbortError") return;
        dispatch({ type: "ERROR", message: friendlyError(err, "Message failed to send. Please try again.") });
      } finally {
        abortRef.current = null;
      }
    },
    [handleAGUIEvent, state.sessionId, state.isStreaming],
  );

  const handleChatUpload = useCallback(
    async (file: File, opts?: { announce?: boolean }) => {
      if (!state.sessionId) return;
      const tempId = crypto.randomUUID();
      setIsChatUploading(true);
      setChatUploadName(file.name);
      addPendingFile(file);
      dispatch({
        type: "APPEND_ASSISTANT",
        id: tempId,
        content: `Uploading and converting **${file.name}**... This can take 30–60 seconds for large files.`,
      });
      try {
        await withTimeout(uploadFile(state.sessionId, file), UPLOAD_TIMEOUT_MS, "Upload timed out");
        dispatch({ type: "FILES_CHANGED" });
        markUploadedFile(file.name);
        try {
          await refreshFiles(state.sessionId);
        } catch {
          // non-blocking; optimistic pending file remains visible
        }
        if (opts?.announce !== false) {
          dispatch({
            type: "UPDATE_ASSISTANT",
            id: tempId,
            content: `**${file.name}** is ready in the workspace. Ask me anything about it.`,
          });
        }
      } catch (err) {
        clearPendingFile(file.name);
        dispatch({
          type: "UPDATE_ASSISTANT",
          id: tempId,
          content: friendlyError(err, "Could not upload the file. Please try again."),
        });
      } finally {
        setIsChatUploading(false);
        setChatUploadName(null);
      }
    },
    [state.sessionId, addPendingFile, clearPendingFile, markUploadedFile, refreshFiles],
  );

  const handleAskAboutFile = useCallback(
    (filename: string) => {
      if (state.isStreaming) return;
      void handleSend(`Analyze "${filename}" and summarize key points, risks, and required actions.`);
    },
    [state.isStreaming, handleSend],
  );

  const handleOpenFile = useCallback(async (filename: string) => {
    if (!state.sessionId) return;
    setSelectedArtifact(filename);
    setArtifactLoading(true);
    setArtifactError(null);
    setArtifactContent("");
    try {
      let lastErr: unknown;
      for (let attempt = 0; attempt < 4; attempt++) {
        if (attempt > 0) await new Promise<void>((r) => setTimeout(r, attempt * 1000));
        try {
          const data = await getFileContent(state.sessionId, filename);
          setArtifactContent(data.content);
          setArtifactMimeType(data.mime_type);
          return;
        } catch (err) {
          lastErr = err;
        }
      }
      setArtifactMimeType(undefined);
      setArtifactError(friendlyError(lastErr, "Could not load artifact content."));
    } finally {
      setArtifactLoading(false);
    }
  }, [state.sessionId]);

  useEffect(() => {
    if (state.isStreaming || generatedFiles.length === 0 || selectedArtifact) return;
    const newest = generatedFiles[0]?.filename;
    if (!newest || lastAutoOpenedGenerated.current === newest) return;
    lastAutoOpenedGenerated.current = newest;
    void handleOpenFile(newest);
  }, [generatedFiles, state.isStreaming, selectedArtifact, handleOpenFile]);

  const agentWorking = state.isStreaming || isChatUploading;

  if (state.stage === "intake") {
    return (
      <IntakeScreen
        sessionState={sessionState}
        uploadState={uploadState}
        selectedFileName={selectedFileName}
        uploadError={uploadError}
        sessionError={sessionError}
        statusMessage={statusMessage}
        onUpload={handleIntakeUpload}
        onRetrySession={startSession}
      />
    );
  }

  return (
    <div className="relative flex h-screen flex-col overflow-hidden bg-app text-app-fg">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_60%_30%_at_50%_0%,rgba(79,133,255,.15),transparent_60%)]" />
      <header className="sticky top-0 z-10 border-b border-white/10 bg-black/50 shadow-[0_1px_0_0_rgba(255,255,255,0.06)] backdrop-blur-xl">
        <div className="flex w-full items-center gap-3 px-4 py-2.5 lg:px-6">
          <div className={`flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-[#5f92ff] to-[#3a6fd8] text-white shadow-[0_10px_24px_rgba(64,124,255,.45)] ring-1 ring-white/20 ${agentWorking ? "agent-working" : ""}`}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
            </svg>
          </div>
          <div className="min-w-0 flex-1">
            <p className="hidden text-[10px] font-semibold uppercase tracking-[0.22em] text-brand-strong/90 sm:block">MERIDIAN</p>
            <h1 className="truncate text-[15px] font-semibold tracking-[0.01em] text-white sm:text-[16px]">Proposal Workspace</h1>
          </div>

          <div className="hidden items-center gap-2 rounded-xl border border-white/20 bg-white/[0.03] px-2.5 py-1.5 text-[11px] text-app-muted md:flex">
            <span className={`h-1.5 w-1.5 rounded-full ${agentWorking ? "bg-brand" : "bg-emerald-400"}`} />
            <span>{agentWorking ? "Agent active" : "Ready"}</span>
            <span className="text-app-muted-strong">· {files.length} file{files.length === 1 ? "" : "s"}</span>
          </div>

          <button
            type="button"
            data-testid="new-chat-button"
            onClick={handleNewChat}
            disabled={state.isStreaming || state.isInitializing || isChatUploading}
            className="interactive-control inline-flex rounded-xl border border-brand/40 bg-brand/[0.08] px-3 py-2 text-xs font-medium text-brand-strong hover:bg-brand/15 hover:border-brand/55 disabled:cursor-not-allowed disabled:opacity-45"
          >
            New chat
          </button>

          <button
            type="button"
            onClick={() => setDocumentsOpen(true)}
            className="interactive-control rounded-xl border border-white/15 bg-white/5 px-3 py-2 text-xs text-app-fg lg:hidden"
          >
            Files ({files.length})
          </button>
        </div>
      </header>

      <div className="relative z-10 flex min-h-0 flex-1">
        <ArtifactsPanel
          uploadedFiles={uploadedFiles}
          generatedFiles={generatedFiles}
          loading={filesLoading}
          onOpenFile={handleOpenFile}
          disableActions={state.isStreaming}
        />

        <div className="flex min-h-0 flex-1">
          <div className={`flex min-h-0 flex-col transition-all duration-300 ${selectedArtifact ? "w-[360px] shrink-0" : "flex-1"}`}>
            <MessageList messages={state.messages} onSuggestion={state.isStreaming || state.isInitializing ? undefined : handleSend} />

            <InputBar
              onSend={handleSend}
              onUpload={handleChatUpload}
              disabled={state.isStreaming}
              isStreaming={state.isStreaming}
              onStop={handleStop}
              isUploadingFile={isChatUploading}
              uploadingFileName={chatUploadName}
            />
          </div>

          <ArtifactCanvas
            filename={selectedArtifact}
            mimeType={artifactMimeType}
            content={artifactContent}
            loading={artifactLoading}
            error={artifactError}
            onClose={() => setSelectedArtifact(null)}
          />
        </div>
      </div>

      <DocumentsDrawer
        open={documentsOpen}
        uploadedFiles={uploadedFiles}
        generatedFiles={generatedFiles}
        loading={filesLoading}
        onOpenFile={handleOpenFile}
        disableActions={state.isStreaming}
        onClose={() => setDocumentsOpen(false)}
      />

      {confirmNewChat && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm" onClick={() => setConfirmNewChat(false)}>
          <div className="w-full max-w-sm rounded-2xl border border-white/12 bg-[#0f1520] p-6 shadow-[0_24px_64px_rgba(0,0,0,0.6)]" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-base font-semibold text-app-fg">Start a new chat?</h2>
            <p className="mt-2 text-sm text-app-muted">This will clear your current messages and uploaded context.</p>
            <div className="mt-5 flex justify-end gap-2">
              <button type="button" onClick={() => setConfirmNewChat(false)} className="interactive-control rounded-xl border border-white/15 bg-white/5 px-4 py-2 text-sm text-app-fg">Cancel</button>
              <button type="button" onClick={() => { setConfirmNewChat(false); void doNewChat(); }} className="interactive-control rounded-xl border border-red-500/30 bg-red-500/15 px-4 py-2 text-sm font-medium text-red-300">Start new chat</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
