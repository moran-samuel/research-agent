# AI Research Assistant (RAG + Local LLM)

A full-stack AI research assistant that performs web search, retrieves relevant context using a vector database, and generates answers using a local LLM.

## 🚀 Features

* Web search integration (DuckDuckGo)
* Retrieval-Augmented Generation (RAG)
* Document chunking + ranking
* Local LLM inference via Ollama
* FastAPI backend
* Streamlit frontend
* Dockerized full-stack deployment

## 🧠 Tech Stack

* FastAPI (backend API)
* Streamlit (frontend UI)
* Chroma (vector database)
* Ollama (local LLM + embeddings)
* Docker & Docker Compose

## 🏗️ Architecture

User Query
→ Web Search
→ Document Chunking
→ Embeddings (Ollama)
→ Vector DB (Chroma)
→ Retrieval + Ranking
→ LLM Answer

## ⚙️ Setup

### 1. Install Ollama

Install and run Ollama locally:
https://ollama.com

Pull required models:

```
ollama pull llama3.1
ollama pull nomic-embed-text
```

### 2. Run with Docker

```
docker compose up --build
```

### 3. Open App

Frontend:
http://localhost:8501

Backend:
http://localhost:8000/docs

## 📌 Future Improvements

* Semantic reranking
* Persistent vector database
* Streaming responses
* Multi-agent workflows

## 💡 Notes

* Ollama must be running locally (not inside Docker)
* Uses `host.docker.internal` to connect containers to host LLM
