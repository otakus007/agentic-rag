import os
from mem0 import Memory

def get_mem0_client() -> Memory:
    config = {
        "vector_store": {
            "provider": "pgvector",
            "config": {
                "connection_string": os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/agentic_rag")
            }
        }
    }
    return Memory.from_config(config)
