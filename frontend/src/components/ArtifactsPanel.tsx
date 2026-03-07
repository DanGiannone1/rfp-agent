"use client";

import type { FileInfo } from "@/lib/types";
import DocumentsList from "./DocumentsList";

interface ArtifactsPanelProps {
  uploadedFiles: FileInfo[];
  generatedFiles: FileInfo[];
  loading?: boolean;
  onAskFile?: (filename: string) => void;
  onOpenFile?: (filename: string) => void;
  disableActions?: boolean;
}

export default function ArtifactsPanel({
  uploadedFiles,
  generatedFiles,
  loading = false,
  onAskFile,
  onOpenFile,
  disableActions = false,
}: ArtifactsPanelProps) {
  return (
    <aside data-testid="artifacts-panel" className="hidden w-80 shrink-0 border-l border-white/10 bg-black/25 lg:flex lg:flex-col">
      {/* Uploaded documents — compact, top section */}
      <section className="border-b border-white/8 px-4 py-3">
        <div className="mb-2 flex items-center justify-between">
          <p className="text-[11px] font-medium uppercase tracking-[0.12em] text-app-muted">Source Documents</p>
          <span className="text-[10px] tabular-nums text-app-muted/70">{uploadedFiles.length}</span>
        </div>
        <DocumentsList
          files={uploadedFiles}
          loading={loading}
          onAskFile={onAskFile}
          onOpenFile={onOpenFile}
          disableActions={disableActions}
          kind="uploaded"
          emptyLabel="No documents uploaded."
        />
      </section>

      {/* Generated artifacts — remaining space */}
      <section className="flex min-h-0 flex-1 flex-col px-4 py-3">
        <div className="mb-2 flex items-center justify-between">
          <p className="text-[11px] font-medium uppercase tracking-[0.12em] text-app-muted">Generated Artifacts</p>
          <span className="text-[10px] tabular-nums text-app-muted/70">{generatedFiles.length}</span>
        </div>
        <div className="min-h-0 flex-1 overflow-y-auto">
          {loading ? (
            <DocumentsList files={[]} loading />
          ) : generatedFiles.length === 0 ? (
            <p className="py-6 text-center text-xs text-app-muted/60">
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
