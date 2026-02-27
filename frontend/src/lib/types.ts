export type SSEEvent =
  | { type: "delta"; content: string }
  | { type: "message"; content: string }
  | { type: "status"; status: string }
  | { type: "tool_start"; tool: string }
  | { type: "tool_end"; tool: string }
  | { type: "done" }
  | { type: "error"; message: string };

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  isStreaming: boolean;
  toolActivity: ToolActivity[];
  timestamp?: string;
}

export interface ToolActivity {
  tool: string;
  status: "running" | "done";
}
