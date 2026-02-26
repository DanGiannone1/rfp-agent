"""Session manager that proxies requests to ACA dynamic session containers.

Each user gets an isolated container via the ACA session pool. The orchestrator
never runs the Copilot SDK directly — it sends blocking HTTP requests to the
session container and polls for status updates, yielding SSE events to the
frontend.
"""

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime, timezone

import httpx
from azure.identity.aio import DefaultAzureCredential

logger = logging.getLogger(__name__)

POOL_MANAGEMENT_ENDPOINT = os.getenv("POOL_MANAGEMENT_ENDPOINT", "")
STATUS_POLL_INTERVAL = 1.5  # seconds between /status polls


def _sse_event(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"


class _SessionPoolAuth(httpx.Auth):
    """httpx Auth that attaches a Bearer token for the ACA session pool.

    In local dev (POOL_MANAGEMENT_ENDPOINT pointing at a plain container)
    no token is needed — we skip auth when the endpoint is a bare http URL.
    """

    def __init__(self):
        self._credential: DefaultAzureCredential | None = None
        self._token: str | None = None
        self._expires_on: float = 0

    def _needs_token(self) -> bool:
        return POOL_MANAGEMENT_ENDPOINT.startswith("https://")

    async def _refresh(self):
        import time

        if not self._needs_token():
            return
        if self._token and time.time() < self._expires_on - 60:
            return
        if self._credential is None:
            self._credential = DefaultAzureCredential()
        tok = await self._credential.get_token(
            "https://dynamicsessions.io/.default"
        )
        self._token = tok.token
        self._expires_on = tok.expires_on

    async def async_auth_flow(self, request):
        await self._refresh()
        if self._token:
            request.headers["Authorization"] = f"Bearer {self._token}"
        yield request

    async def close(self):
        if self._credential:
            await self._credential.close()


class SessionManager:
    """Proxies session lifecycle to ACA dynamic session containers."""

    def __init__(self, cosmos_store=None):
        self._cosmos = cosmos_store
        self._auth = _SessionPoolAuth()
        self._http = httpx.AsyncClient(
            auth=self._auth,
            timeout=httpx.Timeout(connect=10, read=600, write=10, pool=10),
        )
        self._turn_indices: dict[str, int] = {}
        self._cogservices_credential: DefaultAzureCredential | None = None
        self._cogservices_token: str | None = None
        self._cogservices_expires_on: float = 0

    async def _get_cogservices_token(self) -> str | None:
        """Get a Cognitive Services token to forward to session containers.

        Returns None for local dev (http endpoints) — session containers
        handle their own auth via AZURE_OPENAI_TOKEN env var.
        """
        import time

        if not POOL_MANAGEMENT_ENDPOINT.startswith("https://"):
            return None
        if self._cogservices_token and time.time() < self._cogservices_expires_on - 60:
            return self._cogservices_token
        if self._cogservices_credential is None:
            self._cogservices_credential = DefaultAzureCredential()
        tok = await self._cogservices_credential.get_token(
            "https://cognitiveservices.azure.com/.default"
        )
        self._cogservices_token = tok.token
        self._cogservices_expires_on = tok.expires_on
        return self._cogservices_token

    async def start(self):
        logger.info("SessionManager started (pool=%s)", POOL_MANAGEMENT_ENDPOINT)

    async def stop(self):
        await self._http.aclose()
        await self._auth.close()
        if self._cogservices_credential:
            await self._cogservices_credential.close()
        logger.info("SessionManager stopped")

    @property
    def active_count(self) -> int:
        return len(self._turn_indices)

    def _pool_url(self, path: str, session_id: str) -> str:
        base = POOL_MANAGEMENT_ENDPOINT.rstrip("/")
        return f"{base}{path}?identifier={session_id}"

    async def create_session(self) -> dict:
        session_id = uuid.uuid4().hex[:16]
        now = datetime.now(timezone.utc)

        # Ping health to allocate (warm up) the container
        url = self._pool_url("/health", session_id)
        resp = await self._http.get(url)
        resp.raise_for_status()

        self._turn_indices[session_id] = 0

        metadata = {
            "session_id": session_id,
            "status": "active",
            "created_at": now.isoformat(),
            "last_activity_at": now.isoformat(),
        }

        if self._cosmos:
            await self._cosmos.create_session(metadata)

        logger.info("Created session %s", session_id)
        return metadata

    async def validate_session(self, session_id: str):
        """Ensure session exists and recover turn index from Cosmos if needed.

        Call this eagerly (before constructing StreamingResponse) so that
        KeyError can be caught by the endpoint handler.
        """
        if session_id in self._turn_indices:
            return
        if self._cosmos:
            meta = await self._cosmos.get_session(session_id)
            if meta and meta.get("status") == "active":
                messages = await self._cosmos.get_messages(session_id)
                max_turn = max(
                    (m.get("turn_index", 0) for m in messages), default=0
                )
                self._turn_indices[session_id] = max_turn
                return
        raise KeyError(session_id)

    async def send_message(self, session_id: str, prompt: str):
        """Send a message, poll for status, yield SSE events to the frontend.

        This is an async generator that the FastAPI endpoint wraps in a
        StreamingResponse. SSE only flows orchestrator → frontend; the
        session container is called with plain HTTP request/response.
        """
        self._turn_indices[session_id] = self._turn_indices.get(session_id, 0) + 1
        turn = self._turn_indices[session_id]
        now = datetime.now(timezone.utc)

        # Persist user message
        if self._cosmos:
            await self._cosmos.add_message({
                "session_id": session_id,
                "role": "user",
                "content": prompt,
                "tool_activity": [],
                "timestamp": now.isoformat(),
                "turn_index": turn,
            })

        chat_url = self._pool_url("/chat", session_id)
        status_url = self._pool_url("/status", session_id)

        # Get a Cognitive Services token to forward to the session container
        cogservices_token = await self._get_cogservices_token()
        chat_body = {"prompt": prompt}
        if cogservices_token:
            chat_body["token"] = cogservices_token

        # Fire off the blocking /chat request as a background task
        chat_task = asyncio.create_task(
            self._http.post(chat_url, json=chat_body)
        )

        # Poll /status and yield SSE events until /chat completes
        last_status = None
        while not chat_task.done():
            await asyncio.sleep(STATUS_POLL_INTERVAL)
            try:
                status_resp = await self._http.get(
                    status_url,
                    timeout=httpx.Timeout(connect=5, read=5, write=5, pool=5),
                )
                if status_resp.status_code == 200:
                    current = status_resp.json().get("status", "idle")
                    if current != last_status:
                        last_status = current
                        yield _sse_event({"type": "status", "status": current})
            except httpx.HTTPError:
                pass  # status poll failure is non-fatal

        # Get the result from /chat
        chat_resp = chat_task.result()
        if chat_resp.status_code == 409:
            yield _sse_event({"type": "error", "message": "Session is busy"})
            yield _sse_event({"type": "done"})
            return

        chat_resp.raise_for_status()
        result = chat_resp.json()

        yield _sse_event({
            "type": "message",
            "content": result.get("content", ""),
        })
        yield _sse_event({"type": "done"})

        # Persist assistant message
        if self._cosmos:
            now = datetime.now(timezone.utc)
            await self._cosmos.add_message({
                "session_id": session_id,
                "role": "assistant",
                "content": result.get("content", ""),
                "tool_activity": result.get("tool_activity", []),
                "timestamp": now.isoformat(),
                "turn_index": turn,
            })
            await self._cosmos.update_session_activity(session_id, now)

    async def get_session(self, session_id: str) -> dict:
        """Return session metadata + message history from Cosmos."""
        if self._cosmos:
            metadata = await self._cosmos.get_session(session_id)
            if not metadata:
                raise KeyError(session_id)
            messages = await self._cosmos.get_messages(session_id)
            return {**metadata, "messages": messages}

        # In-memory fallback (no history)
        if session_id not in self._turn_indices:
            raise KeyError(session_id)
        return {
            "session_id": session_id,
            "status": "active",
            "messages": [],
        }

    async def delete_session(self, session_id: str):
        self._turn_indices.pop(session_id, None)

        if self._cosmos:
            metadata = await self._cosmos.get_session(session_id)
            if metadata:
                await self._cosmos.close_session(session_id)
                logger.info("Deleted session %s", session_id)
                return
            raise KeyError(session_id)

        logger.info("Deleted session %s", session_id)
