"""FastAPI orchestrator — session CRUD, message streaming, and file upload.

Proxies all AI interactions to isolated session containers via SessionManager.
"""

import json
import logging
import os
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler

import httpx
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from session_manager import SessionManager

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Trace logging (opt-in via LOG_TRACE=true)
# ---------------------------------------------------------------------------
_trace_logger = logging.getLogger("trace")


def _setup_trace_logging() -> None:
    trace_dir = os.getenv("LOG_TRACE_DIR")
    if os.getenv("LOG_TRACE", "").lower() != "true" or not trace_dir:
        return
    path = os.path.join(trace_dir, "trace.jsonl")
    handler = RotatingFileHandler(path, maxBytes=50 * 1024 * 1024, backupCount=1)
    handler.setFormatter(logging.Formatter("%(message)s"))
    _trace_logger.addHandler(handler)
    _trace_logger.setLevel(logging.INFO)
    _trace_logger.propagate = False


def _trace(event: str, **data) -> None:
    if not _trace_logger.handlers:
        return
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "component": "orchestrator",
        "event": event,
        "data": data,
    }
    _trace_logger.info(json.dumps(record, default=str))


# ---------------------------------------------------------------------------
# Globals set during lifespan
# ---------------------------------------------------------------------------
session_manager: SessionManager | None = None
content_processor = None  # ContentProcessor | None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global session_manager, content_processor

    # Content Processing (optional — ADLS + Content Understanding)
    from content_processing import ContentProcessor

    content_processor = ContentProcessor()
    try:
        await content_processor.initialize()
    except Exception:
        logger.warning("Content processing initialization failed — disabled", exc_info=True)
    if content_processor.enabled:
        logger.info("Content processing ready")
    else:
        logger.info("Content processing disabled (ADLS or CU not configured)")

    _setup_trace_logging()

    session_manager = SessionManager(content_processor)
    await session_manager.start()
    logger.info("Application started")

    yield

    await session_manager.stop()
    await content_processor.close()
    logger.info("Application shut down")


app = FastAPI(title="RFP Agent", lifespan=lifespan)

# CORS: allow localhost for dev, plus configurable FRONTEND_URL for production
cors_origins = [
    "http://localhost:3000",
]
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    cors_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def trace_requests(request, call_next):
    t0 = time.monotonic()
    response = await call_next(request)
    _trace(
        "http.request",
        method=request.method,
        path=request.url.path,
        query=str(request.url.query),
        status=response.status_code,
        duration_s=round(time.monotonic() - t0, 4),
    )
    return response


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------
class SendMessageRequest(BaseModel):
    prompt: str


# ---------------------------------------------------------------------------
# Session endpoints
# ---------------------------------------------------------------------------
@app.post("/sessions", status_code=201)
async def create_session() -> dict:
    """Create a new isolated agent session."""
    metadata = await session_manager.create_session()
    return metadata


@app.post("/sessions/{session_id}/messages")
async def send_message(session_id: str, req: SendMessageRequest) -> StreamingResponse:
    """Send a user message and stream back SSE events."""
    try:
        await session_manager.validate_session(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found")

    return StreamingResponse(
        session_manager.send_message(session_id, req.prompt),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/sessions/{session_id}")
async def get_session(session_id: str) -> dict:
    """Check if a session is still active (used for session restore on reload)."""
    try:
        await session_manager.validate_session(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "status": "active"}


@app.delete("/sessions/{session_id}", status_code=204)
async def delete_session(session_id: str):
    """Delete a session."""
    try:
        await session_manager.validate_session(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found")
    await session_manager.delete_session(session_id)


@app.get("/sessions/{session_id}/files")
async def list_files(session_id: str) -> dict:
    """List files in a session's workspace."""
    try:
        await session_manager.validate_session(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        return await session_manager.list_files(session_id)
    except Exception as exc:
        if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code < 500:
            raise HTTPException(status_code=exc.response.status_code, detail="Failed to list files")
        raise


@app.get("/sessions/{session_id}/files/content")
async def get_file_content(session_id: str, filename: str) -> dict:
    """Get text content for a workspace file."""
    try:
        await session_manager.validate_session(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        return await session_manager.get_file_content(session_id, filename)
    except Exception as exc:
        if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code < 500:
            detail = exc.response.text
            try:
                detail = exc.response.json().get("detail", detail)
            except Exception:
                pass
            raise HTTPException(status_code=exc.response.status_code, detail=detail)
        raise


@app.post("/sessions/{session_id}/upload")
async def upload_file(session_id: str, file: UploadFile) -> dict:
    """Upload a document to a session's workspace."""
    try:
        await session_manager.validate_session(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        result = await session_manager.upload_file(session_id, file)
    except Exception as exc:
        if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code < 500:
            detail = exc.response.text
            try:
                detail = exc.response.json().get("detail", detail)
            except Exception:
                pass
            raise HTTPException(status_code=exc.response.status_code, detail=detail)
        raise
    return result


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------
@app.get("/health")
async def health() -> dict:
    """Return service health."""
    return {"status": "ok"}
