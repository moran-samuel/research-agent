from fastapi import FastAPI
from pydantic import BaseModel
from chunking import rank_chunks
from search import search_web
from llm import ask_llm
from prompts import research_prompt
from vector_store import search_docs

app = FastAPI()


class Query(BaseModel):
    question: str


@app.post("/research")
def research(query: Query):
    try:
        results = search_web(query.question)

        context_docs = search_docs(query.question)

        top_chunks = rank_chunks(context_docs, query.question)

        prompt = research_prompt(query.question, top_chunks)

        answer = ask_llm(prompt)

        return {"question": query.question, "answer": answer, "sources": results}
    except Exception as e:
        return {"error": str(e)}
