"use client";

import { useState, useCallback } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import { ChatMessage } from "@/lib/types";
import ToolIndicator from "./ToolIndicator";
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

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";
  const isThinking = message.isStreaming && message.content === "" && message.toolActivity.length === 0;

  const hasTools = message.toolActivity.length > 0;
  const runningTools = message.toolActivity.filter((t) => t.status === "running");
  const doneTools = message.toolActivity.filter((t) => t.status === "done");
  const [toolsExpanded, setToolsExpanded] = useState(false);
  const showToolHeader = hasTools;

  return (
    <article className={`message-row ${isUser ? "message-row-user" : "message-row-assistant"}`} data-testid={isUser ? "user-message" : "assistant-message"}>
      {!isUser && (
        <div className="message-avatar message-avatar-assistant">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="m12 2 2.4 5.1L20 9.2l-4 3.8.9 5.8L12 16.3 7.1 18.8 8 13 4 9.2l5.6-2.1z" />
          </svg>
        </div>
      )}

      <div className={`message-body ${isUser ? "message-body-user" : "message-body-assistant"}`}>
        {showToolHeader && (
          <div className="mb-3">
            <button
              type="button"
              onClick={() => setToolsExpanded(!toolsExpanded)}
              className="tool-toggle"
              aria-expanded={toolsExpanded}
              aria-label={toolsExpanded ? "Collapse tool activity" : "Expand tool activity"}
            >
              <span className="tool-toggle-indicator">✦</span>
              <span>
                {toolsExpanded ? "Hide thinking" : "Show thinking"}
                {runningTools.length > 0 && <span className="text-app-muted"> · Live</span>}
                {runningTools.length === 0 && doneTools.length > 0 && <span className="text-app-muted"> · Complete</span>}
              </span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={`ml-auto transition-transform ${toolsExpanded ? "rotate-180" : ""}`}>
                <polyline points="6 9 12 15 18 9" />
              </svg>
            </button>

            <div className="tool-activity-list" data-collapsed={!toolsExpanded}>
              <div>
                <div className="mt-2 flex flex-col gap-1.5">
                  {message.toolActivity.map((ta) => (
                    <ToolIndicator key={ta.toolCallId} activity={ta} />
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {isThinking ? (
          <div className="thinking-row" data-testid="thinking-indicator" role="status" aria-label="Agent is thinking">
            <span className="thinking-label">Thinking</span>
            <span className="thinking-dots" aria-hidden="true">
              <span />
              <span />
              <span />
            </span>
          </div>
        ) : (
          <div className="prose prose-message">
            <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]} components={markdownComponents}>
              {message.content}
            </ReactMarkdown>
            {message.isStreaming && message.content !== "" && <span className="streaming-cursor" aria-hidden="true" />}
          </div>
        )}
      </div>
    </article>
  );
}
