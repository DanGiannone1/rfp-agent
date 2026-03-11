"use client";

import type { AppFile } from "@/lib/types";
import DocumentsList from "./DocumentsList";

interface ArtifactsPanelProps {
  uploadedFiles: AppFile[];
  generatedFiles: AppFile[];
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
    <aside data-testid="artifacts-panel" className="hidden w-64 shrink-0 bg-var(--color-surface-1)/70 backdrop-blur-2xl rounded-3xl border border-var(--color-border-subtle)/60 shadow-[0_8px_32px_rgba(0,0,0,0.5)] md:flex md:flex-col relative overflow-hidden">
      {/* Sidebar header decoration */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-var(--color-brand-primary)/5 to-transparent pointer-events-none" />

      {/* Uploaded documents — compact, top section */}
      <section className="border-b border-var(--color-border-subtle)/40 px-4 py-5">
        <div className="mb-4 flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-var(--color-brand-primary)/10 text-var(--color-brand-primary)">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
            </svg>
          </div>
          <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-var(--color-text-muted) flex-1">Sources</p>
          {uploadedFiles.length > 0 && (
            <span className="rounded-lg bg-var(--color-surface-2) border border-var(--color-border-subtle) px-2 py-0.5 text-[10px] font-mono text-var(--color-brand-primary)">{uploadedFiles.length}</span>
          )}
        </div>
        <DocumentsList
          files={uploadedFiles}
          loading={loading}
          onOpenFile={onOpenFile}
          disableActions={disableActions}
          kind="uploaded"
          emptyLabel="Upload RFP."
        />
      </section>

      {/* Generated artifacts — remaining space */}
      <section className="flex min-h-0 flex-1 flex-col px-4 py-5">
        <div className="mb-4 flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-var(--color-brand-success)/10 text-var(--color-brand-success)">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
              <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
              <line x1="12" y1="22.08" x2="12" y2="12" />
            </svg>
          </div>
          <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-var(--color-text-muted) flex-1">Outputs</p>
          {generatedFiles.length > 0 && (
            <span className="rounded-lg bg-var(--color-surface-2) border border-var(--color-border-subtle) px-2 py-0.5 text-[10px] font-mono text-var(--color-brand-success)">{generatedFiles.length}</span>
          )}
        </div>
        <div className="min-h-0 flex-1 overflow-y-auto custom-scrollbar">
          {loading ? (
            <DocumentsList files={[]} loading />
          ) : generatedFiles.length === 0 ? (
            <div className="flex flex-col items-center gap-3 py-12 opacity-40">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="text-var(--color-text-muted)">
                <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
              </svg>
              <p className="text-center text-[11px] font-bold uppercase tracking-widest text-var(--color-text-muted)">No deliverables<br/>generated yet.</p>
            </div>
          ) : (
            <DocumentsList files={generatedFiles} onOpenFile={onOpenFile} disableActions={disableActions} kind="generated" />
          )}
        </div>
      </section>

      {/* Profile/Footer Area */}
      <div className="p-4 border-t border-var(--color-border-subtle)/40">
        <div className="p-3 bg-var(--color-app)/60 backdrop-blur-md rounded-2xl border border-var(--color-border-subtle)/50 flex items-center gap-3 hover:bg-var(--color-surface-2)/80 transition-all duration-300 cursor-pointer shadow-inner group">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-var(--color-border-subtle) to-[#241F1C] border border-[#4D433C] flex items-center justify-center text-var(--color-text-primary) font-bold shadow-md group-hover:scale-105 transition-transform">
            N
          </div>
          <div className="flex flex-col flex-1">
            <span className="text-[12px] font-bold text-var(--color-text-primary)">Workspace</span>
            <span className="text-[10px] font-mono text-var(--color-text-muted)">v1.0.4-release</span>
          </div>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-var(--color-text-muted) group-hover:text-white group-hover:rotate-90 transition-all duration-500">
            <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" />
            <circle cx="12" cy="12" r="3" />
          </svg>
        </div>
      </div>
    </aside>
  );
}
