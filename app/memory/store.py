import uuid
from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY
from app.memory.qdrant_client import client, ensure_collection
from qdrant_client.models import PointStruct

gemini_client = genai.Client(api_key=GEMINI_API_KEY, vertexai=False)

def embed(text: str):
    response = gemini_client.models.embed_content(
        model = "gemini-embedding-001",
        contents = [
            types.Content(
                parts = [
                    types.Part.from_text(text=text)
                ]
            )
        ],
        config = types.EmbedContentConfig(
            task_type = "RETRIEVAL_DOCUMENT"
        )
    )
    return response.embeddings[0].values
    


def store_memory(user_id: str, text: str):
    ensure_collection()
    vector = embed(text)

    client.upsert(
        collection_name = "user_memory",
        points = [
            PointStruct(
                id = str(uuid.uuid4()),
                vector = vector,
                payload = {
                    "user_id": user_id,
                    "text": text
                }
            )
        ]
    )
