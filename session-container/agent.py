import asyncio
import json
import os
from collections.abc import AsyncGenerator

from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from copilot import CopilotClient
from copilot.generated.session_events import SessionEventType

load_dotenv()

SYSTEM_PROMPT = """\
You are an RFP analysis agent. Your job is to examine documents in the working \
directory and help the user understand, summarize, and respond to Requests for \
Proposal (RFPs).

You have access to built-in tools (bash, grep, glob, str_replace_editor). Use \
them freely to read files, search for content, and organize your analysis.

When analyzing RFP documents:
- Start by listing available files to understand what you're working with
- Read and summarize key sections (scope, requirements, evaluation criteria, deadlines)
- Highlight compliance requirements and potential risks
- Suggest response strategies when asked
"""


def _sse_event(data: dict) -> str:
    """Format a dict as an SSE data line."""
    return f"data: {json.dumps(data)}\n\n"


class AgentSession:
    """Async context manager that holds a persistent Copilot session.

    Usage::

        async with AgentSession(working_dir) as session:
            # Streaming (for CLI):
            async for event in session.send("hello"):
                print(event)

            # Blocking (for server):
            result = await session.send_and_collect("hello")
            print(result["content"])
    """

    def __init__(self, working_dir: str):
        self._working_dir = working_dir
        self._client: CopilotClient | None = None
        self._session = None
        self._unsubscribe = None
        self._queue: asyncio.Queue[dict | None] = asyncio.Queue()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._tool_names: dict[str, str] = {}
        self._status: str = "idle"

    @property
    def status(self) -> str:
        """Current activity: 'idle', 'thinking', 'tool:<name>', or 'error'."""
        return self._status

    async def __aenter__(self, token: str | None = None):
        if not token:
            token = os.getenv("AZURE_OPENAI_TOKEN")
        if not token:
            credential = DefaultAzureCredential()
            token = credential.get_token(
                "https://cognitiveservices.azure.com/.default"
            ).token

        self._client = CopilotClient(
            {"cli_args": ["--allow-all-tools", "--allow-all-paths"]}
        )
        await self._client.start()

        self._loop = asyncio.get_running_loop()

        self._session = await self._client.create_session(
            {
                "model": os.environ["AZURE_DEPLOYMENT"],
                "provider": {
                    "type": "openai",
                    "base_url": os.environ["AZURE_ENDPOINT"],
                    "bearer_token": token,
                    "wire_api": "responses",
                },
                "system_message": {
                    "mode": "append",
                    "content": SYSTEM_PROMPT,
                },
                "working_directory": self._working_dir,
                "streaming": True,
                "on_permission_request": lambda _req, _ctx: {"kind": "approved"},
            }
        )

        self._unsubscribe = self._session.on(self._on_event)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._unsubscribe:
            self._unsubscribe()
        if self._session:
            await self._session.destroy()
        if self._client:
            await self._client.stop()

    def _on_event(self, event):
        """Push events into the async queue from the SDK's internal thread."""
        item = None

        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            self._status = "thinking"
            delta = getattr(event.data, "delta_content", None) or ""
            if delta:
                item = {"type": "delta", "content": delta}

        elif event.type == SessionEventType.ASSISTANT_MESSAGE:
            content = getattr(event.data, "content", None) or ""
            if content:
                item = {"type": "message", "content": content}

        elif event.type == SessionEventType.TOOL_EXECUTION_START:
            tool = getattr(event.data, "tool_name", None) or "unknown"
            call_id = getattr(event.data, "tool_call_id", None)
            if call_id:
                self._tool_names[call_id] = tool
            self._status = f"tool:{tool}"
            item = {"type": "tool_start", "tool": tool}

        elif event.type == SessionEventType.TOOL_EXECUTION_COMPLETE:
            call_id = getattr(event.data, "tool_call_id", None)
            tool = self._tool_names.pop(call_id, None) if call_id else None
            tool = tool or getattr(event.data, "tool_name", None) or "unknown"
            self._status = "thinking"
            item = {"type": "tool_end", "tool": tool}

        elif event.type == SessionEventType.SESSION_IDLE:
            self._status = "idle"
            self._loop.call_soon_threadsafe(
                self._queue.put_nowait, {"type": "done"}
            )
            self._loop.call_soon_threadsafe(self._queue.put_nowait, None)
            return

        elif event.type == SessionEventType.SESSION_ERROR:
            self._status = "error"
            msg = getattr(event.data, "message", None) or "Unknown error"
            self._loop.call_soon_threadsafe(
                self._queue.put_nowait, {"type": "error", "message": msg}
            )
            self._loop.call_soon_threadsafe(self._queue.put_nowait, None)
            return

        if item:
            self._loop.call_soon_threadsafe(self._queue.put_nowait, item)

    async def send(self, prompt: str) -> AsyncGenerator[str, None]:
        """Send a prompt and yield SSE-formatted events until the session is idle."""
        # Drain any stale items from a previous turn
        while not self._queue.empty():
            self._queue.get_nowait()

        self._status = "thinking"
        await self._session.send({"prompt": prompt})

        while True:
            item = await self._queue.get()
            if item is None:
                break
            yield _sse_event(item)

    async def send_and_collect(self, prompt: str) -> dict:
        """Send a prompt, block until done, return the full result.

        Returns {"content": str, "tool_activity": list[dict]}.
        Raises RuntimeError on agent error.
        """
        content = ""
        tool_activity = []

        async for sse_line in self.send(prompt):
            text = sse_line.strip()
            if not text.startswith("data: "):
                continue
            event = json.loads(text[6:])
            etype = event.get("type")
            if etype == "delta":
                content += event.get("content", "")
            elif etype == "tool_start":
                tool_activity.append({
                    "tool": event.get("tool", "unknown"),
                    "status": "running",
                })
            elif etype == "tool_end":
                for ta in tool_activity:
                    if ta["tool"] == event.get("tool") and ta["status"] == "running":
                        ta["status"] = "done"
                        break
            elif etype == "error":
                raise RuntimeError(event.get("message", "Unknown error"))

        return {"content": content, "tool_activity": tool_activity}


async def run_analysis(prompt: str, working_dir: str) -> AsyncGenerator[str, None]:
    """Run a single-turn RFP analysis, yielding SSE-formatted JSON events.

    Convenience wrapper used by the CLI one-shot mode.
    """
    try:
        async with AgentSession(working_dir) as session:
            async for event in session.send(prompt):
                yield event
    except Exception as exc:
        yield _sse_event({"type": "error", "message": str(exc)})
