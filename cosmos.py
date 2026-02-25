"""Async CosmosDB client for session and message persistence."""

import logging
import uuid
from datetime import datetime, timezone

from azure.cosmos.aio import CosmosClient
from azure.cosmos import PartitionKey, exceptions
from azure.identity.aio import DefaultAzureCredential

logger = logging.getLogger(__name__)

DATABASE_NAME = "rfp_agent"
CONTAINER_NAME = "sessions"


class CosmosStore:
    """Thin async wrapper around a single CosmosDB container.

    Uses ``doc_type`` discrimination to store both session metadata and
    messages in the same container, partitioned by ``session_id``.
    """

    def __init__(self, endpoint: str):
        self._endpoint = endpoint
        self._credential = DefaultAzureCredential()
        self._client: CosmosClient | None = None
        self._container = None

    async def initialize(self):
        self._client = CosmosClient(self._endpoint, credential=self._credential)
        database = await self._client.create_database_if_not_exists(DATABASE_NAME)
        self._container = await database.create_container_if_not_exists(
            id=CONTAINER_NAME,
            partition_key=PartitionKey(path="/session_id"),
        )
        logger.info("CosmosDB initialised: %s/%s", DATABASE_NAME, CONTAINER_NAME)

    async def close(self):
        if self._client:
            await self._client.close()
        if self._credential:
            await self._credential.close()

    # ------------------------------------------------------------------
    # Session CRUD
    # ------------------------------------------------------------------
    async def create_session(self, metadata: dict):
        doc = {
            "id": metadata["session_id"],
            "session_id": metadata["session_id"],
            "doc_type": "session",
            **metadata,
        }
        await self._container.create_item(doc)

    async def get_session(self, session_id: str) -> dict | None:
        try:
            item = await self._container.read_item(
                item=session_id, partition_key=session_id
            )
            return _strip_cosmos_fields(item)
        except exceptions.CosmosResourceNotFoundError:
            return None

    async def update_session_activity(
        self, session_id: str, last_activity_at: datetime
    ):
        try:
            item = await self._container.read_item(
                item=session_id, partition_key=session_id
            )
            item["last_activity_at"] = last_activity_at.isoformat()
            await self._container.replace_item(item=item["id"], body=item)
        except exceptions.CosmosResourceNotFoundError:
            logger.warning("Session %s not found for activity update", session_id)

    async def close_session(self, session_id: str):
        try:
            item = await self._container.read_item(
                item=session_id, partition_key=session_id
            )
            item["status"] = "closed"
            item["closed_at"] = datetime.now(timezone.utc).isoformat()
            await self._container.replace_item(item=item["id"], body=item)
        except exceptions.CosmosResourceNotFoundError:
            logger.warning("Session %s not found for close", session_id)

    # ------------------------------------------------------------------
    # Message CRUD
    # ------------------------------------------------------------------
    async def add_message(self, message: dict):
        doc = {
            "id": uuid.uuid4().hex,
            "doc_type": "message",
            **message,
        }
        await self._container.create_item(doc)

    async def get_messages(self, session_id: str) -> list[dict]:
        query = (
            "SELECT * FROM c "
            "WHERE c.session_id = @sid AND c.doc_type = 'message' "
            "ORDER BY c.turn_index ASC, c.role ASC"
        )
        params = [{"name": "@sid", "value": session_id}]
        items = []
        async for item in self._container.query_items(
            query=query,
            parameters=params,
            partition_key=session_id,
        ):
            items.append(_strip_cosmos_fields(item))
        return items


def _strip_cosmos_fields(doc: dict) -> dict:
    """Remove Cosmos system fields from a document."""
    return {
        k: v
        for k, v in doc.items()
        if not k.startswith("_") and k not in ("etag",)
    }
