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


function FileIcon() {
  return (
    <div className="flex h-8 w-6 shrink-0 items-center justify-center rounded-[0.3rem] border border-white/10 bg-white/[0.04] text-app-muted group-hover:border-brand/30 group-hover:bg-white/[0.07] transition-colors duration-150">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
      </svg>
    </div>
  );
}

interface DocumentsListProps {
  files: FileInfo[];
  loading?: boolean;
  onOpenFile?: (filename: string) => void;
  disableActions?: boolean;
  kind?: "uploaded" | "generated";
  emptyLabel?: string;
}

export default function DocumentsList({
  files,
  loading = false,
  onOpenFile,
  disableActions = false,
  kind,
  emptyLabel,
}: DocumentsListProps) {
  if (loading) {
    return (
      <div className="space-y-2">
        {[0, 1, 2].map((idx) => (
          <div key={idx} className="loading-shimmer h-11 rounded-xl border border-white/10 bg-white/[0.03]" />
        ))}
      </div>
    );
  }

  if (files.length === 0) {
    return (
        <div className="rounded-xl border border-white/[0.12] bg-black/20 px-3 py-2 text-xs text-app-muted">
          {emptyLabel || "No documents attached yet."}
        </div>
      );
  }

  return (
    <div className="space-y-1">
      {files.map((file) => {
        const isClickable = !!onOpenFile && !disableActions;
        // For uploaded files that have been converted, open the markdown version
        const openTarget = kind === "uploaded" && file.has_markdown ? file.filename + ".md" : file.filename;
        return (
          <div
            key={file.filename}
            data-testid="document-item"
            role={isClickable ? "button" : undefined}
            tabIndex={isClickable ? 0 : undefined}
            onClick={isClickable ? () => onOpenFile(openTarget) : undefined}
            onKeyDown={isClickable ? (e) => { if (e.key === "Enter" || e.key === " ") onOpenFile(openTarget); } : undefined}
            title={isClickable ? "Open in canvas" : undefined}
            className={`group flex items-center gap-2.5 rounded-xl border px-2.5 py-2.5 transition-all ${
              isClickable
                ? "cursor-pointer border-white/[0.12] bg-white/[0.02] hover:border-brand/40 hover:bg-brand/[0.10] active:scale-[0.99]"
                : "border-white/[0.12] bg-white/[0.02]"
            }`}
          >
            <FileIcon />
            <div className="min-w-0 flex-1">
              <span data-testid="document-name" className="block min-w-0 truncate text-[13px] font-medium text-app-fg group-hover:text-white" title={file.filename}>{file.filename}</span>
              <div className="flex items-center gap-1.5 mt-1">
                <span className="text-[11px] text-app-muted">{formatSize(file.size)}</span>
                {file.modified_at && <span className="text-[11px] text-app-muted/70">{formatRelativeTime(file.modified_at)}</span>}
              </div>
            </div>
            {isClickable && (
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="shrink-0 text-app-muted/60 transition-colors group-hover:text-brand/80">
                <polyline points="9 18 15 12 9 6" />
              </svg>
            )}
          </div>
        );
      })}
    </div>
  );
}
