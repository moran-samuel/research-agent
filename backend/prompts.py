def research_prompt(question, docs):

    context = "\n\n".join([d.get("body", "") for d in docs if d.get("body")])

    system_message = f"""
You are an AI research assistant. The user is a Master's graduate in Data Analytics and Machine Learning. 

Answer the user's question using the provided documents.

Instructions:
- Provide a clear explanation
- Cite the documents when possible
- If information is missing, say so
- Do not invent facts"""
    
    user_message = f"""Documents:
{context}

Question:
{question}"""
    
    return system_message, user_message
