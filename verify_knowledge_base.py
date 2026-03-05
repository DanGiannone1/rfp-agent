#!/usr/bin/env python3
"""Verify the Foundry IQ knowledge base is set up and retrieval works end-to-end.

Checks:
1. Knowledge source and knowledge base exist in Azure AI Search
2. Indexer status — sync state, document counts, errors
3. MCP retrieval — sends a test query and prints results

Usage:
    uv run python verify_knowledge_base.py

Required env vars:
    AZURE_SEARCH_ENDPOINT  — e.g. https://rfpagent-search.search.windows.net
    AZURE_SEARCH_KEY       — admin key for the search service
    AZURE_SEARCH_KB_NAME   — knowledge base name (default: rfp-knowledge)
    AZURE_SEARCH_KS_NAME   — knowledge source name (default: rfp-documents)
"""

import os
import sys

import httpx
from dotenv import load_dotenv

load_dotenv()

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

SEARCH_ENDPOINT = os.environ.get("AZURE_SEARCH_ENDPOINT", "")
SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY", "")
KB_NAME = os.environ.get("AZURE_SEARCH_KB_NAME", "rfp-knowledge")
KS_NAME = os.environ.get("AZURE_SEARCH_KS_NAME", "rfp-documents")

TEST_QUERY = "Meridian Associates firm overview capabilities"


def main() -> None:
    if not SEARCH_ENDPOINT or not SEARCH_KEY:
        print("ERROR: AZURE_SEARCH_ENDPOINT and AZURE_SEARCH_KEY must be set", file=sys.stderr)
        sys.exit(1)

    client = SearchIndexClient(
        endpoint=SEARCH_ENDPOINT,
        credential=AzureKeyCredential(SEARCH_KEY),
    )

    # ── 1. Check knowledge source exists ─────────────────────────────────
    print(f"Checking knowledge source '{KS_NAME}'...")
    try:
        ks = client.get_knowledge_source(KS_NAME)
        print(f"  Found: {ks.name}")
        print(f"  Description: {ks.description}")
    except Exception as exc:
        print(f"  ERROR: Knowledge source not found: {exc}", file=sys.stderr)
        sys.exit(1)

    # ── 2. Check knowledge base exists ───────────────────────────────────
    print()
    print(f"Checking knowledge base '{KB_NAME}'...")
    try:
        kb = client.get_knowledge_base(KB_NAME)
        print(f"  Found: {kb.name}")
        print(f"  Description: {kb.description}")
        sources = getattr(kb, "knowledge_sources", []) or []
        print(f"  Knowledge sources: {[s.name for s in sources]}")
    except Exception as exc:
        print(f"  ERROR: Knowledge base not found: {exc}", file=sys.stderr)
        sys.exit(1)

    # ── 3. Indexer status ────────────────────────────────────────────────
    print()
    print(f"Checking indexer status for '{KS_NAME}'...")
    try:
        status = client.get_knowledge_source_status(KS_NAME)
        sync_state = getattr(status, "sync_state", None) or "unknown"
        doc_count = getattr(status, "document_count", None)
        error_count = getattr(status, "error_count", None)
        last_sync = getattr(status, "last_sync_time", None)
        print(f"  Sync state: {sync_state}")
        if doc_count is not None:
            print(f"  Document count: {doc_count}")
        if error_count is not None:
            print(f"  Error count: {error_count}")
        if last_sync is not None:
            print(f"  Last sync: {last_sync}")
    except Exception as exc:
        print(f"  WARNING: Could not get status: {exc}")

    # ── 4. MCP retrieval test ────────────────────────────────────────────
    print()
    mcp_url = (
        f"{SEARCH_ENDPOINT}/knowledgebases/{KB_NAME}"
        f"/mcp?api-version=2025-11-01-preview"
    )
    print(f"Testing MCP retrieval at {mcp_url}")
    print(f"  Query: '{TEST_QUERY}'")
    print()

    try:
        resp = httpx.post(
            mcp_url,
            headers={
                "api-key": SEARCH_KEY,
                "Content-Type": "application/json",
            },
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "id": "verify-1",
                "params": {
                    "name": "knowledge_base_retrieve",
                    "arguments": {"query": TEST_QUERY},
                },
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        result = data.get("result", {})
        content = result.get("content", [])

        if not content:
            print("  WARNING: No results returned. The indexer may still be processing.")
            print(f"  Raw response: {data}")
        else:
            print(f"  Got {len(content)} result(s):")
            for i, item in enumerate(content):
                text = item.get("text", "")
                preview = text[:200].replace("\n", " ")
                print(f"  [{i+1}] {preview}...")
    except Exception as exc:
        print(f"  ERROR: MCP retrieval failed: {exc}")
        sys.exit(1)

    print()
    print("Verification complete.")


if __name__ == "__main__":
    main()
