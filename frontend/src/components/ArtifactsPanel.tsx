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
    <aside data-testid="artifacts-panel" className="hidden w-80 shrink-0 border-l border-white/10 bg-black/25 p-4 lg:flex lg:flex-col lg:gap-4">
      <div>
        <p className="inline-flex items-center gap-1.5 text-[11px] font-medium uppercase tracking-[0.14em] text-app-muted">
          <span className="h-1.5 w-1.5 rounded-full bg-brand/90" />
          Workspace Files
        </p>
      </div>

      <section className="rounded-2xl border border-white/10 bg-gradient-to-b from-white/[0.04] to-white/[0.01] p-3">
        <div className="mb-2 flex items-center justify-between">
          <p className="text-xs font-medium text-app-muted-strong">Uploaded Documents</p>
          <span className="rounded-full border border-brand/40 bg-brand/15 px-2 py-0.5 text-[10px] text-brand-strong">
            {uploadedFiles.length}
          </span>
        </div>
        <DocumentsList
          files={uploadedFiles}
          loading={loading}
          onAskFile={onAskFile}
          onOpenFile={onOpenFile}
          disableActions={disableActions}
          kind="uploaded"
          emptyLabel="No source documents uploaded."
        />
      </section>

      <section className="rounded-2xl border border-white/10 bg-gradient-to-b from-white/[0.04] to-white/[0.01] p-3">
        <div className="mb-2 flex items-center justify-between">
          <p className="text-xs font-medium text-app-muted-strong">Generated Artifacts</p>
          <span className="rounded-full border border-brand/40 bg-brand/15 px-2 py-0.5 text-[10px] text-brand-strong">
            {generatedFiles.length}
          </span>
        </div>
        {loading ? (
          <DocumentsList files={[]} loading />
        ) : generatedFiles.length === 0 ? (
          <div className="rounded-xl border border-white/10 bg-black/20 px-3 py-2 text-xs text-app-muted">
            No generated artifacts yet.
          </div>
        ) : (
          <DocumentsList files={generatedFiles} onOpenFile={onOpenFile} disableActions={disableActions} kind="generated" />
        )}
      </section>
    </aside>
  );
}
