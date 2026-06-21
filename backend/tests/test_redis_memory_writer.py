from app.services.redis_memory import RedisMemoryClient
from app.services.redis_memory_writer import RedisMemoryWriter


class FakeMemoryClient:
    enabled = True

    def __init__(self):
        self.records = []

    def write_batch(self, records):
        self.records.extend(records)
        return len(records)


def test_namespace_contract():
    assert RedisMemoryClient.user_id("abc", 7) == "sim:abc:agent:7"
    assert RedisMemoryClient.session_id("abc", "twitter", 7) == "sim:abc:twitter:agent:7"


def test_action_mapping_is_idempotent():
    client = FakeMemoryClient()
    writer = RedisMemoryWriter("abc", client=client)
    action = {
        "round": 2,
        "timestamp": "2026-01-01T00:00:00+00:00",
        "agent_id": 7,
        "agent_name": "Dana",
        "action_type": "CREATE_POST",
        "action_args": {"content": "Pricing should be visible."},
    }
    writer.add_activity_from_dict(action, "twitter")
    first = writer.queue.get_nowait()
    writer.add_activity_from_dict(action, "twitter")
    second = writer.queue.get_nowait()
    assert first["id"] == second["id"]
    assert first["metadata"]["round"] == 2
    assert "Pricing should be visible" in first["text"]
