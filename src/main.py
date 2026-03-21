import os
import tempfile
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from psycopg_pool import AsyncConnectionPool

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
        # Clean up the temp file
        if os.path.exists(file_path):
            os.remove(file_path)


@app.post("/ingest", status_code=202)
async def ingest(
    agent_id: str,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    """Accept a PDF upload and dispatch ingestion as a background task."""
    # Save uploaded file to a temp path
    suffix = os.path.splitext(file.filename or "upload.pdf")[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    background_tasks.add_task(run_ingestion_pipeline, tmp_path, agent_id)
    return {"status": "ingestion_started", "filename": file.filename}
