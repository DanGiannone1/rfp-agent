"use client";

import type { FileInfo } from "@/lib/types";
import DocumentsList from "./DocumentsList";

interface ArtifactsPanelProps {
  uploadedFiles: FileInfo[];
  generatedFiles: FileInfo[];
  loading?: boolean;
  onOpenFile?: (filename: string) => void;
  disableActions?: boolean;
}

export default function ArtifactsPanel({
  uploadedFiles,
  generatedFiles,
  loading = false,
  onOpenFile,
  disableActions = false,
}: ArtifactsPanelProps) {
  return (
    <aside data-testid="artifacts-panel" className="hidden w-72 shrink-0 border-r border-white/10 bg-black/25 md:flex md:flex-col">
      {/* Uploaded documents — compact, top section */}
      <section className="border-b border-white/8 px-3 py-3">
        <div className="mb-2.5 flex items-center gap-2">
          <div className="flex h-5 w-5 items-center justify-center rounded-md bg-white/[0.06]">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-app-muted">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
            </svg>
          </div>
          <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-app-muted flex-1">Source Documents</p>
          {uploadedFiles.length > 0 && (
            <span className="rounded-full bg-white/[0.06] px-1.5 py-0.5 text-[10px] tabular-nums text-app-muted">{uploadedFiles.length}</span>
          )}
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

      {/* Generated artifacts — remaining space */}
      <section className="flex min-h-0 flex-1 flex-col px-3 py-3">
        <div className="mb-2.5 flex items-center gap-2">
          <div className="flex h-5 w-5 items-center justify-center rounded-md bg-white/[0.06]">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-brand/70">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
            </svg>
          </div>
          <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-app-muted flex-1">Generated Artifacts</p>
          {generatedFiles.length > 0 && (
            <span className="rounded-full bg-brand/20 px-1.5 py-0.5 text-[10px] tabular-nums font-semibold text-brand-strong">{generatedFiles.length}</span>
          )}
        </div>
        <div className="min-h-0 flex-1 overflow-y-auto">
          {loading ? (
            <DocumentsList files={[]} loading />
          ) : generatedFiles.length === 0 ? (
            <p className="py-6 text-center text-xs text-app-muted/50">
              Artifacts will appear here as the agent generates deliverables.
            </p>
          ) : (
            <DocumentsList files={generatedFiles} onOpenFile={onOpenFile} disableActions={disableActions} kind="generated" />
          )}
        </div>
      </section>
    </aside>
  );
}
