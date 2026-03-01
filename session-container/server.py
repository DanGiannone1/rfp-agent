"""Lightweight FastAPI server that runs inside each ACA session container.

One container = one user. The module-level ``_session`` singleton holds the
persistent AgentSession so multi-turn context is preserved across requests.

Endpoints:
    POST /chat   — blocks until the agent turn completes, returns JSON result
    GET  /status — returns current agent activity (pollable by orchestrator)
    POST /upload — saves a file to /workspace
    GET  /health — returns 200
"""

import asyncio
import logging
import os
import shutil

from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel

from agent import AgentSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WORKSPACE = os.getenv("WORKSPACE", "/workspace")

app = FastAPI(title="RFP Session")

# ── Module-level singleton ────────────────────────────────────────────────
_session: AgentSession | None = None
_lock = asyncio.Lock()


async def _get_session(token: str | None = None) -> AgentSession:
    """Lazy-init the AgentSession on first request."""
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
async def chat(req: ChatRequest):
    """Run a full agent turn. Blocks until complete, returns JSON result."""
    if _lock.locked():
        raise HTTPException(status_code=409, detail="Session is busy (concurrent turn)")

    try:
        async with _lock:
            session = await _get_session(token=req.token)
            result = await session.send_and_collect(req.prompt)
            return result
    except Exception as exc:
        logger.exception("Chat failed")
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/status")
async def get_status():
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
async def upload(file: UploadFile):
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


@app.get("/health")
async def health():
    return {"status": "ok"}
