from typing import TypedDict, List

class AgentState(TypedDict):
    user_id: str
    query: str
    memory: List[str]
    response: str
    mode: str
    needs_code: bool
    research_queries: list
    docs: list