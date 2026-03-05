"""Session manager that proxies requests to ACA dynamic session containers.

Each user gets an isolated container via the ACA session pool. The orchestrator
never runs the Copilot SDK directly — it streams SSE from the session
container's /chat/stream endpoint and passes events through to the frontend.
"""

import json
import logging
import os
import uuid
from collections.abc import AsyncGenerator
from datetime import datetime, timezone

import httpx
from azure.identity.aio import DefaultAzureCredential
from fastapi import UploadFile

logger = logging.getLogger(__name__)

POOL_MANAGEMENT_ENDPOINT = os.getenv("POOL_MANAGEMENT_ENDPOINT", "")


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

    async def _refresh(self) -> None:
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

    async def close(self) -> None:
        if self._credential:
            await self._credential.close()


class SessionManager:
    """Proxies session lifecycle to ACA dynamic session containers."""

    def __init__(self):
        self._auth = _SessionPoolAuth()
        self._http = httpx.AsyncClient(
            auth=self._auth,
            timeout=httpx.Timeout(connect=10, read=600, write=10, pool=10),
        )
        self._sessions: set[str] = set()
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

    async def start(self) -> None:
        logger.info("SessionManager started (pool=%s)", POOL_MANAGEMENT_ENDPOINT)

    async def stop(self) -> None:
        await self._http.aclose()
        await self._auth.close()
        if self._cogservices_credential:
            await self._cogservices_credential.close()
        logger.info("SessionManager stopped")

    @property
    def active_count(self) -> int:
        return len(self._sessions)

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

        self._sessions.add(session_id)

        logger.info("Created session %s", session_id)
        return {
            "session_id": session_id,
            "status": "active",
            "created_at": now.isoformat(),
            "last_activity_at": now.isoformat(),
        }

    async def validate_session(self, session_id: str) -> None:
        """Ensure session exists. Raises KeyError if not tracked."""
        if session_id not in self._sessions:
            raise KeyError(session_id)

    async def send_message(self, session_id: str, prompt: str) -> AsyncGenerator[str, None]:
        """Stream SSE events from the session container to the frontend."""
        try:
            stream_url = self._pool_url("/chat/stream", session_id)

            cogservices_token = await self._get_cogservices_token()
            chat_body = {"prompt": prompt}
            if cogservices_token:
                chat_body["token"] = cogservices_token

            async with self._http.stream("POST", stream_url, json=chat_body) as resp:
                if resp.status_code == 409:
                    yield _sse_event({"type": "error", "message": "Session is busy"})
                    yield _sse_event({"type": "done"})
                    return

                if resp.status_code >= 400:
                    await resp.aread()
                    try:
                        detail = resp.json().get("detail", resp.text)
                    except Exception:
                        detail = resp.text
                    logger.error(
                        "Session container returned %s for %s: %s",
                        resp.status_code, session_id, detail,
                    )
                    yield _sse_event({"type": "error", "message": f"Session error: {detail}"})
                    yield _sse_event({"type": "done"})
                    return

                async for line in resp.aiter_lines():
                    line = line.strip()
                    if line:
                        yield line + "\n\n"

        except Exception:
            logger.exception("send_message failed for session %s", session_id)
            yield _sse_event({"type": "error", "message": "Internal server error"})
            yield _sse_event({"type": "done"})

    async def upload_file(self, session_id: str, upload_file: UploadFile) -> dict:
        """Proxy a file upload to the session container."""
        url = self._pool_url("/upload", session_id)
        content = await upload_file.read()
        filename = upload_file.filename
        content_type = upload_file.content_type or "application/octet-stream"
        files = {"file": (filename, content, content_type)}
        resp = await self._http.post(url, files=files)
        resp.raise_for_status()
        return resp.json()

    async def list_files(self, session_id: str) -> dict:
        """Proxy GET /files to the session container."""
        url = self._pool_url("/files", session_id)
        resp = await self._http.get(url)
        resp.raise_for_status()
        return resp.json()

    async def get_session(self, session_id: str) -> dict:
        """Return minimal session metadata (no persistence)."""
        if session_id not in self._sessions:
            raise KeyError(session_id)
        return {
            "session_id": session_id,
            "status": "active",
            "messages": [],
        }

    async def delete_session(self, session_id: str) -> None:
        self._sessions.discard(session_id)
        logger.info("Deleted session %s", session_id)
