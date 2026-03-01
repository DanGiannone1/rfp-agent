"use client";

import { useEffect, useRef, useCallback } from "react";
import { ChatMessage } from "@/lib/types";
import MessageBubble from "./MessageBubble";

interface MessageListProps {
  messages: ChatMessage[];
}

export default function MessageList({ messages }: MessageListProps) {
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
    >
      <div className="mx-auto flex max-w-3xl flex-col gap-5 px-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center py-24 text-center">
            <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl accent-gradient shadow-lg shadow-indigo-500/20">
              <svg
                width="24"
                height="24"
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
            <h2 className="mb-2 text-lg font-semibold text-zinc-200">
              Start a conversation
            </h2>
            <p className="max-w-sm text-sm text-zinc-500">
              Ask a question or upload an RFP document to begin your AI-powered
              analysis.
            </p>
            <div className="mt-4 flex items-center gap-2 text-xs text-zinc-600">
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
              </svg>
              <span>Use the paperclip button to attach files</span>
            </div>
          </div>
        )}
        {messages.map((msg) => (
          <div key={msg.id} className="animate-fade-in-up">
            <MessageBubble message={msg} />
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
