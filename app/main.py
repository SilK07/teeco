from fastapi import FastAPI
from pydantic import BaseModel
from app.memory.store import ensure_collection
from contextlib import asynccontextmanager
from app.memory.retrieve import get_user_memory
from app.memory.store import store_memory
from app.agents.graph import agent
from app.agents.deep_graph import get_deep_agent
from app.memory.qdrant_client import client


class MemoryRequest(BaseModel):
    user_id: str
    query: str
    mode: str = "quick"

@asynccontextmanager
async def startup(app: FastAPI):
    ensure_collection()
    yield

app = FastAPI(lifespan = startup)

@app.post("/query")
def query(req: MemoryRequest):
    
    if req.mode == "deep":
        deep_agent = get_deep_agent()
        
        result = deep_agent.invoke({
            "user_id": req.user_id,
            "query": req.query,
            "mode": req.mode,
        })
    else:
        result = agent.invoke({
            "user_id": req.user_id,
            "query": req.query,
            "mode": req.mode,
        })

    if result.get("store"):
        store_memory(req.user_id, req.query)

    return {
        "answer": result["response"],
        "memory_used": result.get("memory", []),
        "docs_used": result.get("docs", []),
    }