"""AgentSession wrapping the GitHub Copilot SDK with an event queue.

Provides a streaming async generator interface for running agent turns
against Azure OpenAI.  Emits AG-UI protocol events.
"""

import asyncio
import os
import sys
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
from dotenv import load_dotenv

from copilot import CopilotClient
from copilot.generated.session_events import SessionEventType

load_dotenv()

SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT", "")
SEARCH_KB_NAME = os.getenv("AZURE_SEARCH_KB_NAME", "rfp-knowledge")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY", "")

SYSTEM_PROMPT = """\
You are an RFP Response Accelerator for Meridian & Associates LLP, a professional \
services firm specializing in audit, tax, and advisory/consulting engagements. Your \
role is to help pursuit teams analyze RFPs, develop winning strategies, and produce \
high-quality proposal content efficiently.

You have access to built-in tools: bash, grep, glob, and str_replace_editor. Use \
them proactively to read files, search for content, and produce structured output.

## Sandbox Environment

You run inside an isolated container with full shell access. You can:
- **Install packages** (`pip install fpdf2 python-docx matplotlib openpyxl` etc.)
- **Write and execute Python scripts** for calculations, data processing, and file generation
- **Generate deliverable files** (PDF, DOCX, XLSX, CSV, JSON, PNG) and save them to \
the working directory where users can download them
- **Run complex computations** — pricing models, sensitivity analyses, scoring calculations

When a skill produces structured output (compliance matrices, risk registers, pricing \
models, scorecards), save it as a downloadable file in the working directory in addition \
to showing it in chat. Prefer PDF or DOCX for polished deliverables, CSV/XLSX for data \
tables, and markdown for working drafts.

## Getting Started

When the workspace has no uploaded documents (or only default files), greet the user \
warmly and guide them to upload their RFP document as the first step. Once an RFP is \
uploaded, use the `convert_document` tool to convert it to markdown for analysis. \
The full suite of RFP workflow tools — from bid/no-bid analysis through compliance \
review — becomes available after conversion. Start by asking the user to drag and \
drop or attach their RFP file.

If the user sends a simple greeting (for example "hi" or "hello"), respond naturally \
and briefly first. Do not mention missing files unless the user asks to start analysis \
or asks what to do next.

## Document Conversion

You have a `convert_document` tool that converts uploaded documents (PDF, images, \
Office files) to structured markdown using Azure Content Understanding. When a user \
uploads a file, call `convert_document` with the filename to produce a `.md` version \
in the working directory. The tool is idempotent — it skips conversion if the markdown \
file already exists. After conversion, read the markdown file to analyze the content.

## Skills & Workflows

You have detailed skill guides loaded for structured RFP workflows. Reference them \
for step-by-step processes, scoring frameworks, and output templates:

1. **Bid/No-Bid Analysis** — Evaluate whether to pursue an opportunity. Produces a \
scorecard across six dimensions (strategic fit, capability match, resource availability, \
win probability, past performance, profitability) with a Go/No-Go/Conditional Go \
recommendation.

2. **Requirements Extraction** — Parse the RFP into discrete requirements. Classify \
each as mandatory/preferred/informational, build a compliance matrix, flag ambiguities, \
and map requirements to response outline sections.

3. **Response Strategy** — Define 3-5 win themes, analyze the competitive landscape, \
develop customer insights, and outline a pricing strategy approach. Produces a strategy \
brief that guides all subsequent drafting.

4. **Draft Generation** — Write proposal sections by combining knowledge base materials \
(past proposals, boilerplate, case studies) with new content tailored to the opportunity. \
Always cite KB sources and flag content gaps.

5. **Executive Summary** — Synthesize all analysis into a compelling 1-2 page summary \
structured as: customer problem, our solution, why Meridian, key differentiators, and \
call to confidence. Must reflect established win themes.

6. **Compliance Review** — Systematic pre-submission check: requirement coverage, \
submission instruction compliance, terminology consistency, sensitive data scan, \
branding/formatting compliance, tone/quality assessment, and executive review readiness. \
Produces a pass/fail checklist with sign-off tracker.

7. **Risk & Gap Analysis** — Identify technical risks, compliance gaps, resource \
constraints, and dependencies. Score severity and likelihood, propose mitigations. \
Produces a risk register.

8. **ROI & Pricing Analysis** — Build bottom-up cost models, analyze margins and \
profitability, run sensitivity scenarios, benchmark against past engagements, and \
recommend competitive price positioning.

9. **Customer Intelligence** — Aggregate all available information about a client \
into a structured briefing: organization profile, relationship history, pain points, \
decision-making insights, strategic value, and personalization recommendations.

10. **Iterative Refinement** — Guide the collaborative editing cycle: cross-section \
consistency checks, section-level improvements, collateral generation (resumes, org \
charts, pricing tables), and review status tracking.

## Working Approach

- **Start by orienting**: List files in the working directory to understand available \
materials before diving into analysis. Skip this for casual greetings and other \
small-talk turns.
- **Be structured**: Use markdown tables, numbered lists, and clear headings. Follow \
the output templates from your skill guides.
- **Be thorough but concise**: Every paragraph should earn its place. Prefer specifics \
and evidence over generic statements.
- **Be proactive**: When you identify risks, gaps, or ambiguities, surface them without \
being asked.
- **Cite sources**: When referencing KB content or specific documents, note where the \
information came from.
- **Professional tone**: Write as a senior proposal manager would — confident, precise, \
client-focused. Use active voice. Avoid jargon unless the RFP uses it.

## Output Formatting

- Use markdown throughout: tables for matrices and scorecards, headers for sections, \
bold for emphasis.
- For compliance and risk items, always include a status or severity indicator.
- When generating proposal content, produce submission-ready prose (not bullet outlines) \
unless the user requests otherwise.
- Flag items needing human review with clear action items.
- Do not expose internal file system details in user-facing responses. Reference files by \
filename only, and avoid absolute paths or mentions of workspace directories.
"""

KB_PROMPT_SECTION = """\
## Knowledge Base

You have access to a `knowledge_base_retrieve` tool that searches Meridian & \
Associates LLP's indexed document repository. The knowledge base contains:

- **Past proposals and engagement letters** — Previously submitted RFP responses, \
including technical approaches, staffing plans, and pricing narratives
- **Boilerplate and approved language** — Firm overview, methodology descriptions, \
service line capabilities, and standard compliance language
- **Personnel records and bios** — Partner, manager, and staff qualifications, \
certifications (CPA, CISA, CIA, etc.), and experience summaries
- **Case studies and past performance** — Client engagement narratives with \
measurable outcomes across audit, tax, and advisory practices
- **Compliance and regulatory documents** — Quality control policies, independence \
procedures, peer review results, and professional standards references
- **Pricing frameworks** — Rate structures, fee estimation templates, and historical \
pricing for comparable engagements
- **Certifications and accreditations** — Firm registrations, insurance certificates, \
minority/diversity certifications, and industry memberships
- **Branding and style guidelines** — Approved firm descriptions, logo usage, and \
editorial standards

Use `knowledge_base_retrieve` proactively whenever you need evidence to support \
claims, verify capabilities, find relevant past work, or retrieve approved language. \
Run multiple searches with varied query terms to maximize coverage — a single query \
rarely surfaces everything relevant.

"""


def _sse_event(event: BaseEvent) -> str:
    """Format an AG-UI event as an SSE data line."""
    return f"data: {event.model_dump_json(exclude_none=True)}\n\n"


class AgentSession:
    """Async context manager that holds a persistent Copilot session.

    Usage::

        async with AgentSession(working_dir) as session:
            async for event in session.send("hello"):
                print(event)
    """

    def __init__(self, working_dir: str, token: str | None = None):
        self._working_dir = working_dir
        self._initial_token = token
        self._client: CopilotClient | None = None
        self._session = None
        self._unsubscribe = None
        self._queue: asyncio.Queue[BaseEvent | None] = asyncio.Queue()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._tool_names: dict[str, str] = {}
        self._status: str = "idle"
        self._credential: DefaultAzureCredential | None = None

        # AG-UI state tracked per turn
        self._thread_id: str = str(uuid.uuid4())
        self._run_id: str = ""
        self._current_message_id: str = ""
        self._message_started: bool = False

    @property
    def status(self) -> str:
        """Current activity: 'idle', 'thinking', 'tool:<name>', or 'error'."""
        return self._status

    async def __aenter__(self) -> "AgentSession":
        token = self._initial_token or os.getenv("AZURE_OPENAI_TOKEN")
        if not token:
            self._credential = DefaultAzureCredential()
            tok = await self._credential.get_token(
                "https://cognitiveservices.azure.com/.default"
            )
            token = tok.token

        self._client = CopilotClient(
            {"cli_args": ["--allow-all-tools", "--allow-all-paths"]}
        )
        await self._client.start()

        self._loop = asyncio.get_running_loop()

        # Resolve skills directory relative to this file
        skills_dir = str(Path(__file__).parent / "skills")

        # Build system prompt — include KB section only when search is configured
        kb_enabled = bool(SEARCH_ENDPOINT)
        system_prompt = SYSTEM_PROMPT
        if kb_enabled:
            system_prompt = SYSTEM_PROMPT.replace(
                "## Skills & Workflows",
                KB_PROMPT_SECTION + "## Skills & Workflows",
            )

        session_config = {
            "model": os.environ["AZURE_DEPLOYMENT"],
            "provider": {
                "type": "openai",
                "base_url": os.environ["AZURE_ENDPOINT"],
                "bearer_token": token,
                "wire_api": "responses",
            },
            "system_message": {
                "mode": "append",
                "content": system_prompt,
            },
            "working_directory": self._working_dir,
            "skill_directories": [skills_dir],
            "excluded_tools": ["web_fetch"],
            "streaming": True,
            "on_permission_request": lambda _req, _ctx: {"kind": "approved"},
        }

        # MCP servers
        mcp_servers = {
            "document_converter": {
                "type": "stdio",
                "command": sys.executable,
                "args": [str(Path(__file__).parent / "tools" / "convert_document.py")],
                "tools": ["convert_document"],
                "env": {
                    "AZURE_ENDPOINT": os.environ.get("AZURE_ENDPOINT", ""),
                    "ADLS_ACCOUNT_NAME": os.getenv("ADLS_ACCOUNT_NAME", ""),
                    "ADLS_FILESYSTEM": os.getenv("ADLS_FILESYSTEM", "documents"),
                    "WORKSPACE": self._working_dir,
                },
            },
        }

        # Add Foundry IQ knowledge base via MCP (optional)
        if kb_enabled:
            mcp_servers["knowledge_base"] = {
                "type": "http",
                "url": (
                    f"{SEARCH_ENDPOINT}/knowledgebases/{SEARCH_KB_NAME}"
                    f"/mcp?api-version=2025-11-01-preview"
                ),
                "headers": {"api-key": SEARCH_KEY},
                "tools": ["knowledge_base_retrieve"],
            }

        session_config["mcp_servers"] = mcp_servers

        self._session = await self._client.create_session(session_config)

        self._unsubscribe = self._session.on(self._on_event)
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

        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            self._status = "thinking"
            delta = getattr(event.data, "delta_content", None) or ""
            if not delta:
                return

            # Emit TextMessageStartEvent on first delta
            if not self._message_started:
                self._current_message_id = str(uuid.uuid4())
                self._message_started = True
                self._enqueue(TextMessageStartEvent(
                    message_id=self._current_message_id,
                    role="assistant",
                ))

            self._enqueue(TextMessageContentEvent(
                message_id=self._current_message_id,
                delta=delta,
            ))

        elif event.type == SessionEventType.ASSISTANT_MESSAGE:
            # End the current text message
            if self._message_started:
                self._enqueue(TextMessageEndEvent(
                    message_id=self._current_message_id,
                ))
                self._message_started = False

        elif event.type == SessionEventType.TOOL_EXECUTION_START:
            tool = getattr(event.data, "tool_name", None) or "unknown"
            call_id = getattr(event.data, "tool_call_id", None) or str(uuid.uuid4())
            self._tool_names[call_id] = tool
            # Internal SDK tools — track them but don't surface to the frontend
            if tool in ("report_intent",):
                return
            self._status = f"tool:{tool}"
            self._enqueue(ToolCallStartEvent(
                tool_call_id=call_id,
                tool_call_name=tool,
                parent_message_id=self._current_message_id or None,
            ))
            # Forward arguments so the frontend can show human-readable context
            args = getattr(event.data, "arguments", None)
            if args:
                import json as _json
                args_str = args if isinstance(args, str) else _json.dumps(args)
                self._enqueue(ToolCallArgsEvent(
                    tool_call_id=call_id,
                    delta=args_str,
                ))

        elif event.type == SessionEventType.TOOL_EXECUTION_COMPLETE:
            call_id = getattr(event.data, "tool_call_id", None)
            if not call_id:
                # Recover the UUID assigned at start by matching on tool name
                tool_name_hint = getattr(event.data, "tool_name", None)
                if tool_name_hint:
                    call_id = next(
                        (k for k, v in self._tool_names.items() if v == tool_name_hint),
                        None,
                    )
            tool = self._tool_names.pop(call_id, None) if call_id else None
            tool = tool or getattr(event.data, "tool_name", None) or "unknown"
            # Suppress end event for internal tools that were filtered at start
            if tool in ("report_intent",):
                return
            self._status = "thinking"
            if call_id:
                self._enqueue(ToolCallEndEvent(tool_call_id=call_id))

        elif event.type == SessionEventType.SESSION_IDLE:
            self._status = "idle"
            self._enqueue(RunFinishedEvent(
                thread_id=self._thread_id,
                run_id=self._run_id,
            ))
            self._loop.call_soon_threadsafe(self._queue.put_nowait, None)
            return

        elif event.type == SessionEventType.SESSION_ERROR:
            self._status = "error"
            msg = getattr(event.data, "message", None) or "Unknown error"
            self._enqueue(RunErrorEvent(message=msg))
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
        self._status = "thinking"

        # Emit RunStartedEvent
        yield _sse_event(RunStartedEvent(
            thread_id=self._thread_id,
            run_id=self._run_id,
        ))

        await self._session.send({"prompt": prompt})

        while True:
            item = await self._queue.get()
            if item is None:
                break
            yield _sse_event(item)

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
