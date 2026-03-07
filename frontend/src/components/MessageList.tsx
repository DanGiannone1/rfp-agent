"use client";

import { useEffect, useRef, useCallback, useState } from "react";
import { ChatMessage } from "@/lib/types";
import MessageBubble from "./MessageBubble";

interface MessageListProps {
  messages: ChatMessage[];
  onSuggestion?: (text: string) => void;
}

const SUGGESTIONS = [
  { icon: "gauge", label: "Bid/No-Bid analysis", description: "Score this opportunity across six weighted dimensions", prompt: "Run a bid/no-bid analysis and score this opportunity across six dimensions." },
  { icon: "checklist", label: "Extract requirements", description: "Parse the RFP into a prioritized requirements matrix", prompt: "Extract all requirements from the RFP and build a prioritized matrix with section and page references." },
  { icon: "doc", label: "Executive summary", description: "Draft a one-page summary with our win themes", prompt: "Draft a one-page executive summary with our key win themes." },
  { icon: "strategy", label: "Response strategy", description: "Define win themes and competitive positioning", prompt: "Develop a response strategy with win themes and competitive positioning." },
];

function SuggestionIcon({ icon }: { icon: string }) {
  const cls = "shrink-0 text-brand";
  switch (icon) {
    case "checklist":
      return <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={cls}><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>;
    case "gauge":
      return <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={cls}><path d="M12 20v-6M6 20V10M18 20V4"/></svg>;
    case "doc":
      return <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={cls}><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>;
    case "shield":
      return <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={cls}><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>;
    case "strategy":
      return <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={cls}><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg>;
    default:
      return null;
  }
}

export default function MessageList({ messages, onSuggestion }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const shouldAutoScroll = useRef(true);
  const rafRef = useRef<number>(0);
  const [showJumpToLatest, setShowJumpToLatest] = useState(false);

  const handleScroll = useCallback(() => {
    const el = containerRef.current;
    if (!el) return;
    const distanceFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight;
    shouldAutoScroll.current = distanceFromBottom < 180;
    setShowJumpToLatest(distanceFromBottom > 260);
  }, []);

  useEffect(() => {
    if (shouldAutoScroll.current) {
      cancelAnimationFrame(rafRef.current);
      rafRef.current = requestAnimationFrame(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
        setShowJumpToLatest(false);
      });
    }
  }, [messages]);

  return (
    <div
      ref={containerRef}
      onScroll={handleScroll}
      className="flex-1 overflow-y-auto"
      role="log"
      aria-label="Chat messages"
      aria-live="polite"
    >
      <div className="mx-auto w-full max-w-4xl px-4 py-5 md:py-7">
        {messages.length === 0 ? (
          <div className="mx-auto flex min-h-[52vh] max-w-3xl flex-col items-center justify-center">
            <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-3xl bg-brand/20 ring-1 ring-brand/35 idle-breathe">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" className="text-brand-strong">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <polyline points="9 13 11 15 15 11"/>
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-app-fg">Your RFP is ready. Where do you want to start?</h2>
            <p className="mt-1.5 text-sm text-app-muted">Pick a starting point or type your own request.</p>

            {onSuggestion && (
              <div className="mt-8 grid w-full grid-cols-1 gap-2 sm:grid-cols-2 sm:gap-3">
                {SUGGESTIONS.map((s, i) => (
                  <button
                    key={s.prompt}
                    type="button"
                    onClick={() => onSuggestion(s.prompt)}
                    style={{ animationDelay: `${i * 60}ms` }}
                    className="interactive-chip animate-fade-in flex items-center gap-3 rounded-xl border border-white/10 bg-white/[0.03] px-4 py-3.5 text-left transition hover:border-brand/40 hover:bg-brand/8 active:bg-brand/15"
                  >
                    <SuggestionIcon icon={s.icon} />
                    <div>
                      <p className="text-[14px] font-medium text-app-fg">{s.label}</p>
                      <p className="mt-0.5 text-[12px] leading-snug text-app-muted">{s.description}</p>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((msg, index) => (
              <div
                key={msg.id}
                className="animate-fade-in"
                style={{ animationDelay: `${Math.min(index * 30, 160)}ms` }}
              >
                <MessageBubble message={msg} />
              </div>
            ))}
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {showJumpToLatest && (
        <button
          type="button"
          data-testid="jump-latest-button"
          onClick={() => {
            shouldAutoScroll.current = true;
            bottomRef.current?.scrollIntoView({ behavior: "smooth" });
            setShowJumpToLatest(false);
          }}
          className="interactive-control animate-fade-in fixed bottom-28 left-1/2 z-20 -translate-x-1/2 flex items-center gap-1.5 rounded-full border border-white/15 bg-black/85 px-3 py-2 text-xs text-app-fg shadow-[0_10px_30px_rgba(0,0,0,.35)] backdrop-blur md:bottom-32 md:left-auto md:right-8 md:translate-x-0"
        >
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
          Jump to latest
        </button>
      )}
    </div>
  );
}
