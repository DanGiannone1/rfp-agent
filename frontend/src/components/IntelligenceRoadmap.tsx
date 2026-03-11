"use client";

import { CheckCircle2, Activity, Terminal, ChevronDown, ChevronRight } from "lucide-react";
import { useState } from "react";
import { MessagePart } from "@/lib/types";

function toolLabelForStatus(name: string, status: "running" | "done"): string {
  const normalized = name.includes("-") ? name.substring(name.indexOf("-") + 1) : name;
  const labels: Record<string, Record<string, string>> = {
    running: {
      search: "Searching", read_file: "Reading unit", write_file: "Writing artifact", 
      knowledge_base_retrieve: "Searching vault", bash: "Executing command"
    },
    done: {
      search: "Search complete", read_file: "Read complete", write_file: "Artifact written",
      knowledge_base_retrieve: "Vault search complete", bash: "Command executed"
    },
  };
  return labels[status][normalized] || labels[status][name] || normalized;
}

function toolContext(name: string, args: string | undefined): string | null {
  if (!args) return null;
  try {
    const p = JSON.parse(args);
    switch (name) {
      case "grep": return p.pattern || null;
      case "glob": return p.pattern || null;
      case "bash": return p.command || null;
      case "knowledge_base_retrieve": return p.query || null;
      case "read_file": return p.path || null;
      case "write_file": return p.path || null;
      default: return null;
    }
  } catch { return null; }
}

export default function IntelligenceRoadmap({ parts, isStreaming }: { parts: (MessagePart & { type: "tool_call" })[]; isStreaming: boolean }) {
  const [expanded, setExpanded] = useState(true);
  const allDone = parts.every((p) => p.status === "done");
  const canCollapse = allDone && !isStreaming && parts.length > 1;
  const isExpanded = canCollapse ? expanded : true;

  return (
    <div className="tool-group">
      <button
        type="button"
        className="tool-group-toggle"
        onClick={() => setExpanded(!expanded)}
        aria-expanded={isExpanded}
      >
        {isExpanded ? <ChevronDown size={14} strokeWidth={3} /> : <ChevronRight size={14} strokeWidth={3} />}
        <Terminal size={14} className="text-brand-primary" />
        <span>Execution Log ({parts.length})</span>
      </button>
      
      {isExpanded && (
        <div className="roadmap-container px-2 py-3">
          {parts.map((part) => {
            const isRunning = part.status === "running";
            const ctx = toolContext(part.tool, part.args);
            return (
              <div key={part.toolCallId} className={`roadmap-step ${isRunning ? "roadmap-step-active" : "roadmap-step-done"}`}>
                <div className={`inline-tool-icon ${isRunning ? "inline-tool-icon-running" : "inline-tool-icon-done"}`}>
                  {isRunning ? <Activity size={12} className="animate-pulse" /> : <CheckCircle2 size={12} />}
                </div>
                <div className="flex flex-col min-w-0">
                  <span className="roadmap-label">{toolLabelForStatus(part.tool, part.status)}</span>
                  {ctx && <span className="inline-tool-context" title={ctx}>{ctx}</span>}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
