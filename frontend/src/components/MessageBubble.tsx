"use client";

import { useState, useCallback, useMemo } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import { ChatMessage, MessagePart } from "@/lib/types";
import type { Components } from "react-markdown";

interface MessageBubbleProps {
  message: ChatMessage;
}

function CodeBlock({ children, ...props }: React.ComponentPropsWithoutRef<"pre">) {
  const [copied, setCopied] = useState(false);

  const codeChild = Array.isArray(children)
    ? (children[0] as React.ReactElement<{ className?: string; children?: React.ReactNode }>)
    : (children as React.ReactElement<{ className?: string; children?: React.ReactNode }>);

  const codeClassName = codeChild?.props?.className || "";
  const langMatch = codeClassName.match(/language-(\w+)/);
  const language = langMatch ? langMatch[1] : "text";

  const handleCopy = useCallback(() => {
    const text = codeChild?.props?.children;
    if (typeof text === "string") {
      navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    }
  }, [codeChild]);

  return (
    <div className="code-block-wrapper">
      <div className="code-block-header">
        <span className="code-block-lang">{language}</span>
        <button type="button" onClick={handleCopy} className="code-block-copy" aria-label="Copy code">
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <pre {...props}>{children}</pre>
    </div>
  );
}

function TableWrapper({ children, ...props }: React.ComponentPropsWithoutRef<"table">) {
  return (
    <div className="table-wrapper">
      <table {...props}>{children}</table>
    </div>
  );
}

const markdownComponents: Components = {
  pre: CodeBlock,
  table: TableWrapper,
};

function toolLabelForStatus(name: string, status: "running" | "done"): string {
  const normalized = name.includes("-") ? name.substring(name.indexOf("-") + 1) : name;
  const labels: Record<string, Record<string, string>> = {
    running: {
      search: "Searching", read_file: "Reading file", write_file: "Writing file",
      view: "Reading file", analyze: "Analyzing", summarize: "Summarizing",
      extract: "Extracting", compare: "Comparing", bash: "Running command",
      grep: "Searching files", glob: "Finding files", str_replace_editor: "Editing file",
      knowledge_base_retrieve: "Searching knowledge base",
    },
    done: {
      search: "Searched", read_file: "Read file", write_file: "Wrote file",
      view: "Read file", analyze: "Analyzed", summarize: "Summarized",
      extract: "Extracted", compare: "Compared", bash: "Ran command",
      grep: "Searched files", glob: "Found files", str_replace_editor: "Edited file",
      knowledge_base_retrieve: "Searched knowledge base",
    },
  };
  return labels[status][normalized] || labels[status][name] || normalized;
}

function toolContext(name: string, args: string | undefined): string | null {
  if (!args) return null;
  try {
    const p = JSON.parse(args);
    switch (name) {
      case "grep": return p.pattern ? String(p.pattern).slice(0, 40) : null;
      case "glob": return p.pattern || null;
      case "bash": return typeof p.command === "string" ? p.command.slice(0, 50) : null;
      case "knowledge_base_retrieve": return p.query ? String(p.query).slice(0, 50) : null;
      case "str_replace_editor": return p.path || null;
      case "view": return p.path || null;
      case "read_file": return p.path || null;
      default: return null;
    }
  } catch { return null; }
}

function InlineToolCall({ part }: { part: MessagePart & { type: "tool_call" } }) {
  const isRunning = part.status === "running";
  const ctx = toolContext(part.tool, part.args);

  return (
    <div className={`inline-tool ${isRunning ? "inline-tool-running" : "inline-tool-done"}`}>
      <div className={`inline-tool-icon ${isRunning ? "inline-tool-icon-running" : "inline-tool-icon-done"}`}>
        {isRunning ? (
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="animate-spin">
            <path d="M21 12a9 9 0 1 1-6.219-8.56" />
          </svg>
        ) : (
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12" />
          </svg>
        )}
      </div>
      <span className="inline-tool-label">{toolLabelForStatus(part.tool, part.status)}</span>
      {ctx && <span className="inline-tool-context" title={ctx}>{ctx}</span>}
    </div>
  );
}

type RenderedSegment =
  | { kind: "text"; part: MessagePart & { type: "text" }; index: number }
  | { kind: "tool_group"; parts: (MessagePart & { type: "tool_call" })[]; startIndex: number };

function groupParts(parts: MessagePart[]): RenderedSegment[] {
  const segments: RenderedSegment[] = [];
  let toolBatch: (MessagePart & { type: "tool_call" })[] = [];
  let toolBatchStart = 0;

  for (let i = 0; i < parts.length; i++) {
    const part = parts[i];
    if (part.type === "tool_call") {
      if (toolBatch.length === 0) toolBatchStart = i;
      toolBatch.push(part);
    } else {
      if (toolBatch.length > 0) {
        segments.push({ kind: "tool_group", parts: toolBatch, startIndex: toolBatchStart });
        toolBatch = [];
      }
      segments.push({ kind: "text", part, index: i });
    }
  }
  if (toolBatch.length > 0) {
    segments.push({ kind: "tool_group", parts: toolBatch, startIndex: toolBatchStart });
  }
  return segments;
}

function ToolGroup({ parts, isStreaming }: { parts: (MessagePart & { type: "tool_call" })[]; isStreaming: boolean }) {
  const [expanded, setExpanded] = useState(true);
  const allDone = parts.every((p) => p.status === "done");
  const canCollapse = allDone && !isStreaming && parts.length > 2;
  const isExpanded = canCollapse ? expanded : true;
  const runningCount = parts.filter((p) => p.status === "running").length;

  return (
    <div className="tool-group">
      {canCollapse && (
        <button
          type="button"
          className="tool-group-toggle"
          onClick={() => setExpanded(!expanded)}
          aria-expanded={isExpanded}
        >
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="9 18 15 12 9 6" />
          </svg>
          <span>
            {isExpanded ? "Hide" : "Show"} {parts.length} step{parts.length === 1 ? "" : "s"}
          </span>
          {!isExpanded && (
            <span style={{ marginLeft: "auto", opacity: 0.5 }}>
              {runningCount > 0 ? `${runningCount} running` : "completed"}
            </span>
          )}
        </button>
      )}
      {isExpanded && parts.map((part) => (
        <InlineToolCall key={part.toolCallId} part={part} />
      ))}
    </div>
  );
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";
  const hasParts = message.parts.length > 0;
  const hasContent = hasParts && message.parts.some((p) => p.type === "text" && p.content !== "");
  const hasTools = hasParts && message.parts.some((p) => p.type === "tool_call");
  const isThinking = message.isStreaming && !hasContent && !hasTools;

  const segments = useMemo(() => groupParts(message.parts), [message.parts]);

  return (
    <article className={`message-row ${isUser ? "message-row-user" : "message-row-assistant"}`} data-testid={isUser ? "user-message" : "assistant-message"}>
      {!isUser && (
        <div className="message-avatar message-avatar-assistant">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <rect x="7" y="7" width="10" height="10" rx="1" />
            <path d="M7 9H5M7 12H5M7 15H5M17 9h2M17 12h2M17 15h2M9 7V5M12 7V5M15 7V5M9 17v2M12 17v2M15 17v2" />
          </svg>
        </div>
      )}

      <div className={`message-body ${isUser ? "message-body-user" : "message-body-assistant"}`}>
        {isThinking ? (
          <div className="thinking-row" data-testid="thinking-indicator" role="status" aria-label="Agent is thinking">
            <span className="thinking-label">Thinking</span>
            <span className="thinking-dots" aria-hidden="true">
              <span />
              <span />
              <span />
            </span>
          </div>
        ) : isUser ? (
          <div className="prose prose-message">
            <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]} components={markdownComponents}>
              {message.content}
            </ReactMarkdown>
          </div>
        ) : (
          <div className="message-parts">
            {segments.map((seg) => {
              if (seg.kind === "text") {
                if (seg.part.content === "") return null;
                const isLast = seg.index === message.parts.length - 1;
                return (
                  <div key={seg.index} className="prose prose-message">
                    <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]} components={markdownComponents}>
                      {seg.part.content}
                    </ReactMarkdown>
                    {message.isStreaming && isLast && <span className="streaming-cursor" aria-hidden="true" />}
                  </div>
                );
              }
              if (seg.kind === "tool_group") {
                return (
                  <ToolGroup
                    key={`tg-${seg.startIndex}`}
                    parts={seg.parts}
                    isStreaming={message.isStreaming}
                  />
                );
              }
              return null;
            })}
            {message.isStreaming && message.parts.length > 0 && message.parts[message.parts.length - 1]?.type === "tool_call" && (
              <div className="thinking-row mt-2" role="status" aria-label="Agent is thinking">
                <span className="thinking-label">Thinking</span>
                <span className="thinking-dots" aria-hidden="true">
                  <span />
                  <span />
                  <span />
                </span>
              </div>
            )}
          </div>
        )}
      </div>
    </article>
  );
}
