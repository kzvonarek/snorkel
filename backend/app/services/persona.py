"""Typed persona inputs used to build OASIS agent profiles."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


@dataclass
class PersonaInput:
    identity: str
    segment: str
    user_char: str
    description: str
    demographics: dict[str, Any] = field(default_factory=dict)
    evidence_references: list[str] = field(default_factory=list)
    confidence: str = "medium"
    username: str | None = None
    traits: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PersonaInput":
        identity = str(data.get("identity") or data.get("name") or "").strip()
        if not identity:
            raise ValueError("persona identity is required")
        segment = str(data.get("segment") or "Unsegmented").strip()
        user_char = str(data.get("user_char") or data.get("persona") or "").strip()
        description = str(data.get("description") or data.get("bio") or identity).strip()
        if not user_char:
            raise ValueError(f"persona user_char is required: {identity}")
        return cls(
            identity=identity,
            segment=segment,
            user_char=user_char,
            description=description,
            demographics=dict(data.get("demographics") or {}),
            evidence_references=list(data.get("evidence_references") or []),
            confidence=str(data.get("confidence") or "medium").lower(),
            username=data.get("username"),
            traits=list(data.get("traits") or []),
        )

    @property
    def uuid(self) -> str:
        return self.identity

    @property
    def name(self) -> str:
        return self.identity

    @property
    def summary(self) -> str:
        return self.description

    @property
    def attributes(self) -> dict[str, Any]:
        return {
            **self.demographics,
            "segment": self.segment,
            "confidence": self.confidence,
            "traits": self.traits,
            "evidence_references": self.evidence_references,
        }

    def get_entity_type(self) -> str:
        """Compatibility for the existing simulation-config heuristics."""
        return self.segment

    def to_dict(self) -> dict[str, Any]:
        return {
            "identity": self.identity,
            "segment": self.segment,
            "user_char": self.user_char,
            "description": self.description,
            "demographics": self.demographics,
            "evidence_references": self.evidence_references,
            "confidence": self.confidence,
            "username": self.username,
            "traits": self.traits,
        }


def load_personas_json(path: str | Path) -> list[PersonaInput]:
    with Path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, dict):
        payload = payload.get("personas", [])
    if not isinstance(payload, list):
        raise ValueError("persona JSON must be a list or contain a personas list")
    return [PersonaInput.from_dict(item) for item in payload]


def load_personas_csv(path: str | Path) -> list[PersonaInput]:
    personas: list[PersonaInput] = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            demographics = {
                key: row[key]
                for key in ("age", "gender", "country", "profession", "mbti")
                if row.get(key)
            }
            data: dict[str, Any] = dict(row)
            data["demographics"] = demographics
            data["traits"] = _split_values(row.get("traits"))
            data["evidence_references"] = _split_values(row.get("evidence_references"))
            personas.append(PersonaInput.from_dict(data))
    return personas


def dump_personas(personas: Iterable[PersonaInput], path: str | Path) -> None:
    with Path(path).open("w", encoding="utf-8") as handle:
        json.dump([p.to_dict() for p in personas], handle, ensure_ascii=False, indent=2)


def _split_values(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split("|") if item.strip()]
