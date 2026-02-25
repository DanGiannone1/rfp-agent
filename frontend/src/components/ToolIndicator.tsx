import { ToolActivity } from "@/lib/types";

interface ToolIndicatorProps {
  activity: ToolActivity;
}

export default function ToolIndicator({ activity }: ToolIndicatorProps) {
  const isRunning = activity.status === "running";

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium ${
        isRunning
          ? "shimmer-bg animate-shimmer text-amber-300 ring-1 ring-amber-500/20"
          : "bg-emerald-500/15 text-emerald-400"
      }`}
    >
      {isRunning ? (
        <span className="relative flex h-1.5 w-1.5">
          <span className="absolute inline-flex h-full w-full animate-glow-pulse rounded-full bg-amber-400 opacity-75" />
          <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-amber-400" />
        </span>
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
      {activity.tool}
      <span className="text-[10px] opacity-70">
        {isRunning ? "running" : "done"}
      </span>
    </span>
  );
}
