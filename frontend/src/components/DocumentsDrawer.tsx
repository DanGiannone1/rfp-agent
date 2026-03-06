"use client";

import type { FileInfo } from "@/lib/types";
import DocumentsList from "./DocumentsList";

interface DocumentsDrawerProps {
  open: boolean;
  uploadedFiles: FileInfo[];
  generatedFiles: FileInfo[];
  loading?: boolean;
  onAskFile?: (filename: string) => void;
  disableActions?: boolean;
  onAnalyzeUploaded?: () => void;
  onSummarizeArtifacts?: () => void;
  onClose: () => void;
}

export default function DocumentsDrawer({
  open,
  uploadedFiles,
  generatedFiles,
  loading = false,
  onAskFile,
  disableActions = false,
  onAnalyzeUploaded,
  onSummarizeArtifacts,
  onClose,
}: DocumentsDrawerProps) {
  return (
    <div
      data-testid="documents-drawer"
      role="dialog"
      aria-modal={open}
      aria-label="Workspace files"
      className={`fixed inset-0 z-40 transition-opacity duration-200 ${open ? "pointer-events-auto opacity-100" : "pointer-events-none opacity-0"}`}
      onKeyDown={(e) => { if (e.key === "Escape") onClose(); }}
    >
      <button
        type="button"
        aria-label="Close documents panel"
        onClick={onClose}
        className={`absolute inset-0 bg-black/50 backdrop-blur-[1px] transition-opacity duration-200 ${open ? "opacity-100" : "opacity-0"}`}
      />
      <div className={`absolute right-0 top-0 h-full w-full max-w-md border-l border-white/12 bg-[#070b13] p-4 shadow-[0_20px_60px_rgba(0,0,0,.45)] transition-transform duration-200 ease-out ${open ? "translate-x-0" : "translate-x-full"}`}>
        <div className="mb-3 flex items-center justify-between">
          <h2 className="inline-flex items-center gap-2 text-base font-semibold">
            <span className="h-1.5 w-1.5 rounded-full bg-brand/90" />
            Workspace Files
          </h2>
          <button
            type="button"
            onClick={onClose}
            className="interactive-control rounded-lg border border-white/15 bg-white/5 px-2 py-1 text-sm"
          >
            Close
          </button>
        </div>
        <div className="space-y-4">
          <section className="rounded-2xl border border-white/10 bg-gradient-to-b from-white/[0.04] to-white/[0.01] p-3">
            <div className="mb-2 flex items-center justify-between">
              <p className="text-xs font-medium text-app-muted-strong">Uploaded Documents</p>
              <span className="rounded-full border border-brand/40 bg-brand/15 px-2 py-0.5 text-[10px] text-brand-strong">
                {uploadedFiles.length}
              </span>
            </div>
            {uploadedFiles.length > 0 && (
              <button
                type="button"
                onClick={onAnalyzeUploaded}
                disabled={disableActions}
                className="interactive-control mb-2 w-full rounded-lg border border-white/14 bg-white/[0.04] px-2 py-1.5 text-left text-[11px] text-app-muted-strong disabled:cursor-not-allowed disabled:opacity-45"
              >
                Analyze uploaded docs
              </button>
            )}
            <DocumentsList files={uploadedFiles} loading={loading} onAskFile={onAskFile} disableActions={disableActions} />
          </section>
          <section className="rounded-2xl border border-white/10 bg-gradient-to-b from-white/[0.04] to-white/[0.01] p-3">
            <div className="mb-2 flex items-center justify-between">
              <p className="text-xs font-medium text-app-muted-strong">Generated Artifacts</p>
              <span className="rounded-full border border-brand/40 bg-brand/15 px-2 py-0.5 text-[10px] text-brand-strong">
                {generatedFiles.length}
              </span>
            </div>
            {generatedFiles.length > 0 && (
              <button
                type="button"
                onClick={onSummarizeArtifacts}
                disabled={disableActions}
                className="interactive-control mb-2 w-full rounded-lg border border-white/14 bg-white/[0.04] px-2 py-1.5 text-left text-[11px] text-app-muted-strong disabled:cursor-not-allowed disabled:opacity-45"
              >
                Summarize generated artifacts
              </button>
            )}
            {loading ? (
              <DocumentsList files={[]} loading />
            ) : generatedFiles.length === 0 ? (
              <div className="rounded-xl border border-white/10 bg-black/20 px-3 py-2 text-xs text-app-muted">
                No generated artifacts yet.
              </div>
            ) : (
              <DocumentsList files={generatedFiles} onAskFile={onAskFile} disableActions={disableActions} />
            )}
          </section>
        </div>
      </div>
    </div>
  );
}
