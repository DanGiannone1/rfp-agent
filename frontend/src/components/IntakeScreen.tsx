"use client";

import { useRef, useState } from "react";
import { IntakeState } from "@/lib/types";
import { ACCEPTED_EXTENSIONS } from "@/lib/constants";
import { isAllowedFile } from "@/lib/utils";
import GlassPanel from "./ui/GlassPanel";

interface IntakeScreenProps {
  intake: IntakeState;
  statusMessage: string | null;
  onUpload: (file: File) => Promise<void>;
  onRetrySession: () => void;
}

export default function IntakeScreen({
  intake,
  statusMessage,
  onUpload,
  onRetrySession,
}: IntakeScreenProps) {
  const fileRef = useRef<HTMLInputElement>(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);

  const preparing = intake.sessionState === "preparing";
  const ready = intake.sessionState === "ready";
  const uploading = intake.uploadState === "uploading";
  const busy = preparing || uploading;

  async function pickAndUpload(file: File | null) {
    if (!file) return;
    setLocalError(null);
    if (!isAllowedFile(file.name)) {
      setLocalError("Unsupported file type.");
      return;
    }
    await onUpload(file);
  }

  async function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setIsDragOver(false);
    if (!ready || busy) return;
    await pickAndUpload(e.dataTransfer.files?.[0] || null);
  }

  const activeStatus = localError || intake.error || statusMessage;

  return (
    <main className="relative flex min-h-screen items-center justify-center bg-app p-4 text-text-primary font-sans overflow-hidden">
      <div className="ambient-orb-1 animate-blob" />
      <div className="ambient-orb-2 animate-blob" />
      
      <GlassPanel variant="heavy" className="relative z-10 w-full max-w-2xl p-6 md:p-12 rounded-[2.5rem]">
        <header className="mb-10 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-primary/10 border border-brand-primary/20 mb-4">
            <span className="h-1.5 w-1.5 rounded-full bg-brand-primary animate-pulse" />
            <p className="text-[11px] font-bold uppercase tracking-[0.2em] text-brand-primary">Meridian & Associates</p>
          </div>
          <h1 className="mt-2 text-4xl font-black uppercase tracking-tight md:text-6xl text-text-primary">Win More.<br/>Faster.</h1>
          <p className="mx-auto mt-6 max-w-xl text-[15px] text-text-secondary leading-relaxed">
            Upload any RFP. Our intelligence engine instantly generates compliance matrices, scoring models, and strategic summaries in one premium workspace.
          </p>
        </header>

        <div
          role="button"
          tabIndex={ready && !busy ? 0 : -1}
          aria-disabled={!ready || busy}
          aria-label="Upload RFP file"
          className={`relative overflow-hidden border-2 border-dashed py-14 px-6 text-center transition-all duration-500 md:py-20 md:px-8 rounded-3xl ${
            isDragOver 
              ? "border-brand-primary bg-brand-primary/5 scale-[1.02] shadow-[0_0_40px_rgba(217,93,57,0.15)]" 
              : "border-border-subtle bg-app/40 scale-100 hover:border-brand-primary/50 hover:bg-surface-1/60"
          } ${!ready || busy ? "opacity-50" : "cursor-pointer"} shadow-inner group`}
          onClick={() => {
            if (!ready || busy) return;
            fileRef.current?.click();
          }}
          onKeyDown={(e) => {
            if (!ready || busy) return;
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              fileRef.current?.click();
            }
          }}
          onDragOver={(e) => {
            e.preventDefault();
            if (!ready || busy) return;
            setIsDragOver(true);
          }}
          onDragLeave={(e) => {
            e.preventDefault();
            setIsDragOver(false);
          }}
          onDrop={handleDrop}
        >
          <input
            ref={fileRef}
            type="file"
            accept={ACCEPTED_EXTENSIONS.join(",")}
            className="hidden"
            data-testid="intake-upload-input"
            onChange={async (e) => {
              await pickAndUpload(e.target.files?.[0] || null);
              e.target.value = "";
            }}
          />

          <div className={`mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-primary to-brand-warning text-white shadow-[0_0_30px_rgba(217,93,57,0.3)] relative ${preparing ? "agent-working" : ""}`}>
            <div className="absolute inset-0 bg-white/20 rounded-2xl blur-[2px]" />
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="relative z-10">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
              <path d="M12 18v-6" />
              <path d="m9 15 3-3 3 3" />
            </svg>
          </div>

          <h2 className="text-xl font-bold uppercase tracking-wide text-text-primary">
            {preparing ? "Booting Engine..." : uploading ? "Parsing Data..." : "Drop RFP Document"}
          </h2>
          <p className="mt-3 text-sm font-medium text-text-muted">
            {preparing ? "Initializing sandbox." : uploading ? "Extracting content..." : "or click to browse"}
          </p>
        </div>

        <div className="mt-10 flex flex-col items-center gap-5 border-t border-border-subtle pt-10 text-center">
          <p className="text-[11px] font-bold uppercase tracking-widest text-text-muted opacity-60">
            Accepts PDF, DOCX, XLSX, TXT, CSV, JSON, MD, RTF, HTML
          </p>
          <div className="flex flex-wrap items-center justify-center gap-6">
            {["Encrypted", "Isolated", "SOC 2 Type II"].map((item) => (
              <span key={item} className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-widest text-text-muted">
                <span className="h-1.5 w-1.5 rounded-full bg-brand-success shadow-[0_0_8px_rgba(122,155,118,0.5)]" />
                {item}
              </span>
            ))}
          </div>
        </div>

        {intake.filename && (
          <div className="mt-8 p-4 bg-app/60 rounded-2xl border border-brand-primary/20 flex items-center justify-center gap-3 animate-fade-in">
            <span className="text-[11px] font-bold text-text-muted uppercase tracking-widest">Target:</span>
            <span className="text-sm font-bold text-brand-primary truncate max-w-xs">{intake.filename}</span>
          </div>
        )}

        {activeStatus && (
          <div className="mt-6 border-l-2 border-brand-primary bg-brand-primary/5 p-4 rounded-r-xl">
            <p className="text-[13px] font-medium text-text-primary">{activeStatus}</p>
          </div>
        )}

        <div className="mt-8 flex justify-center">
          {(intake.error || intake.sessionState === "error") && (
            <button
              type="button"
              data-testid="intake-retry-button"
              onClick={onRetrySession}
              className="bg-brand-primary px-8 py-3 text-xs font-bold uppercase tracking-[0.2em] text-white hover:bg-brand-warning transition-all rounded-xl shadow-[0_4px_20px_rgba(217,93,57,0.3)] hover:scale-105 active:scale-95"
            >
              Retry Connection
            </button>
          )}
        </div>
      </GlassPanel>
    </main>
  );
}
