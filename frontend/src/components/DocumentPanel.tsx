"use client";

import { useState, useEffect, useRef } from "react";
import { listFiles } from "@/lib/api";
import type { FileInfo } from "@/lib/types";
import { formatSize } from "@/lib/utils";

interface DocumentPanelProps {
  sessionId: string | null;
  refreshKey: number;
}

const CONVERTING_WINDOW_MS = 120_000;

export default function DocumentPanel({ sessionId, refreshKey }: DocumentPanelProps) {
  const [files, setFiles] = useState<FileInfo[]>([]);
  const [open, setOpen] = useState(false);
  const [convertingNames, setConvertingNames] = useState<Set<string>>(new Set());
  const uploadTimestamps = useRef<Map<string, number>>(new Map());

  useEffect(() => {
    if (refreshKey > 0) {
      uploadTimestamps.current.set(`__refresh_${refreshKey}`, Date.now());
    }
  }, [refreshKey]);

  useEffect(() => {
    if (!sessionId) return;
    const sid = sessionId;
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout>;

    async function tick() {
      try {
        const data = await listFiles(sid);
        if (cancelled) return;

        const tickNow = Date.now();
        const originals = data.files.filter(
          (f) => !f.filename.endsWith(".md") || !data.files.some((o) => f.filename === `${o.filename}.md`),
        );

        for (const f of originals) {
          if (!uploadTimestamps.current.has(f.filename)) {
            uploadTimestamps.current.set(f.filename, tickNow);
          }
        }

        const converting = new Set<string>();
        for (const f of originals) {
          if (f.has_markdown) continue;
          const ts = uploadTimestamps.current.get(f.filename);
          if (ts && tickNow - ts < CONVERTING_WINDOW_MS) converting.add(f.filename);
        }

        setFiles(originals);
        setConvertingNames(converting);

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

  if (files.length === 0) {
    return <div data-testid="document-panel" />;
  }

  return (
    <div data-testid="document-panel" className="border-t border-border-subtle bg-surface-1">
      <div className="mx-auto w-full max-w-4xl px-4 py-2">
        <button
          data-testid="document-panel-toggle"
          onClick={() => setOpen((v) => !v)}
          className="flex w-full items-center gap-2 py-1 text-sm text-text-primary/90 transition hover:text-text-primary"
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
          <span className="font-semibold tracking-wide">Documents ({files.length})</span>
        </button>

        {open && (
          <div className="mt-2 flex flex-wrap gap-2 pb-1">
            {files.map((file) => {
              const isConverting = !file.has_markdown && convertingNames.has(file.filename);
              return (
                <div
                  key={file.filename}
                  data-testid="document-item"
                  className="flex items-center gap-2 rounded-xl border border-border-subtle bg-surface-2 px-3 py-1.5 text-xs"
                >
                  <span data-testid="document-name" className="max-w-[170px] truncate text-text-primary" title={file.filename}>
                    {file.filename}
                  </span>
                  <span className="text-text-secondary">{formatSize(file.size)}</span>

                  {file.has_markdown ? (
                    <span data-testid="conversion-done" className="rounded-full bg-brand-success/15 px-2 py-0.5 text-[10px] font-medium text-brand-success">
                      Converted
                    </span>
                  ) : isConverting ? (
                    <span data-testid="conversion-converting" className="rounded-full bg-brand-warning/15 px-2 py-0.5 text-[10px] font-medium text-brand-warning">
                      Converting...
                    </span>
                  ) : (
                    <span data-testid="conversion-failed" className="rounded-full bg-red-500/15 px-2 py-0.5 text-[10px] font-medium text-red-300">
                      Failed
                    </span>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
