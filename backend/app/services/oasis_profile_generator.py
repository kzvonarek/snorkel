"""Convert evidence-backed persona inputs into OASIS profile files."""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .persona import PersonaInput


@dataclass
class OasisAgentProfile:
    user_id: int
    user_name: str
    name: str
    bio: str
    persona: str
    karma: int = 1000
    friend_count: int = 100
    follower_count: int = 150
    statuses_count: int = 500
    age: int | None = None
    gender: str | None = None
    mbti: str | None = None
    country: str | None = None
    profession: str | None = None
    interested_topics: list[str] = field(default_factory=list)
    source_entity_uuid: str | None = None
    source_entity_type: str | None = None
    evidence_references: list[str] = field(default_factory=list)
    confidence: str = "medium"
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


class OasisProfileGenerator:
    """Build profiles directly from customer personas, without a graph dependency."""

    def __init__(self, *_: Any, **__: Any):
        pass

    def generate_profiles_from_personas(
        self, personas: list[PersonaInput]
    ) -> list[OasisAgentProfile]:
        profiles: list[OasisAgentProfile] = []
        for index, persona in enumerate(personas):
            demographics = persona.demographics
            username = persona.username or _username(persona.identity, index)
            profiles.append(
                OasisAgentProfile(
                    user_id=index,
                    user_name=username,
                    name=persona.identity,
                    bio=persona.description,
                    persona=persona.user_char,
                    age=_optional_int(demographics.get("age")),
                    gender=demographics.get("gender"),
                    mbti=demographics.get("mbti"),
                    country=demographics.get("country"),
                    profession=demographics.get("profession") or persona.segment,
                    interested_topics=list(persona.traits),
                    source_entity_uuid=persona.identity,
                    source_entity_type=persona.segment,
                    evidence_references=list(persona.evidence_references),
                    confidence=persona.confidence,
                )
            )
        return profiles

    def save_profiles(
        self, profiles: list[OasisAgentProfile], file_path: str, platform: str = "reddit"
    ) -> None:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        if platform == "twitter":
            self._save_twitter_csv(profiles, file_path)
        else:
            self._save_reddit_json(profiles, file_path)

    def _save_twitter_csv(self, profiles: list[OasisAgentProfile], file_path: str) -> None:
        with open(file_path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["user_id", "name", "username", "user_char", "description"])
            for profile in profiles:
                user_char = " ".join(
                    part for part in (profile.bio, profile.persona) if part
                ).replace("\n", " ").replace("\r", " ")
                writer.writerow([
                    profile.user_id,
                    profile.name,
                    profile.user_name,
                    user_char,
                    profile.bio.replace("\n", " ").replace("\r", " "),
                ])

    def _save_reddit_json(self, profiles: list[OasisAgentProfile], file_path: str) -> None:
        data = []
        for profile in profiles:
            item = {
                "user_id": profile.user_id,
                "username": profile.user_name,
                "name": profile.name,
                "bio": (profile.bio or profile.name)[:150],
                "persona": profile.persona,
                "karma": profile.karma,
                "created_at": profile.created_at,
                "age": profile.age or 30,
                "gender": _gender(profile.gender),
                "mbti": profile.mbti or "ISTJ",
                "country": profile.country or "Unknown",
                "profession": profile.profession or "Unknown",
                "interested_topics": profile.interested_topics,
            }
            data.append(item)
        with open(file_path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)

    def save_profiles_to_json(
        self, profiles: list[OasisAgentProfile], file_path: str, platform: str = "reddit"
    ) -> None:
        self.save_profiles(profiles, file_path, platform)


def _username(identity: str, index: int) -> str:
    value = re.sub(r"[^a-z0-9_]", "_", identity.lower()).strip("_")
    return value or f"agent_{index}"


def _optional_int(value: Any) -> int | None:
    try:
        return int(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


def _gender(value: str | None) -> str:
    normalized = (value or "other").strip().lower()
    return normalized if normalized in {"male", "female", "other"} else "other"
