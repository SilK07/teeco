from app.memory.store import embed
from app.memory.qdrant_client import client
from app.research.chunker import chunk_text
from qdrant_client.models import PointStruct
import uuid


def store_research_doc(text):

    chunks = chunk_text(text)

    for chunk in chunks:

        vector = embed(chunk)

        client.upsert(
            collection_name="research_docs",
            points = [
                PointStruct(
                    id = str(uuid.uuid4()),
                    vector = vector,
                    payload = {
                        "text": chunk
                    }
                )
            ]
        )

def retrieve_research(query, limit=5):

    vector = embed(query)

    results = client.query_points(
        collection_name = "research_docs",
        query = vector,
        limit = limit
    )

    return [
        r.payload["text"]
        for r in results.points
    ]