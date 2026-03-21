"""Qdrant embedding and upsert logic.

Embeds text blocks using OpenAI's text-embedding-3-small model
and upserts them into per-agent_id Qdrant collections.
"""
import os
import uuid
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


def get_qdrant_client() -> QdrantClient:
    """Create a Qdrant client. Uses QDRANT_URL env var or defaults to localhost."""
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    return QdrantClient(url=url)


def get_embedding(text: str) -> List[float]:
    """Get embedding vector using OpenAI text-embedding-3-small via the openai client."""
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-mock-key"))
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


EMBEDDING_DIM = 1536  # text-embedding-3-small dimension


def embed_and_upsert(blocks: List[Dict[str, Any]], agent_id: str) -> int:
    """Embed text blocks and upsert into a Qdrant collection for the given agent.
    
    Collection name: kb_{agent_id}
    Returns the number of points upserted.
    """
    qdrant = get_qdrant_client()
    collection_name = f"kb_{agent_id}"
    
    # Ensure collection exists
    collections = [c.name for c in qdrant.get_collections().collections]
    if collection_name not in collections:
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )
    
    points = []
    for block in blocks:
        vector = get_embedding(block["content"])
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "content": block["content"],
                "block_type": block["block_type"],
                "page_number": block["page_number"],
                "agent_id": agent_id,
            },
        )
        points.append(point)
    
    if points:
        qdrant.upsert(collection_name=collection_name, points=points)
    
    return len(points)
