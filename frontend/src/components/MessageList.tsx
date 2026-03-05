"use client";

import { useEffect, useRef, useCallback } from "react";
import { ChatMessage } from "@/lib/types";
import MessageBubble from "./MessageBubble";

interface MessageListProps {
  messages: ChatMessage[];
  onSuggestion?: (text: string) => void;
}

const SUGGESTIONS = [
  {
    icon: (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2" />
        <rect x="9" y="3" width="6" height="4" rx="1" />
        <path d="M9 14l2 2 4-4" />
      </svg>
    ),
    text: "Extract and classify all requirements from this RFP into a compliance matrix",
    label: "Requirements",
  },
  {
    icon: (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 3v18" />
        <path d="M3 12h18" />
        <path d="M16 7l-4-4-4 4" />
        <path d="M8 17l4 4 4-4" />
        <path d="M7 8L3 12l4 4" />
        <path d="M17 16l4-4-4-4" />
      </svg>
    ),
    text: "Perform a bid/no-bid analysis with scoring across strategic fit, capability, and win probability",
    label: "Bid/No-Bid",
  },
  {
    icon: (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <path d="M16 13H8" />
        <path d="M16 17H8" />
        <path d="M10 9H8" />
      </svg>
    ),
    text: "Draft an executive summary highlighting our key differentiators and win themes",
    label: "Executive Summary",
  },
  {
    icon: (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
        <path d="M6 8h4" />
        <path d="M6 11h3" />
        <path d="M6 14h4" />
      </svg>
    ),
    text: "Search our knowledge base for relevant past proposals, certifications, and company materials",
    label: "Knowledge Base",
  },
];

export default function MessageList({ messages, onSuggestion }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const shouldAutoScroll = useRef(true);

  const handleScroll = useCallback(() => {
    const el = containerRef.current;
    if (!el) return;
    const distanceFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight;
    shouldAutoScroll.current = distanceFromBottom < 150;
  }, []);

  useEffect(() => {
    if (shouldAutoScroll.current) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div
      ref={containerRef}
      onScroll={handleScroll}
      className="chat-bg flex-1 overflow-y-auto py-6"
      role="log"
      aria-label="Chat messages"
      aria-live="polite"
    >
      <div className="mx-auto flex max-w-3xl flex-col gap-5 px-4">
        {/* Empty state */}
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center py-16 text-center animate-fade-in">
            {/* Logo */}
            <div className="relative mb-6">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl accent-gradient shadow-xl shadow-indigo-500/20">
                <svg
                  width="28"
                  height="28"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="text-white"
                >
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                </svg>
              </div>
              {/* Decorative glow ring */}
              <div className="absolute -inset-3 rounded-3xl bg-indigo-500/5 blur-xl" aria-hidden="true" />
            </div>

            <h2 className="mb-2 text-xl font-semibold text-zinc-100">
              RFP Response Accelerator
            </h2>
            <p className="mb-8 max-w-md text-sm leading-relaxed text-zinc-500">
              Upload an RFP document to get started. I&apos;ll help you analyze requirements, assess bid viability, draft responses, and search your knowledge base for relevant materials.
            </p>

            {/* Suggestion chips */}
            {onSuggestion && (
              <div className="grid w-full max-w-lg grid-cols-1 gap-2 sm:grid-cols-2">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s.label}
                    type="button"
                    onClick={() => onSuggestion(s.text)}
                    className="group flex items-center gap-3 rounded-xl border border-zinc-800 bg-zinc-900/50 px-4 py-3 text-left text-sm text-zinc-400 transition-all duration-200 hover:border-indigo-500/30 hover:bg-zinc-800/70 hover:text-zinc-200"
                  >
                    <span className="shrink-0 text-zinc-600 transition-colors group-hover:text-indigo-400">
                      {s.icon}
                    </span>
                    <span>{s.label}</span>
                  </button>
                ))}
              </div>
            )}

            {/* File hint */}
            <div className="mt-6 flex items-center gap-2 rounded-lg bg-zinc-900/50 px-3 py-2 text-xs text-zinc-600">
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
                <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
              </svg>
              <span>Attach files with the paperclip button or drag and drop</span>
            </div>
          </div>
        )}

        {/* Messages */}
        {messages.map((msg, index) => (
          <div
            key={msg.id}
            className="animate-fade-in-up"
            style={{ animationDelay: `${Math.min(index * 30, 150)}ms` }}
          >
            <MessageBubble message={msg} />
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
