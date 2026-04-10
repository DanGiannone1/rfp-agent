"""AgentSession wrapping the GitHub Copilot SDK with an event queue.

Provides a streaming async generator interface for running agent turns
against Azure OpenAI.  Emits AG-UI protocol events.
"""

import asyncio
import json as _json
import logging as _logging
import os
import threading
import time as _time
import uuid
from collections.abc import AsyncGenerator
from pathlib import Path

from ag_ui.core.events import (
    BaseEvent,
    RunErrorEvent,
    RunFinishedEvent,
    RunStartedEvent,
    TextMessageContentEvent,
    TextMessageEndEvent,
    TextMessageStartEvent,
    ToolCallArgsEvent,
    ToolCallEndEvent,
    ToolCallStartEvent,
)
from azure.identity.aio import DefaultAzureCredential
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from tracing import attach_context, get_current_context, get_tracer, truncate
from copilot import CopilotClient
from copilot.generated.session_events import SessionEventType
from copilot.tools import define_tool

load_dotenv()

_LOG = os.getenv("LOG_AGENT_EVENTS", "").lower() == "true"
_logger = _logging.getLogger("agent.events")
_trace_logger = _logging.getLogger("trace")


def _log_event(msg: str) -> None:
    if _LOG:
        _logger.info(msg)


def _trace(event: str, **data) -> None:
    if not _trace_logger.handlers:
        return
    from datetime import datetime, timezone
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "component": "session",
        "event": event,
        "data": data,
    }
    _trace_logger.info(_json.dumps(record, default=str))


SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KB_NAME = os.getenv("AZURE_SEARCH_KB_NAME", "rfp-knowledge")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY", "")

SYSTEM_PROMPT = """\
You are an RFP agent for Meridian & Associates LLP.

The workspace contains the uploaded RFP source file and any generated artifacts.

Runtime rules:
- Start structured work by reading the uploaded RFP in full with `read_full_file`.
- If there is exactly one visible file in the workspace, call `read_full_file` without a path.
- Load the one skill that best matches the user's request.
- Do not invoke additional skills as hidden prerequisites unless the user explicitly asks for them.
- Save finished deliverables with `write_file`.
- If you load a skill that defines a document output, treat saving that deliverable with `write_file` as required before your final reply.
- Do not return the full deliverable only in chat when `write_file` is available.
- Do not use hidden metadata files as task inputs.
- Do not reread the same uploaded source file repeatedly in the same turn unless the user asks you to revisit it.

Available skills:
- bid-no-bid-analysis
- requirements-extraction
- response-strategy
- draft-generation
- executive-summary
- compliance-review
- risk-gap-analysis
- pricing-analysis
- customer-intelligence
- iterative-refinement

Working style:
- Read before drafting.
- Ground the response in the RFP and any tools actually available in this session.
- Do not invent firm-specific facts, metrics, case studies, or certifications.
- Do not invent commercial concessions, free inclusions, discounts, partnerships, or relationship history.
- Omit fields that are not stated in the RFP or verified by tools; never use bracketed placeholders such as `[Not specified]`.
- Never render missing metadata as "Not specified", "Unknown", "TBD", or similar; omit the field entirely.
- When you infer from the RFP rather than verified external evidence, phrase it cautiously or omit the claim.
- If evidence is unavailable, use strong but unquantified language instead of illustrative proof points.
- Write in a professional proposal tone.
- Do not mention tools, file paths, or hidden runtime behavior to the user.
- When a deliverable is saved, tell the user in one short sentence what is ready and what it contains, using the task's own language where natural.
- Mention the concrete deliverable type and 2-3 key contents or decisions, but do not mention the workspace or filename unless asked.
- If the user explicitly says not to ask follow-up questions, end with a short completion statement only.
"""

KB_PROMPT_SECTION = """\

When `knowledge_base_retrieve` is available, use it to ground Meridian-specific claims.
If the KB does not support a claim, avoid making that claim.
"""


def _sse_event(event: BaseEvent) -> str:
    """Format an AG-UI event as an SSE data line."""
    return f"data: {event.model_dump_json(exclude_none=True)}\n\n"


def _jsonable(value):
    """Best-effort conversion of SDK event payloads into JSON-safe structures."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v) for v in value]
    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        try:
            return _jsonable(model_dump())
        except Exception:
            pass
    if hasattr(value, "__dict__"):
        try:
            return {
                str(k): _jsonable(v)
                for k, v in vars(value).items()
                if not str(k).startswith("_")
            }
        except Exception:
            pass
    return repr(value)


def _tool_result_preview(result, limit: int = 240) -> str | None:
    if result is None:
        return None

    content = None
    if isinstance(result, dict):
        content = result.get("content") or result.get("detailed_content")
    else:
        content = getattr(result, "content", None) or getattr(result, "detailed_content", None)

    if content is None:
        content = _jsonable(result)

    text = str(content)
    if len(text) <= limit:
        return text
    return truncate(text, limit)


def _path_within_workspace(workspace: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(workspace)
        return True
    except ValueError:
        return False


class ReadFullFileParams(BaseModel):
    path: str = Field(
        default="",
        description=(
            "Optional path to a UTF-8 text or markdown file in the current workspace. "
            "If omitted and there is exactly one visible file in the workspace, that file will be read."
        ),
    )


class WriteFileParams(BaseModel):
    path: str = Field(description="Path to a UTF-8 text or markdown artifact in the current workspace")
    content: str = Field(description="Complete text content to write to the file")


def _build_read_full_file_tool(working_dir: str, turn_read_paths: set[str]):
    workspace_root = Path(working_dir).resolve()

    @define_tool(
        name="read_full_file",
        description=(
            "Read a complete UTF-8 text or markdown file from the current workspace in one call. "
            "Use this for full-document reads before summarizing, extracting requirements, or drafting. "
            "If there is exactly one visible file in the workspace, you may omit the path."
        ),
    )
    def read_full_file(params: ReadFullFileParams) -> str:
        raw_path = params.path.strip()
        if raw_path:
            candidate = Path(raw_path)
            resolved = (candidate if candidate.is_absolute() else workspace_root / candidate).resolve()
        else:
            visible_files = [
                entry.resolve()
                for entry in sorted(workspace_root.iterdir())
                if entry.is_file() and not entry.name.startswith(".")
            ]
            if len(visible_files) != 1:
                visible_names = [path.name for path in visible_files]
                raise ValueError(
                    "path is required when the workspace does not contain exactly one visible file. "
                    f"Visible files: {visible_names}"
                )
            resolved = visible_files[0]
            raw_path = resolved.name

        if not _path_within_workspace(workspace_root, resolved):
            raise ValueError("path must stay within the current workspace")
        if not resolved.exists() or not resolved.is_file():
            raise ValueError(f"file not found: {raw_path}")
        if resolved.name.startswith("."):
            raise ValueError(f"hidden metadata files are not valid task inputs: {raw_path}")

        size_bytes = resolved.stat().st_size
        raw_bytes = resolved.read_bytes()
        if b"\x00" in raw_bytes:
            raise ValueError(f"binary file is not supported: {raw_path}")

        uploaded_manifest = workspace_root / ".uploaded_files.json"
        uploaded_names: set[str] = set()
        if uploaded_manifest.exists():
            try:
                payload = _json.loads(uploaded_manifest.read_text(encoding="utf-8"))
                uploaded_names = {
                    str(name)
                    for name in payload.get("uploaded_files", [])
                    if isinstance(name, str)
                }
            except Exception:
                uploaded_names = set()

        resolved_key = str(resolved)
        if resolved.name in uploaded_names and resolved_key in turn_read_paths:
            return (
                f"PATH: {resolved}\n"
                "ALREADY_READ_THIS_TURN: true\n\n"
                "Use the full contents already returned earlier in this turn instead of "
                f"rereading {resolved.name}."
            )
        turn_read_paths.add(resolved_key)

        text = raw_bytes.decode("utf-8", errors="replace")
        line_count = text.count("\n") + (1 if text else 0)

        return (
            f"PATH: {resolved}\n"
            f"SIZE_BYTES: {size_bytes}\n"
            f"LINE_COUNT: {line_count}\n\n"
            f"{text}"
        )

    return read_full_file


def _build_write_file_tool(working_dir: str):
    workspace_root = Path(working_dir).resolve()

    @define_tool(
        name="write_file",
        description=(
            "Write a complete UTF-8 text or markdown artifact to the current workspace in one call. "
            "Use this to save proposal outputs such as executive_summary.md."
        ),
    )
    def write_file(params: WriteFileParams) -> str:
        raw_path = params.path.strip()
        if not raw_path:
            raise ValueError("path is required")

        candidate = Path(raw_path)
        resolved = (candidate if candidate.is_absolute() else workspace_root / candidate).resolve()

        if not _path_within_workspace(workspace_root, resolved):
            raise ValueError("path must stay within the current workspace")
        if resolved.name.startswith("."):
            raise ValueError("hidden metadata files are not valid output targets")

        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(params.content, encoding="utf-8")

        size_bytes = resolved.stat().st_size
        line_count = params.content.count("\n") + (1 if params.content else 0)

        return (
            f"PATH: {resolved}\n"
            f"SIZE_BYTES: {size_bytes}\n"
            f"LINE_COUNT: {line_count}\n"
            "STATUS: wrote file"
        )

    return write_file


class AgentSession:
    """Async context manager that holds a persistent Copilot session.

    Usage::

        async with AgentSession(working_dir) as session:
            async for event in session.send("hello"):
                print(event)
    """

    def __init__(self, working_dir: str, token: str | None = None, session_id: str = "default"):
        self._working_dir = working_dir
        self._initial_token = token
        self._token = token
        self._session_id = session_id
        self._client: CopilotClient | None = None
        self._session = None
        self._unsubscribe = None
        self._queue: asyncio.Queue[BaseEvent | None] = asyncio.Queue()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._tool_names: dict[str, tuple[str, float]] = {}  # call_id → (tool_name, start_time)
        self._tools_called: int = 0
        self._turn_start: float = 0.0
        self._status: str = "idle"
        self._credential: DefaultAzureCredential | None = None
        self._turn_read_paths: set[str] = set()

        # AG-UI state tracked per turn
        self._thread_id: str = str(uuid.uuid4())
        self._run_id: str = ""
        self._current_message_id: str = ""
        self._message_started: bool = False

        # Tracing state tracked per turn
        self._otel_ctx = None
        self._active_spans = {}  # call_id -> (span, start_time_ns)

        # Raw SDK event dump (opt-in, local file)
        self._raw_sdk_log_lock = threading.Lock()
        self._raw_sdk_log_path: str | None = None
        if os.getenv("LOG_RAW_SDK_EVENTS", "").lower() == "true":
            logs_dir = os.getenv("LOG_RAW_SDK_EVENTS_DIR") or os.getenv("LOG_TRACE_DIR")
            if logs_dir:
                raw_dir = Path(logs_dir) / "sdk-events"
                raw_dir.mkdir(parents=True, exist_ok=True)
                self._raw_sdk_log_path = str(raw_dir / f"{self._session_id}.jsonl")

    @property
    def raw_sdk_log_path(self) -> str | None:
        return self._raw_sdk_log_path

    def _write_raw_sdk_record(self, record: dict) -> None:
        if not self._raw_sdk_log_path:
            return
        payload = {
            "ts": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
            "session_id": self._session_id,
            **record,
        }
        line = _json.dumps(payload, default=str)
        with self._raw_sdk_log_lock:
            with open(self._raw_sdk_log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")

    @property
    def status(self) -> str:
        """Current activity: 'idle', 'thinking', 'tool:<name>', or 'error'."""
        return self._status

    @property
    def token(self) -> str | None:
        return self._token

    def _base_span_attributes(self) -> dict[str, str]:
        attrs = {
            "session.id": self._session_id,
            "session_id": self._session_id,
            "thread_id": self._thread_id,
        }
        if self._run_id:
            attrs["run_id"] = self._run_id
        return attrs

    async def __aenter__(self) -> "AgentSession":
        if self._raw_sdk_log_path:
            Path(self._raw_sdk_log_path).write_text("", encoding="utf-8")

        token = self._token or self._initial_token or os.getenv("AZURE_OPENAI_TOKEN")
        if not token:
            self._credential = DefaultAzureCredential()
            tok = await self._credential.get_token(
                "https://cognitiveservices.azure.com/.default"
            )
            token = tok.token
        self._token = token

        self._client = CopilotClient(
            {
                "cli_args": [
                    "--allow-all-tools",
                    "--allow-all-paths",
                    "--disable-builtin-mcps",
                    "--no-custom-instructions",
                ],
                "use_logged_in_user": False,
            }
        )
        await self._client.start()

        self._loop = asyncio.get_running_loop()

        skills_dir = str(Path(__file__).parent / "skills")
        kb_enabled = bool(SEARCH_ENDPOINT and SEARCH_KEY)
        system_prompt = SYSTEM_PROMPT + (KB_PROMPT_SECTION if kb_enabled else "")
        available_tools = ["skill", "report_intent", "read_full_file", "write_file"]
        runtime_tool_allowlist = set(available_tools)
        if kb_enabled:
            runtime_tool_allowlist.add("knowledge_base_retrieve")
        custom_tools = [
            _build_read_full_file_tool(self._working_dir, self._turn_read_paths),
            _build_write_file_tool(self._working_dir),
        ]
        mcp_servers = {}
        if kb_enabled:
            mcp_servers["knowledge_base"] = {
                "type": "http",
                "url": (
                    f"{SEARCH_ENDPOINT.rstrip('/')}/knowledgebases/"
                    f"{SEARCH_KB_NAME}/mcp?api-version=2025-11-01-preview"
                ),
                "headers": {
                    "api-key": SEARCH_KEY,
                },
                "tools": ["knowledge_base_retrieve"],
            }

        async def _pre_tool_use(input_data, _ctx):
            tool_name = input_data.get("toolName")
            normalized_tool_name = str(tool_name or "").lower()
            raw_args = input_data.get("toolArgs") or {}
            trace_payload = {
                "session_id": self._session_id,
                "thread_id": self._thread_id,
                "run_id": self._run_id,
                "tool": normalized_tool_name,
                "args": raw_args if isinstance(raw_args, dict) else str(raw_args),
            }
            if normalized_tool_name not in runtime_tool_allowlist:
                decision = {
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        "Only the configured RFP workflow tools are enabled in this runtime."
                    ),
                    "additionalContext": (
                        "Use read_full_file to read the RFP, skill to load the matching "
                        "workflow, write_file to save the deliverable, and "
                        "knowledge_base_retrieve only when it is available."
                    ),
                }
                _trace("agent.pre_tool_use", **trace_payload, decision="deny", reason=decision["permissionDecisionReason"])
                self._write_raw_sdk_record({"kind": "pre_tool_use", **trace_payload, "decision": "deny"})
                return decision

            _trace("agent.pre_tool_use", **trace_payload, decision="allow")
            self._write_raw_sdk_record({"kind": "pre_tool_use", **trace_payload, "decision": "allow"})
            return {"permissionDecision": "allow"}

        session_config = {
            "model": os.environ["AZURE_DEPLOYMENT"],
            "provider": {
                "type": "azure",
                "base_url": os.environ["AZURE_ENDPOINT"],
                "bearer_token": token,
                "wire_api": "chat",
                "azure": {
                    "api_version": "2024-10-21",
                },
            },
            "system_message": {
                "mode": "replace",
                "content": system_prompt,
            },
            "working_directory": self._working_dir,
            "tools": custom_tools,
            "available_tools": available_tools,
            "streaming": True,
            "on_permission_request": lambda _req, _ctx: {"kind": "approved"},
            "hooks": {"on_pre_tool_use": _pre_tool_use},
            "skill_directories": [skills_dir],
        }
        if mcp_servers:
            session_config["mcp_servers"] = mcp_servers

        self._session = await self._client.create_session(session_config)

        self._unsubscribe = self._session.on(self._on_event)
        session_trace = {
            "session_id": self._session_id,
            "working_dir": self._working_dir,
            "thread_id": self._thread_id,
            "raw_log_path": self._raw_sdk_log_path,
            "model": os.environ.get("AZURE_DEPLOYMENT"),
            "client_use_logged_in_user": False,
            "custom_instructions_disabled": True,
            "builtin_mcps_disabled": True,
            "system_message_mode": "replace",
            "available_tools": available_tools,
            "runtime_tool_allowlist": sorted(runtime_tool_allowlist),
            "custom_tools": [tool.name for tool in custom_tools],
            "skill_directories": [skills_dir],
            "mcp_servers": sorted((session_config.get("mcp_servers") or {}).keys()),
            "knowledge_base_enabled": kb_enabled,
        }
        _trace("agent.session_initialized", **session_trace)
        self._write_raw_sdk_record(
            {
                "kind": "session_initialized",
                **session_trace,
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._unsubscribe:
            self._unsubscribe()
        if self._session:
            await self._session.destroy()
        if self._client:
            await self._client.stop()
        if self._credential:
            await self._credential.close()

    def _enqueue(self, event: BaseEvent) -> None:
        """Thread-safe enqueue of an AG-UI event."""
        self._loop.call_soon_threadsafe(self._queue.put_nowait, event)

    def _on_event(self, event) -> None:
        """Push events into the async queue from the SDK's internal thread."""
        self._write_raw_sdk_record(
            {
                "kind": "sdk_event",
                "thread_id": self._thread_id,
                "run_id": self._run_id,
                "event_type": str(getattr(event, "type", "UNKNOWN")),
                "data": _jsonable(getattr(event, "data", None)),
            }
        )

        # Tracing: Attach parent turn context to the current SDK background thread
        with attach_context(self._otel_ctx):
            if event.type == SessionEventType.SESSION_INFO:
                info_type = getattr(event.data, "info_type", None)
                message = getattr(event.data, "message", None)
                _trace(
                    "agent.session_info",
                    session_id=self._session_id,
                    thread_id=self._thread_id,
                    run_id=self._run_id,
                    info_type=info_type,
                    message=message,
                )

            elif event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
                self._status = "thinking"
                delta = getattr(event.data, "delta_content", None) or ""
                if not delta:
                    return

                # Emit TextMessageStartEvent on first delta
                if not self._message_started:
                    self._current_message_id = str(uuid.uuid4())
                    self._message_started = True
                    _log_event(f"[THINKING] {delta[:120]}")
                    _trace(
                        "agent.thinking",
                        session_id=self._session_id,
                        thread_id=self._thread_id,
                        run_id=self._run_id,
                        text=delta[:120],
                    )
                    self._enqueue(TextMessageStartEvent(
                        message_id=self._current_message_id,
                        role="assistant",
                    ))

                    # Tracing: Snapshot first thoughts
                    thinking_attrs = self._base_span_attributes()
                    thinking_attrs["thought.preview"] = truncate(delta, 200)
                    get_tracer().start_span(
                        "agent.thinking",
                        attributes=thinking_attrs,
                    ).end()

                self._enqueue(TextMessageContentEvent(
                    message_id=self._current_message_id,
                    delta=delta,
                ))

            elif event.type == SessionEventType.ASSISTANT_MESSAGE:
                final_content = (
                    getattr(event.data, "content", None)
                    or getattr(event.data, "transformed_content", None)
                    or getattr(event.data, "partial_output", None)
                    or ""
                )

                if not self._message_started and final_content:
                    self._current_message_id = str(uuid.uuid4())
                    self._message_started = True
                    self._enqueue(TextMessageStartEvent(
                        message_id=self._current_message_id,
                        role="assistant",
                    ))
                    self._enqueue(TextMessageContentEvent(
                        message_id=self._current_message_id,
                        delta=final_content,
                    ))

                # End the current text message
                if self._message_started:
                    self._enqueue(TextMessageEndEvent(
                        message_id=self._current_message_id,
                    ))
                    self._message_started = False

            elif event.type == SessionEventType.TOOL_EXECUTION_START:
                tool = getattr(event.data, "tool_name", None) or "unknown"
                call_id = getattr(event.data, "tool_call_id", None) or str(uuid.uuid4())
                self._tool_names[call_id] = (tool, _time.monotonic())
                # Internal SDK tools — track them but don't surface to the frontend
                if tool in ("report_intent", "skill"):
                    return

                # Tracing: Start tool call span
                args = getattr(event.data, "arguments", None)
                args_str = (args if isinstance(args, str) else _json.dumps(args)) if args else None

                tool_attrs = self._base_span_attributes()
                tool_attrs.update({
                    "gen_ai.call.type": "tool",
                    "tool.name": tool,
                    "tool.call_id": call_id,
                    "tool.arguments": truncate(args_str or "{}", 1000),
                })
                tool_span_start_ns = _time.time_ns()
                tool_span = get_tracer().start_span(
                    "agent.tool_call",
                    attributes=tool_attrs,
                    start_time=tool_span_start_ns,
                )
                self._active_spans[call_id] = (tool_span, tool_span_start_ns)

                self._status = f"tool:{tool}"
                self._enqueue(ToolCallStartEvent(
                    tool_call_id=call_id,
                    tool_call_name=tool,
                    parent_message_id=self._current_message_id or None,
                ))
                # Forward arguments so the frontend can show human-readable context
                if args_str:
                    self._enqueue(ToolCallArgsEvent(
                        tool_call_id=call_id,
                        delta=args_str,
                    ))
                _log_event(f"[TOOL] >>> {tool}  args={args_str or '{}'}")
                _trace(
                    "agent.tool_start",
                    session_id=self._session_id,
                    thread_id=self._thread_id,
                    run_id=self._run_id,
                    tool=tool,
                    call_id=call_id,
                    args=args_str or "{}",
                )

            elif event.type == SessionEventType.TOOL_EXECUTION_COMPLETE:
                call_id = getattr(event.data, "tool_call_id", None)
                if not call_id:
                    # Recover the UUID assigned at start by matching on tool name
                    tool_name_hint = getattr(event.data, "tool_name", None)
                    if tool_name_hint:
                        call_id = next(
                            (k for k, (n, _) in self._tool_names.items() if n == tool_name_hint),
                            None,
                        )
                entry = self._tool_names.pop(call_id, None) if call_id else None
                tool = entry[0] if entry else (getattr(event.data, "tool_name", None) or "unknown")
                duration = _time.monotonic() - entry[1] if entry else 0.0
                result = getattr(event.data, "result", None)
                result_preview = _tool_result_preview(result)

                # Tracing: End tool call span with result preview
                if call_id in self._active_spans:
                    span, span_start_ns = self._active_spans.pop(call_id)
                    span.set_attribute("tool.result_preview", result_preview or "")
                    span.set_attribute("tool.duration_s", round(duration, 4))
                    span.end(end_time=max(span_start_ns, _time.time_ns()))

                # Suppress end event for internal tools that were filtered at start
                if tool in ("report_intent", "skill"):
                    return
                self._status = "thinking"
                self._tools_called += 1
                if call_id:
                    self._enqueue(ToolCallEndEvent(tool_call_id=call_id))
                _log_event(f"[TOOL] <<< {tool}  duration={duration:.2f}s")
                _trace(
                    "agent.tool_end",
                    session_id=self._session_id,
                    thread_id=self._thread_id,
                    run_id=self._run_id,
                    tool=tool,
                    call_id=call_id,
                    duration_s=round(duration, 2),
                    result_preview=result_preview,
                )

            elif event.type == SessionEventType.SESSION_IDLE:
                self._status = "idle"
                turn_duration = _time.monotonic() - self._turn_start
                _log_event(
                    f"[TURN END] duration={turn_duration:.2f}s"
                    f"  tools={self._tools_called}"
                )
                _trace(
                    "agent.turn_end",
                    session_id=self._session_id,
                    thread_id=self._thread_id,
                    run_id=self._run_id,
                    duration_s=round(turn_duration, 2),
                    tools_called=self._tools_called,
                )
                self._enqueue(RunFinishedEvent(
                    thread_id=self._thread_id,
                    run_id=self._run_id,
                ))
                self._loop.call_soon_threadsafe(self._queue.put_nowait, None)
                return

            elif event.type == SessionEventType.SESSION_ERROR:
                self._status = "error"
                msg = getattr(event.data, "message", None) or "Unknown error"

                # Tracing: Close any dangling tool spans
                for call_id, (span, span_start_ns) in self._active_spans.items():
                    span.record_exception(Exception(msg))
                    span.end(end_time=max(span_start_ns, _time.time_ns()))
                self._active_spans.clear()

                if (
                    "too many requests" in msg.lower()
                    or "429" in msg
                    or "rate limit" in msg.lower()
                ):
                    msg = (
                        "The AI service is temporarily rate-limited. "
                        "Please wait 30–60 seconds and try again."
                    )
                _log_event(f"[ERROR] {msg}")
                _trace(
                    "agent.error",
                    session_id=self._session_id,
                    thread_id=self._thread_id,
                    run_id=self._run_id,
                    message=msg,
                )
                self._enqueue(RunErrorEvent(message=msg))
                self._enqueue(RunFinishedEvent(
                    thread_id=self._thread_id,
                    run_id=self._run_id,
                ))
                self._loop.call_soon_threadsafe(self._queue.put_nowait, None)
                return

    async def send(self, prompt: str) -> AsyncGenerator[str, None]:
        """Send a prompt and yield SSE-formatted AG-UI events until the session is idle."""
        # Drain any stale items from a previous turn
        while not self._queue.empty():
            self._queue.get_nowait()

        # Reset per-turn state
        self._run_id = str(uuid.uuid4())
        self._current_message_id = ""
        self._message_started = False
        self._tools_called = 0
        self._turn_read_paths.clear()
        self._turn_start = _time.monotonic()
        self._status = "thinking"

        _log_event(f"[TURN START] thread={self._thread_id} run={self._run_id}")
        _trace(
            "agent.turn_start",
            session_id=self._session_id,
            thread_id=self._thread_id,
            run_id=self._run_id,
        )
        self._write_raw_sdk_record(
            {
                "kind": "turn_start",
                "thread_id": self._thread_id,
                "run_id": self._run_id,
                "prompt": prompt,
            }
        )

        # Tracing: Start turn span and capture context for the SDK callback thread
        tracer = get_tracer()
        turn_attrs = self._base_span_attributes()
        turn_attrs.update({
            "gen_ai.system": "gh-copilot-sdk",
            "gen_ai.request.model": os.getenv("AZURE_DEPLOYMENT", "unknown"),
            "gen_ai.operation.name": "chat",
        })
        turn_span_start_ns = _time.time_ns()
        turn_span = tracer.start_span(
            "agent.turn",
            attributes=turn_attrs,
            start_time=turn_span_start_ns,
        )
        self._otel_ctx = get_current_context()

        # Emit RunStartedEvent
        yield _sse_event(RunStartedEvent(
            thread_id=self._thread_id,
            run_id=self._run_id,
        ))

        try:
            await self._session.send({"prompt": prompt})

            while True:
                item = await self._queue.get()
                if item is None:
                    break
                yield _sse_event(item)
        except Exception as exc:
            self._write_raw_sdk_record(
                {
                    "kind": "turn_exception",
                    "thread_id": self._thread_id,
                    "run_id": self._run_id,
                    "error": repr(exc),
                }
            )
            turn_span.record_exception(exc)
            raise
        finally:
            self._write_raw_sdk_record(
                {
                    "kind": "turn_finalized",
                    "thread_id": self._thread_id,
                    "run_id": self._run_id,
                    "status": self._status,
                }
            )
            turn_span.end(end_time=max(turn_span_start_ns, _time.time_ns()))

async def run_analysis(prompt: str, working_dir: str) -> AsyncGenerator[str, None]:
    """Run a single-turn RFP analysis, yielding SSE-formatted AG-UI events.

    Convenience wrapper used by the CLI one-shot mode.
    """
    try:
        async with AgentSession(working_dir) as session:
            async for event in session.send(prompt):
                yield event
    except Exception as exc:
        yield _sse_event(RunErrorEvent(message=str(exc)))
