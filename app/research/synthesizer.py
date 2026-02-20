from app.utils.gemini_llm import generate

def synthesize_answer(query, docs):

    context = "\n".join(docs)

    prompt = f"""
    Use ONLY this context:
    {context}

    Answer this:
    {query}
    """

    return generate(prompt)