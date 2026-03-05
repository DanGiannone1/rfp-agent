"""Stdio MCP server exposing a convert_document tool.

Converts uploaded documents (PDF, images, Office) to structured markdown
using Azure Content Understanding's prebuilt-layout analyzer. Optionally
uploads the original and markdown to ADLS Gen2.
"""

import json
import logging
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

mcp = FastMCP("document_converter")


def _derive_cu_endpoint() -> str | None:
    """Derive Content Understanding endpoint from AZURE_ENDPOINT.

    AZURE_ENDPOINT is typically something like
    ``https://myresource.cognitiveservices.azure.com/openai/v1/``
    or ``https://myresource.services.ai.azure.com/openai/v1/``.
    Content Understanding just needs the origin (scheme + host).
    """
    raw = os.getenv("AZURE_ENDPOINT")
    if not raw:
        return None
    parsed = urlparse(raw)
    if parsed.scheme and parsed.hostname:
        return f"{parsed.scheme}://{parsed.hostname}/"
    return None


async def _upload_to_adls(path: str, data: bytes, content_type: str) -> bool:
    """Upload data to ADLS Gen2. Returns True on success."""
    account = os.getenv("ADLS_ACCOUNT_NAME")
    filesystem = os.getenv("ADLS_FILESYSTEM", "documents")
    if not account:
        return False

    try:
        from azure.identity.aio import DefaultAzureCredential
        from azure.storage.filedatalake import ContentSettings
        from azure.storage.filedatalake.aio import DataLakeServiceClient

        credential = DefaultAzureCredential()
        try:
            account_url = f"https://{account}.dfs.core.windows.net"
            client = DataLakeServiceClient(
                account_url=account_url, credential=credential
            )
            try:
                fs_client = client.get_file_system_client(filesystem)
                file_client = fs_client.get_file_client(path)
                await file_client.upload_data(
                    data,
                    overwrite=True,
                    content_settings=ContentSettings(content_type=content_type),
                )
                logger.info("Uploaded to ADLS: %s", path)
                return True
            finally:
                await client.close()
        finally:
            await credential.close()
    except Exception:
        logger.warning("ADLS upload failed for %s", path, exc_info=True)
        return False


@mcp.tool()
async def convert_document(filename: str) -> str:
    """Convert a document to markdown using Azure Content Understanding.

    The file must exist in the current working directory. Produces a
    ``{filename}.md`` file alongside the original. Skips conversion if the
    markdown file already exists (idempotent).

    Args:
        filename: Name of the file to convert (must exist in working directory).

    Returns:
        JSON string with markdown_path and size, or an error message.
    """
    workspace = Path(os.getenv("WORKSPACE", "/workspace"))
    file_path = workspace / filename

    # Prevent path traversal — resolved path must stay under workspace
    real_path = file_path.resolve()
    real_workspace = workspace.resolve()
    if not (real_path == real_workspace or str(real_path).startswith(str(real_workspace) + os.sep)):
        return json.dumps({"error": f"Invalid filename: {filename}"})

    if not file_path.exists():
        return json.dumps({"error": f"File not found: {filename}"})

    md_path = Path(workspace) / f"{filename}.md"

    # Idempotent — skip if already converted
    if md_path.exists():
        return json.dumps({
            "markdown_path": f"{filename}.md",
            "size": md_path.stat().st_size,
            "cached": True,
        })

    cu_endpoint = _derive_cu_endpoint()
    if not cu_endpoint:
        return json.dumps({"error": "Content Understanding not configured (AZURE_ENDPOINT not set)"})

    # Read the file
    file_bytes = file_path.read_bytes()
    content_type = _guess_content_type(filename)

    # Call Content Understanding
    try:
        from azure.ai.contentunderstanding.aio import ContentUnderstandingClient
        from azure.identity.aio import DefaultAzureCredential

        credential = DefaultAzureCredential()
        try:
            cu_client = ContentUnderstandingClient(
                endpoint=cu_endpoint, credential=credential
            )
            try:
                poller = await cu_client.begin_analyze_binary(
                    analyzer_id="prebuilt-layout",
                    binary_input=file_bytes,
                )
                result = await poller.result()
            finally:
                await cu_client.close()
        finally:
            await credential.close()
    except Exception as exc:
        logger.exception("Content Understanding failed for %s", filename)
        return json.dumps({"error": f"Content Understanding failed: {exc}"})

    if not result.contents:
        return json.dumps({"error": "Content Understanding produced no content"})

    markdown = result.contents[0].markdown

    # Write markdown to workspace
    md_path.write_text(markdown, encoding="utf-8")
    logger.info("Wrote %s (%d bytes)", md_path.name, len(markdown))

    # Fire-and-forget ADLS uploads (best effort)
    session_id = os.getenv("SESSION_ID", "local")
    await _upload_to_adls(
        f"originals/{session_id}/{filename}", file_bytes, content_type
    )
    await _upload_to_adls(
        f"markdown/{session_id}/{filename}.md",
        markdown.encode("utf-8"),
        "text/markdown",
    )

    return json.dumps({
        "markdown_path": f"{filename}.md",
        "size": len(markdown),
    })


def _guess_content_type(filename: str) -> str:
    """Return a reasonable content type for the given filename."""
    ext = Path(filename).suffix.lower()
    return {
        ".pdf": "application/pdf",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xls": "application/vnd.ms-excel",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".tiff": "image/tiff",
        ".bmp": "image/bmp",
        ".html": "text/html",
        ".htm": "text/html",
        ".txt": "text/plain",
        ".csv": "text/csv",
        ".rtf": "application/rtf",
    }.get(ext, "application/octet-stream")


if __name__ == "__main__":
    mcp.run(transport="stdio")
