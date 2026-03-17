def research_prompt(question, docs):

    context = "\n\n".join([d.get("body", "") for d in docs if d.get("body")])

    return f"""
You are an AI research assistant.

Answer the user's question using the provided documents.

Documents:
{context}

Question:
{question}

Instructions:
- Provide a clear explanation
- Cite the documents when possible
- If information is missing, say so
- Do not invent facts
"""
