from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from app.config import QDRANT_KEY, QDRANT_URL

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_KEY,
    timeout=60
)

def ensure_collection():
    collections = [
        ("user_memory", 3072),
        ("research_docs", 3072)
    ]

    for name, size in collections:
        if name not in [c.name for c in client.get_collections().collections]:
            client.create_collection(
                collection_name = name,
                vectors_config = VectorParams(
                    size = size,
                    distance = Distance.COSINE
                )
            )   