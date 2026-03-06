import { ToolActivity } from "@/lib/types";

interface ToolIndicatorProps {
  activity: ToolActivity;
}

function toolLabel(name: string): string {
  const labels: Record<string, string> = {
    search: "Searching",
    read_file: "Reading file",
    write_file: "Writing file",
    analyze: "Analyzing",
    summarize: "Summarizing",
    extract: "Extracting",
    compare: "Comparing",
    bash: "Running command",
    grep: "Searching workspace",
    glob: "Finding files",
    str_replace_editor: "Editing file",
    convert_document: "Converting document",
    knowledge_base_retrieve: "Searching knowledge base",
  };
  return labels[name] || name;
}

function toolContext(name: string, args: string | undefined): string | null {
  if (!args) return null;
  try {
    const p = JSON.parse(args);
    switch (name) {
      case "convert_document":
        return p.filename || null;
      case "grep":
        return p.pattern ? `"${String(p.pattern).slice(0, 40)}"` : null;
      case "glob":
        return p.pattern || null;
      case "bash":
        return typeof p.command === "string" ? p.command.slice(0, 50) : null;
      case "knowledge_base_retrieve":
        return p.query ? `"${String(p.query).slice(0, 50)}"` : null;
      case "str_replace_editor":
        return p.path || null;
      default:
        return null;
    }
  } catch {
    return null;
  }
}

export default function ToolIndicator({ activity }: ToolIndicatorProps) {
  const isRunning = activity.status === "running";
  const context = toolContext(activity.tool, activity.args);

  return (
    <div className={`tool-item ${isRunning ? "tool-item-running" : "tool-item-done"}`}>
      <div className="flex items-center gap-2 min-w-0">
        {isRunning ? (
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="animate-spin shrink-0">
            <path d="M21 12a9 9 0 1 1-6.219-8.56" />
          </svg>
        ) : (
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="shrink-0">
            <polyline points="20 6 9 17 4 12" />
          </svg>
        )}
        <span className="text-xs font-medium shrink-0">{toolLabel(activity.tool)}</span>
        {context && (
          <span className="truncate text-[11px] text-app-muted" title={context}>{context}</span>
        )}
        <span className="ml-auto shrink-0 text-[11px] text-app-muted">{isRunning ? "…" : "Done"}</span>
      </div>
    </div>
  );
}
