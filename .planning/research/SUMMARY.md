# Ecosystem Research: Agentic RAG

## Key Findings

**Stack:**
- Orchestrator: LangGraph (Stateful multi-actor framework)
- Backend/API: FastAPI
- Vector Database: Qdrant
- Data Ingestion: MinerU (PDF parsing)
- Memory: mem0
- LLM Router: LiteLLM

**Table Stakes:**
- Precise retrieval with citations
- Multi-tenancy for bots/users
- Robust OAuth (Microsoft, Google)

**Watch Out For:**
- State Explosion: LangGraph states can become overwhelmingly complex if sub-graphs aren't modularized.
- Context Limits: mem0 stores long-term concepts, but we must carefully inject only relevant memories per query.
