"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";

interface ArtifactCanvasProps {
  filename: string | null;
  mimeType?: string;
  content: string;
  loading: boolean;
  error: string | null;
  onClose: () => void;
}

function isMarkdown(filename: string | null, mimeType?: string): boolean {
  if (!filename) return false;
  return filename.toLowerCase().endsWith(".md") || (mimeType || "").includes("markdown");
}

export default function ArtifactCanvas({
  filename,
  mimeType,
  content,
  loading,
  error,
  onClose,
}: ArtifactCanvasProps) {
  const [copied, setCopied] = useState(false);

  if (!filename) return null;

  function handleCopy() {
    navigator.clipboard.writeText(content).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    });
  }

  function handleDownload() {
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename!;
    a.click();
    URL.revokeObjectURL(url);
  }

  const btnClass = "interactive-control rounded-lg border border-white/15 bg-white/[0.04] px-2 py-1 text-xs text-app-muted-strong hover:text-app-fg";

  return (
    <aside className="hidden w-[44%] min-w-[420px] shrink-0 border-l border-white/10 bg-black/35 xl:flex xl:flex-col">
      <div className="flex items-center justify-between border-b border-white/10 px-4 py-3">
        <div className="min-w-0">
          <p className="text-[11px] uppercase tracking-[0.14em] text-app-muted">Canvas</p>
          <h3 className="truncate text-sm font-semibold text-app-fg" title={filename}>{filename}</h3>
        </div>
        <div className="flex shrink-0 items-center gap-2">
          {!loading && !error && content && (
            <>
              <button type="button" onClick={handleCopy} className={btnClass}>
                {copied ? "Copied!" : "Copy"}
              </button>
              <button type="button" onClick={handleDownload} className={btnClass}>
                Download
              </button>
            </>
          )}
          <button type="button" onClick={onClose} className={btnClass}>
            Close
          </button>
        </div>
      </div>

      <div className="min-h-0 flex-1 overflow-auto p-6">
        {loading && (
          <div className="rounded-xl border border-white/10 bg-white/[0.03] px-3 py-2 text-sm text-app-muted">
            Loading artifact...
          </div>
        )}

        {!loading && error && (
          <div className="rounded-xl border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-300">
            {error}
          </div>
        )}

        {!loading && !error && (
          isMarkdown(filename, mimeType) ? (
            <article className="prose prose-message prose-canvas max-w-none">
              <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]}>
                {content || "_Empty artifact_"}
              </ReactMarkdown>
            </article>
          ) : (
            <pre className="overflow-x-auto rounded-xl border border-white/12 bg-black/25 p-3 text-xs text-app-fg whitespace-pre-wrap">
              {content || "Empty artifact"}
            </pre>
          )
        )}
      </div>
    </aside>
  );
}
