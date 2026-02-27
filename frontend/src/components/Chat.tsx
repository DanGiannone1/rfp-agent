"use client";

import { useReducer, useRef, useCallback, useEffect } from "react";
import { useIsAuthenticated, useMsal } from "@azure/msal-react";
import { ChatMessage, SSEEvent } from "@/lib/types";
import { authEnabled, loginRequest } from "@/lib/auth";
import { streamSSE } from "@/lib/sse";
import { createSession, getSession } from "@/lib/api";
import {
  getStoredSessionId,
  storeSessionId,
  clearSessionId,
} from "@/lib/session";
import MessageList from "./MessageList";
import InputBar from "./InputBar";

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
  | { type: "SET_INITIALIZING"; value: boolean };

interface State {
  messages: ChatMessage[];
  isStreaming: boolean;
  sessionId: string | null;
  isInitializing: boolean;
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

    default:
      return state;
  }
}

const initialState: State = {
  messages: [],
  isStreaming: false,
  sessionId: null,
  isInitializing: true,
};

export default function Chat() {
  const [state, dispatch] = useReducer(reducer, initialState);
  const abortRef = useRef<AbortController | null>(null);
  const isAuthenticated = useIsAuthenticated();
  const { instance } = useMsal();

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
          state.sessionId ?? undefined,
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

  // Gate: require login when Entra ID auth is configured
  if (authEnabled && !isAuthenticated) {
    return (
      <div className="flex h-screen flex-col items-center justify-center gap-6 bg-background text-foreground">
        <div className="flex h-14 w-14 items-center justify-center rounded-2xl accent-gradient shadow-lg shadow-indigo-500/20">
          <svg
            width="24"
            height="24"
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
        <h1 className="text-2xl font-semibold">RFP Agent</h1>
        <p className="text-sm text-zinc-500">Sign in to start your analysis</p>
        <button
          onClick={() => instance.loginRedirect(loginRequest)}
          className="accent-gradient rounded-full px-6 py-2.5 text-sm font-medium text-white shadow-lg shadow-indigo-500/20 transition-all hover:brightness-110"
        >
          Sign in with Microsoft
        </button>
      </div>
    );
  }

  return (
    <div className="flex h-screen flex-col bg-background text-foreground">
      <header className="glass sticky top-0 z-10 border-b border-border-subtle">
        <div className="mx-auto flex max-w-3xl items-center gap-3 px-4 py-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg accent-gradient">
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
            <h1 className="text-lg font-semibold">RFP Agent</h1>
            <p className="text-xs text-zinc-500">AI-powered analysis</p>
          </div>
          <button
            onClick={handleNewChat}
            disabled={state.isStreaming || state.isInitializing}
            className="rounded-lg border border-border-subtle px-3 py-1.5 text-sm text-zinc-400 transition-colors hover:bg-white/5 hover:text-zinc-200 disabled:pointer-events-none disabled:opacity-40"
          >
            New chat
          </button>
        </div>
      </header>
      {state.isInitializing ? (
        <div className="flex flex-1 items-center justify-center">
          <p className="text-sm text-zinc-500">Starting session...</p>
        </div>
      ) : (
        <>
          <MessageList messages={state.messages} />
          <InputBar onSend={handleSend} disabled={state.isStreaming} />
        </>
      )}
    </div>
  );
}
