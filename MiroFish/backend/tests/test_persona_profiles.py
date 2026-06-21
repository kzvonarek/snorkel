import csv
import json

from app.services.oasis_profile_generator import OasisProfileGenerator
from app.services.persona import PersonaInput


def test_persona_converts_to_oasis_profiles(tmp_path):
    persona = PersonaInput.from_dict({
        "identity": "Dana",
        "segment": "SMB",
        "user_char": "Price-sensitive owner who wants transparent pricing.",
        "description": "Runs a small design studio.",
        "demographics": {"age": 38, "country": "US"},
        "evidence_references": ["ticket:42"],
        "confidence": "high",
        "traits": ["price-sensitive"],
    })
    generator = OasisProfileGenerator()
    profile = generator.generate_profiles_from_personas([persona])[0]
    assert profile.persona == persona.user_char
    assert profile.source_entity_type == "SMB"
    assert profile.evidence_references == ["ticket:42"]

    twitter = tmp_path / "twitter.csv"
    reddit = tmp_path / "reddit.json"
    generator.save_profiles([profile], str(twitter), "twitter")
    generator.save_profiles([profile], str(reddit), "reddit")

    with twitter.open(encoding="utf-8") as handle:
        row = next(csv.DictReader(handle))
    assert "Price-sensitive" in row["user_char"]
    assert json.loads(reddit.read_text(encoding="utf-8"))[0]["user_id"] == 0
