"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import { File, Copy, Download, Maximize2, MessageSquare } from "lucide-react";
import BespokeIcon from "./ui/BespokeIcon";
import { isMarkdown, isCsv } from "@/lib/utils";
import CsvTable from "./CsvTable";

interface ArtifactCanvasProps {
  filename: string | null;
  mimeType?: string;
  content: string;
  loading: boolean;
  error: string | null;
  onClose: () => void;
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

  return (
    <aside className="hidden lg:flex lg:flex-col flex-1 min-w-0 bg-var(--color-surface-canvas)/80 backdrop-blur-[50px] rounded-[2rem] border border-var(--color-border-subtle)/50 shadow-2xl relative overflow-hidden h-full">
      {/* Background Accent */}
      <div className="absolute top-0 right-0 w-full h-32 bg-gradient-to-b from-var(--color-brand-primary)/5 to-transparent pointer-events-none" />

      <div className="relative z-10 flex items-center justify-between border-b border-var(--color-border-subtle)/40 px-8 py-4 bg-white/[0.01]">
        <div className="flex items-center gap-4">
          <div className="p-2 rounded-xl bg-var(--color-brand-primary)/10 text-var(--color-brand-primary) shadow-[inset_0_0_10px_rgba(217,93,57,0.1)] border border-var(--color-brand-primary)/20 transition-transform hover:scale-105">
            <BespokeIcon icon={File} size={18} glowColor="rgba(217, 93, 57, 0.4)" />
          </div>
          <div className="flex flex-col min-w-0">
            <h3 className="truncate text-[15px] font-bold text-var(--color-text-primary) tracking-tight" title={filename}>{filename}</h3>
            <span className="text-[10px] font-mono text-var(--color-text-muted) uppercase tracking-[0.2em] mt-0.5">/deliverables/</span>
          </div>
        </div>
        <div className="flex shrink-0 items-center gap-3">
          {!loading && !error && content && (
            <div className="flex items-center gap-1 bg-var(--color-app)/80 backdrop-blur-md p-1 rounded-xl border border-var(--color-border-subtle)/50 shadow-inner">
              <button type="button" onClick={handleCopy} title={copied ? "Copied!" : "Copy"} className="p-2 text-var(--color-text-muted) hover:text-var(--color-brand-primary) hover:bg-var(--color-brand-primary)/10 rounded-lg transition-all">
                {copied ? <BespokeIcon icon={Maximize2} size={16} /> : <Copy size={16} />}
              </button>
              <button type="button" onClick={handleDownload} title={downloaded ? "Downloaded!" : "Download"} className="p-2 text-var(--color-text-muted) hover:text-var(--color-brand-primary) hover:bg-var(--color-brand-primary)/10 rounded-lg transition-all">
                <Download size={16} />
              </button>
            </div>
          )}
          
          <button 
            type="button" 
            onClick={onClose}
            className="flex items-center gap-2 bg-[linear-gradient(110deg,#F4F1EA,45%,#ffffff,55%,#F4F1EA)] bg-[length:200%_100%] animate-shimmer text-[#141210] hover:brightness-110 text-[11px] font-bold px-5 py-2.5 rounded-xl transition-all shadow-[0_0_20px_rgba(244,241,234,0.15)] hover:shadow-[0_0_25px_rgba(244,241,234,0.25)] hover:-translate-y-0.5"
          >
            <MessageSquare size={14} fill="currentColor" />
            DISCUSS
          </button>
        </div>
      </div>

      <div className="relative z-10 min-h-0 flex-1 overflow-auto custom-scrollbar px-12 py-12">
        {loading && (
          <div className="max-w-4xl mx-auto space-y-6">
            <div className="loading-shimmer h-12 w-64 rounded-xl bg-var(--color-surface-1)/40 border border-var(--color-border-subtle)/40" />
            <div className="space-y-3">
              <div className="loading-shimmer h-4 w-full rounded-lg bg-var(--color-surface-1)/40 border border-var(--color-border-subtle)/40" />
              <div className="loading-shimmer h-4 w-5/6 rounded-lg bg-var(--color-surface-1)/40 border border-var(--color-border-subtle)/40" />
            </div>
            <div className="loading-shimmer h-64 w-full rounded-2xl bg-var(--color-surface-1)/40 border border-var(--color-border-subtle)/40" />
          </div>
        )}

        {!loading && error && (
          <div className="max-w-xl mx-auto rounded-2xl border border-var(--color-brand-warning)/30 bg-var(--color-brand-warning)/10 p-6 text-center shadow-xl animate-fade-in">
            <p className="text-sm font-bold text-var(--color-text-primary) uppercase tracking-widest">{error}</p>
          </div>
        )}

        {!loading && !error && (
          <div className="max-w-5xl mx-auto">
            {isMarkdown(filename, mimeType) ? (
              <article className="prose prose-message prose-canvas canvas-content">
                <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]}>
                  {content || "_Empty artifact_"}
                </ReactMarkdown>
              </article>
            ) : isCsv(filename) ? (
              <CsvTable content={content || ""} />
            ) : (
              <pre className="overflow-x-auto rounded-2xl border border-var(--color-border-subtle)/60 bg-var(--color-surface-canvas) p-8 text-[13px] text-var(--color-text-secondary) font-mono leading-relaxed shadow-inner">
                {content || "Empty artifact"}
              </pre>
            )}
          </div>
        )}
      </div>
    </aside>
  );
}
