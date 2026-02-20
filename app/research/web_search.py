from tavily import TavilyClient
from app.config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)

def web_search(query):

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=3
    )

    docs = []

    for r in response["results"]:
        if r.get("content"):
            docs.append(r["content"])
    
    return docs