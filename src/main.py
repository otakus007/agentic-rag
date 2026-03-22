import os
import uuid
import tempfile
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from psycopg_pool import AsyncConnectionPool
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import asyncio
from src.auth.dependencies import get_current_user

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/agentic_rag")
    pool = AsyncConnectionPool(conninfo=db_url, open=False)
    await pool.open()
    # Create tables if not exists
    async with pool.connection() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS chatbots (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                agent_id TEXT UNIQUE NOT NULL,
                kb_id TEXT NOT NULL,
                model TEXT NOT NULL DEFAULT 'gpt-4o-mini',
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
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


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest, user: dict = Depends(get_current_user)):
    """SSE streaming chat endpoint. Yields token-by-token responses."""
    from src.agent.graph import app_graph

    async def event_generator():
        try:
            result = app_graph.invoke({
                "messages": [{"role": "user", "content": request.message}],
                "user_id": user["user_id"],
                "agent_id": request.agent_id,
            })

            last_msg = result["messages"][-1]
            answer = last_msg.content if hasattr(last_msg, "content") else str(last_msg)

            # Stream tokens (simulate chunked delivery)
            words = answer.split(" ")
            for i, word in enumerate(words):
                token = word if i == 0 else " " + word
                yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
                await asyncio.sleep(0.02)

            # Send sources
            raw_sources = result.get("sources", [])
            sources = [
                {"content": s.get("content", ""), "page_number": s.get("page_number", 0), "block_type": s.get("block_type", "")}
                for s in raw_sources
            ]
            yield f"data: {json.dumps({'type': 'sources', 'sources': sources})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# --- Admin: Knowledge Base Management ---

class KBInfo(BaseModel):
    name: str
    agent_id: str
    document_count: int


class KBDetail(KBInfo):
    vector_size: int


@app.get("/admin/kb", response_model=List[KBInfo])
def list_knowledge_bases(user: dict = Depends(get_current_user)):
    """List all knowledge base collections. Requires auth."""
    from src.ingestion.embedder import get_qdrant_client

    qdrant = get_qdrant_client()
    collections = qdrant.get_collections().collections
    result = []
    for c in collections:
        if c.name.startswith("kb_"):
            agent_id = c.name[3:]  # strip "kb_" prefix
            count = qdrant.count(collection_name=c.name).count
            result.append(KBInfo(name=c.name, agent_id=agent_id, document_count=count))
    return result


@app.get("/admin/kb/{agent_id}", response_model=KBDetail)
def get_knowledge_base(agent_id: str, user: dict = Depends(get_current_user)):
    """Get details of a specific knowledge base. Requires auth."""
    from src.ingestion.embedder import get_qdrant_client

    qdrant = get_qdrant_client()
    collection_name = f"kb_{agent_id}"

    collections = [c.name for c in qdrant.get_collections().collections]
    if collection_name not in collections:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Knowledge base '{agent_id}' not found")

    info = qdrant.get_collection(collection_name)
    count = qdrant.count(collection_name=collection_name).count
    vector_size = info.config.params.vectors.size if hasattr(info.config.params.vectors, 'size') else 0

    return KBDetail(
        name=collection_name,
        agent_id=agent_id,
        document_count=count,
        vector_size=vector_size,
    )


@app.delete("/admin/kb/{agent_id}")
def delete_knowledge_base(agent_id: str, user: dict = Depends(get_current_user)):
    """Delete a knowledge base collection. Requires auth."""
    from src.ingestion.embedder import get_qdrant_client

    qdrant = get_qdrant_client()
    collection_name = f"kb_{agent_id}"

    collections = [c.name for c in qdrant.get_collections().collections]
    if collection_name not in collections:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Knowledge base '{agent_id}' not found")

    qdrant.delete_collection(collection_name)
    return {"status": "deleted", "agent_id": agent_id}


# --- Admin: Chatbot Builder ---

def _get_all_model_names():
    """Flatten all provider models into a single list."""
    from src.llm.adapters import get_all_models
    all_models = get_all_models()
    return [m for models in all_models.values() for m in models]


class ChatbotCreate(BaseModel):
    name: str
    description: str = ""
    agent_id: str
    kb_id: str
    model: str = "gpt-4o-mini"


class ChatbotResponse(BaseModel):
    id: str
    name: str
    description: str
    agent_id: str
    kb_id: str
    model: str
    created_at: Optional[str] = None


@app.get("/admin/models")
def list_models(user: dict = Depends(get_current_user)):
    """List available LLM models grouped by provider."""
    from src.llm.adapters import get_all_models
    return {"models": get_all_models()}


@app.post("/admin/chatbots", response_model=ChatbotResponse, status_code=201)
async def create_chatbot(body: ChatbotCreate, request: Request, user: dict = Depends(get_current_user)):
    """Create a new chatbot configuration."""
    if body.model not in _get_all_model_names():
        raise HTTPException(status_code=400, detail=f"Model '{body.model}' not available")

    chatbot_id = str(uuid.uuid4())
    pool = request.state.pool
    async with pool.connection() as conn:
        await conn.execute(
            "INSERT INTO chatbots (id, name, description, agent_id, kb_id, model) VALUES (%s, %s, %s, %s, %s, %s)",
            (chatbot_id, body.name, body.description, body.agent_id, body.kb_id, body.model),
        )

    return ChatbotResponse(
        id=chatbot_id, name=body.name, description=body.description,
        agent_id=body.agent_id, kb_id=body.kb_id, model=body.model,
    )


@app.get("/admin/chatbots", response_model=List[ChatbotResponse])
async def list_chatbots(request: Request, user: dict = Depends(get_current_user)):
    """List all chatbot configurations."""
    pool = request.state.pool
    async with pool.connection() as conn:
        cur = await conn.execute("SELECT id, name, description, agent_id, kb_id, model, created_at FROM chatbots ORDER BY created_at DESC")
        rows = await cur.fetchall()

    return [
        ChatbotResponse(
            id=r[0], name=r[1], description=r[2], agent_id=r[3],
            kb_id=r[4], model=r[5], created_at=str(r[6]) if r[6] else None,
        )
        for r in rows
    ]


@app.get("/admin/chatbots/{chatbot_id}", response_model=ChatbotResponse)
async def get_chatbot(chatbot_id: str, request: Request, user: dict = Depends(get_current_user)):
    """Get a chatbot by ID."""
    pool = request.state.pool
    async with pool.connection() as conn:
        cur = await conn.execute("SELECT id, name, description, agent_id, kb_id, model, created_at FROM chatbots WHERE id = %s", (chatbot_id,))
        row = await cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Chatbot not found")

    return ChatbotResponse(
        id=row[0], name=row[1], description=row[2], agent_id=row[3],
        kb_id=row[4], model=row[5], created_at=str(row[6]) if row[6] else None,
    )


@app.put("/admin/chatbots/{chatbot_id}", response_model=ChatbotResponse)
async def update_chatbot(chatbot_id: str, body: ChatbotCreate, request: Request, user: dict = Depends(get_current_user)):
    """Update a chatbot configuration."""
    if body.model not in _get_all_model_names():
        raise HTTPException(status_code=400, detail=f"Model '{body.model}' not available")

    pool = request.state.pool
    async with pool.connection() as conn:
        cur = await conn.execute("SELECT id FROM chatbots WHERE id = %s", (chatbot_id,))
        if not await cur.fetchone():
            raise HTTPException(status_code=404, detail="Chatbot not found")

        await conn.execute(
            "UPDATE chatbots SET name=%s, description=%s, agent_id=%s, kb_id=%s, model=%s WHERE id=%s",
            (body.name, body.description, body.agent_id, body.kb_id, body.model, chatbot_id),
        )

    return ChatbotResponse(
        id=chatbot_id, name=body.name, description=body.description,
        agent_id=body.agent_id, kb_id=body.kb_id, model=body.model,
    )


@app.delete("/admin/chatbots/{chatbot_id}")
async def delete_chatbot(chatbot_id: str, request: Request, user: dict = Depends(get_current_user)):
    """Delete a chatbot."""
    pool = request.state.pool
    async with pool.connection() as conn:
        cur = await conn.execute("DELETE FROM chatbots WHERE id = %s RETURNING id", (chatbot_id,))
        if not await cur.fetchone():
            raise HTTPException(status_code=404, detail="Chatbot not found")

    return {"status": "deleted", "id": chatbot_id}


# --- Admin: User Management ---

class UserResponse(BaseModel):
    user_id: str
    email: str
    role: str
    created_at: Optional[str] = None


class UserRoleUpdate(BaseModel):
    role: str  # "admin" or "user"


@app.get("/admin/users", response_model=List[UserResponse])
async def list_users(request: Request, user: dict = Depends(get_current_user)):
    """List all users. Requires auth."""
    pool = request.state.pool
    async with pool.connection() as conn:
        cur = await conn.execute("SELECT user_id, email, role, created_at FROM users ORDER BY created_at DESC")
        rows = await cur.fetchall()
    return [
        UserResponse(user_id=r[0], email=r[1], role=r[2], created_at=str(r[3]) if r[3] else None)
        for r in rows
    ]


@app.put("/admin/users/{user_id}/role")
async def update_user_role(
    user_id: str, body: UserRoleUpdate, request: Request, user: dict = Depends(get_current_user)
):
    """Update a user's role. Requires auth."""
    if body.role not in ("admin", "user"):
        raise HTTPException(status_code=400, detail="Role must be 'admin' or 'user'")

    pool = request.state.pool
    async with pool.connection() as conn:
        cur = await conn.execute(
            "UPDATE users SET role = %s WHERE user_id = %s RETURNING user_id",
            (body.role, user_id),
        )
        if not await cur.fetchone():
            raise HTTPException(status_code=404, detail="User not found")

    return {"status": "updated", "user_id": user_id, "role": body.role}


# --- Admin: Document CRUD ---

class DocumentChunk(BaseModel):
    id: str
    content: str
    page_number: int
    block_type: str


@app.get("/admin/kb/{agent_id}/documents", response_model=List[DocumentChunk])
def list_documents(agent_id: str, limit: int = 50, offset: int = 0, user: dict = Depends(get_current_user)):
    """List document chunks in a knowledge base. Requires auth."""
    from src.ingestion.embedder import get_qdrant_client

    qdrant = get_qdrant_client()
    collection_name = f"kb_{agent_id}"

    results = qdrant.scroll(
        collection_name=collection_name,
        limit=limit,
        offset=offset,
        with_payload=True,
        with_vectors=False,
    )[0]

    return [
        DocumentChunk(
            id=str(point.id),
            content=point.payload.get("content", ""),
            page_number=point.payload.get("page_number", 0),
            block_type=point.payload.get("block_type", ""),
        )
        for point in results
    ]


@app.delete("/admin/kb/{agent_id}/documents/{doc_id}")
def delete_document(agent_id: str, doc_id: str, user: dict = Depends(get_current_user)):
    """Delete a specific document chunk from a knowledge base. Requires auth."""
    from src.ingestion.embedder import get_qdrant_client
    from qdrant_client.models import PointIdsList

    qdrant = get_qdrant_client()
    collection_name = f"kb_{agent_id}"

    qdrant.delete(
        collection_name=collection_name,
        points_selector=PointIdsList(points=[doc_id]),
    )

    return {"status": "deleted", "agent_id": agent_id, "doc_id": doc_id}


# --- API Info ---

@app.get("/api/version")
def api_version():
    """Return API version info."""
    return {"version": "1.2.0", "api_prefix": "/v1", "status": "production"}
