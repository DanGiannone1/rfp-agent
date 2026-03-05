"""AgentSession wrapping the GitHub Copilot SDK with an event queue.

Provides both streaming (async generator) and blocking (collect) interfaces
for running agent turns against Azure OpenAI.
"""

import asyncio
import json
import os
from collections.abc import AsyncGenerator
from pathlib import Path

from azure.identity import DefaultAzureCredential
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

{kb_prompt}\
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
materials before diving into analysis.
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

    async def __aenter__(self, token: str | None = None) -> "AgentSession":
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

        # Build session config
        kb_enabled = bool(SEARCH_ENDPOINT)
        system_prompt = SYSTEM_PROMPT.format(
            kb_prompt=KB_PROMPT_SECTION if kb_enabled else ""
        )

        # Resolve skills directory relative to this file
        skills_dir = str(Path(__file__).parent / "skills")

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

        # Add Foundry IQ knowledge base via MCP (optional)
        if kb_enabled:
            session_config["mcp_servers"] = {
                "knowledge_base": {
                    "type": "http",
                    "url": (
                        f"{SEARCH_ENDPOINT}/knowledgebases/{SEARCH_KB_NAME}"
                        f"/mcp?api-version=2025-11-01-preview"
                    ),
                    "headers": {"api-key": SEARCH_KEY},
                    "tools": ["knowledge_base_retrieve"],
                },
            }

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

    def _on_event(self, event) -> None:
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
