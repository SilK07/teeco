from app.memory.retrieve import get_user_memory
from app.utils.gemini_llm import generate
from app.research.planner import generate_search_queries
from app.research.retriever import retrieve_research
from app.research.synthesizer import synthesize_answer
from app.research.retriever import store_research_doc
from app.research.web_search import web_search

def retrieve_memory(state):
    memories = get_user_memory(state["user_id"], state["query"])
    state["memory"] = memories
    return state


def classify_query(state):
    query = state["query"].lower()
    
    code_keywords = [
        "write code",
        "show code",
        "implement",
        "generate code",
        "build",
        "create api",
        "example code",
        "code snippet",
        "script"
    ]
    state["needs_code"] = any(k in query for k in code_keywords)
    return state


def answer_node(state):

    memory_context = "\n".join(state["memory"])

    prompt  = f"""
       You are a senior research engineer.
       User preference : {memory_context}
       Answer this query: {state['query']}
    """

    state["response"] = generate(prompt)
    return state

def code_node(state):

    memory_context = "\n".join(state["memory"])

    prompt = f"""
        You are a senior software engineer. 
        User preference: {memory_context}
        Generate clean production-ready code for: {state['query']}
    """

    state["response"] = generate(prompt)
    return state

def memory_filter(state):

    query = state["query"].lower()

    if "prefer" in query or "i like" in query:
        state["store"] = True
    else:
        state["store"] = False

    return state

def planner_node(state):

    queries = generate_search_queries(state["query"])
    state["research_queries"] = queries

    return state

def research_node(state):

    all_docs = []
    for q in state["research_queries"]:
        
        results = web_search(q)

        for doc in results:
            store_research_doc(doc)
            all_docs.append(doc)
    
    state["fetched_docs"] = all_docs
    return state

def retrieve_docs_node(state):

    docs = retrieve_research(state["query"])
    state["docs"] = docs

    return state

def synthesis_node(state):

    answer = synthesize_answer(
        state["query"],
        state["docs"]
    )

    state["response"] = answer
    return state