import chromadb
import requests

from chunking import chunk_text

# replace with ollama to keep docker image size small
# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text):

    if not text or not text.strip():
        raise ValueError("Empty text cannot be embedded")

    response = requests.post(
        "http://host.docker.internal:11434/v1/embeddings",
        json={"model": "nomic-embed-text", "input": [text]},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    # # print("embed response:", data)

    embedding = data.get("data", [{}])[0].get("embedding")

    if embedding is None:
        raise ValueError("No embedding in response")

    # # If API returns nested list [[...]], unwrap one level
    # if (
    #     isinstance(embedding, list)
    #     and len(embedding) > 0
    #     and isinstance(embedding[0], list)
    # ):
    #     return embedding[0]
    return embedding


client = chromadb.PersistentClient(path="/app/chroma_db")
collection = client.get_or_create_collection(name="research_docs")


def add_documents(docs):
    valid_chunks = []
    embeddings = []
    metadatas = []
    ids = []

    for i, d in enumerate(docs):
        body = (d.get("body") or "").strip()
        if not body:
            continue
        
        link = d.get("link", "")
        if link:
            existing = collection.get(where={"link": link})
            if existing and existing["ids"]:
                continue
        chunks = chunk_text(body)
        for j, chunk in enumerate(chunks):
            emb = get_embedding(chunk)
            if not emb:
                continue
            valid_chunks.append(chunk)
            embeddings.append(emb)
            metadatas.append({"title": d.get("title", ""), "link": d.get("link", "")})
            ids.append(f"{i}_{j}")

    if not valid_chunks:
        return
    


    collection.add(
        documents=valid_chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )


def search_docs(query, k=5):

    query_embedding = get_embedding(query)

    results = collection.query(query_embeddings=[query_embedding], n_results=k)

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    combined = []

    for d, m in zip(docs, metas):
        combined.append({"body": d, "title": m["title"], "link": m["link"]})

    return combined
