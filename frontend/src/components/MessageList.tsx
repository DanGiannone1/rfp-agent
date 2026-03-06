"use client";

import { useEffect, useRef, useCallback, useState } from "react";
import { ChatMessage } from "@/lib/types";
import MessageBubble from "./MessageBubble";

interface MessageListProps {
  messages: ChatMessage[];
  onSuggestion?: (text: string) => void;
}

const SUGGESTIONS = [
  "Extract mandatory requirements into a compliance matrix.",
  "Run a bid/no-bid score across six dimensions.",
  "Draft a one-page executive summary with win themes.",
  "List top delivery risks and mitigation actions.",
];

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
          <div className="mx-auto flex min-h-[52vh] max-w-3xl flex-col justify-center space-y-3.5 md:space-y-4">
            <div className="message-card message-card-assistant">
              <div className="message-avatar message-avatar-assistant">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="m12 2 2.4 5.1L20 9.2l-4 3.8.9 5.8L12 16.3 7.1 18.8 8 13 4 9.2l5.6-2.1z" />
                </svg>
              </div>
              <div className="message-body">
                <p className="text-[1.03rem] font-medium text-app-fg">RFP uploaded. What should we do first?</p>
                <p className="mt-2 text-sm text-app-muted-strong">Pick a suggested prompt or type your own request.</p>
              </div>
            </div>

            {onSuggestion && (
              <div className="grid gap-2 sm:grid-cols-2">
                {SUGGESTIONS.map((prompt) => (
                  <button
                    key={prompt}
                    type="button"
                    onClick={() => onSuggestion(prompt)}
                    className="interactive-chip rounded-2xl border border-white/12 bg-white/[0.03] px-3 py-2.5 text-left text-sm text-app-muted-strong hover:border-brand/45 hover:bg-brand/12 hover:text-app-fg"
                  >
                    {prompt}
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
          className="interactive-control fixed bottom-28 left-1/2 z-20 -translate-x-1/2 rounded-full border border-white/15 bg-black/85 px-3 py-2 text-xs text-app-fg shadow-[0_10px_30px_rgba(0,0,0,.35)] backdrop-blur md:bottom-32 md:left-auto md:right-8 md:translate-x-0"
        >
          Jump to latest
        </button>
      )}
    </div>
  );
}
