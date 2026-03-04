"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { ChatMessage } from "@/lib/types";
import ToolIndicator from "./ToolIndicator";

interface MessageBubbleProps {
  message: ChatMessage;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";
  const isThinking =
    message.isStreaming &&
    message.content === "" &&
    message.toolActivity.length === 0;

  const hasTools = message.toolActivity.length > 0;
  const runningTools = message.toolActivity.filter((t) => t.status === "running");
  const doneTools = message.toolActivity.filter((t) => t.status === "done");
  const [toolsExpanded, setToolsExpanded] = useState(true);

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm transition-all duration-200 ${
          isUser
            ? "accent-gradient text-white shadow-lg shadow-indigo-500/10"
            : "bg-surface text-zinc-100 ring-1 ring-white/[0.06] shadow-sm"
        }`}
      >
        {/* Tool activity section */}
        {hasTools && (
          <div className="mb-3">
            {/* Toggle header for tool activity */}
            <button
              type="button"
              onClick={() => setToolsExpanded(!toolsExpanded)}
              className="mb-1.5 flex items-center gap-1.5 text-[11px] font-medium uppercase tracking-wider text-zinc-500 transition-colors hover:text-zinc-400"
              aria-expanded={toolsExpanded}
              aria-label={toolsExpanded ? "Collapse tool activity" : "Expand tool activity"}
            >
              <svg
                width="10"
                height="10"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                className={`transition-transform duration-200 ${toolsExpanded ? "rotate-90" : ""}`}
              >
                <polyline points="9 18 15 12 9 6" />
              </svg>
              {runningTools.length > 0 ? (
                <span>
                  {runningTools.length} tool{runningTools.length !== 1 ? "s" : ""} running
                  {doneTools.length > 0 && ` / ${doneTools.length} done`}
                </span>
              ) : (
                <span>{doneTools.length} tool{doneTools.length !== 1 ? "s" : ""} used</span>
              )}
            </button>

            {/* Collapsible tool list */}
            <div
              className="tool-activity-list"
              data-collapsed={!toolsExpanded}
            >
              <div>
                <div className="flex flex-wrap gap-1.5">
                  {message.toolActivity.map((ta, i) => (
                    <ToolIndicator key={`${ta.tool}-${i}`} activity={ta} />
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Thinking indicator */}
        {isThinking ? (
          <div className="flex items-center gap-3 py-1" role="status" aria-label="Agent is thinking">
            <div className="flex items-center gap-1">
              <span className="h-2 w-2 rounded-full bg-indigo-400 animate-typing-dot" />
              <span className="h-2 w-2 rounded-full bg-indigo-400 animate-typing-dot [animation-delay:0.2s]" />
              <span className="h-2 w-2 rounded-full bg-indigo-400 animate-typing-dot [animation-delay:0.4s]" />
            </div>
            <span className="text-sm text-zinc-500">Thinking...</span>
          </div>
        ) : (
          <div className="prose prose-sm max-w-none prose-p:my-1 prose-pre:my-2 prose-headings:mt-3 prose-headings:mb-1.5 prose-li:my-0.5 prose-ul:my-1 prose-ol:my-1">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.content}
            </ReactMarkdown>
            {/* Streaming cursor */}
            {message.isStreaming && message.content !== "" && (
              <span className="inline-flex items-center gap-0.5 ml-0.5 align-baseline" aria-hidden="true">
                <span className="inline-block h-4 w-0.5 rounded-full bg-indigo-400 animate-cursor-blink" />
              </span>
            )}
          </div>
        )}

        {/* Timestamp */}
        {message.timestamp && !message.isStreaming && (
          <div className="mt-2 text-[10px] text-zinc-600">
            {new Date(message.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
          </div>
        )}
      </div>
    </div>
  );
}
