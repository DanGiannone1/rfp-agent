"""Lightweight FastAPI server that runs inside each ACA session container.

One container = one user. The module-level ``_session`` singleton holds the
persistent AgentSession so multi-turn context is preserved across requests.

Endpoints:
    POST /chat   — blocks until the agent turn completes, returns JSON result
    GET  /status — returns current agent activity (pollable by orchestrator)
    POST /upload — saves a file to /workspace
    GET  /files  — lists files in /workspace with metadata
    GET  /health — returns 200
"""

import asyncio
import logging
import os

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agent import AgentSession, _sse_event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WORKSPACE = os.getenv("WORKSPACE", "/workspace")

app = FastAPI(title="RFP Session")

# ── Module-level singleton ────────────────────────────────────────────────
_session: AgentSession | None = None
_lock = asyncio.Lock()


async def _get_or_create_session(token: str | None = None) -> AgentSession:
    """Lazy-init the AgentSession singleton on first request."""
    global _session
    if _session is None:
        _session = AgentSession(WORKSPACE)
        await _session.__aenter__(token=token)
        logger.info("AgentSession initialised (workspace=%s)", WORKSPACE)
    return _session


# ── Request models ────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    prompt: str
    token: str | None = None


# ── Endpoints ─────────────────────────────────────────────────────────────
@app.post("/chat")
async def chat(req: ChatRequest) -> dict:
    """Run a full agent turn. Blocks until complete, returns JSON result."""
    logger.info("POST /chat received (prompt=%r, has_token=%s)", req.prompt[:50], bool(req.token))
    if _lock.locked():
        raise HTTPException(status_code=409, detail="Session is busy (concurrent turn)")

    try:
        chat_timeout = int(os.getenv("CHAT_TIMEOUT_SECONDS", "300"))
    except ValueError:
        chat_timeout = 300

    try:
        async with _lock:
            logger.info("Acquiring session...")
            session = await _get_or_create_session(token=req.token)
            logger.info("Session acquired, sending prompt...")
            result = await asyncio.wait_for(
                session.send_and_collect(req.prompt),
                timeout=chat_timeout,
            )
            logger.info("Got result (content length=%d)", len(result.get("content", "")))
            return result
    except asyncio.TimeoutError:
        logger.warning("Chat turn timed out after %ds", chat_timeout)
        # Reset session status so /status doesn't report stale activity
        if _session is not None:
            _session._status = "idle"
            # Drain the queue to discard stale events from the cancelled turn
            while not _session._queue.empty():
                _session._queue.get_nowait()
        raise HTTPException(
            status_code=504,
            detail=f"Agent turn timed out after {chat_timeout}s",
        )
    except Exception as exc:
        logger.exception("Chat failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest) -> StreamingResponse:
    """Run a full agent turn, streaming SSE events as they happen."""
    if _lock.locked():
        raise HTTPException(status_code=409, detail="Session is busy (concurrent turn)")

    try:
        chat_timeout = int(os.getenv("CHAT_TIMEOUT_SECONDS", "300"))
    except ValueError:
        chat_timeout = 300

    async def generate():
        try:
            async with _lock:
                session = await _get_or_create_session(token=req.token)
                async for event in asyncio.wait_for(
                    _consume_stream(session, req.prompt),
                    timeout=chat_timeout,
                ):
                    yield event
        except asyncio.TimeoutError:
            logger.warning("Chat stream timed out after %ds", chat_timeout)
            if _session is not None:
                _session._status = "idle"
                while not _session._queue.empty():
                    _session._queue.get_nowait()
            yield _sse_event({"type": "error", "message": f"Agent turn timed out after {chat_timeout}s"})
            yield _sse_event({"type": "done"})
        except Exception as exc:
            logger.exception("Chat stream failed: %s", exc)
            yield _sse_event({"type": "error", "message": str(exc)})
            yield _sse_event({"type": "done"})

    return StreamingResponse(generate(), media_type="text/event-stream")


async def _consume_stream(session: AgentSession, prompt: str):
    """Helper to wrap the async generator so wait_for can timeout it."""
    async for event in session.send(prompt):
        yield event


@app.get("/status")
async def get_status() -> dict:
    """Return the agent's current activity. Designed to be polled."""
    if _session is None:
        return {"status": "idle"}
    return {"status": _session.status}


UPLOAD_MAX_BYTES = 50 * 1024 * 1024  # 50 MB
ALLOWED_EXTENSIONS = {
    ".pdf", ".doc", ".docx", ".txt", ".csv", ".json", ".xml",
    ".md", ".xlsx", ".pptx", ".xls", ".rtf", ".html", ".htm",
}


@app.post("/upload")
async def upload(file: UploadFile) -> dict:
    """Save an uploaded file to the workspace directory."""
    from pathlib import PurePosixPath

    # Sanitize filename — strip path components
    raw_name = file.filename or "upload"
    safe_name = PurePosixPath(raw_name).name
    if not safe_name:
        raise HTTPException(status_code=400, detail="Invalid filename")

    # Extension allowlist
    ext = os.path.splitext(safe_name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{ext}' not allowed",
        )

    os.makedirs(WORKSPACE, exist_ok=True)
    dest = os.path.join(WORKSPACE, safe_name)

    # Verify resolved path is under WORKSPACE (prevent traversal)
    real_dest = os.path.realpath(dest)
    real_workspace = os.path.realpath(WORKSPACE)
    if not real_dest.startswith(real_workspace + os.sep) and real_dest != real_workspace:
        raise HTTPException(status_code=400, detail="Invalid file path")

    # Stream file with size limit
    bytes_written = 0
    with open(real_dest, "wb") as f:
        while chunk := await file.read(8192):
            bytes_written += len(chunk)
            if bytes_written > UPLOAD_MAX_BYTES:
                f.close()
                os.remove(real_dest)
                raise HTTPException(status_code=413, detail="File too large (50 MB limit)")
            f.write(chunk)

    logger.info("Uploaded %s (%d bytes)", safe_name, bytes_written)
    return {"path": real_dest, "filename": safe_name, "size": bytes_written}


@app.get("/files")
async def list_files() -> dict:
    """List all files in the workspace with metadata."""
    from datetime import datetime, timezone
    from pathlib import Path

    workspace = Path(WORKSPACE)
    if not workspace.exists():
        return {"files": []}

    files = []
    for entry in sorted(workspace.iterdir()):
        if not entry.is_file():
            continue
        stat = entry.stat()
        md_sibling = workspace / f"{entry.name}.md"
        files.append({
            "filename": entry.name,
            "size": stat.st_size,
            "modified_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
            "has_markdown": md_sibling.exists(),
        })

    return {"files": files}


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
