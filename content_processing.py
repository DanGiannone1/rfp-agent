"""Optional document processing: ADLS storage + Content Understanding markdown conversion.

Follows the cosmos.py pattern — initialize()/close() lifecycle, DefaultAzureCredential,
entirely optional (disabled when env vars are unset).
"""

import logging
import os
from collections.abc import Awaitable, Callable

from azure.identity.aio import DefaultAzureCredential

logger = logging.getLogger(__name__)


class ContentProcessor:
    """Uploads originals to ADLS and converts documents to markdown via Content Understanding."""

    def __init__(self):
        self._adls_account = os.getenv("ADLS_ACCOUNT_NAME", "")
        self._adls_filesystem = os.getenv("ADLS_FILESYSTEM", "documents")
        # Content Understanding runs on the same Foundry/Cognitive Services resource
        # as Azure OpenAI. Derive the base endpoint from AZURE_ENDPOINT by stripping
        # any path suffix (e.g. /openai/v1/).
        self._cu_endpoint = self._derive_cu_endpoint()

        self._credential: DefaultAzureCredential | None = None
        self._adls_client = None  # DataLakeServiceClient
        self._filesystem_client = None  # FileSystemClient
        self._cu_client = None  # ContentUnderstandingClient

    @staticmethod
    def _derive_cu_endpoint() -> str:
        """Derive the Content Understanding endpoint from AZURE_ENDPOINT.

        AZURE_ENDPOINT is typically something like
        ``https://myresource.cognitiveservices.azure.com/openai/v1/``
        or ``https://myresource.services.ai.azure.com/openai/v1/``.
        Content Understanding just needs the origin (scheme + host).
        """
        from urllib.parse import urlparse

        raw = os.getenv("AZURE_ENDPOINT", "")
        if not raw:
            return ""
        parsed = urlparse(raw)
        if parsed.scheme and parsed.hostname:
            return f"{parsed.scheme}://{parsed.hostname}/"
        return ""

    @property
    def enabled(self) -> bool:
        return bool(self._adls_account or self._cu_endpoint)

    async def initialize(self) -> None:
        self._credential = DefaultAzureCredential()

        if self._adls_account:
            try:
                from azure.storage.filedatalake.aio import DataLakeServiceClient

                account_url = f"https://{self._adls_account}.dfs.core.windows.net"
                self._adls_client = DataLakeServiceClient(
                    account_url=account_url, credential=self._credential
                )
                self._filesystem_client = self._adls_client.get_file_system_client(
                    self._adls_filesystem
                )
                logger.info("ADLS connected (%s/%s)", self._adls_account, self._adls_filesystem)
            except Exception:
                logger.warning("ADLS unavailable — uploads won't be stored", exc_info=True)
                self._adls_client = None
                self._filesystem_client = None

        if self._cu_endpoint:
            try:
                from azure.ai.contentunderstanding.aio import ContentUnderstandingClient

                self._cu_client = ContentUnderstandingClient(
                    endpoint=self._cu_endpoint, credential=self._credential
                )
                logger.info("Content Understanding connected (%s)", self._cu_endpoint)
            except Exception:
                logger.warning("Content Understanding unavailable — no markdown conversion", exc_info=True)
                self._cu_client = None

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
    ) -> None:
        """Background entry point — never raises, logs all errors as warnings."""
        try:
            # 1. Upload original to ADLS
            await self._upload_to_adls(
                f"originals/{session_id}/{filename}", file_bytes, content_type
            )

            # 2. Convert to markdown via Content Understanding
            markdown = await self._analyze_document(file_bytes)

            if markdown:
                md_filename = f"{filename}.md"
                md_bytes = markdown.encode("utf-8")

                # 3. Upload markdown to ADLS
                await self._upload_to_adls(
                    f"markdown/{session_id}/{md_filename}", md_bytes, "text/markdown"
                )

                # 4. Forward markdown to session container
                try:
                    await forward_markdown_fn(md_filename, md_bytes)
                except Exception:
                    logger.warning(
                        "Failed to forward markdown for %s/%s", session_id, filename, exc_info=True
                    )
        except Exception:
            logger.warning(
                "Document processing failed for %s/%s", session_id, filename, exc_info=True
            )

    async def _upload_to_adls(self, path: str, data: bytes, content_type: str) -> None:
        if not self._filesystem_client:
            return
        try:
            from azure.storage.filedatalake import ContentSettings

            file_client = self._filesystem_client.get_file_client(path)
            await file_client.upload_data(
                data, overwrite=True, content_settings=ContentSettings(content_type=content_type)
            )
            logger.info("Uploaded to ADLS: %s", path)
        except Exception:
            logger.warning("ADLS upload failed for %s", path, exc_info=True)

    async def _analyze_document(self, file_bytes: bytes) -> str | None:
        if not self._cu_client:
            return None
        try:
            poller = await self._cu_client.begin_analyze_binary(
                analyzer_id="prebuilt-layout",
                binary_input=file_bytes,
            )
            result = await poller.result()
            if result.contents:
                return result.contents[0].markdown
            return None
        except Exception:
            logger.warning("Content Understanding analysis failed", exc_info=True)
            return None
