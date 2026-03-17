from __future__ import annotations

from memory.vector_store import VectorStore


class RetrievalEngine:
    def __init__(self, vector_store: VectorStore) -> None:
        self.vector_store = vector_store

    def retrieve(self, query: str, limit: int = 5) -> dict:
        return self.vector_store.search_element(query=query, limit=limit)
