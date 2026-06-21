"""Non-blocking simulation action writer for Redis AMS."""

from __future__ import annotations

import hashlib
import json
import threading
import time
from queue import Empty, Queue
from typing import Any

from .redis_memory import RedisMemoryClient


class RedisMemoryWriter:
    BATCH_SIZE = 20
    MAX_RETRIES = 3

    def __init__(self, simulation_id: str, client: RedisMemoryClient | None = None):
        self.simulation_id = simulation_id
        self.client = client or RedisMemoryClient()
        self.queue: Queue[dict[str, Any]] = Queue()
        self.running = False
        self.thread: threading.Thread | None = None
        self.stats = {"queued": 0, "indexed": 0, "failed": 0, "status": "idle", "last_error": None}

    def start(self) -> None:
        if self.running:
            return
        self.running = True
        self.stats["status"] = "running" if self.client.enabled else "degraded"
        self.thread = threading.Thread(target=self._run, daemon=True, name=f"ams-{self.simulation_id}")
        self.thread.start()

    def stop(self) -> None:
        self.running = False
        if self.thread:
            self.thread.join(timeout=15)
        self.stats["status"] = "complete" if not self.stats["failed"] else "degraded"

    def add_activity_from_dict(self, data: dict[str, Any], platform: str) -> None:
        if data.get("event_type") or data.get("action_type") == "DO_NOTHING":
            return
        text = _activity_text(data)
        if not text:
            return
        stable = json.dumps([self.simulation_id, platform, data], sort_keys=True, ensure_ascii=False)
        record = {
            "id": hashlib.sha256(stable.encode("utf-8")).hexdigest(),
            "text": text,
            "timestamp": data.get("timestamp"),
            "metadata": {
                "simulation_id": self.simulation_id,
                "platform": platform,
                "agent_id": data.get("agent_id", 0),
                "agent_name": data.get("agent_name", ""),
                "action_type": data.get("action_type", ""),
                "round": data.get("round", 0),
                "source": "actions.jsonl",
            },
        }
        self.queue.put(record)
        self.stats["queued"] += 1

    def _run(self) -> None:
        while self.running or not self.queue.empty():
            batch = []
            try:
                batch.append(self.queue.get(timeout=0.5))
            except Empty:
                continue
            while len(batch) < self.BATCH_SIZE:
                try:
                    batch.append(self.queue.get_nowait())
                except Empty:
                    break
            if not self.client.enabled:
                self.stats["failed"] += len(batch)
                self.stats["last_error"] = "AMS disabled or client package unavailable"
                continue
            for attempt in range(self.MAX_RETRIES):
                try:
                    self.stats["indexed"] += self.client.write_batch(batch)
                    self.stats["last_error"] = None
                    break
                except Exception as exc:
                    self.stats["last_error"] = str(exc)
                    if attempt + 1 == self.MAX_RETRIES:
                        self.stats["failed"] += len(batch)
                        self.stats["status"] = "degraded"
                    else:
                        time.sleep(2 ** attempt)


class RedisMemoryManager:
    _writers: dict[str, RedisMemoryWriter] = {}
    _lock = threading.Lock()

    @classmethod
    def create_writer(cls, simulation_id: str) -> RedisMemoryWriter:
        with cls._lock:
            cls.stop_writer(simulation_id)
            writer = RedisMemoryWriter(simulation_id)
            writer.start()
            cls._writers[simulation_id] = writer
            return writer

    @classmethod
    def get_writer(cls, simulation_id: str) -> RedisMemoryWriter | None:
        return cls._writers.get(simulation_id)

    @classmethod
    def stop_writer(cls, simulation_id: str) -> None:
        writer = cls._writers.pop(simulation_id, None)
        if writer:
            writer.stop()

    @classmethod
    def stop_all(cls) -> None:
        for simulation_id in list(cls._writers):
            cls.stop_writer(simulation_id)

    @classmethod
    def status(cls, simulation_id: str) -> dict[str, Any]:
        writer = cls.get_writer(simulation_id)
        return dict(writer.stats) if writer else {"status": "not_started", "queued": 0, "indexed": 0, "failed": 0}


def _activity_text(data: dict[str, Any]) -> str:
    args = data.get("action_args") or {}
    content_fields = ("content", "quote_content", "comment_content", "post_content", "original_content", "response")
    content = next((str(args[key]).strip() for key in content_fields if args.get(key)), "")
    if not content and data.get("result"):
        content = str(data["result"]).strip()
    if not content:
        return ""
    name = data.get("agent_name") or f"Agent {data.get('agent_id', 0)}"
    action = str(data.get("action_type") or "ACTION").replace("_", " ").lower()
    return f"{name} {action}: {content}"
