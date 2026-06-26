from rank_bm25 import BM25Okapi

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
def rank_chunks(chunks, query, top_k=3):

    if not chunks:
        return []
 
    # BM25 expects tokenized input — split each chunk and the query into word lists
    tokenized_chunks = [chunk["body"].lower().split() for chunk in chunks]
    tokenized_query = query.lower().split()
 
    bm25 = BM25Okapi(tokenized_chunks)
    scores = bm25.get_scores(tokenized_query)
 
    # Pair each chunk with its score, sort descending, return top_k
    ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in ranked[:top_k]]
