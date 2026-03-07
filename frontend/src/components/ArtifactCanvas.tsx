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

function isCsv(filename: string | null): boolean {
  return !!filename && filename.toLowerCase().endsWith(".csv");
}

function CsvTable({ content }: { content: string }) {
  const rows = content.trim().split("\n").map((line) => line.split(",").map((cell) => cell.trim().replace(/^"|"$/g, "")));
  if (rows.length === 0) return <pre className="text-xs text-app-muted">Empty CSV</pre>;
  const [header, ...body] = rows;
  return (
    <div className="table-wrapper">
      <table className="w-full border-collapse text-xs">
        <thead>
          <tr>
            {header.map((cell, i) => (
              <th key={i} className="bg-brand/15 px-3 py-2 text-left font-semibold text-app-fg">{cell}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {body.map((row, ri) => (
            <tr key={ri} className="border-t border-white/8">
              {row.map((cell, ci) => (
                <td key={ci} className="px-3 py-1.5 text-app-muted-strong">{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
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
  const [downloaded, setDownloaded] = useState(false);

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
    setDownloaded(true);
    setTimeout(() => setDownloaded(false), 1800);
  }

  const iconBtnClass = "interactive-control rounded-lg border border-white/15 bg-white/[0.04] p-1.5 text-app-muted-strong hover:text-app-fg";

  return (
    <aside className="hidden lg:flex lg:flex-col flex-1 min-w-0 max-w-[680px] border-l border-white/10 bg-[#0d1018]">
      <div className="flex items-center justify-between border-b border-white/10 px-4 py-3">
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="truncate text-sm font-semibold text-app-fg" title={filename}>{filename}</h3>
            <span className="shrink-0 rounded-md bg-white/[0.06] px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-app-muted">
              {filename.split('.').pop()?.toUpperCase() ?? 'FILE'}
            </span>
          </div>
        </div>
        <div className="flex shrink-0 items-center gap-2">
          {!loading && !error && content && (
            <>
              <button type="button" onClick={handleCopy} title={copied ? "Copied!" : "Copy"} className={iconBtnClass}>
                {copied ? (
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                ) : (
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                )}
              </button>
              <button type="button" onClick={handleDownload} title={downloaded ? "Downloaded!" : "Download"} className={iconBtnClass}>
                {downloaded ? (
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                ) : (
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                )}
              </button>
            </>
          )}
          <button type="button" onClick={onClose} title="Close" className={iconBtnClass}>
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>
      </div>

      <div className="min-h-0 flex-1 overflow-auto p-6">
        {loading && (
          <div className="space-y-3 pt-2">
            <div className="loading-shimmer h-6 w-48 rounded-lg border border-white/10 bg-white/[0.03]" />
            <div className="loading-shimmer h-4 w-full rounded-lg border border-white/10 bg-white/[0.03]" />
            <div className="loading-shimmer h-4 w-5/6 rounded-lg border border-white/10 bg-white/[0.03]" />
            <div className="loading-shimmer h-4 w-4/6 rounded-lg border border-white/10 bg-white/[0.03]" />
            <div className="loading-shimmer mt-4 h-24 w-full rounded-xl border border-white/10 bg-white/[0.03]" />
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
          ) : isCsv(filename) ? (
            <CsvTable content={content || ""} />
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
