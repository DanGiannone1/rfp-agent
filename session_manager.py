import asyncio
import json
import logging
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from agent import AgentSession

logger = logging.getLogger(__name__)

SESSION_TTL_MINUTES = int(os.getenv("SESSION_TTL_MINUTES", "30"))
CLEANUP_INTERVAL_SECONDS = 60


@dataclass
class ManagedSession:
    session_id: str
    agent: AgentSession
    working_dir: str
    created_at: datetime
    last_activity_at: datetime
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    turn_index: int = 0
    status: str = "active"


class SessionManager:
    """Manages the lifecycle of multiple concurrent AgentSessions."""

    def __init__(self, cosmos_store=None):
        self._sessions: dict[str, ManagedSession] = {}
        self._cosmos = cosmos_store
        self._cleanup_task: asyncio.Task | None = None

    async def start(self):
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
        logger.info("SessionManager started (TTL=%dm)", SESSION_TTL_MINUTES)

    async def stop(self):
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

        for sid in list(self._sessions):
            await self._destroy_session(sid)
        logger.info("SessionManager stopped, all sessions destroyed")

    @property
    def active_count(self) -> int:
        return len(self._sessions)

    async def create_session(self, working_dir: str) -> dict:
        session_id = uuid.uuid4().hex[:16]
        now = datetime.now(timezone.utc)

        agent = AgentSession(working_dir)
        await agent.__aenter__()

        managed = ManagedSession(
            session_id=session_id,
            agent=agent,
            working_dir=working_dir,
            created_at=now,
            last_activity_at=now,
        )
        self._sessions[session_id] = managed

        metadata = {
            "session_id": session_id,
            "working_dir": working_dir,
            "status": "active",
            "created_at": now.isoformat(),
            "last_activity_at": now.isoformat(),
        }

        if self._cosmos:
            await self._cosmos.create_session(metadata)

        logger.info("Created session %s (dir=%s)", session_id, working_dir)
        return metadata

    async def send_message(self, session_id: str, prompt: str):
        managed = self._sessions.get(session_id)
        if not managed:
            raise KeyError(session_id)

        if managed.lock.locked():
            raise RuntimeError("Session is busy (concurrent turn)")

        async with managed.lock:
            managed.last_activity_at = datetime.now(timezone.utc)
            managed.turn_index += 1
            turn = managed.turn_index

            # Persist user message
            if self._cosmos:
                await self._cosmos.add_message({
                    "session_id": session_id,
                    "role": "user",
                    "content": prompt,
                    "tool_activity": [],
                    "timestamp": managed.last_activity_at.isoformat(),
                    "turn_index": turn,
                })

            # Collect assistant content for persistence
            full_content = ""
            tool_activity = []

            async for sse_line in managed.agent.send(prompt):
                # Parse the SSE line to track content
                text = sse_line.strip()
                if text.startswith("data: "):
                    try:
                        event = json.loads(text[6:])
                        if event.get("type") == "delta":
                            full_content += event.get("content", "")
                        elif event.get("type") == "tool_start":
                            tool_activity.append({
                                "tool": event.get("tool", "unknown"),
                                "status": "running",
                            })
                        elif event.get("type") == "tool_end":
                            for ta in tool_activity:
                                if ta["tool"] == event.get("tool") and ta["status"] == "running":
                                    ta["status"] = "done"
                                    break
                    except json.JSONDecodeError:
                        pass

                yield sse_line

            # Persist assistant message
            if self._cosmos:
                managed.last_activity_at = datetime.now(timezone.utc)
                await self._cosmos.add_message({
                    "session_id": session_id,
                    "role": "assistant",
                    "content": full_content,
                    "tool_activity": tool_activity,
                    "timestamp": managed.last_activity_at.isoformat(),
                    "turn_index": turn,
                })
                await self._cosmos.update_session_activity(
                    session_id, managed.last_activity_at
                )

    async def get_session(self, session_id: str) -> dict:
        """Return session metadata + message history from Cosmos (or in-memory fallback)."""
        if self._cosmos:
            metadata = await self._cosmos.get_session(session_id)
            if not metadata:
                raise KeyError(session_id)
            messages = await self._cosmos.get_messages(session_id)
            return {**metadata, "messages": messages}

        # In-memory fallback (no history persistence)
        managed = self._sessions.get(session_id)
        if not managed:
            raise KeyError(session_id)
        return {
            "session_id": session_id,
            "working_dir": managed.working_dir,
            "status": managed.status,
            "created_at": managed.created_at.isoformat(),
            "last_activity_at": managed.last_activity_at.isoformat(),
            "messages": [],
        }

    async def delete_session(self, session_id: str):
        if session_id not in self._sessions:
            # Check Cosmos for closed sessions
            if self._cosmos:
                metadata = await self._cosmos.get_session(session_id)
                if metadata:
                    await self._cosmos.close_session(session_id)
                    return
            raise KeyError(session_id)

        await self._destroy_session(session_id)

        if self._cosmos:
            await self._cosmos.close_session(session_id)

        logger.info("Deleted session %s", session_id)

    def has_session(self, session_id: str) -> bool:
        return session_id in self._sessions

    async def _destroy_session(self, session_id: str):
        managed = self._sessions.pop(session_id, None)
        if managed:
            try:
                await managed.agent.__aexit__(None, None, None)
            except Exception:
                logger.exception("Error destroying session %s", session_id)

    async def _cleanup_loop(self):
        while True:
            await asyncio.sleep(CLEANUP_INTERVAL_SECONDS)
            now = datetime.now(timezone.utc)
            expired = [
                sid
                for sid, s in self._sessions.items()
                if (now - s.last_activity_at).total_seconds()
                > SESSION_TTL_MINUTES * 60
            ]
            for sid in expired:
                logger.info("Cleaning up expired session %s", sid)
                await self._destroy_session(sid)
                if self._cosmos:
                    await self._cosmos.close_session(sid)
