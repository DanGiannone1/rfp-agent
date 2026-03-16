"use client";

import type { AppFile } from "@/lib/types";
import { formatSize, formatRelativeTime } from "@/lib/utils";

function RichPreview({ filename, size }: { filename: string; size: number }) {
  const isScore = filename.toLowerCase().includes("score");
  const isMatrix = filename.toLowerCase().includes("matrix");

  if (isScore) {
    return (
      <div className="mt-2 w-24">
        <div className="flex justify-between text-[9px] font-bold text-var(--color-text-muted) uppercase tracking-tighter mb-1">
          <span>Confidence</span>
          <span>84%</span>
        </div>
        <div className="preview-indicator">
          <div className="preview-indicator-fill" style={{ width: "84%" }} />
        </div>
      </div>
    );
  }

  if (isMatrix) {
    return (
      <div className="mt-2 flex items-center gap-1.5">
        <span className="px-1.5 py-0.5 rounded-md bg-var(--color-brand-success)/10 border border-var(--color-brand-success)/30 text-var(--color-brand-success) text-[9px] font-bold uppercase tracking-widest">Compliance Active</span>
      </div>
    );
  }

  return null;
}

interface DocumentsListProps {
  files: AppFile[];
  loading?: boolean;
  onOpenFile?: (filename: string) => void;
  disableActions?: boolean;
  kind?: "uploaded" | "generated";
  emptyLabel?: string;
}

function FileIcon({ filename, isActive }: { filename: string; isActive?: boolean }) {
  const isPdf = filename.toLowerCase().endsWith(".pdf");
  const isCsv = filename.toLowerCase().endsWith(".csv");
  const isMd = filename.toLowerCase().endsWith(".md");

  let color = "text-var(--color-text-muted)";
  let bg = "bg-var(--color-text-muted)/10";
  if (isPdf) { color = "text-var(--color-brand-primary)"; bg = "bg-var(--color-brand-primary)/10"; }
  if (isCsv) { color = "text-var(--color-brand-secondary)"; bg = "bg-var(--color-brand-secondary)/10"; }
  if (isMd) { color = "text-var(--color-brand-success)"; bg = "bg-var(--color-brand-success)/10"; }

  return (
    <div className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ${bg} ${color} relative transition-transform duration-300 group-hover:scale-110 shadow-sm`}>
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={isActive ? "2.5" : "2"} strokeLinecap="round" strokeLinejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
      </svg>
    </div>
  );
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
      <div className="space-y-2 px-1">
        {[0, 1, 2].map((idx) => (
          <div key={idx} className="loading-shimmer h-12 rounded-xl border border-var(--color-border-subtle)/40 bg-var(--color-surface-1)/40" />
        ))}
      </div>
    );
  }

  if (files.length === 0) {
    return (
        <div className="rounded-xl border border-var(--color-border-subtle)/40 bg-var(--color-app)/40 px-3 py-4 text-[10px] font-bold uppercase tracking-widest text-var(--color-text-muted) text-center italic">
          {emptyLabel || "No records."}
        </div>
      );
  }

  return (
    <div className="space-y-1">
      {files.map((file) => {
        const isClickable = !!onOpenFile && !disableActions;
        const openTarget = kind === "uploaded" && file.has_markdown ? file.filename + ".md" : file.filename;
        return (
          <div
            key={file.filename}
            data-testid="document-item"
            role={isClickable ? "button" : undefined}
            tabIndex={isClickable ? 0 : undefined}
            onClick={isClickable ? () => onOpenFile(openTarget) : undefined}
            onKeyDown={isClickable ? (e) => { if (e.key === "Enter" || e.key === " ") onOpenFile(openTarget); } : undefined}
            className={`group relative flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-500 overflow-hidden ${
              isClickable
                ? "cursor-pointer border-l-2 border-transparent hover:bg-var(--color-surface-2)/40 hover:backdrop-blur-sm shadow-sm"
                : "border-l-2 border-transparent opacity-80"
            }`}
          >
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-var(--color-text-primary)/5 to-transparent -translate-x-[100%] group-hover:translate-x-[100%] transition-transform duration-1000" />
            
            <FileIcon filename={file.filename} />
            
            <div className="min-w-0 flex-1 relative z-10">
              <span data-testid="document-name" className={`block min-w-0 truncate text-[13px] transition-colors ${isClickable ? 'text-var(--color-text-secondary) group-hover:text-var(--color-text-primary)' : 'text-[#8C847A]'}`} title={file.filename}>{file.filename}</span>
              <div className="flex items-center gap-2 mt-0.5">
                <span className="text-[10px] font-mono text-var(--color-text-muted)">{formatSize(file.size)}</span>
                {file.modified_at && <span className="text-[10px] font-mono text-var(--color-text-muted)/60">{formatRelativeTime(file.modified_at)}</span>}
                {kind === "uploaded" && (
                  file.has_markdown ? (
                    <span data-testid="conversion-done" className="rounded-full bg-brand-success/15 px-2 py-0.5 text-[10px] font-medium text-brand-success">Converted</span>
                  ) : (
                    <span data-testid="conversion-converting" className="rounded-full bg-brand-warning/15 px-2 py-0.5 text-[10px] font-medium text-brand-warning">Converting...</span>
                  )
                )}
              </div>
              <RichPreview filename={file.filename} size={file.size} />
            </div>
            
            {isClickable && (
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="shrink-0 text-var(--color-text-muted)/40 transition-colors group-hover:text-var(--color-brand-primary) relative z-10">
                <polyline points="9 18 15 12 9 6" />
              </svg>
            )}
          </div>
        );
      })}
    </div>
  );
}
