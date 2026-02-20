from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes import retrieve_memory, classify_query, answer_node, code_node


builder = StateGraph(AgentState)

builder.add_node("retrieve_memory", retrieve_memory)
builder.add_node("classify_query", classify_query)
builder.add_node("answer", answer_node)
builder.add_node("code", code_node)

builder.set_entry_point("retrieve_memory")

builder.add_edge("retrieve_memory", "classify_query")

builder.add_conditional_edges(
    "classify_query",
    lambda state: "code" if state["needs_code"] else "answer",
)

builder.add_edge("answer", END)

builder.add_edge("code", END)

agent = builder.compile()