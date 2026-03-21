import os
import tempfile
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Depends
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from psycopg_pool import AsyncConnectionPool
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from src.auth.dependencies import get_current_user

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/agentic_rag")
    pool = AsyncConnectionPool(conninfo=db_url, open=False)
    await pool.open()
    app.state.pool = pool
    yield {"pool": pool}
    await pool.close()

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}


def run_ingestion_pipeline(file_path: str, agent_id: str):
    """Background task: parse PDF and upsert embeddings into Qdrant."""
    from src.ingestion.parser import parse_pdf
    from src.ingestion.embedder import embed_and_upsert
    
    try:
        blocks = parse_pdf(file_path)
        embed_and_upsert(blocks, agent_id=agent_id)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@app.post("/ingest", status_code=202)
async def ingest(
    agent_id: str,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
):
    """Accept a PDF upload and dispatch ingestion as a background task. Requires auth."""
    suffix = os.path.splitext(file.filename or "upload.pdf")[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode="wb") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    background_tasks.add_task(run_ingestion_pipeline, tmp_path, agent_id)
    return {"status": "ingestion_started", "filename": file.filename}


class ChatRequest(BaseModel):
    message: str
    agent_id: str


class Source(BaseModel):
    content: str
    page_number: int
    block_type: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, user: dict = Depends(get_current_user)):
    """Send a message and get an AI response with citations. Requires auth."""
    from src.agent.graph import app_graph
    
    result = app_graph.invoke({
        "messages": [{"role": "user", "content": request.message}],
        "user_id": user["user_id"],  # From JWT token
        "agent_id": request.agent_id,
    })
    
    last_msg = result["messages"][-1]
    answer = last_msg.content if hasattr(last_msg, "content") else str(last_msg)
    
    raw_sources = result.get("sources", [])
    sources = [
        Source(
            content=s.get("content", ""),
            page_number=s.get("page_number", 0),
            block_type=s.get("block_type", ""),
        )
        for s in raw_sources
    ]
    
    return ChatResponse(answer=answer, sources=sources)
