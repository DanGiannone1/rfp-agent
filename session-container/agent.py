"""AgentSession wrapping the GitHub Copilot SDK with an event queue.

Provides a streaming async generator interface for running agent turns
against Azure OpenAI.  Emits AG-UI protocol events.
"""

import asyncio
import json as _json
import logging as _logging
import os
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
from dotenv import load_dotenv

from copilot import CopilotClient
from copilot.generated.session_events import SessionEventType

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
You are an RFP Response Accelerator for Meridian & Associates LLP, a professional \
services firm specializing in audit, tax, and advisory/consulting engagements. Your \
role is to help pursuit teams analyze RFPs, develop winning strategies, and produce \
high-quality proposal content efficiently.

You have access to built-in tools: bash, grep, glob, and str_replace_editor.

**Reading documents:** Always read RFP and proposal documents in full using `bash` \
or `str_replace_editor`. Do not use `grep` or `glob` as a substitute for reading — \
keyword searching an RFP misses context, nuance, and requirements that don't use \
standard trigger words. If a document is very large (hundreds of pages), read it \
section by section and extract findings from each section before moving to the next. \
Never skip sections.

**grep and glob** are for cross-file tasks: finding files in the workspace, verifying \
consistency across multiple drafted sections, confirming a term appears across documents, \
or spot-checking after a full read. They are not a primary analysis tool for RFPs.

## Sandbox Environment

You run inside an isolated container with full shell access. You can:
- **Write and execute Python scripts** for calculations, data processing, and structured output
- **Generate deliverable files** and save them to the working directory where users can download them
- **Run complex computations** — pricing models, sensitivity analyses, scoring calculations

When a skill produces structured output (compliance matrices, risk registers, pricing \
models, scorecards), save it as a file in the working directory. Use **markdown (.md) \
for all narrative deliverables** (executive summaries, strategy briefs, compliance \
reviews), **CSV for scored matrices and data tables**, and **JSON for structured data**. \
Do not attempt to install packages or generate binary formats (DOCX, PDF, XLSX) — the \
workspace renderer displays markdown and CSV natively.

**Do not reproduce saved file content in chat.** When you save a deliverable, briefly \
state what you created and any key highlights or next steps — the user can view the \
full content in the artifact panel. Repeating the full artifact in chat is redundant \
and clutters the conversation.

## Getting Started

**Accuracy over speed:** Prioritize correctness and completeness over speed. Do not skip steps or rely on partial reads.

When the user sends their first message, RFP documents have already been uploaded and \
converted to markdown — you will find a `.md` file in the working directory alongside \
the original. Start by listing files to orient yourself, then read the markdown to \
understand the opportunity before responding.

**Reading RFP documents:** Always attempt to read the full document in one pass. \
Do not use search (grep) to extract requirements or summaries before you have read the full RFP. \
Most RFPs are well within what you can handle in a single read. Only fall back to \
chunked reading if the file is very large (roughly 500+ KB or 10,000+ lines) — \
in that case, read it section by section in logical order (front matter and scope \
first, then technical requirements, staffing, pricing, and administrative sections) \
and complete your analysis incrementally before synthesizing findings. Do not \
summarize prematurely — read the entire document before drawing conclusions.

If the user sends a simple greeting (for example "hi" or "hello"), respond naturally \
and briefly first. Do not mention missing files unless the user asks to start analysis \
or asks what to do next.

## Skills & Workflows

**Before starting any structured task, read the relevant skill guide.** Each skill \
contains the step-by-step process, scoring framework, and output template you must \
follow. Do not improvise a workflow when a skill exists for the task — the skill is \
the authoritative procedure. If a request maps to one of the skills below, read that \
skill first, then execute it. Skill guides are at \
`/app/skills/{skill-name}/SKILL.md` (e.g. \
`/app/skills/bid-no-bid-analysis/SKILL.md`).

The available skills are:

1. **Bid/No-Bid Analysis** — Evaluate whether to pursue an opportunity. Produces a \
scorecard across six dimensions (strategic fit, capability match, resource availability, \
win probability, past performance, profitability) with a Go/No-Go/Conditional Go \
recommendation.

2. **Requirements Extraction** — Parse the RFP into discrete requirements. Classify \
each as mandatory/preferred/informational, build a traceability matrix with section and \
page references, flag ambiguities, and map requirements to response outline sections.

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

8. **Pricing Analysis** — Build bottom-up cost models, analyze margins and \
profitability, run sensitivity scenarios, benchmark against past engagements, and \
recommend competitive price positioning.

9. **Customer Intelligence** — Aggregate all available information about a client \
into a structured briefing: organization profile, relationship history, pain points, \
decision-making insights, strategic value, and personalization recommendations.

10. **Iterative Refinement** — Guide the collaborative editing cycle: cross-section \
consistency checks, section-level improvements, collateral generation (resumes, org \
charts, pricing tables), and review status tracking.

## Working Approach

- **Check for a skill first**: Before doing any structured work, identify whether a \
skill covers the request. If one does, read it and follow its process — do not skip \
steps or improvise. Skills exist for: bid/no-bid, requirements extraction, response \
strategy, draft generation, executive summary, compliance review, risk & gap analysis, \
pricing analysis, customer intelligence, and iterative refinement.
- **Start by orienting**: Review available documents before diving into analysis. \
Skip this for casual greetings and other small-talk turns.
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

## Communicating With Users

You are talking to business professionals — proposal managers, partners, and pursuit \
team members. Speak accordingly.

- **Do not narrate technical operations.** Never mention tools, file paths, workspace \
directories, grep commands, markdown files, or shell operations in your responses. \
Say "I'll review the RFP" not "I'll read the .md file". Say "I've prepared the \
compliance matrix" not "I've saved the CSV to the working directory".
- **Summarize what you're doing in business terms.** If you need to explain your \
process, say "I'm analyzing the RFP", "I'm checking our past proposals", or \
"I'm reviewing the drafted sections" — not the underlying tool calls.
- **Present outputs, not operations.** Lead with findings and deliverables. The user \
does not need to know how you produced them.
- **When a deliverable is ready**, simply say what it is and what they can do next. \
Do not describe that you saved a file or where it was saved.

## Output Formatting

- Use markdown throughout: tables for matrices and scorecards, headers for sections, \
bold for emphasis.
- For compliance and risk items, always include a status or severity indicator.
- When generating proposal content, produce submission-ready prose (not bullet outlines) \
unless the user requests otherwise.
- Flag items needing human review with clear action items.
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

Use `knowledge_base_retrieve` whenever you need to ground a claim in Meridian's \
actual capabilities, history, or approved language. This applies across the full \
proposal lifecycle: understanding whether the firm has done similar work before \
analyzing an opportunity, finding approved boilerplate and case studies before \
drafting sections, verifying certifications and personnel qualifications when \
assessing compliance, and benchmarking pricing against historical engagements. \
The KB is the authoritative source for anything about Meridian — prefer it over \
generating content from general knowledge.

Run multiple searches with varied query terms to maximize coverage. A single query \
rarely surfaces everything relevant; searching by service type, industry, engagement \
type, and specific requirement usually uncovers different documents. When the KB \
doesn't have what you need, note it so the user can follow up with the team.

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
        self._token = token
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

        # AG-UI state tracked per turn
        self._thread_id: str = str(uuid.uuid4())
        self._run_id: str = ""
        self._current_message_id: str = ""
        self._message_started: bool = False

    @property
    def status(self) -> str:
        """Current activity: 'idle', 'thinking', 'tool:<name>', or 'error'."""
        return self._status

    @property
    def token(self) -> str | None:
        return self._token

    def set_token(self, token: str | None) -> None:
        if token:
            self._token = token
        else:
            self._token = None

    async def __aenter__(self) -> "AgentSession":
        token = self._token or self._initial_token or os.getenv("AZURE_OPENAI_TOKEN")
        if not token:
            self._credential = DefaultAzureCredential()
            tok = await self._credential.get_token(
                "https://cognitiveservices.azure.com/.default"
            )
            token = tok.token
        self._token = token

        self._client = CopilotClient(
            {"cli_args": ["--allow-all-tools", "--allow-all-paths"]}
        )
        await self._client.start()

        self._loop = asyncio.get_running_loop()

        # Resolve skills directory relative to this file
        skills_dir = str(Path(__file__).parent / "skills")

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

        # MCP servers — knowledge base via Foundry IQ (optional).
        if SEARCH_ENDPOINT:
            kb_url = (
                f"{SEARCH_ENDPOINT}/knowledgebases/{SEARCH_KB_NAME}"
                f"/mcp?api-version=2025-11-01-preview"
            )
            if SEARCH_KEY:
                mcp_servers = {
                    "knowledge_base": {
                        "type": "http",
                        "url": kb_url,
                        "headers": {"api-key": SEARCH_KEY},
                        "tools": ["knowledge_base_retrieve"],
                    }
                }
            else:
                search_credential = self._credential or DefaultAzureCredential()
                search_tok = await search_credential.get_token(
                    "https://search.azure.com/.default"
                )
                mcp_servers = {
                    "knowledge_base": {
                        "type": "http",
                        "url": kb_url,
                        "headers": {"Authorization": f"Bearer {search_tok.token}"},
                        "tools": ["knowledge_base_retrieve"],
                    }
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
                _log_event(f"[THINKING] {delta[:120]}")
                _trace("agent.thinking", text=delta[:120])
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
            self._tool_names[call_id] = (tool, _time.monotonic())
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
            args_str = (args if isinstance(args, str) else _json.dumps(args)) if args else None
            if args_str:
                self._enqueue(ToolCallArgsEvent(
                    tool_call_id=call_id,
                    delta=args_str,
                ))
            _log_event(f"[TOOL] >>> {tool}  args={args_str or '{}'}")
            _trace("agent.tool_start", tool=tool, call_id=call_id, args=args_str or "{}")

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
            # Suppress end event for internal tools that were filtered at start
            if tool in ("report_intent",):
                return
            self._status = "thinking"
            self._tools_called += 1
            if call_id:
                self._enqueue(ToolCallEndEvent(tool_call_id=call_id))
            _log_event(f"[TOOL] <<< {tool}  duration={duration:.2f}s")
            _trace("agent.tool_end", tool=tool, call_id=call_id, duration_s=round(duration, 2))

        elif event.type == SessionEventType.SESSION_IDLE:
            self._status = "idle"
            turn_duration = _time.monotonic() - self._turn_start
            _log_event(
                f"[TURN END] duration={turn_duration:.2f}s"
                f"  tools={self._tools_called}"
            )
            _trace("agent.turn_end", duration_s=round(turn_duration, 2),
                   tools_called=self._tools_called)
            self._enqueue(RunFinishedEvent(
                thread_id=self._thread_id,
                run_id=self._run_id,
            ))
            self._loop.call_soon_threadsafe(self._queue.put_nowait, None)
            return

        elif event.type == SessionEventType.SESSION_ERROR:
            self._status = "error"
            msg = getattr(event.data, "message", None) or "Unknown error"
            if (
                "too many requests" in msg.lower()
                or "429" in msg
                or "rate limit" in msg.lower()
                or "capierror" in msg.lower()
            ):
                msg = (
                    "The AI service is temporarily rate-limited. "
                    "Please wait 30–60 seconds and try again."
                )
            _log_event(f"[ERROR] {msg}")
            _trace("agent.error", message=msg)
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
        self._turn_start = _time.monotonic()
        self._status = "thinking"

        _log_event(f"[TURN START] thread={self._thread_id} run={self._run_id}")
        _trace("agent.turn_start", thread_id=self._thread_id, run_id=self._run_id)

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
