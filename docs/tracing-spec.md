# Foundry Tracing — Implementation Spec

## Overview

Add optional OpenTelemetry tracing to the session container so that every agent turn — including all tool calls, arguments, and outcomes — is visible in the Microsoft Foundry portal's Observability tab (backed by Azure Application Insights).

Tracing is **opt-in**: if `APPLICATIONINSIGHTS_CONNECTION_STRING` is not set or the OTel packages are not installed, the app behaves identically to today with zero overhead. No `if tracing_enabled:` guards are scattered through business logic — a no-op stub pattern absorbs all calls silently.

---

## Goals

- Per-turn parent spans with session/thread/run metadata
- Per-tool-call child spans with tool name and arguments
- Visible in Foundry portal Observability > Traces within ~2 minutes of execution
- Zero impact on existing behaviour when not configured
- Packages are optional extras, not required dependencies
- Local dev works without any tracing config

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
