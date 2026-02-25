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


async def _get_session() -> AgentSession:
    """Lazy-init the AgentSession on first request."""
    global _session
    if _session is None:
        _session = AgentSession(WORKSPACE)
        await _session.__aenter__()
        logger.info("AgentSession initialised (workspace=%s)", WORKSPACE)
    return _session


# ── Request models ────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    prompt: str


# ── Endpoints ─────────────────────────────────────────────────────────────
@app.post("/chat")
async def chat(req: ChatRequest):
    """Run a full agent turn. Blocks until complete, returns JSON result."""
    if _lock.locked():
        raise HTTPException(status_code=409, detail="Session is busy (concurrent turn)")

    async with _lock:
        session = await _get_session()
        result = await session.send_and_collect(req.prompt)
        return result


@app.get("/status")
async def get_status():
    """Return the agent's current activity. Designed to be polled."""
    if _session is None:
        return {"status": "idle"}
    return {"status": _session.status}


@app.post("/upload")
async def upload(file: UploadFile):
    """Save an uploaded file to the workspace directory."""
    os.makedirs(WORKSPACE, exist_ok=True)
    dest = os.path.join(WORKSPACE, file.filename)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"path": dest}


@app.get("/health")
async def health():
    return {"status": "ok"}
