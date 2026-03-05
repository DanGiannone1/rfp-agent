"use client";

import { useState, useRef, useCallback, FormEvent, KeyboardEvent } from "react";

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
  const [isFocused, setIsFocused] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed && !selectedFile) return;

    if (selectedFile && onUpload) {
      onUpload(selectedFile);
      setSelectedFile(null);
      // If there's also text, send it as a separate message
      if (trimmed) {
        onSend(trimmed);
        setInput("");
        if (textareaRef.current) {
          textareaRef.current.style.height = "auto";
        }
      }
      return;
    }

    if (trimmed) {
      onSend(trimmed);
      setInput("");
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }

  const handleTextareaChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    // Auto-resize
    const el = e.target;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 192)}px`;
  }, []);

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) setSelectedFile(file);
    // Reset so re-selecting the same file triggers onChange
    e.target.value = "";
  }

  function removeFile() {
    setSelectedFile(null);
  }

  function handleDragOver(e: React.DragEvent) {
    e.preventDefault();
    setIsDragOver(true);
  }

  function handleDragLeave(e: React.DragEvent) {
    e.preventDefault();
    setIsDragOver(false);
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) setSelectedFile(file);
  }

  const canSend = input.trim() || selectedFile;

  return (
    <form
      onSubmit={handleSubmit}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`glass border-t transition-colors duration-200 ${
        isDragOver
          ? "border-indigo-500/50 bg-indigo-500/5"
          : "border-border-subtle"
      }`}
    >
      {/* File attachment chip */}
      {selectedFile && (
        <div className="mx-auto max-w-3xl px-4 pt-3 animate-slide-up">
          <span className="inline-flex items-center gap-2 rounded-lg bg-indigo-500/10 px-3 py-1.5 text-xs text-indigo-300 ring-1 ring-indigo-500/20 transition-all">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="shrink-0">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
            </svg>
            <span className="max-w-[200px] truncate">{selectedFile.name}</span>
            <span className="text-[10px] text-indigo-400/60">
              {(selectedFile.size / 1024).toFixed(0)} KB
            </span>
            <button
              type="button"
              onClick={removeFile}
              className="ml-0.5 rounded-full p-0.5 text-indigo-400/60 transition-colors hover:bg-white/10 hover:text-indigo-300"
              aria-label={`Remove file ${selectedFile.name}`}
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </span>
        </div>
      )}

      {/* Drag overlay hint */}
      {isDragOver && (
        <div className="mx-auto max-w-3xl px-4 pt-2 animate-fade-in">
          <p className="text-xs text-indigo-400">Drop file to attach</p>
        </div>
      )}

      <div className="mx-auto flex max-w-3xl items-end gap-2 px-4 py-3">
        <input
          ref={fileRef}
          type="file"
          accept={ACCEPTED_TYPES}
          onChange={handleFileChange}
          className="hidden"
          aria-label="Upload file"
        />

        {/* Attach button */}
        <button
          type="button"
          onClick={() => fileRef.current?.click()}
          disabled={disabled}
          title="Attach file"
          aria-label="Attach file"
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-zinc-700/50 bg-zinc-800/50 text-zinc-400 transition-all duration-200 hover:border-indigo-500/40 hover:bg-zinc-800 hover:text-indigo-400 disabled:opacity-40 disabled:pointer-events-none"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
          </svg>
        </button>

        {/* Textarea with glow effect */}
        <div
          className={`relative flex-1 rounded-2xl transition-all duration-200 ${
            isFocused ? "input-surface-focus" : ""
          }`}
        >
          <textarea
            ref={textareaRef}
            data-testid="chat-input"
            value={input}
            onChange={handleTextareaChange}
            onKeyDown={handleKeyDown}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Send a message..."
            disabled={disabled}
            rows={1}
            className="w-full resize-none rounded-2xl input-surface bg-transparent px-4 py-2.5 text-sm leading-relaxed text-zinc-100 outline-none placeholder:text-zinc-500 disabled:opacity-40 focus:border-transparent"
            style={{ minHeight: "2.5rem", maxHeight: "12rem" }}
            aria-label="Message input"
          />
        </div>

        {/* Send button */}
        <button
          data-testid="send-button"
          type="submit"
          disabled={disabled || !canSend}
          className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-white transition-all duration-200 ${
            canSend && !disabled
              ? "accent-gradient shadow-lg shadow-indigo-500/20 hover:shadow-indigo-500/30 hover:brightness-110 active:scale-95"
              : "bg-zinc-800 text-zinc-500 opacity-50"
          }`}
          aria-label="Send message"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
        </button>
      </div>

      {/* Keyboard hint */}
      <div className="mx-auto max-w-3xl px-4 pb-2">
        <p className="text-[10px] text-zinc-600">
          <kbd className="rounded border border-zinc-700/50 px-1 py-0.5 text-[10px] font-mono">Enter</kbd> to send
          {" / "}
          <kbd className="rounded border border-zinc-700/50 px-1 py-0.5 text-[10px] font-mono">Shift+Enter</kbd> for new line
        </p>
      </div>
    </form>
  );
}
