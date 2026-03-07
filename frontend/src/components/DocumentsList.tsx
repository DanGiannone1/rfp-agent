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

function fileExtension(filename: string): string {
  const dot = filename.lastIndexOf(".");
  return dot >= 0 ? filename.slice(dot + 1).toUpperCase() : "";
}

function FileIcon({ ext, className }: { ext: string; className?: string }) {
  return (
    <div className={`flex h-8 w-7 flex-col items-center justify-center rounded-[0.3rem] border border-white/12 bg-white/[0.04] text-[7px] font-bold uppercase leading-none tracking-wider text-app-muted-strong ${className || ""}`}>
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="mb-0.5 text-app-muted/60">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
      </svg>
      {ext && <span>{ext.slice(0, 4)}</span>}
    </div>
  );
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
    <div className="space-y-1">
      {files.map((file) => {
        const ext = fileExtension(file.filename);
        return (
          <div key={file.filename} data-testid="document-item" className="group flex items-center gap-2.5 rounded-lg px-2 py-1.5 transition-colors hover:bg-white/[0.04]">
            <FileIcon ext={ext} />
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-1.5">
                <span data-testid="document-name" className="min-w-0 truncate text-xs font-medium text-app-fg" title={file.filename}>{file.filename}</span>
                {kind === "uploaded" && file.has_markdown && (
                  <svg data-testid="conversion-done" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="shrink-0 text-emerald-400" aria-label="Converted">
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                )}
              </div>
              <div className="flex items-center gap-1.5">
                <span className="text-[10px] text-app-muted">{formatSize(file.size)}</span>
                <span className="text-[10px] text-app-muted/60">{formatRelativeTime(file.modified_at)}</span>
              </div>
            </div>
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
            </div>
          </div>
        );
      })}
    </div>
  );
}
