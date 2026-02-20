from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes import (
    planner_node,
    research_node,
    retrieve_docs_node,
    synthesis_node
)

def get_deep_agent():
    builder = StateGraph(AgentState)

    builder.add_node("planner", planner_node)
    builder.add_node("research", research_node)
    builder.add_node("retrieve_docs", retrieve_docs_node)
    builder.add_node("synthesis", synthesis_node)

    builder.set_entry_point("planner")

    builder.add_edge("planner", "research")
    builder.add_edge("research", "retrieve_docs")
    builder.add_edge("retrieve_docs", "synthesis")
    builder.add_edge("synthesis", END)

    return builder.compile()