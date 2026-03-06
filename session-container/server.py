"""Lightweight FastAPI server that runs inside each ACA session container.

One container = one user. The module-level ``_session`` singleton holds the
persistent AgentSession so multi-turn context is preserved across requests.

Endpoints:
    POST /chat/stream — streams SSE events for an agent turn
    POST /upload      — saves a file to /workspace
    GET  /files       — lists files in /workspace with metadata
    POST /reset       — destroys agent + clears workspace (local dev)
    GET  /health      — returns 200
"""

import asyncio
import logging
import os
import uuid

from ag_ui.core.events import RunErrorEvent, RunFinishedEvent
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
        _session = AgentSession(WORKSPACE, token=token)
        await _session.__aenter__()
        logger.info("AgentSession initialised (workspace=%s)", WORKSPACE)
    return _session


async def _destroy_session_locked() -> None:
    """Destroy singleton agent session; caller must hold _lock."""
    global _session
    if _session is None:
        return
    try:
        await _session.__aexit__(None, None, None)
    except Exception:
        logger.warning("Error destroying session", exc_info=True)
    _session = None


# ── Request models ────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    prompt: str
    token: str | None = None


# ── Endpoints ─────────────────────────────────────────────────────────────
@app.post("/chat/stream")
async def chat_stream(req: ChatRequest) -> StreamingResponse:
    """Run a full agent turn, streaming SSE events as they happen."""
    try:
        chat_timeout = int(os.getenv("CHAT_TIMEOUT_SECONDS", "300"))
    except ValueError:
        chat_timeout = 300

    async def generate():
        thread_id = str(uuid.uuid4())
        run_id = str(uuid.uuid4())
        try:
            async with _lock:
                session = await _get_or_create_session(token=req.token)
                async with asyncio.timeout(chat_timeout):
                    async for event in session.send(req.prompt):
                        yield event
        except asyncio.TimeoutError:
            logger.warning("Chat stream timed out after %ds", chat_timeout)
            async with _lock:
                await _destroy_session_locked()
            yield _sse_event(RunErrorEvent(message=f"Agent turn timed out after {chat_timeout}s"))
            yield _sse_event(RunFinishedEvent(thread_id=thread_id, run_id=run_id))
        except Exception:
            logger.exception("Chat stream failed")
            async with _lock:
                await _destroy_session_locked()
            yield _sse_event(RunErrorEvent(message="Agent turn failed. Please retry."))
            yield _sse_event(RunFinishedEvent(thread_id=thread_id, run_id=run_id))

    return StreamingResponse(generate(), media_type="text/event-stream")


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


@app.post("/reset")
async def reset() -> dict:
    """Reset the session: destroy the agent and clean the workspace.

    In production each session gets a fresh container, so this is a no-op.
    In local dev, the single shared container uses this to simulate isolation.
    """
    global _session
    import shutil
    from pathlib import Path

    # Acquire the lock so we don't destroy an agent mid-turn or race with cleanup
    async with _lock:
        if _session is not None:
            await _destroy_session_locked()
            logger.info("Agent session destroyed")

        # Clean workspace while still holding the lock
        ws = Path(WORKSPACE)
        if ws.exists():
            shutil.rmtree(ws)
        ws.mkdir(parents=True, exist_ok=True)
        logger.info("Workspace cleaned: %s", WORKSPACE)

    return {"status": "reset"}


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
