# Project Roadmap: Agentic RAG Platform

## Phase 1: Core Scaffold & LangGraph Hello World
**Goal:** Setup Poetry, FastAPI, basic LiteLLM integration, and a "Hello World" LangGraph state machine with memory persistence (PostgresSaver).
**Status:** Pending

## Phase 2: Mem0 Integration & User Memory
**Goal:** Connect Mem0 for retrieving and storing cross-session semantic facts per `user_id`, independent of the short-term checkpoint logic.
**Status:** Pending

## Phase 3: Document Ingestion Pipeline
**Goal:** Integrate MinerU for parsing PDFs and saving embeddings into Qdrant vector database.
**Status:** Pending

## Phase 4: Full Multi-Tenant RAG Flow
**Goal:** Connect LangGraph to query Qdrant based on Mem0 injected history. Output proper citations.
**Status:** Pending

## Phase 5: OAuth & API Gateways
**Goal:** Add Microsoft/Google SSO middleware to FastAPI. Associate `user_id` tokens with API requests to enforce multi-tenancy.
**Status:** Pending

## Phase 6: Custom Tool/Visualizer Extensions (Open Source schema separation)
**Goal:** Introduce `Tool Nodes` safely isolated via conditional edges for executing action plans or generating UI graphs.
**Status:** Pending
