"""OpenTelemetry tracing shim for the session container.

Handles optional OTel initialization, context propagation across SDK threads,
and provides no-op fallbacks if tracing is disabled or packages are missing.
"""

import logging
import os
from contextlib import contextmanager
from typing import Any, Generator, Optional

from fastapi import FastAPI

logger = logging.getLogger(__name__)

_enabled = False
_tracer = None


class _NoopSpan:
    """Stub span that absorbs all OTel calls silently."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def set_attribute(self, key: str, value: Any):
        pass

    def record_exception(self, exception: Exception):
        pass

    def end(self, end_time: Optional[int] = None):
        pass

    def is_recording(self) -> bool:
        return False


class _NoopTracer:
    """Stub tracer that returns no-op spans."""

    def start_as_current_span(self, name: str, *args, **kwargs):
        return _NoopSpan()

    def start_span(self, name: str, *args, **kwargs):
        return _NoopSpan()


def setup_tracing(app: Optional[FastAPI] = None) -> None:
    """Initialize Azure Monitor tracing if connection string is present."""
    global _enabled, _tracer

    conn_str = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if not conn_str:
        logger.debug("Tracing: No connection string found, tracing disabled.")
        return

    try:
        from azure.monitor.opentelemetry import configure_azure_monitor
        from opentelemetry import trace
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        # 1. Configure Azure Monitor (SDK + Exporter)
        configure_azure_monitor(connection_string=conn_str)

        # 2. Instrument FastAPI if app is provided
        if app:
            FastAPIInstrumentor.instrument_app(app)

        # 3. Initialize global tracer
        _tracer = trace.get_tracer("rfp-agent.session-container")
        _enabled = True
        logger.info("Tracing enabled: Data sent to Application Insights.")

    except ImportError:
        logger.warning(
            "Tracing: APPLICATIONINSIGHTS_CONNECTION_STRING is set but OTel packages are missing. "
            "Install with: uv sync --extra tracing"
        )
    except Exception:
        logger.exception("Tracing: Failed to initialize OpenTelemetry.")


def get_tracer() -> Any:
    """Return the active OTel tracer or a no-op stub."""
    return _tracer if _enabled else _NoopTracer()


def is_enabled() -> bool:
    """Return True if tracing is active."""
    return _enabled


def get_current_context() -> Optional[Any]:
    """Capture the current OTel context (used to propagate to SDK threads)."""
    if not _enabled:
        return None
    try:
        from opentelemetry import context
        return context.get_current()
    except ImportError:
        return None


@contextmanager
def attach_context(otel_ctx: Optional[Any]) -> Generator[None, None, None]:
    """Attach a previously captured OTel context to the current thread."""
    if not _enabled or otel_ctx is None:
        yield
        return

    try:
        from opentelemetry import context
        token = context.attach(otel_ctx)
        try:
            yield
        finally:
            context.detach(token)
    except ImportError:
        yield


def truncate(text: Any, limit: int = 1000) -> str:
    """Safely truncate text for span attributes to avoid the 8KB App Insights limit."""
    if not isinstance(text, str):
        text = str(text)
    if len(text) <= limit:
        return text
    return text[:limit] + "... (truncated)"
