"use client";

import { useRef, useState } from "react";

interface IntakeScreenProps {
  sessionState: "preparing" | "ready" | "error";
  uploadState: "idle" | "uploading";
  selectedFileName: string | null;
  uploadError: string | null;
  sessionError: string | null;
  statusMessage: string | null;
  onUpload: (file: File) => Promise<void>;
  onRetrySession: () => void;
}

const ACCEPTED_EXTENSIONS = [
  ".pdf", ".doc", ".docx", ".txt", ".csv", ".json", ".xml", ".md", ".xlsx", ".pptx", ".xls", ".rtf", ".html", ".htm",
];

function isAllowedFile(filename: string): boolean {
  const lower = filename.toLowerCase();
  return ACCEPTED_EXTENSIONS.some((ext) => lower.endsWith(ext));
}

export default function IntakeScreen({
  sessionState,
  uploadState,
  selectedFileName,
  uploadError,
  sessionError,
  statusMessage,
  onUpload,
  onRetrySession,
}: IntakeScreenProps) {
  const fileRef = useRef<HTMLInputElement>(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);

  const preparing = sessionState === "preparing";
  const ready = sessionState === "ready";
  const uploading = uploadState === "uploading";
  const busy = preparing || uploading;

  async function pickAndUpload(file: File | null) {
    if (!file) return;
    setLocalError(null);
    if (!isAllowedFile(file.name)) {
      setLocalError("This file type is not supported. Please upload PDF, DOCX, XLSX, TXT, CSV, JSON, XML, MD, PPTX, RTF, or HTML.");
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

  const activeStatus = localError || uploadError || sessionError || statusMessage;

  return (
    <main className="relative flex min-h-screen items-start pt-12 sm:items-center sm:pt-0 justify-center overflow-hidden bg-app p-4 text-app-fg">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_25%_15%,rgba(79,133,255,.15),transparent_38%)]" />

      <section className="relative z-10 w-full max-w-xl rounded-3xl border border-white/10 bg-white/[0.03] p-5 shadow-[0_30px_80px_rgba(0,0,0,.45)] backdrop-blur-xl md:p-8">
        <header className="mb-6">
          <p className="text-[13px] font-medium uppercase tracking-[0.16em] text-app-muted">Meridian & Associates</p>
          <h1 className="mt-2 text-2xl font-semibold md:text-3xl">Win more contracts, faster.</h1>
          <p className="mt-2 max-w-2xl text-sm text-app-muted-strong">
            Upload any RFP and the AI agent instantly generates compliance matrices, bid scoring, executive summaries, and risk analysis — all in one workspace.
          </p>
        </header>

        <div
          role="button"
          tabIndex={ready && !busy ? 0 : -1}
          aria-disabled={!ready || busy}
          aria-label="Upload RFP file"
          className={`rounded-2xl border-2 border-dashed py-10 px-6 text-center transition-all duration-200 md:py-14 md:px-8 ${
            isDragOver ? "border-brand bg-brand/10 scale-[1.02]" : "border-white/20 bg-black/20 scale-100"
          } ${!ready || busy ? "opacity-70" : "cursor-pointer"}`}
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

          <div className={`mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-[1.25rem] bg-brand/20 text-brand-strong ${preparing ? "agent-working" : ""}`}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
              <path d="M12 18v-6" />
              <path d="m9 15 3-3 3 3" />
            </svg>
          </div>

          <h2 className="text-lg font-medium">
            {preparing ? "Preparing your session..." : uploading ? "Converting document..." : "Drop an RFP file here"}
          </h2>
          <p className="mt-2 text-sm text-app-muted">
            {preparing
              ? "This usually takes a few seconds."
              : uploading
                ? selectedFileName ? `Processing ${selectedFileName}` : "Uploading and extracting content..."
                : "or click to choose from your device"}
          </p>
          {uploading && (
            <p className="mt-2 text-xs text-app-muted/70">Large documents can take 1–2 minutes to process.</p>
          )}
        </div>

        <p className="mt-2 text-[11px] text-app-muted/60">
            Accepts PDF, DOCX, XLSX, PPTX, TXT, CSV, JSON, XML, MD, RTF, HTML
          </p>
        <div className="mt-4 flex flex-wrap items-center gap-3 border-t border-white/8 pt-4">
          {["End-to-end encrypted", "Session-isolated sandbox", "Files auto-deleted after 24h", "SOC 2 Type II"].map((item) => (
            <span key={item} className="flex items-center gap-1.5 text-[11px] text-app-muted/60">
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="text-emerald-500/70"><polyline points="20 6 9 17 4 12"/></svg>
              {item}
            </span>
          ))}
        </div>

        {selectedFileName && (
          <p className="mt-3 text-xs text-app-muted">Selected file: <span className="text-app-fg">{selectedFileName}</span></p>
        )}

        {activeStatus && (
          <p className={`mt-4 rounded-xl border px-3 py-2 text-sm ${
            sessionError || uploadError || localError
              ? "border-red-500/30 bg-red-500/10 text-red-300"
              : "border-amber-500/30 bg-amber-500/10 text-amber-200"
          }`}>
            {activeStatus}
          </p>
        )}

        <div className="mt-5 flex justify-end">
          {(sessionError || sessionState === "error") && (
            <button
              type="button"
              data-testid="intake-retry-button"
              onClick={onRetrySession}
              className="rounded-xl border border-white/20 bg-white/5 px-4 py-2 text-sm font-semibold text-app-fg transition hover:bg-white/10"
            >
              Retry session setup
            </button>
          )}
        </div>
      </section>
    </main>
  );
}
