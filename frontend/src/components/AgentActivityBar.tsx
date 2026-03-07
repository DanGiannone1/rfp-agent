"use client";

import { useState } from "react";
import type { ToolActivity } from "@/lib/types";

interface AgentActivityBarProps {
  isStreaming: boolean;
  toolActivity: ToolActivity[];
}

function toolLabel(name: string): string {
  const normalized = name.includes("-") ? name.substring(name.indexOf("-") + 1) : name;
  const labels: Record<string, string> = {
    bash: "Running command",
    grep: "Searching workspace",
    glob: "Finding files",
    view: "Reading file",
    str_replace_editor: "Editing file",
    convert_document: "Converting document",
    knowledge_base_retrieve: "Searching knowledge base",
  };
  return labels[normalized] || labels[name] || normalized;
}

function toolContext(name: string, args: string | undefined): string | null {
  if (!args) return null;
  try {
    const p = JSON.parse(args);
    switch (name) {
      case "convert_document": return p.filename || null;
      case "grep": return p.pattern ? `"${String(p.pattern).slice(0, 40)}"` : null;
      case "glob": return p.pattern || null;
      case "bash": return typeof p.command === "string" ? p.command.slice(0, 50) : null;
      case "knowledge_base_retrieve": return p.query ? `"${String(p.query).slice(0, 50)}"` : null;
      case "str_replace_editor": return p.path || null;
      default: return null;
    }
  } catch { return null; }
}

export default function AgentActivityBar({ isStreaming, toolActivity }: AgentActivityBarProps) {
  const running = toolActivity.filter((t) => t.status === "running");
  const completed = toolActivity.filter((t) => t.status === "done");
  const hasActivity = isStreaming || toolActivity.length > 0;
  const [expanded, setExpanded] = useState(true);

  const statusText =
    running.length > 0
      ? `Working on ${running.length} step${running.length === 1 ? "" : "s"}`
      : isStreaming
        ? "Thinking..."
        : `Completed ${completed.length} step${completed.length === 1 ? "" : "s"}`;

  const visibleItems = toolActivity.slice(-4);
  const canToggle = visibleItems.length > 0;
  const isExpanded = running.length > 0 || isStreaming ? true : expanded;

  if (!hasActivity) return null;

  return (
    <section className="border-b border-white/10 bg-black/25 px-4 py-2">
      <div className="mx-auto w-full max-w-4xl">
        <div className="mb-2 flex items-center justify-between gap-2">
          <div className="inline-flex items-center gap-2 rounded-full border border-white/12 bg-white/[0.03] px-3 py-1 text-xs text-app-muted-strong">
            {running.length > 0 || isStreaming ? (
              <span className="inline-block h-2 w-2 animate-pulse rounded-full bg-brand" />
            ) : (
              <span className="inline-block h-2 w-2 rounded-full bg-emerald-400" />
            )}
            {statusText}
          </div>
          {canToggle && (
            <button
              type="button"
              onClick={() => setExpanded((v) => !v)}
              className="interactive-control rounded-md border border-white/12 bg-white/[0.03] px-2 py-1 text-[11px] text-app-muted"
              aria-expanded={isExpanded}
              aria-label={isExpanded ? "Collapse agent activity" : "Expand agent activity"}
            >
              {isExpanded ? "Hide" : "Show"}
            </button>
          )}
        </div>

        {isExpanded && visibleItems.length > 0 && (
          <div className="space-y-1">
            {visibleItems.map((item) => {
              const isRunning = item.status === "running";
              const ctx = toolContext(item.tool, item.args);
              return (
                <div key={item.toolCallId} className="flex min-w-0 items-center gap-2 text-xs text-app-muted">
                  {isRunning ? (
                    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="shrink-0 animate-spin text-brand">
                      <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                    </svg>
                  ) : (
                    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="shrink-0 text-emerald-300">
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                  )}
                  <span className="shrink-0">{toolLabel(item.tool)}</span>
                  {ctx && <span className="truncate text-app-muted/70">{ctx}</span>}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
}
