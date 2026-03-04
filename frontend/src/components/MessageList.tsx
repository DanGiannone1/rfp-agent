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
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
      </svg>
    ),
    text: "Summarize this RFP document",
    label: "Summarize",
  },
  {
    icon: (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
      </svg>
    ),
    text: "What are the key requirements?",
    label: "Requirements",
  },
  {
    icon: (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
      </svg>
    ),
    text: "Identify compliance risks",
    label: "Compliance",
  },
  {
    icon: (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="1" y="4" width="22" height="16" rx="2" ry="2" />
        <line x1="1" y1="10" x2="23" y2="10" />
      </svg>
    ),
    text: "Draft a response outline",
    label: "Draft",
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
              How can I help you?
            </h2>
            <p className="mb-8 max-w-md text-sm leading-relaxed text-zinc-500">
              Upload an RFP document and ask questions, or start a conversation to get AI-powered analysis and insights.
            </p>

            {/* Suggestion chips */}
            {onSuggestion && (
              <div className="grid w-full max-w-lg grid-cols-2 gap-2">
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
