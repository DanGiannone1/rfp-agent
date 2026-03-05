#!/usr/bin/env python3
"""Upload sample knowledge base PDFs to ADLS Gen2 for indexing by Foundry IQ.

Walks sample_data/knowledge_base/ and uploads every PDF to the configured ADLS
container. The Azure AI Search indexer (created by setup_knowledge_base.py)
will automatically pick up new documents and index them.

Usage:
    uv run python index_knowledge_base.py

Required env vars:
    ADLS_ACCOUNT_NAME   — ADLS Gen2 storage account
    ADLS_FILESYSTEM     — container name (default: documents)

Authentication: uses DefaultAzureCredential (az login locally, managed identity in prod).
"""

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ADLS_ACCOUNT_NAME = os.getenv("ADLS_ACCOUNT_NAME", "")
ADLS_FILESYSTEM = os.getenv("ADLS_FILESYSTEM", "documents")
SAMPLE_DATA_DIR = Path(__file__).parent / "sample_data" / "knowledge_base"


async def main() -> None:
    if not ADLS_ACCOUNT_NAME:
        print("ERROR: ADLS_ACCOUNT_NAME must be set", file=sys.stderr)
        sys.exit(1)

    from azure.identity.aio import DefaultAzureCredential
    from azure.storage.filedatalake.aio import DataLakeServiceClient
    from azure.storage.filedatalake import ContentSettings

    account_url = f"https://{ADLS_ACCOUNT_NAME}.dfs.core.windows.net"
    credential = DefaultAzureCredential()

    try:
        async with DataLakeServiceClient(
            account_url=account_url, credential=credential
        ) as client:
            fs = client.get_file_system_client(ADLS_FILESYSTEM)

            # Ensure container exists
            try:
                await fs.get_file_system_properties()
            except Exception:
                print(f"Creating filesystem '{ADLS_FILESYSTEM}'...")
                await fs.create_file_system()

            # Collect all PDFs
            pdfs = sorted(SAMPLE_DATA_DIR.rglob("*.pdf"))
            if not pdfs:
                print(f"No PDFs found in {SAMPLE_DATA_DIR}")
                sys.exit(1)

            print(f"Found {len(pdfs)} PDFs to upload to {ADLS_ACCOUNT_NAME}/{ADLS_FILESYSTEM}")
            print()

            uploaded = 0
            skipped = 0
            errors = 0

            for pdf_path in pdfs:
                # Use category/filename as the ADLS path
                rel = pdf_path.relative_to(SAMPLE_DATA_DIR)
                adls_path = f"knowledge_base/{rel}"

                try:
                    file_client = fs.get_file_client(adls_path)

                    # Check if file already exists with same size
                    try:
                        props = await file_client.get_file_properties()
                        if props.size == pdf_path.stat().st_size:
                            print(f"  skip  {rel} (unchanged)")
                            skipped += 1
                            continue
                    except Exception:
                        pass  # File doesn't exist yet

                    data = pdf_path.read_bytes()
                    await file_client.upload_data(
                        data,
                        overwrite=True,
                        content_settings=ContentSettings(
                            content_type="application/pdf"
                        ),
                    )
                    size_kb = len(data) / 1024
                    print(f"  upload {rel} ({size_kb:.0f} KB)")
                    uploaded += 1
                except Exception as exc:
                    print(f"  ERROR  {rel}: {exc}", file=sys.stderr)
                    errors += 1

            print()
            print(f"Done: {uploaded} uploaded, {skipped} skipped, {errors} errors")

            # Verify uploads by listing files in knowledge_base/ prefix
            print()
            print("Verifying ADLS contents...")
            adls_count = 0
            async for path in fs.get_paths(path="knowledge_base", recursive=True):
                if path.name.endswith(".pdf"):
                    adls_count += 1
            print(f"  {adls_count} PDFs found in knowledge_base/ on ADLS")

            if uploaded > 0:
                print()
                print("The Azure AI Search indexer will process new documents automatically.")
    finally:
        await credential.close()


if __name__ == "__main__":
    asyncio.run(main())
