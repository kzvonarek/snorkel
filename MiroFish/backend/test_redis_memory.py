import asyncio
import os
from app.services.zep_graph_memory_updater import update_agent_memory
from app.services.zep_entity_reader import read_entity_context
from app.services.graph_builder import build_initial_graph

async def run_test():
    test_agent = "agent_test_999"
    print(f"🚀 Starting memory validation for agent: {test_agent}\n")

    # 1. Test Chat/Episodic Memory (Redis List)
    print("Writing chat interactions to Redis...")
    await update_agent_memory(test_agent, "user", "Hello! Remember that my favorite color is deep blue.")
    await update_agent_memory(test_agent, "assistant", "Got it! I will remember that your favorite color is deep blue.")
    print("✅ Chat history written successfully.\n")

    # 2. Test Knowledge Graph Entities (Redis Hash)
    print("Writing knowledge graph nodes/edges to Redis...")
    mock_entities = [{"name": "deep blue", "type": "Color", "description": "The user's favorite color."}]
    mock_edges = [{"source": "user", "target": "deep blue", "relationship": "likes"}]
    await build_initial_graph(test_agent, mock_entities, mock_edges)
    print("✅ Graph entities written successfully.\n")

    # 3. Test Retrieval
    print("Attempting to read entity context back from Redis...")
    context = await read_entity_context(test_agent, "deep blue")
    print(f"\n📥 Retrieved Context from Redis:\n{context}\n")
    print("🎉 Verification Complete! Your MiroFish backend is safely talking to Redis.")

# Run the async test loop
if __name__ == "__main__":
    # Ensure environment variables match your setup
    os.environ["REDIS_HOST"] = "localhost"
    os.environ["REDIS_PORT"] = "6379"
    asyncio.run(run_test())