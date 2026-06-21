"""Read-only access to OASIS SQLite databases and simulation artifacts."""

from __future__ import annotations

import csv
import json
import os
import sqlite3
from pathlib import Path
from typing import Any

from ..config import Config


class SimulationQueryService:
    def __init__(self, simulation_id: str):
        self.simulation_id = simulation_id
        self.simulation_dir = Path(Config.OASIS_SIMULATION_DATA_DIR) / simulation_id

    def database_path(self, platform: str) -> Path:
        return self.simulation_dir / f"{platform}_simulation.db"

    def _connect(self, platform: str) -> sqlite3.Connection:
        path = self.database_path(platform)
        if not path.exists():
            raise FileNotFoundError(f"simulation database not found: {path}")
        connection = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True)
        connection.row_factory = sqlite3.Row
        return connection

    def rows(
        self,
        table: str,
        platform: str | None = None,
        limit: int = 500,
        query: str | None = None,
    ) -> list[dict[str, Any]]:
        if table not in {"post", "comment", "user", "follow"}:
            raise ValueError(f"unsupported OASIS table: {table}")
        results = []
        for current in ([platform] if platform else ["twitter", "reddit"]):
            try:
                with self._connect(current) as connection:
                    columns = [row[1] for row in connection.execute(f"PRAGMA table_info({table})")]
                    if not columns:
                        continue
                    params: list[Any] = []
                    sql = f"SELECT * FROM {table}"
                    text_columns = [name for name in columns if name in {"content", "text", "body", "bio", "name", "username"}]
                    if query and text_columns:
                        sql += " WHERE " + " OR ".join(f"CAST({name} AS TEXT) LIKE ?" for name in text_columns)
                        params.extend([f"%{query}%"] * len(text_columns))
                    sql += " LIMIT ?"
                    params.append(max(1, min(limit - len(results), 5000)))
                    for row in connection.execute(sql, params):
                        item = dict(row)
                        item["platform"] = current
                        item["source_table"] = table
                        results.append(item)
            except (FileNotFoundError, sqlite3.DatabaseError):
                continue
            if len(results) >= limit:
                break
        return results[:limit]

    def posts(self, **kwargs: Any) -> list[dict[str, Any]]:
        return self.rows("post", **kwargs)

    def comments(self, **kwargs: Any) -> list[dict[str, Any]]:
        return self.rows("comment", **kwargs)

    def actions(self, platform: str | None = None, limit: int = 1000) -> list[dict[str, Any]]:
        actions = []
        for current in ([platform] if platform else ["twitter", "reddit"]):
            candidates = [
                self.simulation_dir / current / "actions.jsonl",
                self.simulation_dir / f"{current}_actions.jsonl",
            ]
            path = next((candidate for candidate in candidates if candidate.exists()), None)
            if not path:
                continue
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if "event_type" not in item:
                        item["platform"] = current
                        actions.append(item)
                    if len(actions) >= limit:
                        return actions
        return actions

    def agents(self) -> list[dict[str, Any]]:
        reddit = self.simulation_dir / "reddit_profiles.json"
        if reddit.exists():
            with reddit.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        twitter = self.simulation_dir / "twitter_profiles.csv"
        if twitter.exists():
            with twitter.open("r", encoding="utf-8") as handle:
                return list(csv.DictReader(handle))
        return []

    def personas(self) -> list[dict[str, Any]]:
        path = self.simulation_dir / "personas.json"
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def statistics(self) -> dict[str, Any]:
        personas = self.personas()
        actions = self.actions(limit=100000)
        return {
            "simulation_id": self.simulation_id,
            "agents": len(self.agents()),
            "segments": sorted({item.get("segment", "Unsegmented") for item in personas}),
            "posts": len(self.posts(limit=100000)),
            "comments": len(self.comments(limit=100000)),
            "actions": len(actions),
            "rounds": max((int(item.get("round", 0) or 0) for item in actions), default=0),
            "databases": {
                platform: self.database_path(platform).exists()
                for platform in ("twitter", "reddit")
            },
        }

    def panorama(self, query: str | None = None, limit: int = 1000) -> dict[str, Any]:
        return {
            "statistics": self.statistics(),
            "posts": self.posts(limit=limit, query=query),
            "comments": self.comments(limit=limit, query=query),
            "actions": self.actions(limit=limit),
            "personas": self.personas(),
        }
