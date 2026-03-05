"""Document processing: ADLS storage + Content Understanding markdown conversion.

Both ADLS_ACCOUNT_NAME and AZURE_ENDPOINT must be set for processing to be enabled.
When either is missing the processor reports ``enabled = False`` and callers should skip it.
"""

import logging
import os
from collections.abc import Awaitable, Callable
from urllib.parse import urlparse

from azure.identity.aio import DefaultAzureCredential

logger = logging.getLogger(__name__)


class ContentProcessor:
    """Uploads originals to ADLS and converts documents to markdown via Content Understanding."""

    def __init__(self):
        self._adls_account = os.getenv("ADLS_ACCOUNT_NAME")
        self._adls_filesystem = os.getenv("ADLS_FILESYSTEM", "documents")
        self._cu_endpoint = self._derive_cu_endpoint()

        self._credential: DefaultAzureCredential | None = None
        self._adls_client = None  # DataLakeServiceClient
        self._filesystem_client = None  # FileSystemClient
        self._cu_client = None  # ContentUnderstandingClient

    @property
    def enabled(self) -> bool:
        return bool(self._adls_account and self._cu_endpoint)

    @staticmethod
    def _derive_cu_endpoint() -> str | None:
        """Derive the Content Understanding endpoint from AZURE_ENDPOINT.

        AZURE_ENDPOINT is typically something like
        ``https://myresource.cognitiveservices.azure.com/openai/v1/``
        or ``https://myresource.services.ai.azure.com/openai/v1/``.
        Content Understanding just needs the origin (scheme + host).

        Returns ``None`` if AZURE_ENDPOINT is not set or cannot be parsed.
        """
        raw = os.getenv("AZURE_ENDPOINT")
        if not raw:
            return None
        parsed = urlparse(raw)
        if parsed.scheme and parsed.hostname:
            return f"{parsed.scheme}://{parsed.hostname}/"
        logger.warning("Cannot derive Content Understanding endpoint from AZURE_ENDPOINT=%r", raw)
        return None

    async def initialize(self) -> None:
        if not self.enabled:
            logger.info("Content processing disabled (ADLS or CU endpoint not configured)")
            return

        self._credential = DefaultAzureCredential()

        from azure.storage.filedatalake.aio import DataLakeServiceClient

        account_url = f"https://{self._adls_account}.dfs.core.windows.net"
        self._adls_client = DataLakeServiceClient(
            account_url=account_url, credential=self._credential
        )
        self._filesystem_client = self._adls_client.get_file_system_client(
            self._adls_filesystem
        )
        logger.info("ADLS connected (%s/%s)", self._adls_account, self._adls_filesystem)

        from azure.ai.contentunderstanding.aio import ContentUnderstandingClient

        self._cu_client = ContentUnderstandingClient(
            endpoint=self._cu_endpoint, credential=self._credential
        )
        logger.info("Content Understanding connected (%s)", self._cu_endpoint)

    async def close(self) -> None:
        if self._cu_client:
            await self._cu_client.close()
        if self._adls_client:
            await self._adls_client.close()
        if self._credential:
            await self._credential.close()

    async def process_document(
        self,
        session_id: str,
        filename: str,
        file_bytes: bytes,
        content_type: str,
        forward_markdown_fn: Callable[[str, bytes], Awaitable[None]],
    ) -> dict:
        """Process an uploaded document — never raises, returns a result dict."""
        result = {
            "adls_original": False,
            "markdown_produced": False,
            "adls_markdown": False,
            "markdown_forwarded": False,
            "error": None,
        }

        if not self.enabled:
            result["error"] = "Content processing is not enabled"
            return result

        # 1. Upload original to ADLS
        result["adls_original"] = await self._upload_to_adls(
            f"originals/{session_id}/{filename}", file_bytes, content_type
        )

        # 2. Convert to markdown via Content Understanding
        try:
            markdown = await self._analyze_document(file_bytes)
        except Exception:
            logger.warning("Content Understanding failed for %s", filename, exc_info=True)
            markdown = None

        if markdown is None:
            result["error"] = "Content Understanding failed to produce markdown"
            return result

        result["markdown_produced"] = True
        md_filename = f"{filename}.md"
        md_bytes = markdown.encode("utf-8")

        # 3. Upload markdown to ADLS
        result["adls_markdown"] = await self._upload_to_adls(
            f"markdown/{session_id}/{md_filename}", md_bytes, "text/markdown"
        )

        # 4. Forward markdown to session container
        try:
            await forward_markdown_fn(md_filename, md_bytes)
            result["markdown_forwarded"] = True
        except Exception:
            logger.warning("Failed to forward markdown for %s", filename, exc_info=True)

        return result

    async def _upload_to_adls(self, path: str, data: bytes, content_type: str) -> bool:
        """Upload data to ADLS. Returns True on success, False on failure."""
        try:
            from azure.storage.filedatalake import ContentSettings

            file_client = self._filesystem_client.get_file_client(path)
            await file_client.upload_data(
                data, overwrite=True, content_settings=ContentSettings(content_type=content_type)
            )
            logger.info("Uploaded to ADLS: %s", path)
            return True
        except Exception:
            logger.warning("ADLS upload failed for %s", path, exc_info=True)
            return False

    async def _analyze_document(self, file_bytes: bytes) -> str | None:
        """Convert document bytes to markdown via Content Understanding.

        Returns the markdown string, or None if no content was produced.
        Raises on transport / API errors (caller is expected to catch).
        """
        poller = await self._cu_client.begin_analyze_binary(
            analyzer_id="prebuilt-layout",
            binary_input=file_bytes,
        )
        result = await poller.result()
        if result.contents:
            return result.contents[0].markdown
        return None
