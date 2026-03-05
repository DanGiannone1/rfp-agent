"use client";

import { useReducer, useRef, useCallback, useEffect } from "react";
import { ChatMessage, SSEEvent } from "@/lib/types";
import { streamSSE } from "@/lib/sse";
import { createSession, getSession, uploadFile } from "@/lib/api";
import {
  getStoredSessionId,
  storeSessionId,
  clearSessionId,
} from "@/lib/session";
import MessageList from "./MessageList";
import InputBar from "./InputBar";
import DocumentPanel from "./DocumentPanel";

type Action =
  | { type: "USER_SEND"; content: string }
  | { type: "ASSISTANT_START" }
  | { type: "DELTA"; content: string }
  | { type: "STATUS"; status: string }
  | { type: "MESSAGE"; content: string }
  | { type: "TOOL_START"; tool: string }
  | { type: "TOOL_END"; tool: string }
  | { type: "DONE" }
  | { type: "ERROR"; message: string }
  | { type: "LOAD_HISTORY"; messages: ChatMessage[] }
  | { type: "SET_SESSION_ID"; sessionId: string }
  | { type: "SET_INITIALIZING"; value: boolean }
  | { type: "FILE_UPLOADED"; filename: string }
  | { type: "FILES_CHANGED" };

interface State {
  messages: ChatMessage[];
  isStreaming: boolean;
  sessionId: string | null;
  isInitializing: boolean;
  fileRefreshKey: number;
}

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "SET_SESSION_ID":
      return { ...state, sessionId: action.sessionId };

    case "SET_INITIALIZING":
      return { ...state, isInitializing: action.value };

    case "LOAD_HISTORY":
      return { ...state, messages: action.messages };

    case "USER_SEND":
      return {
        ...state,
        messages: [
          ...state.messages,
          {
            id: crypto.randomUUID(),
            role: "user",
            content: action.content,
            isStreaming: false,
            toolActivity: [],
          },
        ],
        isStreaming: true,
      };

    case "ASSISTANT_START":
      return {
        ...state,
        messages: [
          ...state.messages,
          {
            id: crypto.randomUUID(),
            role: "assistant",
            content: "",
            isStreaming: true,
            toolActivity: [],
          },
        ],
      };

    case "DELTA": {
      const msgs = [...state.messages];
      const last = { ...msgs[msgs.length - 1] };
      last.content += action.content;
      msgs[msgs.length - 1] = last;
      return { ...state, messages: msgs };
    }

    case "STATUS": {
      const msgs = [...state.messages];
      const last = { ...msgs[msgs.length - 1] };
      if (action.status.startsWith("tool:")) {
        const tool = action.status.slice(5);
        // Mark any previously running tools as done
        const activity = last.toolActivity.map((ta) =>
          ta.status === "running" ? { ...ta, status: "done" as const } : ta,
        );
        // Add the new tool as running (if not already tracked)
        const alreadyTracked = activity.some(
          (ta) => ta.tool === tool && ta.status === "running",
        );
        if (!alreadyTracked) {
          activity.push({ tool, status: "running" });
        }
        last.toolActivity = activity;
      } else {
        // Non-tool status (e.g. "thinking", "idle") — mark all running tools as done
        last.toolActivity = last.toolActivity.map((ta) =>
          ta.status === "running" ? { ...ta, status: "done" as const } : ta,
        );
      }
      msgs[msgs.length - 1] = last;
      return { ...state, messages: msgs };
    }

    case "MESSAGE": {
      const msgs = [...state.messages];
      const last = { ...msgs[msgs.length - 1] };
      last.content = action.content;
      // Mark all remaining running tools as done
      last.toolActivity = last.toolActivity.map((ta) =>
        ta.status === "running" ? { ...ta, status: "done" as const } : ta,
      );
      msgs[msgs.length - 1] = last;
      return { ...state, messages: msgs };
    }

    case "TOOL_START": {
      const msgs = [...state.messages];
      const last = { ...msgs[msgs.length - 1] };
      last.toolActivity = [
        ...last.toolActivity,
        { tool: action.tool, status: "running" },
      ];
      msgs[msgs.length - 1] = last;
      return { ...state, messages: msgs };
    }

    case "TOOL_END": {
      const msgs = [...state.messages];
      const last = { ...msgs[msgs.length - 1] };
      last.toolActivity = last.toolActivity.map((ta) =>
        ta.tool === action.tool && ta.status === "running"
          ? { ...ta, status: "done" as const }
          : ta,
      );
      msgs[msgs.length - 1] = last;
      return { ...state, messages: msgs };
    }

    case "DONE": {
      const msgs = [...state.messages];
      const last = { ...msgs[msgs.length - 1] };
      last.isStreaming = false;
      msgs[msgs.length - 1] = last;
      return { ...state, messages: msgs, isStreaming: false };
    }

    case "ERROR": {
      const msgs = [...state.messages];
      if (msgs.length > 0 && msgs[msgs.length - 1].role === "assistant") {
        const last = { ...msgs[msgs.length - 1] };
        last.content += `\n\n**Error:** ${action.message}`;
        last.isStreaming = false;
        msgs[msgs.length - 1] = last;
      }
      return { ...state, messages: msgs, isStreaming: false };
    }

    case "FILES_CHANGED":
      return { ...state, fileRefreshKey: state.fileRefreshKey + 1 };

    case "FILE_UPLOADED":
      return {
        ...state,
        messages: [
          ...state.messages,
          {
            id: crypto.randomUUID(),
            role: "user",
            content: `Uploaded: **${action.filename}**`,
            isStreaming: false,
            toolActivity: [],
          },
        ],
      };

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
};

export default function Chat() {
  const [state, dispatch] = useReducer(reducer, initialState);
  const abortRef = useRef<AbortController | null>(null);

  // Initialise or restore session on mount
  useEffect(() => {
    let cancelled = false;

    async function init() {
      const stored = getStoredSessionId();

      if (stored) {
        try {
          const data = await getSession(stored);
          if (cancelled) return;

          if (data.status === "active") {
            dispatch({ type: "SET_SESSION_ID", sessionId: stored });

            // Convert persisted messages to ChatMessage[]
            const history: ChatMessage[] = data.messages.map((m) => ({
              id: crypto.randomUUID(),
              role: m.role,
              content: m.content,
              isStreaming: false,
              toolActivity: (m.tool_activity || []).map((ta) => ({
                tool: ta.tool,
                status: ta.status,
              })),
              timestamp: m.timestamp,
            }));
            dispatch({ type: "LOAD_HISTORY", messages: history });
            dispatch({ type: "SET_INITIALIZING", value: false });
            return;
          }
        } catch {
          // Session gone — fall through to create new
        }
        clearSessionId();
      }

      // Create a fresh session
      try {
        const meta = await createSession();
        if (cancelled) return;
        storeSessionId(meta.session_id);
        dispatch({ type: "SET_SESSION_ID", sessionId: meta.session_id });
      } catch (err) {
        console.error("Failed to create session:", err);
      }

      if (!cancelled) {
        dispatch({ type: "SET_INITIALIZING", value: false });
      }
    }

    init();
    return () => {
      cancelled = true;
    };
  }, []);

  const handleNewChat = useCallback(async () => {
    // Abort any in-flight stream
    abortRef.current?.abort();
    abortRef.current = null;

    // Clear old session
    clearSessionId();

    dispatch({ type: "SET_INITIALIZING", value: true });
    dispatch({ type: "LOAD_HISTORY", messages: [] });

    try {
      const meta = await createSession();
      storeSessionId(meta.session_id);
      dispatch({ type: "SET_SESSION_ID", sessionId: meta.session_id });
    } catch (err) {
      console.error("Failed to create session:", err);
    }

    dispatch({ type: "SET_INITIALIZING", value: false });
  }, []);

  const handleSend = useCallback(
    async (content: string) => {
      dispatch({ type: "USER_SEND", content });
      dispatch({ type: "ASSISTANT_START" });

      const controller = new AbortController();
      abortRef.current = controller;

      try {
        for await (const event of streamSSE(
          content,
          controller.signal,
          state.sessionId!,
        )) {
          handleSSEEvent(event);
        }
        dispatch({ type: "DONE" });
      } catch (err: unknown) {
        if (err instanceof Error && err.name === "AbortError") return;
        dispatch({
          type: "ERROR",
          message: err instanceof Error ? err.message : "Unknown error",
        });
      } finally {
        abortRef.current = null;
      }
    },
    [state.sessionId],
  );

  const handleUpload = useCallback(
    async (file: File) => {
      if (!state.sessionId) return;
      try {
        const result = await uploadFile(state.sessionId, file);
        dispatch({ type: "FILE_UPLOADED", filename: result.filename });
        dispatch({ type: "FILES_CHANGED" });

        let autoPrompt: string;
        if (result.markdown_ready) {
          autoPrompt = `I've uploaded "${result.filename}" for analysis. The document has been converted to markdown (${result.filename}.md) for analysis. Please read the document and confirm what you see — summarize the RFP title, issuing organization, key dates, and scope of work. Then list the workflow options available (bid/no-bid analysis, requirements extraction, response strategy, etc.) so I know what I can ask for next.`;
        } else {
          const errorNote = result.processing_error
            ? ` (${result.processing_error})`
            : "";
          autoPrompt = `I've uploaded "${result.filename}" but document conversion to markdown failed${errorNote}. The original file is in the workspace. Please attempt to work with it directly and let me know what you find.`;
        }
        handleSend(autoPrompt);
      } catch (err) {
        dispatch({
          type: "ERROR",
          message: err instanceof Error ? err.message : "Upload failed",
        });
      }
    },
    [state.sessionId, handleSend],
  );

  function handleSSEEvent(event: SSEEvent) {
    switch (event.type) {
      case "delta":
        dispatch({ type: "DELTA", content: event.content });
        break;
      case "status":
        dispatch({ type: "STATUS", status: event.status });
        break;
      case "message":
        dispatch({ type: "MESSAGE", content: event.content });
        break;
      case "tool_start":
        dispatch({ type: "TOOL_START", tool: event.tool });
        break;
      case "tool_end":
        dispatch({ type: "TOOL_END", tool: event.tool });
        break;
      case "done":
        dispatch({ type: "DONE" });
        break;
      case "error":
        dispatch({ type: "ERROR", message: event.message });
        break;
    }
  }

  return (
    <div className="flex h-screen flex-col bg-background text-foreground">
      {/* Header */}
      <header className="glass sticky top-0 z-10 border-b border-border-subtle">
        <div className="mx-auto flex max-w-3xl items-center gap-3 px-4 py-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg accent-gradient shadow-md shadow-indigo-500/10">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="text-white"
            >
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
          </div>
          <div className="flex-1">
            <h1 className="text-base font-semibold tracking-tight">RFP Agent</h1>
            <p className="text-[11px] text-zinc-500">Copilot SDK + Azure OpenAI</p>
          </div>

          {/* Streaming status indicator */}
          {state.isStreaming && (
            <div className="flex items-center gap-1.5 rounded-full bg-indigo-500/10 px-2.5 py-1 text-[11px] text-indigo-400 ring-1 ring-indigo-500/20 animate-fade-in">
              <span className="relative flex h-1.5 w-1.5">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-indigo-400 opacity-75" />
                <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-indigo-500" />
              </span>
              Processing
            </div>
          )}

          <button
            data-testid="new-chat-button"
            onClick={handleNewChat}
            disabled={state.isStreaming || state.isInitializing}
            className="flex items-center gap-1.5 rounded-lg border border-zinc-700/50 px-3 py-1.5 text-sm text-zinc-400 transition-all duration-200 hover:border-zinc-600 hover:bg-white/5 hover:text-zinc-200 disabled:pointer-events-none disabled:opacity-40 active:scale-[0.98]"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            New chat
          </button>
        </div>
      </header>

      {/* Main content */}
      {state.isInitializing ? (
        <div data-testid="initializing" className="flex flex-1 flex-col items-center justify-center gap-3 animate-fade-in">
          <div className="flex items-center gap-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="animate-spin-slow text-indigo-400">
              <path d="M21 12a9 9 0 1 1-6.219-8.56" />
            </svg>
            <p className="text-sm text-zinc-500">Starting session...</p>
          </div>
        </div>
      ) : (
        <>
          <DocumentPanel sessionId={state.sessionId} refreshKey={state.fileRefreshKey} />
          <MessageList messages={state.messages} onSuggestion={state.isStreaming ? undefined : handleSend} />
          <InputBar onSend={handleSend} onUpload={handleUpload} disabled={state.isStreaming} />
        </>
      )}
    </div>
  );
}
