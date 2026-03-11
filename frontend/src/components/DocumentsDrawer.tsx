"use client";

import type { AppFile } from "@/lib/types";
import DocumentsList from "./DocumentsList";

interface DocumentsDrawerProps {
  open: boolean;
  uploadedFiles: AppFile[];
  generatedFiles: AppFile[];
  loading?: boolean;
  onOpenFile?: (filename: string) => void;
  disableActions?: boolean;
  onClose: () => void;
}

export default function DocumentsDrawer({
  open,
  uploadedFiles,
  generatedFiles,
  loading = false,
  onOpenFile,
  disableActions = false,
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
        className={`absolute inset-0 bg-app/60 backdrop-blur-[1px] transition-opacity duration-200 ${open ? "opacity-100" : "opacity-0"}`}
      />
      <div className={`absolute right-0 top-0 flex h-full w-full max-w-md flex-col border-l border-border-subtle bg-surface-1 shadow-[0_20px_60px_rgba(0,0,0,.45)] transition-transform duration-200 ease-out ${open ? "translate-x-0" : "translate-x-full"}`}>
        <div className="flex items-center justify-between border-b border-border-subtle px-4 py-3">
          <h2 className="text-base font-semibold">Workspace Files</h2>
          <button
            type="button"
            onClick={onClose}
            className="interactive-control rounded-lg border border-border-subtle bg-surface-2 px-2 py-1 text-sm text-text-primary hover:bg-surface-2/80"
          >
            Close
          </button>
        </div>

        <section className="border-b border-border-subtle px-4 py-3">
          <div className="mb-2 flex items-center justify-between">
            <p className="text-[11px] font-medium uppercase tracking-[0.12em] text-text-secondary">Source Documents</p>
            <span className="text-[10px] tabular-nums text-text-muted">{uploadedFiles.length}</span>
          </div>
          <DocumentsList
            files={uploadedFiles}
            loading={loading}
            onOpenFile={onOpenFile}
            disableActions={disableActions}
            kind="uploaded"
            emptyLabel="No documents uploaded."
          />
        </section>

        <section className="flex min-h-0 flex-1 flex-col px-4 py-3">
          <div className="mb-2 flex items-center justify-between">
            <p className="text-[11px] font-medium uppercase tracking-[0.12em] text-text-secondary">Generated Artifacts</p>
            <span className="text-[10px] tabular-nums text-text-muted">{generatedFiles.length}</span>
          </div>
          <div className="min-h-0 flex-1 overflow-y-auto">
            {loading ? (
              <DocumentsList files={[]} loading />
            ) : generatedFiles.length === 0 ? (
              <p className="py-6 text-center text-xs text-text-muted">
                Artifacts will appear here as the agent generates deliverables.
              </p>
            ) : (
              <DocumentsList files={generatedFiles} onOpenFile={onOpenFile} disableActions={disableActions} kind="generated" />
            )}
          </div>
        </section>
      </div>
    </div>
  );
}
