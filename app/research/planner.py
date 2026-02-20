from app.utils.gemini_llm import generate


def generate_search_queries(query):

    prompt = """
    You are a research planner.

    Generate 3 search queries for:
    {query}

    Return as a Python list:
    """

    response = generate(prompt)

    try:
        return eval(response)
    except:
        return [query]