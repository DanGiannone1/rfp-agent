"use client";

import { useState, useEffect, useRef } from "react";
import { listFiles } from "@/lib/api";
import type { FileInfo } from "@/lib/types";

interface DocumentPanelProps {
  sessionId: string | null;
  refreshKey: number;
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

/** How long (ms) a file without markdown is considered "converting" after upload */
const CONVERTING_WINDOW_MS = 120_000;

export default function DocumentPanel({ sessionId, refreshKey }: DocumentPanelProps) {
  const [files, setFiles] = useState<FileInfo[]>([]);
  const [open, setOpen] = useState(true);
  const [convertingNames, setConvertingNames] = useState<Set<string>>(new Set());
  const uploadTimestamps = useRef<Map<string, number>>(new Map());

  // Track when refreshKey bumps (i.e. a new file was uploaded)
  useEffect(() => {
    if (refreshKey > 0) {
      // We don't know the exact filename yet; we'll tag new files in the next tick
      uploadTimestamps.current.set(`__refresh_${refreshKey}`, Date.now());
    }
  }, [refreshKey]);

  // Single effect: fetch immediately, then poll every 10s while any file lacks markdown
  useEffect(() => {
    if (!sessionId) return;
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout>;

    async function tick() {
      try {
        const data = await listFiles(sessionId!);
        if (cancelled) return;
        const tickNow = Date.now();
        const originals = data.files.filter(
          (f) => !f.filename.endsWith(".md") || !data.files.some((o) => f.filename === `${o.filename}.md`),
        );
        // Tag any newly-seen files with a timestamp
        for (const f of originals) {
          if (!uploadTimestamps.current.has(f.filename)) {
            uploadTimestamps.current.set(f.filename, tickNow);
          }
        }
        // Compute which files are in the converting window (uses ref only inside effect)
        const converting = new Set<string>();
        for (const f of originals) {
          if (f.has_markdown) continue;
          const ts = uploadTimestamps.current.get(f.filename);
          if (ts && tickNow - ts < CONVERTING_WINDOW_MS) {
            converting.add(f.filename);
          }
        }
        setFiles(originals);
        setConvertingNames(converting);
        // Schedule next poll only if some file still lacks markdown
        if (originals.length > 0 && !originals.every((f) => f.has_markdown)) {
          timer = setTimeout(tick, 10_000);
        }
      } catch {
        // non-critical
      }
    }

    tick();
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [sessionId, refreshKey]);

  function isConverting(file: FileInfo): boolean {
    if (file.has_markdown) return false;
    return convertingNames.has(file.filename);
  }

  // Empty state: show a subtle collapsed bar
  if (files.length === 0) {
    return (
      <div data-testid="document-panel" className="border-b border-border-subtle bg-surface-secondary/30">
        <div className="mx-auto max-w-3xl px-4">
          <div className="flex items-center gap-2 py-2 text-xs text-zinc-600">
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
            </svg>
            <span>No documents uploaded</span>
            <span className="text-zinc-700">&mdash;</span>
            <span className="text-zinc-700">use the paperclip button to attach files</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div data-testid="document-panel" className="border-b border-border-subtle bg-surface-secondary/50">
      <div className="mx-auto max-w-3xl px-4">
        <button
          data-testid="document-panel-toggle"
          onClick={() => setOpen((v) => !v)}
          className="flex w-full items-center gap-2 py-2 text-xs text-zinc-400 hover:text-zinc-300 transition-colors"
        >
          <svg
            width="12"
            height="12"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className={`transition-transform ${open ? "rotate-90" : ""}`}
          >
            <polyline points="9 18 15 12 9 6" />
          </svg>
          Documents ({files.length})
        </button>

        {open && (
          <div className="flex flex-wrap gap-2 pb-2.5">
            {files.map((file) => (
              <div
                key={file.filename}
                data-testid="document-item"
                className="flex items-center gap-2 rounded-lg border border-zinc-700/50 bg-surface-primary/50 px-3 py-1.5 text-xs"
              >
                <svg
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="shrink-0 text-zinc-500"
                >
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                </svg>
                <span data-testid="document-name" className="text-zinc-300 truncate max-w-[150px]" title={file.filename}>
                  {file.filename}
                </span>
                <span className="text-zinc-600">{formatSize(file.size)}</span>
                {file.has_markdown ? (
                  <span data-testid="conversion-done" className="rounded-full bg-emerald-500/10 px-1.5 py-0.5 text-[10px] text-emerald-400 ring-1 ring-emerald-500/20">
                    Converted
                  </span>
                ) : isConverting(file) ? (
                  <span data-testid="conversion-converting" className="flex items-center gap-1 rounded-full bg-amber-500/10 px-1.5 py-0.5 text-[10px] text-amber-400 ring-1 ring-amber-500/20">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="animate-spin-slow">
                      <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                    </svg>
                    Converting...
                  </span>
                ) : (
                  <span data-testid="conversion-failed" className="rounded-full bg-red-500/10 px-1.5 py-0.5 text-[10px] text-red-400 ring-1 ring-red-500/20">
                    Failed
                  </span>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
