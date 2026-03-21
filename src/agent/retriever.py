"""Qdrant retriever module.

Performs semantic search against per-agent_id Qdrant collections
to retrieve relevant document chunks for RAG context injection.
"""
from typing import List, Dict, Any
from src.ingestion.embedder import get_qdrant_client, get_embedding

TOP_K = 5  # Number of results to retrieve


def retrieve_context(query: str, agent_id: str, top_k: int = TOP_K) -> List[Dict[str, Any]]:
    """Search the kb_{agent_id} Qdrant collection for relevant document chunks.
    
    Returns a list of dicts with: content, block_type, page_number, score.
    Returns empty list if collection doesn't exist or search fails.
    """
    try:
        qdrant = get_qdrant_client()
        collection_name = f"kb_{agent_id}"
        
        # Check if collection exists
        collections = [c.name for c in qdrant.get_collections().collections]
        if collection_name not in collections:
            return []
        
        query_vector = get_embedding(query)
        
        results = qdrant.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
        )
        
        return [
            {
                "content": hit.payload.get("content", ""),
                "block_type": hit.payload.get("block_type", ""),
                "page_number": hit.payload.get("page_number", 0),
                "score": hit.score,
            }
            for hit in results
        ]
    except Exception as e:
        print(f"Qdrant retrieval error: {e}")
        return []
