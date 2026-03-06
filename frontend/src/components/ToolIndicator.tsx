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
    grep: "Searching code",
    glob: "Finding files",
    str_replace_editor: "Editing file",
    convert_document: "Converting document",
    knowledge_base_retrieve: "Searching knowledge base",
  };
  return labels[name] || name;
}

export default function ToolIndicator({ activity }: ToolIndicatorProps) {
  const isRunning = activity.status === "running";

  return (
    <div className={`tool-item ${isRunning ? "tool-item-running" : "tool-item-done"}`}>
      <div className="flex items-center gap-2">
        {isRunning ? (
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="animate-spin shrink-0">
            <path d="M21 12a9 9 0 1 1-6.219-8.56" />
          </svg>
        ) : (
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="shrink-0">
            <polyline points="20 6 9 17 4 12" />
          </svg>
        )}
        <span className="text-xs font-medium">{toolLabel(activity.tool)}</span>
        <span className="ml-auto text-[11px] text-app-muted">{isRunning ? "In progress" : "Done"}</span>
      </div>
    </div>
  );
}
