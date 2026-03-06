"use client";

import { useReducer, useRef, useCallback, useEffect, useState, useMemo } from "react";
import { AGUIEvent, ChatMessage, FileInfo } from "@/lib/types";
import { streamSSE } from "@/lib/sse";
import { createSession, listFiles, uploadFile } from "@/lib/api";
import { clearSessionId, storeSessionId, storeMessages } from "@/lib/session";
import MessageList from "./MessageList";
import InputBar from "./InputBar";
import IntakeScreen from "./IntakeScreen";
import DocumentsDrawer from "./DocumentsDrawer";
import ArtifactsPanel from "./ArtifactsPanel";
import AgentActivityBar from "./AgentActivityBar";

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
  | { type: "APPEND_ASSISTANT"; content: string }
  | { type: "RESET_FOR_NEW_CHAT" };

interface State {
  messages: ChatMessage[];
  isStreaming: boolean;
  sessionId: string | null;
  isInitializing: boolean;
  fileRefreshKey: number;
  stage: ChatStage;
}

const SESSION_TIMEOUT_MS = 12_000;
const UPLOAD_TIMEOUT_MS = 30_000;

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
          },
          {
            id: `pending-${crypto.randomUUID()}`,
            role: "assistant",
            content: "",
            isStreaming: true,
            toolActivity: [],
          },
        ],
      };

    case "RUN_STARTED":
      return state;

    case "ASSISTANT_START": {
      if (state.messages.length > 0) {
        const msgs = [...state.messages];
        const last = msgs[msgs.length - 1];
        if (
          last.role === "assistant" &&
          last.isStreaming &&
          last.content === "" &&
          last.id.startsWith("pending-")
        ) {
          msgs[msgs.length - 1] = { ...last, id: action.messageId };
          return { ...state, messages: msgs };
        }
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
          },
        ],
      };
    }

    case "DELTA": {
      if (state.messages.length === 0) return state;
      const msgs = [...state.messages];
      const last = { ...msgs[msgs.length - 1] };
      last.content += action.delta;
      msgs[msgs.length - 1] = last;
      return { ...state, messages: msgs };
    }

    case "MESSAGE_END":
      return state;

    case "TOOL_START": {
      if (state.messages.length === 0) return state;
      const msgs = [...state.messages];
      const last = { ...msgs[msgs.length - 1] };
      last.toolActivity = [
        ...last.toolActivity,
        { tool: action.toolCallName, toolCallId: action.toolCallId, status: "running" },
      ];
      msgs[msgs.length - 1] = last;
      return { ...state, messages: msgs };
    }

    case "TOOL_ARGS": {
      if (state.messages.length === 0) return state;
      const msgs = [...state.messages];
      const last = { ...msgs[msgs.length - 1] };
      last.toolActivity = last.toolActivity.map((ta) =>
        ta.toolCallId === action.toolCallId
          ? { ...ta, args: (ta.args || "") + action.delta }
          : ta,
      );
      msgs[msgs.length - 1] = last;
      return { ...state, messages: msgs };
    }

    case "TOOL_END": {
      if (state.messages.length === 0) return state;
      const msgs = [...state.messages];
      const last = { ...msgs[msgs.length - 1] };
      last.toolActivity = last.toolActivity.map((ta) =>
        ta.toolCallId === action.toolCallId ? { ...ta, status: "done" as const } : ta,
      );
      msgs[msgs.length - 1] = last;
      return { ...state, messages: msgs };
    }

    case "DONE": {
      const msgs = [...state.messages];
      if (msgs.length > 0 && msgs[msgs.length - 1].role === "assistant") {
        const last = { ...msgs[msgs.length - 1] };
        last.isStreaming = false;
        last.toolActivity = last.toolActivity.map((ta) =>
          ta.status === "running" ? { ...ta, status: "done" as const } : ta,
        );
        msgs[msgs.length - 1] = last;
      }
      return { ...state, messages: msgs, isStreaming: false };
    }

    case "ERROR": {
      const msgs = [...state.messages];
      if (msgs.length > 0 && msgs[msgs.length - 1].role === "assistant") {
        const last = { ...msgs[msgs.length - 1] };
        last.content += `\n\n${action.message}`;
        last.isStreaming = false;
        msgs[msgs.length - 1] = last;
      } else {
        msgs.push({
          id: crypto.randomUUID(),
          role: "assistant",
          content: action.message,
          isStreaming: false,
          toolActivity: [],
        });
      }
      return { ...state, messages: msgs, isStreaming: false };
    }

    case "APPEND_ASSISTANT":
      return {
        ...state,
        messages: [
          ...state.messages,
          {
            id: crypto.randomUUID(),
            role: "assistant",
            content: action.content,
            isStreaming: false,
            toolActivity: [],
          },
        ],
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
  const [uploadState, setUploadState] = useState<"idle" | "uploading" | "processing">("idle");
  const [sessionState, setSessionState] = useState<"preparing" | "ready" | "error">("preparing");
  const [chatUploadName, setChatUploadName] = useState<string | null>(null);
  const [isChatUploading, setIsChatUploading] = useState(false);
  const [hasFetchedFiles, setHasFetchedFiles] = useState(false);
  const [serverFiles, setServerFiles] = useState<FileInfo[]>([]);
  const [pendingFiles, setPendingFiles] = useState<FileInfo[]>([]);
  const [documentsOpen, setDocumentsOpen] = useState(false);
  const abortRef = useRef<AbortController | null>(null);
  const files = useMemo(() => mergeVisibleFiles(serverFiles, pendingFiles), [serverFiles, pendingFiles]);
  const latestAssistantMessage = useMemo(
    () => [...state.messages].reverse().find((m) => m.role === "assistant") || null,
    [state.messages],
  );
  const uploadedNameSet = useMemo(
    () => new Set([...uploadedFileNames, ...pendingFiles.map((f) => f.filename)]),
    [uploadedFileNames, pendingFiles],
  );
  const uploadedFiles = useMemo(() => files.filter((f) => uploadedNameSet.has(f.filename)), [files, uploadedNameSet]);
  const generatedFiles = useMemo(() => files.filter((f) => !uploadedNameSet.has(f.filename)), [files, uploadedNameSet]);
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
    clearSessionId();
    setSessionError(null);
    setUploadError(null);
    setStatusMessage(null);
    setSessionState("preparing");
    setServerFiles([]);
    setPendingFiles([]);
    setHasFetchedFiles(false);
    setUploadedFileNames([]);
    dispatch({ type: "SET_INITIALIZING", value: true });

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
  }, []);

  useEffect(() => {
    startSession();
  }, [startSession]);

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
    } else if (isUploading || uploadState === "processing") {
      timer = setTimeout(() => {
        setStatusMessage("Still processing your file. This can take a bit for large documents.");
      }, 12000);
    } else {
      setStatusMessage(null);
    }

    return () => {
      if (timer) clearTimeout(timer);
    };
  }, [state.isInitializing, isUploading, uploadState, sessionError, uploadError]);

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
        await withTimeout(uploadFile(state.sessionId, file), UPLOAD_TIMEOUT_MS, "Upload timed out");
        setUploadState("processing");
        dispatch({ type: "FILES_CHANGED" });
        setUploadedFileName(file.name);
        markUploadedFile(file.name);
        try {
          await refreshFiles(state.sessionId);
        } catch {
          // non-blocking; optimistic pending file remains visible
        }
        await new Promise((resolve) => setTimeout(resolve, 550));
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

  const handleNewChat = useCallback(async () => {
    const hasActiveContext = state.messages.length > 0 || Boolean(uploadedFileName) || files.length > 0;
    if (hasActiveContext && typeof window !== "undefined") {
      const ok = window.confirm("Start a new chat? This will clear current messages and uploaded context.");
      if (!ok) return;
    }

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
    dispatch({ type: "RESET_FOR_NEW_CHAT" });

    await startSession();
  }, [state.messages.length, uploadedFileName, files.length, startSession]);

  const handleStop = useCallback(() => {
    if (!state.isStreaming) return;
    abortRef.current?.abort();
    abortRef.current = null;
    dispatch({ type: "DONE" });
    dispatch({ type: "APPEND_ASSISTANT", content: "_Generation stopped by user._" });
  }, [state.isStreaming]);

  function handleAGUIEvent(event: AGUIEvent) {
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
        break;
      case "RUN_ERROR":
        dispatch({ type: "ERROR", message: event.message || "Something went wrong while generating the response. Please retry." });
        break;
    }
  }

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
    [state.sessionId, state.isStreaming],
  );

  const handleChatUpload = useCallback(
    async (file: File, opts?: { announce?: boolean }) => {
      if (!state.sessionId) return;
      setIsChatUploading(true);
      setChatUploadName(file.name);
      addPendingFile(file);
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
          dispatch({ type: "APPEND_ASSISTANT", content: `Uploaded **${file.name}**. Ready for your next instruction.` });
        }
      } catch (err) {
        clearPendingFile(file.name);
        dispatch({ type: "ERROR", message: friendlyError(err, "Could not upload the file. Please try again.") });
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

  const handleAnalyzeUploaded = useCallback(() => {
    if (state.isStreaming || uploadedFiles.length === 0) return;
    const names = uploadedFiles.map((f) => `"${f.filename}"`).join(", ");
    void handleSend(`Analyze the uploaded documents ${names}. Provide key requirements, risks, and next actions in a concise matrix.`);
  }, [state.isStreaming, uploadedFiles, handleSend]);

  const handleSummarizeArtifacts = useCallback(() => {
    if (state.isStreaming || generatedFiles.length === 0) return;
    const names = generatedFiles.map((f) => `"${f.filename}"`).join(", ");
    void handleSend(`Summarize generated artifacts ${names}. Explain what each file is for and what should be reviewed by humans.`);
  }, [state.isStreaming, generatedFiles, handleSend]);

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
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_12%_0%,rgba(63,124,255,.12),transparent_28%),radial-gradient(circle_at_85%_0%,rgba(20,184,166,.08),transparent_24%),linear-gradient(180deg,#070b13_0%,#05070c_40%)]" />
      <header className="sticky top-0 z-10 border-b border-white/10 bg-black/35 backdrop-blur-xl">
        <div className="flex w-full items-center gap-3 px-4 py-3 lg:px-6">
          <div className={`flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-brand to-cyan-400 text-white shadow-[0_10px_24px_rgba(64,124,255,.45)] ring-1 ring-white/20 ${agentWorking ? "agent-working" : ""}`}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
          </div>
          <div className="min-w-0 flex-1">
            <p className="hidden text-[10px] font-semibold uppercase tracking-[0.16em] text-brand-strong/90 sm:block">Meridian Platform</p>
            <h1 className="truncate text-[15px] font-semibold tracking-[0.01em] text-white sm:text-[16px]">Agentic RFP Response System</h1>
            <p className="hidden truncate text-xs text-app-muted sm:block">Pursuit Copilot Workspace</p>
          </div>

          <div className="hidden items-center gap-2 rounded-xl border border-white/12 bg-white/[0.03] px-2.5 py-1.5 text-[11px] text-app-muted lg:flex">
            <span className={`h-1.5 w-1.5 rounded-full ${agentWorking ? "bg-brand" : "bg-emerald-400"}`} />
            <span className="text-app-muted-strong">Session {state.sessionId ? state.sessionId.slice(0, 6) : "-----"}</span>
            <span>{agentWorking ? "Working" : "Idle"}</span>
            <span className="text-app-muted-strong">{files.length} file{files.length === 1 ? "" : "s"}</span>
          </div>

          <button
            type="button"
            data-testid="new-chat-button"
            onClick={handleNewChat}
            disabled={state.isStreaming || state.isInitializing || isChatUploading}
            className="interactive-control hidden rounded-xl border border-white/15 bg-white/5 px-3 py-2 text-xs text-app-fg lg:inline-flex disabled:cursor-not-allowed disabled:opacity-45"
          >
            New chat
          </button>

          <button
            type="button"
            onClick={handleNewChat}
            disabled={state.isStreaming || state.isInitializing || isChatUploading}
            className="interactive-control rounded-xl border border-white/15 bg-white/5 px-3 py-2 text-xs text-app-fg lg:hidden disabled:cursor-not-allowed disabled:opacity-45"
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
        <div className="flex min-h-0 flex-1 flex-col">
          <AgentActivityBar
            isStreaming={state.isStreaming}
            toolActivity={latestAssistantMessage?.toolActivity || []}
          />
          <MessageList messages={state.messages} onSuggestion={state.isStreaming ? undefined : handleSend} />

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

        <ArtifactsPanel
          uploadedFiles={uploadedFiles}
          generatedFiles={generatedFiles}
          loading={filesLoading}
          onAskFile={handleAskAboutFile}
          disableActions={state.isStreaming}
          onAnalyzeUploaded={handleAnalyzeUploaded}
          onSummarizeArtifacts={handleSummarizeArtifacts}
        />
      </div>

      <DocumentsDrawer
        open={documentsOpen}
        uploadedFiles={uploadedFiles}
        generatedFiles={generatedFiles}
        loading={filesLoading}
        onAskFile={handleAskAboutFile}
        disableActions={state.isStreaming}
        onAnalyzeUploaded={handleAnalyzeUploaded}
        onSummarizeArtifacts={handleSummarizeArtifacts}
        onClose={() => setDocumentsOpen(false)}
      />
    </div>
  );
}
