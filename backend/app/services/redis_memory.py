"""Redis Agent Memory Server client with graceful degradation."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from ..config import Config

try:
    from agent_memory_client import MemoryAPIClient, MemoryClientConfig
    from agent_memory_client.models import ClientMemoryRecord, MemoryTypeEnum
except ImportError:  # Allows SQLite-only operation when AMS extras are absent.
    MemoryAPIClient = MemoryClientConfig = ClientMemoryRecord = MemoryTypeEnum = None


@dataclass
class MemorySearchHit:
    id: str
    text: str
    score: float
    metadata: dict[str, Any]
    user_id: str | None = None
    session_id: str | None = None


class RedisMemoryClient:
    NAMESPACE_PREFIX = "snorkel"

    def __init__(self, base_url: str | None = None, timeout: float | None = None):
        self.base_url = base_url or Config.AMS_BASE_URL
        self.timeout = timeout or Config.AMS_TIMEOUT
        self.enabled = bool(Config.AMS_ENABLED and self.base_url and MemoryAPIClient)

    @staticmethod
    def user_id(simulation_id: str, agent_id: int | str) -> str:
        return f"sim:{simulation_id}:agent:{agent_id}"

    @staticmethod
    def session_id(simulation_id: str, platform: str, agent_id: int | str) -> str:
        return f"sim:{simulation_id}:{platform}:agent:{agent_id}"

    @staticmethod
    def namespace(simulation_id: str) -> str:
        return f"snorkel:sim:{simulation_id}"

    def _client(self):
        if not self.enabled:
            raise RuntimeError("Redis Agent Memory Server is disabled or unavailable")
        client = MemoryAPIClient(MemoryClientConfig(
            base_url=self.base_url,
            timeout=self.timeout,
            default_namespace=self.NAMESPACE_PREFIX,
        ))
        if Config.AMS_API_KEY:
            client._client.headers["Authorization"] = f"Bearer {Config.AMS_API_KEY}"
        return client

    async def health_async(self) -> dict[str, Any]:
        if not self.enabled:
            return {"available": False, "reason": "disabled_or_client_missing"}
        try:
            async with self._client() as client:
                response = await client.health_check()
            return {"available": True, "details": response.model_dump(mode="json")}
        except Exception as exc:
            return {"available": False, "reason": str(exc)}

    def health(self) -> dict[str, Any]:
        return asyncio.run(self.health_async())

    async def write_batch_async(self, records: list[dict[str, Any]]) -> int:
        if not records or not self.enabled:
            return 0
        memories = []
        for record in records:
            metadata = dict(record.get("metadata") or {})
            simulation_id = str(metadata["simulation_id"])
            agent_id = metadata["agent_id"]
            platform = str(metadata.get("platform") or "unknown")
            timestamp = _timestamp(record.get("timestamp"))
            memories.append(ClientMemoryRecord(
                id=str(record["id"]),
                text=str(record["text"]),
                user_id=self.user_id(simulation_id, agent_id),
                session_id=self.session_id(simulation_id, platform, agent_id),
                namespace=self.namespace(simulation_id),
                memory_type=MemoryTypeEnum.EPISODIC,
                topics=[platform, str(metadata.get("action_type") or "action")],
                entities=[str(metadata.get("agent_name") or agent_id)],
                created_at=timestamp,
                updated_at=timestamp,
                event_date=timestamp,
                metadata=metadata,
            ))
        async with self._client() as client:
            await client.create_long_term_memory(memories)
        return len(memories)

    def write_batch(self, records: list[dict[str, Any]]) -> int:
        return asyncio.run(self.write_batch_async(records))

    async def search_async(
        self,
        simulation_id: str,
        query: str,
        limit: int = 10,
        mode: str = "hybrid",
        agent_id: int | str | None = None,
    ) -> list[MemorySearchHit]:
        if not self.enabled:
            return []
        kwargs: dict[str, Any] = {
            "text": query,
            "search_mode": mode,
            "namespace": {"eq": self.namespace(simulation_id)},
            "limit": limit,
        }
        if agent_id is not None:
            kwargs["user_id"] = {"eq": self.user_id(simulation_id, agent_id)}
        async with self._client() as client:
            result = await client.search_long_term_memory(**kwargs)
        hits = []
        for memory in result.memories:
            distance = float(getattr(memory, "dist", 1.0) or 0.0)
            hits.append(MemorySearchHit(
                id=memory.id,
                text=memory.text,
                score=max(0.0, 1.0 - distance),
                metadata=dict(memory.metadata or {}),
                user_id=memory.user_id,
                session_id=memory.session_id,
            ))
        return hits

    def search(self, *args: Any, **kwargs: Any) -> list[MemorySearchHit]:
        return asyncio.run(self.search_async(*args, **kwargs))


def _timestamp(value: Any) -> datetime:
    if isinstance(value, datetime):
        result = value
    elif value:
        result = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    else:
        result = datetime.now(timezone.utc)
    return result if result.tzinfo else result.replace(tzinfo=timezone.utc)
