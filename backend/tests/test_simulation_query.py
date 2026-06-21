import json
import sqlite3

from app.config import Config
from app.services.simulation_query import SimulationQueryService


def test_sqlite_queries_and_statistics(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "OASIS_SIMULATION_DATA_DIR", str(tmp_path))
    sim = tmp_path / "sim_test"
    sim.mkdir()
    database = sim / "twitter_simulation.db"
    connection = sqlite3.connect(database)
    connection.execute("CREATE TABLE post (post_id INTEGER PRIMARY KEY, user_id INTEGER, content TEXT)")
    connection.execute("CREATE TABLE comment (comment_id INTEGER PRIMARY KEY, post_id INTEGER, content TEXT)")
    connection.execute("INSERT INTO post VALUES (1, 0, 'Pricing is unclear')")
    connection.execute("INSERT INTO comment VALUES (1, 1, 'I agree')")
    connection.commit()
    connection.close()
    (sim / "personas.json").write_text(json.dumps([{"identity": "Dana", "segment": "SMB"}]), encoding="utf-8")
    (sim / "reddit_profiles.json").write_text(json.dumps([{"user_id": 0, "name": "Dana"}]), encoding="utf-8")

    service = SimulationQueryService("sim_test")
    assert service.posts(query="Pricing")[0]["post_id"] == 1
    stats = service.statistics()
    assert stats["posts"] == 1
    assert stats["comments"] == 1
    assert stats["segments"] == ["SMB"]
