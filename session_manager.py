"""Session manager that proxies requests to ACA dynamic session containers.

Each user gets an isolated container via the ACA session pool. The orchestrator
never runs the Copilot SDK directly — it streams SSE from the session
container's /chat/stream endpoint and passes events through to the frontend.
"""

import json
import logging
import os
import re
import uuid
from collections.abc import AsyncGenerator

import httpx
from azure.identity.aio import DefaultAzureCredential
from fastapi import UploadFile

logger = logging.getLogger(__name__)
_trace_logger = logging.getLogger("trace")


def _trace(event: str, **data) -> None:
    if not _trace_logger.handlers:
        return
    import json as _json
    from datetime import datetime, timezone
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "component": "orchestrator",
        "event": event,
        "data": data,
    }
    _trace_logger.info(_json.dumps(record, default=str))

POOL_MANAGEMENT_ENDPOINT = os.getenv("POOL_MANAGEMENT_ENDPOINT", "")

# Session IDs are created as uuid4().hex[:16] — exactly 16 lowercase hex chars
_SESSION_ID_RE = re.compile(r"^[0-9a-f]{16}$")


def _sse_event(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"


def _agui_error(message: str) -> str:
    return _sse_event({"type": "RUN_ERROR", "message": message})


def _agui_finished() -> str:
    return _sse_event(
        {
            "type": "RUN_FINISHED",
            "thread_id": str(uuid.uuid4()),
            "run_id": str(uuid.uuid4()),
        }
    )


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

    def __init__(self, content_processor=None):
        self._content_processor = content_processor
        self._auth = _SessionPoolAuth()
        self._http = httpx.AsyncClient(
            auth=self._auth,
            timeout=httpx.Timeout(connect=10, read=600, write=10, pool=10),
        )
        self._sessions: set[str] = set()
        # Tracks session IDs explicitly deleted via API so validate_session
        # doesn't rehydrate them from a generic health probe in local dev.
        self._deleted_sessions: set[str] = set()
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

        # In local dev (http), reset the shared container so sessions don't
        # see stale workspace files or agent context from previous sessions.
        # In production (https / ACA), each session gets a fresh container.
        if not POOL_MANAGEMENT_ENDPOINT.startswith("https://"):
            try:
                reset_url = self._pool_url("/reset", session_id)
                resp = await self._http.post(reset_url)
                resp.raise_for_status()
            except Exception:
                logger.debug("Reset not available, skipping", exc_info=True)

        # Ping health to allocate (warm up) the container.
        # Use a shorter timeout (30s) so the frontend gets a quick error
        # instead of hanging when the session pool is exhausted.
        url = self._pool_url("/health", session_id)
        resp = await self._http.get(url, timeout=httpx.Timeout(connect=10, read=30, write=10, pool=10))
        resp.raise_for_status()

        self._sessions.add(session_id)
        self._deleted_sessions.discard(session_id)

        logger.info("Created session %s", session_id)
        return {
            "session_id": session_id,
            "status": "active",
        }

    async def validate_session(self, session_id: str) -> None:
        """Ensure session exists, probing pool state for orchestrator restarts."""
        if session_id in self._deleted_sessions:
            raise KeyError(session_id)

        if session_id in self._sessions:
            return

        # Reject malformed IDs before probing — in local dev the health endpoint
        # always returns 200 regardless of identifier, so any ID would pass.
        if not _SESSION_ID_RE.match(session_id):
            raise KeyError(session_id)

        url = self._pool_url("/health", session_id)
        try:
            resp = await self._http.get(url)
            resp.raise_for_status()
        except Exception as exc:
            raise KeyError(session_id) from exc
        self._sessions.add(session_id)

    async def delete_session(self, session_id: str) -> None:
        """Delete session and best-effort reset container context."""
        reset_url = self._pool_url("/reset", session_id)
        try:
            resp = await self._http.post(reset_url)
            resp.raise_for_status()
        except Exception:
            logger.warning("Session reset failed for %s during delete", session_id, exc_info=True)
            return
        self._sessions.discard(session_id)
        self._deleted_sessions.add(session_id)

    async def send_message(self, session_id: str, prompt: str) -> AsyncGenerator[str, None]:
        """Stream SSE events from the session container to the frontend."""
        try:
            stream_url = self._pool_url("/chat/stream", session_id)

            cogservices_token = await self._get_cogservices_token()
            chat_body = {"prompt": prompt}
            headers = {}
            if cogservices_token:
                headers["X-Cogservices-Token"] = cogservices_token

            async with self._http.stream("POST", stream_url, json=chat_body, headers=headers) as resp:
                if resp.status_code == 409:
                    yield _agui_error("Session is busy. Wait for the current response to finish and retry.")
                    yield _agui_finished()
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
                    yield _agui_error(f"Session error: {detail}")
                    yield _agui_finished()
                    return

                async for line in resp.aiter_lines():
                    line = line.strip()
                    if line:
                        yield line + "\n\n"

        except Exception:
            logger.exception("send_message failed for session %s", session_id)
            yield _agui_error("Internal server error")
            yield _agui_finished()

    async def upload_file(self, session_id: str, upload_file: UploadFile) -> dict:
        """Proxy a file upload to the session container, then run CU processing."""
        url = self._pool_url("/upload", session_id)
        max_bytes = 50 * 1024 * 1024  # 50 MB — match session container limit
        content = await upload_file.read(max_bytes + 1)
        if len(content) > max_bytes:
            from fastapi import HTTPException
            raise HTTPException(status_code=413, detail="File too large (50 MB limit)")
        filename = upload_file.filename or "upload"
        content_type = upload_file.content_type or "application/octet-stream"
        if not (self._content_processor and self._content_processor.enabled):
            from fastapi import HTTPException
            raise HTTPException(
                status_code=503,
                detail="Document processing is not available. Azure Content Understanding and ADLS must be configured.",
            )
        files = {"file": (filename, content, content_type)}
        resp = await self._http.post(url, files=files)
        resp.raise_for_status()
        result = resp.json()
        _trace("fs.upload", session_id=session_id, filename=filename,
               size=len(content), status=resp.status_code)

        async def forward_markdown(md_filename: str, md_bytes: bytes) -> None:
            """Upload the converted markdown to the session container."""
            md_url = self._pool_url("/upload", session_id)
            md_files = {"file": (md_filename, md_bytes, "text/markdown")}
            md_resp = await self._http.post(md_url, files=md_files)
            md_resp.raise_for_status()

        proc = await self._content_processor.process_document(
            session_id=session_id,
            filename=filename,
            file_bytes=content,
            content_type=content_type,
            forward_markdown_fn=forward_markdown,
        )
        if not proc["markdown_forwarded"]:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=500,
                detail=proc.get("error") or "Document conversion failed. Please try again.",
            )

        result["markdown_ready"] = True
        return result

    async def list_files(self, session_id: str) -> dict:
        """Proxy GET /files to the session container."""
        url = self._pool_url("/files", session_id)
        resp = await self._http.get(url)
        resp.raise_for_status()
        result = resp.json()
        files = result.get("files", [])
        _trace("fs.list", session_id=session_id, file_count=len(files),
               filenames=[f["filename"] for f in files])
        return result

    async def get_file_content(self, session_id: str, filename: str) -> dict:
        """Proxy GET /files/content to the session container."""
        from urllib.parse import quote
        _trace("fs.content_request", session_id=session_id, filename=filename)
        url = self._pool_url("/files/content", session_id)
        # Append filename directly to preserve the identifier param already in the URL.
        # httpx params= replaces the entire query string, which would drop identifier.
        try:
            resp = await self._http.get(f"{url}&filename={quote(filename, safe='')}")
            resp.raise_for_status()
        except Exception as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            _trace("fs.content_error", session_id=session_id, filename=filename,
                   status=status, error=str(exc))
            raise
        result = resp.json()
        _trace("fs.content_response", session_id=session_id, filename=filename,
               size=result.get("size"), mime_type=result.get("mime_type"))
        return result
