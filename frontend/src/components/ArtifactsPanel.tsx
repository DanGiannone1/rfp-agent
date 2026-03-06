"use client";

import type { FileInfo } from "@/lib/types";
import DocumentsList from "./DocumentsList";

interface ArtifactsPanelProps {
  uploadedFiles: FileInfo[];
  generatedFiles: FileInfo[];
  loading?: boolean;
  onAskFile?: (filename: string) => void;
  disableActions?: boolean;
  onAnalyzeUploaded?: () => void;
  onSummarizeArtifacts?: () => void;
}

export default function ArtifactsPanel({
  uploadedFiles,
  generatedFiles,
  loading = false,
  onAskFile,
  disableActions = false,
  onAnalyzeUploaded,
  onSummarizeArtifacts,
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
    </aside>
  );
}
