from duckduckgo_search import DDGS
from vector_store import add_documents


def search_web(query, num_results=10):

    docs = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=num_results):
            docs.append({"title": r["title"], "link": r["href"], "body": r["body"]})

    add_documents(docs)

    return docs
