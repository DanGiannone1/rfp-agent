"use client";

import { useState, useRef, FormEvent } from "react";

interface InputBarProps {
  onSend: (message: string) => void;
  onUpload?: (file: File) => void;
  disabled: boolean;
}

const ACCEPTED_TYPES =
  ".pdf,.doc,.docx,.txt,.csv,.json,.xml,.md,.xlsx,.pptx,.xls,.rtf,.html,.htm";

export default function InputBar({ onSend, onUpload, disabled }: InputBarProps) {
  const [input, setInput] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (selectedFile && onUpload) {
      onUpload(selectedFile);
      setSelectedFile(null);
    }
    const trimmed = input.trim();
    if (!trimmed && !selectedFile) return;
    if (trimmed) {
      onSend(trimmed);
      setInput("");
    }
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) setSelectedFile(file);
    // Reset so re-selecting the same file triggers onChange
    e.target.value = "";
  }

  function removeFile() {
    setSelectedFile(null);
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="glass border-t border-border-subtle"
    >
      {selectedFile && (
        <div className="mx-auto max-w-3xl px-4 pt-2">
          <span className="inline-flex items-center gap-1.5 rounded-full bg-indigo-500/10 px-3 py-1 text-xs text-indigo-300 ring-1 ring-indigo-500/20">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
            </svg>
            {selectedFile.name}
            <button
              type="button"
              onClick={removeFile}
              className="ml-0.5 rounded-full p-0.5 hover:bg-white/10"
            >
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </span>
        </div>
      )}
      <div className="mx-auto flex max-w-3xl gap-2 px-4 py-3">
        <input
          ref={fileRef}
          type="file"
          accept={ACCEPTED_TYPES}
          onChange={handleFileChange}
          className="hidden"
        />
        <button
          type="button"
          onClick={() => fileRef.current?.click()}
          disabled={disabled}
          title="Attach file"
          className="flex items-center justify-center rounded-full border border-zinc-700/50 bg-zinc-800/50 p-2 text-zinc-400 transition-colors hover:border-indigo-500/50 hover:text-indigo-400 disabled:opacity-50"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
          </svg>
        </button>
        <input
          data-testid="chat-input"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Send a message..."
          disabled={disabled}
          className="flex-1 rounded-full border border-zinc-700/50 bg-zinc-800/50 px-4 py-2 text-sm text-zinc-100 outline-none placeholder:text-zinc-500 focus:border-indigo-500/50 focus:ring-2 focus:ring-indigo-500/20 disabled:opacity-50"
        />
        <button
          data-testid="send-button"
          type="submit"
          disabled={disabled || (!input.trim() && !selectedFile)}
          className="accent-gradient rounded-full px-4 py-2 text-sm font-medium text-white shadow-lg shadow-indigo-500/20 transition-all hover:brightness-110 disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </form>
  );
}
