import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { ChatMessage } from "@/lib/types";
import ToolIndicator from "./ToolIndicator";

interface MessageBubbleProps {
  message: ChatMessage;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm ${
          isUser
            ? "accent-gradient text-white shadow-lg shadow-indigo-500/10"
            : "bg-surface text-zinc-100 ring-1 ring-white/[0.06]"
        }`}
      >
        {message.toolActivity.length > 0 && (
          <div className="mb-2 flex flex-wrap gap-1.5">
            {message.toolActivity.map((ta, i) => (
              <ToolIndicator key={`${ta.tool}-${i}`} activity={ta} />
            ))}
          </div>
        )}
        <div className="prose prose-sm max-w-none prose-p:my-1 prose-pre:my-2">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {message.content}
          </ReactMarkdown>
          {message.isStreaming && (
            <span className="inline-flex items-center gap-1 ml-1">
              <span className="h-1.5 w-1.5 rounded-full bg-current animate-bounce-dot" />
              <span className="h-1.5 w-1.5 rounded-full bg-current animate-bounce-dot [animation-delay:0.2s]" />
              <span className="h-1.5 w-1.5 rounded-full bg-current animate-bounce-dot [animation-delay:0.4s]" />
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
