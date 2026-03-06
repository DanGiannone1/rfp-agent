"use client";

import { useState, useRef, useCallback, FormEvent, KeyboardEvent } from "react";

interface InputBarProps {
  onSend: (message: string) => void;
  onUpload?: (file: File, opts?: { announce?: boolean }) => Promise<void>;
  disabled: boolean;
  isStreaming?: boolean;
  onStop?: () => void;
  isUploadingFile?: boolean;
  uploadingFileName?: string | null;
}

const ACCEPTED_TYPES =
  ".pdf,.doc,.docx,.txt,.csv,.json,.xml,.md,.xlsx,.pptx,.xls,.rtf,.html,.htm";

export default function InputBar({
  onSend,
  onUpload,
  disabled,
  isStreaming,
  onStop,
  isUploadingFile,
  uploadingFileName,
}: InputBarProps) {
  const [input, setInput] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [localUploading, setLocalUploading] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const uploadBusy = localUploading || Boolean(isUploadingFile);

  function resetInputHeight() {
    if (textareaRef.current) textareaRef.current.style.height = "auto";
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed && !selectedFile) return;

    if (selectedFile && onUpload) {
      setLocalUploading(true);
      await onUpload(selectedFile, { announce: !trimmed });
      setSelectedFile(null);
      setLocalUploading(false);
      if (!trimmed) return;
    }

    if (trimmed) {
      onSend(trimmed);
      setInput("");
      resetInputHeight();
    }
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      void handleSubmit(e);
    }
  }

  const handleTextareaChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    const el = e.target;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
  }, []);

  const canSend = Boolean(input.trim() || selectedFile);

  return (
    <form
      onSubmit={(e) => void handleSubmit(e)}
      className="sticky bottom-0 border-t border-white/10 bg-[linear-gradient(180deg,rgba(5,7,12,.7)_0%,rgba(5,7,12,.98)_42%)] backdrop-blur-xl"
    >
      <div className="mx-auto w-full max-w-4xl px-4 pb-[calc(max(env(safe-area-inset-bottom),0.75rem)+1.3rem)] pt-2.5 sm:pb-[calc(max(env(safe-area-inset-bottom),0.75rem)+0.9rem)] sm:pt-3">
        {(selectedFile || uploadBusy) && (
          <div className={`mb-2 inline-flex items-center gap-2 rounded-xl border border-brand/35 bg-brand/12 px-3 py-1.5 text-xs text-brand-strong ${uploadBusy ? "loading-shimmer" : ""}`}>
            <span className="max-w-[220px] truncate">{uploadingFileName || selectedFile?.name || "Uploading file"}</span>
            {uploadBusy ? (
              <span className="inline-flex items-center gap-1 text-brand/90">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="animate-spin">
                  <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                </svg>
                Uploading...
              </span>
            ) : (
              <>
                <span className="text-brand/80">{((selectedFile?.size || 0) / 1024).toFixed(0)} KB</span>
                <button
                  type="button"
                  onClick={() => setSelectedFile(null)}
                  className="rounded-md p-0.5 transition hover:bg-white/10"
                  aria-label={`Remove file ${selectedFile?.name || "selected file"}`}
                >
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                  </svg>
                </button>
              </>
            )}
          </div>
        )}

        <input
          ref={fileRef}
          type="file"
          accept={ACCEPTED_TYPES}
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) setSelectedFile(file);
            e.target.value = "";
          }}
          className="hidden"
          aria-label="Upload file"
        />

        <div className="flex items-end gap-2 rounded-3xl border border-white/20 bg-white/[0.05] p-2 shadow-[0_14px_36px_rgba(0,0,0,.35)]">
          <button
            type="button"
            onClick={() => fileRef.current?.click()}
            disabled={disabled || uploadBusy}
            aria-label="Attach file"
            className="interactive-control flex h-9 w-9 shrink-0 items-center justify-center rounded-2xl border border-white/10 bg-black/25 text-app-muted hover:text-app-fg disabled:cursor-not-allowed disabled:opacity-40"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
            </svg>
          </button>

          <textarea
            ref={textareaRef}
            data-testid="chat-input"
            value={input}
            onChange={handleTextareaChange}
            onKeyDown={handleKeyDown}
            placeholder="Ask for requirements, strategy, compliance, pricing..."
            disabled={disabled || uploadBusy}
            rows={1}
            className="min-h-9 max-h-52 flex-1 resize-none bg-transparent px-2 py-2 text-sm leading-relaxed text-app-fg outline-none placeholder:text-app-muted disabled:opacity-50"
            aria-label="Message input"
          />

          {isStreaming ? (
            <button
              data-testid="stop-button"
              type="button"
              onClick={onStop}
              className="interactive-control flex h-9 w-9 shrink-0 items-center justify-center rounded-2xl bg-amber-500/20 text-amber-300 hover:bg-amber-500/30"
              aria-label="Stop generation"
            >
              <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
                <rect x="4" y="4" width="16" height="16" rx="2" />
              </svg>
            </button>
          ) : (
            <button
              data-testid="send-button"
              type="submit"
              disabled={disabled || uploadBusy || !canSend}
              className="interactive-control flex h-9 w-9 shrink-0 items-center justify-center rounded-2xl bg-brand text-white hover:bg-brand-strong disabled:cursor-not-allowed disabled:bg-white/8 disabled:text-white/35"
              aria-label="Send message"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13" />
                <polygon points="22 2 15 22 11 13 2 9 22 2" />
              </svg>
            </button>
          )}
        </div>

      </div>
    </form>
  );
}
