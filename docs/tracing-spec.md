# Tracing & Observability

---

## Local Dev Console Logging (`LOG_AGENT_EVENTS`)

A lightweight console logging mode built into `session-container/agent.py`. Useful for
investigating what the agent is doing — which tools it calls, in what order, how long
each takes, and how many turns it takes to settle — without setting up any cloud
infrastructure.

### Enabling it

Add to `.env`:
```
LOG_AGENT_EVENTS=true
```

Then start with `uv run dev.py` (see [Starting services correctly](#starting-services-correctly) below).

### What gets logged

```
INFO:agent.events:[TURN START] thread=92c3aaec... run=7b15164f...
INFO:agent.events:[THINKING] I'll start by listing the files in the working directory...
INFO:agent.events:[TOOL] >>> bash  args={"command": "ls -la"}
INFO:agent.events:[TOOL] <<< bash  duration=0.17s
INFO:agent.events:[TOOL] >>> view  args={"path": "/workspace"}
INFO:agent.events:[TOOL] <<< view  duration=0.09s
INFO:agent.events:[TOOL] >>> glob  args={"pattern": "**/*"}
INFO:agent.events:[TOOL] <<< glob  duration=0.08s
INFO:agent.events:[THINKING] Plan: I can see the RFP document...
INFO:agent.events:[TURN END] duration=44.28s  tools=4
```

`[THINKING]` only fires on the **first text delta** of each message (one line per assistant
message, not per token). `[TURN END]` includes wall-clock duration and total tool calls for
the turn.

### Implementation

- Module-level flag `_LOG = os.getenv("LOG_AGENT_EVENTS", "").lower() == "true"` — checked
  once at import time, zero overhead when disabled.
- `_log_event(msg)` helper returns immediately if `_LOG` is false — no `if _LOG:` scattered
  through event handlers.
- Tool timings: `_tool_names` stores `(tool_name, start_time)` tuples; duration computed at
  `TOOL_EXECUTION_COMPLETE`.
- Log level is `INFO` via Python's `logging` module (`logger = logging.getLogger("agent.events")`).
  Set `PYTHONUNBUFFERED=1` to prevent output buffering in the terminal.

---

### Starting services correctly

**Always use `uv run dev.py`** — it sets `POOL_MANAGEMENT_ENDPOINT=http://localhost:8080`
and `WORKSPACE=./workspace` before starting the child processes. If you start services
manually without these, session creation will fail with:

```
httpx.UnsupportedProtocol: Request URL is missing an 'http://' or 'https://' protocol.
```

If you must start services individually (e.g. to capture logs per-process):

```bash
# Session container — with event logging
LOG_AGENT_EVENTS=true PYTHONUNBUFFERED=1 \
  uv run uvicorn server:app --port 8080 \
  > /tmp/session-container.log 2>&1 &

# Orchestrator — must set POOL_MANAGEMENT_ENDPOINT explicitly
POOL_MANAGEMENT_ENDPOINT=http://localhost:8080 PYTHONUNBUFFERED=1 \
  uv run uvicorn app:app --port 8000 \
  > /tmp/orchestrator.log 2>&1 &

# Frontend
cd frontend && npm run dev > /tmp/frontend.log 2>&1 &
```

---

### Investigating agent behaviour

Start the stack with `LOG_AGENT_EVENTS=true`, use the frontend to upload an RFP and
trigger a workflow (e.g. "Run a bid/no-bid analysis"), then read the log:

```bash
# If started with services split (logs to file):
grep -E "\[TURN|TOOL|THINKING|ERROR" /tmp/session-container.log

# If started with dev.py (logs interleaved in terminal):
# filter with grep in a second terminal:
tail -f /tmp/session-container.log | grep -E "\[TURN|TOOL|THINKING|ERROR"
```

Sample output from a real bid/no-bid analysis run (City of Lakewood audit RFP):

```
[TURN START] thread=92c3aaec... run=7c711356...
[TOOL] >>> bash  args={"command": "ls -la", "description": "List files in the current directory"}
[TOOL] <<< bash  duration=0.17s
[TOOL] >>> bash  args={"command": "ls -la || ..."}
[TOOL] <<< bash  duration=0.16s
[TOOL] >>> view  args={"path": "/workspace"}
[TOOL] <<< view  duration=0.09s
[TOOL] >>> glob  args={"pattern": "**/*"}
[TOOL] <<< glob  duration=0.08s
[THINKING] Plan: ...
[TURN END] duration=44.28s  tools=4
```

For a repeatable investigation, the existing `tests/comprehensive.spec.ts` Journey 2
("Upload Document and Discuss") is the closest match — upload a `.txt` RFP file and
send a message. The `navigateToChatViaIntake` helper handles session retry logic.

---

# Foundry Tracing — Implementation Spec

## Overview

Add optional OpenTelemetry tracing to the session container so that every agent turn — including all tool calls, arguments, and outcomes — is visible in the Microsoft Foundry portal's Observability tab (backed by Azure Application Insights).

Tracing is **opt-in**: if `APPLICATIONINSIGHTS_CONNECTION_STRING` is not set or the OTel packages are not installed, the app behaves identically to today with zero overhead. No `if tracing_enabled:` guards are scattered through business logic — a no-op stub pattern absorbs all calls silently.

---

## "Sense-level" Tracing Strategy

To avoid hitting the 8KB span attribute limit while maintaining high visibility, we capture:

1. **Assistant Thoughts**: The first 200 characters of the assistant's initial response delta.
2. **Tool Calls**: Full tool name and truncated arguments (up to 1,000 characters).
3. **Tool Results**: The first 200 characters of the tool's output.

This provides enough context to understand the agent's logic without cluttering Application Insights with massive document blobs.

## Out of scope (this iteration)

- Orchestrator-level distributed tracing (end-to-end `traceparent` propagation from frontend through orchestrator to session container)
- Groundedness or safety evaluation scores (separate Foundry feature)
- Logging prompt/completion content to App Insights (data residency concern — revisit separately)
- Frontend tracing

---

## Architecture

```
session-container/server.py       calls setup_tracing(app) on startup
session-container/agent.py        calls get_tracer() — uses spans around turns and tool calls
session-container/tracing.py      NEW — no-op stubs or real OTel, selected at startup

        if APPLICATIONINSIGHTS_CONNECTION_STRING set AND packages installed:
                OTel SDK → Azure Monitor Exporter → Application Insights → Foundry portal
        else:
                _NoopTracer / _NoopSpan — all calls are zero-cost pass-throughs
```

### Why a dedicated module rather than inline guards

Inline `if tracing_enabled:` checks would spread conditional logic across `agent.py` and `server.py`. A stub module keeps the tracing concern isolated: callers write unconditional tracing code, and the stub absorbs it when tracing is off. This also makes the real implementation swappable (e.g. a different OTLP backend) without touching `agent.py`.

### Why not `azure-ai-projects` / `AIProjectClient`

`AIProjectClient.telemetry` is designed for Foundry-native frameworks (Semantic Kernel, LangChain-Azure, Azure AI Agents SDK) which auto-instrument themselves. The GitHub Copilot SDK is not one of these. `AIProjectClient` would only provide the App Insights connection string — the instrumentation still has to be manual. Going directly to `azure-monitor-opentelemetry` skips the indirection.

### Thread-safety

The Copilot SDK's `_on_event` callback fires on the SDK's **internal thread**, not the asyncio event loop thread. OpenTelemetry context (which span is "current") is thread-local and does not cross thread boundaries automatically.

Solution: at the start of each turn in `send()`, capture the current OTel context with `opentelemetry.context.get_current()` and store it on the session instance. In `_on_event`, explicitly attach that context before starting a child span and detach it after ending the span. This makes the child spans correctly parented without polluting the SDK thread's context.

---

## Files changed

| File | Change |
|---|---|
| `session-container/tracing.py` | **New file** — stub module |
| `session-container/pyproject.toml` | Add `[project.optional-dependencies] tracing = [...]` |
| `session-container/server.py` | Import and call `setup_tracing(app)` after app init |
| `session-container/agent.py` | Import `get_tracer`, add parent span in `send()`, add child spans in `_on_event` |
| `infra/deploy.sh` | Create App Insights resource, pass connection string to session container env |
| `.env.example` | Document `APPLICATIONINSIGHTS_CONNECTION_STRING` |

---

## `session-container/tracing.py` — detailed spec

### Public interface

```python
def setup_tracing(app: FastAPI | None = None) -> None
def get_tracer() -> _NoopTracer | opentelemetry.trace.Tracer
def get_context() -> opentelemetry.context.Context | None  # returns current OTel context
def is_enabled() -> bool
```

### No-op stubs (active when tracing is off)

`_NoopSpan` must implement:
- `__enter__` / `__exit__` — context manager support
- `set_attribute(key, value)` — silent no-op
- `record_exception(exc)` — silent no-op
- `end()` — silent no-op

`_NoopTracer` must implement:
- `start_span(name, context=None, **kwargs) -> _NoopSpan`

`_NoopContext` — returned by `get_context()` when disabled; `context.attach()` must handle it without error (pass `None` or return a no-op token).

### `setup_tracing` behaviour

1. Read `APPLICATIONINSIGHTS_CONNECTION_STRING` from env. If absent, return immediately — no-ops remain active.
2. Attempt to import `azure.monitor.opentelemetry` and `opentelemetry.trace`. If `ImportError`, log a `WARNING`:
   ```
   Tracing: APPLICATIONINSIGHTS_CONNECTION_STRING is set but OTel packages are not installed.
   Install with: uv sync --extra tracing
   ```
   Return without raising — app continues normally.
3. Call `configure_azure_monitor(connection_string=conn_str)`.
4. If `app` is provided, call `FastAPIInstrumentor.instrument_app(app)` to capture HTTP request/response traces.
5. Assign `_tracer = opentelemetry.trace.get_tracer("rfp-agent.session-container")`.
6. Set `_enabled = True`.
7. Log `INFO: Tracing enabled → Application Insights`.

---

## `session-container/agent.py` — detailed spec

### Imports added

```python
from tracing import get_tracer
import opentelemetry.context as otel_context  # only used when tracing enabled; guard with try/except or import unconditionally (SDK is a no-op stub)
```

Because `opentelemetry` may not be installed, import it inside `tracing.py` only. Expose `attach_context(ctx)` and `detach_context(token)` helpers from `tracing.py` that fall back to no-ops.

Revised public interface for `tracing.py`:

```python
def attach_context(ctx) -> object   # returns token; no-op token if disabled
def detach_context(token) -> None   # no-op if disabled
```

### Instance state added to `AgentSession.__init__`

```python
self._otel_ctx = None                        # OTel context captured at turn start
self._active_spans: dict[str, tuple] = {}    # call_id → (span, context_token)
```

### `send()` changes

Wrap the existing body in a parent span:

```python
async def send(self, prompt: str) -> AsyncGenerator[str, None]:
    # ... existing drain + reset logic unchanged ...

    tracer = get_tracer()
    span = tracer.start_span(
        "agent.turn",
        attributes={
            "thread_id": self._thread_id,
            "run_id": self._run_id,
        }
    )
    self._otel_ctx = otel_context.get_current() if is_enabled() else None

    # ... existing RunStartedEvent yield + session.send() call unchanged ...

    try:
        while True:
            item = await self._queue.get()
            if item is None:
                break
            yield _sse_event(item)
    except Exception as exc:
        span.record_exception(exc)
        raise
    finally:
        span.end()
```

### `_on_event` changes

**`TOOL_EXECUTION_START` — add after existing logic:**

```python
token = attach_context(self._otel_ctx)
span = get_tracer().start_span(
    "agent.tool_call",
    attributes={
        "tool.name": tool,
        "tool.call_id": call_id,
        "tool.arguments": args_str or "",
    }
)
self._active_spans[call_id] = (span, token)
```

**`TOOL_EXECUTION_COMPLETE` — add after existing logic:**

```python
if call_id in self._active_spans:
    span, token = self._active_spans.pop(call_id)
    span.end()
    detach_context(token)
```

**`SESSION_ERROR` — add before existing enqueue:**

```python
if call_id in self._active_spans:  # close any open tool spans on error
    for span, token in self._active_spans.values():
        span.record_exception(Exception(msg))
        span.end()
        detach_context(token)
    self._active_spans.clear()
```

---

## `session-container/pyproject.toml` — detailed spec

```toml
[project.optional-dependencies]
tracing = [
    "opentelemetry-sdk>=1.30.0",
    "opentelemetry-instrumentation-fastapi>=0.51b0",
    "azure-monitor-opentelemetry>=1.6.0",
]
```

Install for a tracing-enabled deployment:
```bash
uv sync --extra tracing
```

Local dev (no tracing):
```bash
uv sync   # unchanged — no new required deps
```

---

## `session-container/server.py` — detailed spec

Add after `app = FastAPI(title="RFP Session")`:

```python
from tracing import setup_tracing
setup_tracing(app)
```

That's the only change to `server.py`.

---

## `infra/deploy.sh` — detailed spec

### New resource: Application Insights

Create an Application Insights workspace-based instance in the same resource group:

```bash
# Create Log Analytics workspace (required for workspace-based App Insights)
az monitor log-analytics workspace create \
  --resource-group "$RG" \
  --workspace-name "${PREFIX}-logs" \
  --location "$LOCATION"

# Create Application Insights
az monitor app-insights component create \
  --app "${PREFIX}-insights" \
  --resource-group "$RG" \
  --location "$LOCATION" \
  --workspace "$(az monitor log-analytics workspace show \
      --resource-group "$RG" \
      --workspace-name "${PREFIX}-logs" \
      --query id -o tsv)"
```

### Pass connection string to session container

```bash
APPINSIGHTS_CONN=$(az monitor app-insights component show \
  --app "${PREFIX}-insights" \
  --resource-group "$RG" \
  --query connectionString -o tsv)

# Add to session pool environment variables alongside existing ones
--env-vars "APPLICATIONINSIGHTS_CONNECTION_STRING=$APPINSIGHTS_CONN" ...
```

### Dockerfile change

The session container Dockerfile needs `uv sync --extra tracing` instead of bare `uv sync` so the OTel packages are present in the production image. Local dev continues to use bare `uv sync`.

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | No | If set (and packages installed), enables tracing. Retrieve from Azure portal → App Insights → Connection String. |

Add to `.env.example`:
```
# Optional: enable Foundry tracing (requires: uv sync --extra tracing)
# APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...;IngestionEndpoint=...
```

---

## What traces look like in Foundry portal

Navigate to: **Foundry portal → your project → Observability → Traces**

Each agent turn appears as a trace tree (spans appear within ~2 minutes of execution):

```
agent.turn  [thread_id=abc, run_id=xyz]                          2.3s
  ├── agent.tool_call  [tool.name=bash, args="ls /workspace"]    0.4s
  ├── agent.tool_call  [tool.name=grep, args="evaluation crit…"] 0.2s
  ├── agent.tool_call  [tool.name=knowledge_base_retrieve, …]    0.6s
  └── agent.tool_call  [tool.name=bash, args="python score.py"]  1.1s
```

HTTP request spans from FastAPI instrumentation appear as a separate root span per `/chat/stream` request, linked by trace context.

---

## Testing

No new Playwright tests required — the existing test suite validates functional behaviour. Tracing is infrastructure-only.

Manual verification:
1. Set `APPLICATIONINSIGHTS_CONNECTION_STRING` in `.env`
2. Run `uv sync --extra tracing && uv run dev.py`
3. Send a message in the UI that triggers tool calls
4. Wait ~2 minutes, check Foundry portal Observability > Traces
5. Confirm turn span with correct `thread_id` / `run_id` and child spans per tool call

Verify no-op path:
1. Unset `APPLICATIONINSIGHTS_CONNECTION_STRING`
2. Run `uv run dev.py`
3. Confirm no errors, no import warnings, behaviour unchanged

---

## Open questions

1. **Prompt content in traces** — should the user's prompt text be attached as a span attribute? Useful for debugging but raises data residency considerations. Defaulting to off; could be gated on a separate `TRACE_INCLUDE_CONTENT=true` env var.
2. **Orchestrator distributed tracing** — propagating `traceparent` headers through the SSE proxy so frontend → orchestrator → session container appear as one trace. Out of scope here but the foundation this spec lays (OTel in the session container) is the prerequisite.
3. **Retention policy** — Application Insights default retention is 90 days. Should this be configurable in `deploy.sh`?
