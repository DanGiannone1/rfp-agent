"use client";

import type { FileInfo } from "@/lib/types";

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function formatRelativeTime(iso: string): string {
  const ts = Date.parse(iso);
  if (Number.isNaN(ts)) return "";
  const diffMs = Date.now() - ts;
  const mins = Math.max(0, Math.floor(diffMs / 60000));
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

interface DocumentsListProps {
  files: FileInfo[];
  loading?: boolean;
  onAskFile?: (filename: string) => void;
  onOpenFile?: (filename: string) => void;
  disableActions?: boolean;
  kind?: "uploaded" | "generated";
  emptyLabel?: string;
}

export default function DocumentsList({
  files,
  loading = false,
  onAskFile,
  onOpenFile,
  disableActions = false,
  kind,
  emptyLabel,
}: DocumentsListProps) {
  if (loading) {
    return (
      <div className="space-y-2">
        {[0, 1, 2].map((idx) => (
          <div key={idx} className="loading-shimmer h-9 rounded-xl border border-white/10 bg-white/[0.03]" />
        ))}
      </div>
    );
  }

  if (files.length === 0) {
    return (
        <div className="rounded-xl border border-white/10 bg-black/20 px-3 py-2 text-xs text-app-muted">
          {emptyLabel || "No documents attached yet."}
        </div>
      );
  }

  return (
    <div className="space-y-2">
      {files.map((file) => (
        <div key={file.filename} data-testid="document-item" className="group rounded-xl border border-white/12 bg-white/[0.04] px-3 py-2 text-xs">
          <div className="flex items-center gap-2">
            <span data-testid="document-name" className="min-w-0 flex-1 truncate font-medium text-app-fg" title={file.filename}>{file.filename}</span>
            {kind === "generated" ? (
              <span className="shrink-0 rounded-full bg-emerald-500/15 px-2 py-0.5 text-[10px] font-medium text-emerald-300">Ready</span>
            ) : file.has_markdown ? (
              <span data-testid="conversion-done" className="shrink-0 rounded-full bg-emerald-500/15 px-2 py-0.5 text-[10px] font-medium text-emerald-300">Indexed</span>
            ) : (
              <span className="shrink-0 rounded-full bg-slate-500/20 px-2 py-0.5 text-[10px] font-medium text-slate-300">Uploaded</span>
            )}
          </div>
          <div className="mt-1 flex items-center gap-2">
            <span className="text-[10px] text-app-muted">{formatSize(file.size)}</span>
            <span className="text-[10px] text-app-muted/70">{formatRelativeTime(file.modified_at)}</span>
            <div className="flex items-center gap-1 opacity-0 transition-opacity group-hover:opacity-100">
              {onAskFile && (
                <button
                  type="button"
                  disabled={disableActions}
                  onClick={() => onAskFile(file.filename)}
                  className="interactive-control rounded-md border border-white/15 bg-white/[0.04] px-1.5 py-0.5 text-[10px] text-app-muted hover:text-app-fg disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Ask
                </button>
              )}
              {onOpenFile && (
                <button
                  type="button"
                  disabled={disableActions}
                  onClick={() => onOpenFile(file.filename)}
                  className="interactive-control rounded-md border border-white/15 bg-white/[0.04] px-1.5 py-0.5 text-[10px] text-app-muted hover:text-app-fg disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Open
                </button>
              )}
              <button
                type="button"
                disabled={disableActions}
                onClick={() => navigator.clipboard.writeText(file.filename)}
                className="interactive-control rounded-md border border-white/15 bg-white/[0.04] px-1.5 py-0.5 text-[10px] text-app-muted hover:text-app-fg disabled:cursor-not-allowed disabled:opacity-40"
              >
                Copy
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
