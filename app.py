import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from agent import run_analysis
from session_manager import SessionManager

logger = logging.getLogger(__name__)

DEFAULT_WORKING_DIR = os.getenv("WORKING_DIR", "./workspace")

# ---------------------------------------------------------------------------
# Globals set during lifespan
# ---------------------------------------------------------------------------
session_manager: SessionManager | None = None
cosmos_store = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global session_manager, cosmos_store

    # Try to initialise CosmosDB (optional — runs fine without it)
    cosmos_endpoint = os.getenv("COSMOS_ENDPOINT")
    if cosmos_endpoint:
        try:
            from cosmos import CosmosStore

            cosmos_store = CosmosStore(cosmos_endpoint)
            await cosmos_store.initialize()
            logger.info("CosmosDB connected (%s)", cosmos_endpoint)
        except Exception:
            logger.warning("CosmosDB unavailable — running without persistence", exc_info=True)
            cosmos_store = None

    session_manager = SessionManager(cosmos_store)
    await session_manager.start()
    logger.info("Application started")

    yield

    await session_manager.stop()
    if cosmos_store:
        await cosmos_store.close()
    logger.info("Application shut down")


app = FastAPI(title="RFP Agent", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://frontend:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------
class AnalyzeRequest(BaseModel):
    prompt: str
    working_dir: str = Field(default=None)


class CreateSessionRequest(BaseModel):
    working_dir: str = Field(default=None)


class SendMessageRequest(BaseModel):
    prompt: str


# ---------------------------------------------------------------------------
# Legacy single-turn endpoint (backward compat)
# ---------------------------------------------------------------------------
@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    working_dir = req.working_dir or DEFAULT_WORKING_DIR
    return StreamingResponse(
        run_analysis(req.prompt, working_dir),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


# ---------------------------------------------------------------------------
# Session endpoints
# ---------------------------------------------------------------------------
@app.post("/sessions", status_code=201)
async def create_session(req: CreateSessionRequest):
    working_dir = req.working_dir or DEFAULT_WORKING_DIR
    metadata = await session_manager.create_session(working_dir)
    return metadata


@app.post("/sessions/{session_id}/messages")
async def send_message(session_id: str, req: SendMessageRequest):
    if not session_manager.has_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        return StreamingResponse(
            session_manager.send_message(session_id, req.prompt),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    try:
        return await session_manager.get_session(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found")


@app.delete("/sessions/{session_id}", status_code=204)
async def delete_session(session_id: str):
    try:
        await session_manager.delete_session(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found")


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "active_sessions": session_manager.active_count if session_manager else 0,
        "cosmos_connected": cosmos_store is not None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
