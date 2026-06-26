from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json
from pydantic import BaseModel
from chunking import rank_chunks
from search import search_web
from llm import ask_llm
from prompts import research_prompt
from vector_store import search_docs, add_documents

app = FastAPI()


class Query(BaseModel):
    question: str


@app.post("/research")
def research(query: Query):
    try:
        results = search_web(query.question)
        add_documents(results)


        context_docs = search_docs(query.question)
        top_chunks = rank_chunks(context_docs, query.question)

        system_message, user_message = research_prompt(query.question, top_chunks)

        def stream():
            # Send sources as first line so the frontend can parse them
            yield json.dumps({"sources": results}) + "\n"
            for token in ask_llm(system_message, user_message):
                yield token
 
        return StreamingResponse(stream(), media_type="text/plain")
    except Exception as e:
        return StreamingResponse(
            iter([json.dumps({"error": str(e)})]),
            media_type="text/plain"
        )
