"""FastAPI orchestrator — session CRUD, message streaming, and file upload.

Proxies all AI interactions to isolated session containers via SessionManager.
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from session_manager import SessionManager

logger = logging.getLogger(__name__)

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
        import httpx
        if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code < 500:
            raise HTTPException(status_code=exc.response.status_code, detail="Failed to list files")
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
        import httpx
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
