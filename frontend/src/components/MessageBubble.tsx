"use client";

import { useMemo } from "react";
import { Sparkles } from "lucide-react";
import { ChatMessage, MessagePart } from "@/lib/types";
import BespokeIcon from "./ui/BespokeIcon";
import IntelligenceRoadmap from "./IntelligenceRoadmap";
import MarkdownRenderer from "./MarkdownRenderer";

interface MessageBubbleProps {
  message: ChatMessage;
}

type RenderedSegment =
  | { kind: "text"; part: MessagePart & { type: "text" }; index: number }
  | { kind: "tool_group"; parts: (MessagePart & { type: "tool_call" })[]; startIndex: number };

function groupParts(parts: MessagePart[]): RenderedSegment[] {
  const segments: RenderedSegment[] = [];
  let toolBatch: (MessagePart & { type: "tool_call" })[] = [];
  let toolBatchStart = 0;

  for (let i = 0; i < parts.length; i++) {
    const part = parts[i];
    if (part.type === "tool_call") {
      if (toolBatch.length === 0) toolBatchStart = i;
      toolBatch.push(part);
    } else {
      if (toolBatch.length > 0) {
        segments.push({ kind: "tool_group", parts: toolBatch, startIndex: toolBatchStart });
        toolBatch = [];
      }
      segments.push({ kind: "text", part, index: i });
    }
  }
  if (toolBatch.length > 0) {
    segments.push({ kind: "tool_group", parts: toolBatch, startIndex: toolBatchStart });
  }
  return segments;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";
  const segments = useMemo(() => groupParts(message.parts), [message.parts]);
  const isThinking = message.isStreaming && message.parts.length === 0;

  return (
    <article className={`message-row ${isUser ? "message-row-user" : "message-row-assistant"}`}>
      {!isUser && (
        <div className="message-avatar-assistant shadow-xl">
          <BespokeIcon icon={Sparkles} size={16} glowColor="rgba(217, 93, 57, 0.5)" strokeWidth={2.5} />
        </div>
      )}

      <div className={`message-body ${isUser ? "message-body-user" : "message-body-assistant"}`}>
        <div className="message-parts">
          {segments.map((seg, idx) => {
            if (seg.kind === "text") {
              return (
                <MarkdownRenderer 
                  key={seg.index} 
                  content={seg.part.content} 
                  className="animate-fade-in" 
                />
              );
            } else {
              return (
                <IntelligenceRoadmap 
                  key={seg.startIndex} 
                  parts={seg.parts} 
                  isStreaming={message.isStreaming} 
                />
              );
            }
          })}
        </div>
        
        {isThinking && (
          <div className="thinking-row">
            <div className="thinking-dots"><span/><span/><span/></div>
            <span className="thinking-label">Synthesizing</span>
          </div>
        )}
      </div>
    </article>
  );
}
