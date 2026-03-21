import os
from fastapi import FastAPI
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
