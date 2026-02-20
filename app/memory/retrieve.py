from app.memory.store import embed
from app.memory.qdrant_client import client

def get_user_memory(user_id: str, query: str, limit: int = 5):

    vector = embed(query)

    results = client.query_points(
        collection_name = "user_memory",
        query = vector,
        with_payload = True,
        limit = limit,
    )

    memories = []
    for r in results.points:
        payload = r.payload
        if payload and payload.get("user_id") == user_id:
            memories.append(payload.get("text", ""))

    return memories