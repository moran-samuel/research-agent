def chunk_text(text, chunk_size=400, overlap=100):
    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# key word ranking function to boost relevance of chunks that contain more query words
def rank_chunks(chunks, query):

    scored = []

    query_words = set(query.lower().split())

    for chunk in chunks:
        text = chunk["body"].lower()
        score = sum(1 for w in query_words if w in text)

        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [c for _, c in scored[:3]]
