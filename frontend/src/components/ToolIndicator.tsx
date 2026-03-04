import { ToolActivity } from "@/lib/types";

interface ToolIndicatorProps {
  activity: ToolActivity;
}

/** Map common tool names to descriptive labels */
function toolLabel(name: string): string {
  const labels: Record<string, string> = {
    search: "Searching",
    read_file: "Reading file",
    write_file: "Writing file",
    analyze: "Analyzing",
    summarize: "Summarizing",
    extract: "Extracting",
    compare: "Comparing",
  };
  // Use mapped label for running, plain name for done
  return labels[name] || name;
}

export default function ToolIndicator({ activity }: ToolIndicatorProps) {
  const isRunning = activity.status === "running";

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-lg px-2.5 py-1 text-xs font-medium transition-all duration-300 animate-scale-in ${
        isRunning
          ? "shimmer-bg animate-shimmer text-amber-300 ring-1 ring-amber-500/20"
          : "bg-emerald-500/10 text-emerald-400 ring-1 ring-emerald-500/10"
      }`}
    >
      {isRunning ? (
        <svg
          width="12"
          height="12"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="animate-spin-slow"
        >
          <path d="M21 12a9 9 0 1 1-6.219-8.56" />
        </svg>
      ) : (
        <svg
          width="12"
          height="12"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <polyline points="20 6 9 17 4 12" />
        </svg>
      )}
      <span>{isRunning ? toolLabel(activity.tool) : activity.tool}</span>
    </span>
  );
}
