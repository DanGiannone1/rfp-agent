#!/usr/bin/env python3
"""One-time setup script: creates a Foundry IQ knowledge source + knowledge base.

Reads configuration from environment variables (or .env file). Idempotent —
safe to re-run (uses create_or_update).

Usage:
    uv run python setup_knowledge_base.py

Required env vars:
    AZURE_SEARCH_ENDPOINT  — e.g. https://rfpagent-search.search.windows.net
    AZURE_SEARCH_KEY       — admin key for the search service
    AZURE_ENDPOINT         — Azure OpenAI / Foundry endpoint
    ADLS_CONNECTION_STRING — ADLS connection string (key-based) or ResourceId string
                             for managed identity. If unset, constructed from
                             AZURE_SUBSCRIPTION_ID + AZURE_RESOURCE_GROUP + ADLS_ACCOUNT_NAME.
    ADLS_FILESYSTEM        — ADLS filesystem/container name (default: documents)

Optional env vars:
    AZURE_SEARCH_KB_NAME         — knowledge base name (default: rfp-knowledge)
    AZURE_SEARCH_KS_NAME         — knowledge source name (default: rfp-documents)
    AZURE_SEARCH_EMBEDDING_MODEL — embedding deployment name (default: text-embedding-3-large)
    AZURE_SEARCH_CHAT_MODEL      — chat model deployment name (default: gpt-4.1-mini)
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    AzureBlobKnowledgeSource,
    AzureBlobKnowledgeSourceParameters,
    AzureOpenAIVectorizerParameters,
    KnowledgeBase,
    KnowledgeBaseAzureOpenAIModel,
    KnowledgeRetrievalLowReasoningEffort,
    KnowledgeRetrievalOutputMode,
    KnowledgeSourceAzureOpenAIVectorizer,
    KnowledgeSourceContentExtractionMode,
    KnowledgeSourceIngestionParameters,
    KnowledgeSourceReference,
)

# ── Configuration ────────────────────────────────────────────────────────

SEARCH_ENDPOINT = os.environ.get("AZURE_SEARCH_ENDPOINT", "")
SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY", "")
AZURE_ENDPOINT = os.environ.get("AZURE_ENDPOINT", "")
ADLS_CONNECTION_STRING = os.environ.get("ADLS_CONNECTION_STRING", "")
ADLS_ACCOUNT_NAME = os.environ.get("ADLS_ACCOUNT_NAME", "")
ADLS_FILESYSTEM = os.environ.get("ADLS_FILESYSTEM", "documents")
AZURE_SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID", "")
AZURE_RESOURCE_GROUP = os.environ.get("AZURE_RESOURCE_GROUP", "")

KB_NAME = os.environ.get("AZURE_SEARCH_KB_NAME", "rfp-knowledge")
KS_NAME = os.environ.get("AZURE_SEARCH_KS_NAME", "rfp-documents")
EMBEDDING_MODEL = os.environ.get("AZURE_SEARCH_EMBEDDING_MODEL", "text-embedding-3-large")
CHAT_MODEL = os.environ.get("AZURE_SEARCH_CHAT_MODEL", "gpt-4.1-mini")


def _require(name: str, value: str) -> str:
    if not value:
        print(f"ERROR: {name} must be set", file=sys.stderr)
        sys.exit(1)
    return value


def _aoai_resource_url(endpoint: str) -> str:
    """Convert a Foundry/Cognitive Services endpoint to an Azure OpenAI resource URL.

    Handles both forms:
      - https://name.cognitiveservices.azure.com/openai/v1/ → https://name.openai.azure.com/
      - https://name.services.ai.azure.com/ → https://name.openai.azure.com/
    """
    from urllib.parse import urlparse

    parsed = urlparse(endpoint)
    hostname = parsed.hostname or ""
    name = hostname.split(".")[0]
    return f"https://{name}.openai.azure.com/"


def main() -> None:
    _require("AZURE_SEARCH_ENDPOINT", SEARCH_ENDPOINT)
    _require("AZURE_SEARCH_KEY", SEARCH_KEY)
    _require("AZURE_ENDPOINT", AZURE_ENDPOINT)

    aoai_url = _aoai_resource_url(AZURE_ENDPOINT)

    # Build ADLS connection string for Azure AI Search indexer
    if ADLS_CONNECTION_STRING:
        adls_connection = ADLS_CONNECTION_STRING
    else:
        _require("ADLS_ACCOUNT_NAME", ADLS_ACCOUNT_NAME)
        _require("AZURE_SUBSCRIPTION_ID", AZURE_SUBSCRIPTION_ID)
        _require("AZURE_RESOURCE_GROUP", AZURE_RESOURCE_GROUP)
        adls_connection = (
            f"ResourceId=/subscriptions/{AZURE_SUBSCRIPTION_ID}"
            f"/resourceGroups/{AZURE_RESOURCE_GROUP}"
            f"/providers/Microsoft.Storage/storageAccounts/{ADLS_ACCOUNT_NAME};"
        )

    print(f"Search endpoint: {SEARCH_ENDPOINT}")
    print(f"Azure OpenAI URL: {aoai_url}")
    print(f"ADLS connection: {adls_connection[:80]}...")
    print()

    client = SearchIndexClient(
        endpoint=SEARCH_ENDPOINT,
        credential=AzureKeyCredential(SEARCH_KEY),
    )

    # ── 1. Knowledge Source (blob → ADLS Gen2) ──────────────────────────

    aoai_params = AzureOpenAIVectorizerParameters(
        resource_url=aoai_url,
        deployment_name=EMBEDDING_MODEL,
        model_name=EMBEDDING_MODEL,
    )

    chat_params = AzureOpenAIVectorizerParameters(
        resource_url=aoai_url,
        deployment_name=CHAT_MODEL,
        model_name=CHAT_MODEL,
    )

    knowledge_source = AzureBlobKnowledgeSource(
        name=KS_NAME,
        description=(
            "RFP documents, past proposals, and company knowledge stored on ADLS Gen2. "
            "Includes PDFs, Word documents, spreadsheets, and images."
        ),
        azure_blob_parameters=AzureBlobKnowledgeSourceParameters(
            connection_string=adls_connection,
            container_name=ADLS_FILESYSTEM,
            is_adls_gen2=True,
            ingestion_parameters=KnowledgeSourceIngestionParameters(
                content_extraction_mode=KnowledgeSourceContentExtractionMode.STANDARD,
                embedding_model=KnowledgeSourceAzureOpenAIVectorizer(
                    azure_open_ai_parameters=aoai_params,
                ),
                chat_completion_model=KnowledgeBaseAzureOpenAIModel(
                    azure_open_ai_parameters=chat_params,
                ),
            ),
        ),
    )

    print(f"Creating knowledge source '{KS_NAME}'...")
    client.create_or_update_knowledge_source(knowledge_source)
    print(f"  Done.")

    # ── 2. Knowledge Base ────────────────────────────────────────────────

    kb_model_params = AzureOpenAIVectorizerParameters(
        resource_url=aoai_url,
        deployment_name=CHAT_MODEL,
        model_name=CHAT_MODEL,
    )

    knowledge_base = KnowledgeBase(
        name=KB_NAME,
        description=(
            "Knowledge base for RFP analysis. Contains uploaded RFP documents, "
            "past proposals, boilerplate responses, and company reference materials."
        ),
        retrieval_instructions=(
            "Search the document knowledge source for any questions about RFP requirements, "
            "compliance criteria, past proposals, company capabilities, or reference materials. "
            "Formulate specific, targeted queries — break broad questions into focused sub-queries."
        ),
        output_mode=KnowledgeRetrievalOutputMode.EXTRACTIVE_DATA,
        retrieval_reasoning_effort=KnowledgeRetrievalLowReasoningEffort(),
        knowledge_sources=[KnowledgeSourceReference(name=KS_NAME)],
        models=[KnowledgeBaseAzureOpenAIModel(azure_open_ai_parameters=kb_model_params)],
    )

    print(f"Creating knowledge base '{KB_NAME}'...")
    client.create_or_update_knowledge_base(knowledge_base)
    print(f"  Done.")

    print()
    print("Setup complete. The indexer will begin processing documents automatically.")
    print(f"MCP endpoint: {SEARCH_ENDPOINT}/knowledgebases/{KB_NAME}/mcp?api-version=2025-11-01-preview")


if __name__ == "__main__":
    main()
