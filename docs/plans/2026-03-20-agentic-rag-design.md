# Agentic RAG Chatbot System Design

## Overview
A multi-tenant, admin-managed Agentic RAG platform built from scratch in Python to facilitate complex workflows like visualizations, action planning, and external tool usage.

## Architecture

### 1. Orchestration Layer (LangGraph + PostgresSaver)
We will use **LangGraph** as the core agent state machine, persisted via **PostgresSaver**.
- **State Persistence**: Uses PostgreSQL for checkpointing, enabling Human-in-the-Loop (HITL) and pause/resume. FastAPI will manage production connection pooling (`psycopg_pool`) via lifespan events.
- **State Management**: Every invocation uses a `thread_id` formatted as `tenant_id:user_id:session_id`. We will implement a background pruning job to delete checkpoints older than 24 hours, keeping the uncompressed state graph lightweight.
- A Supervisor Agent routes user queries to the appropriate sub-graphs (e.g., General Chat, RAG Retrieval, Graphing Tool).

### 2. Document Ingestion (MinerU + Qdrant)
- **MinerU** is an independent data extraction tool. It parses chaotic PDFs/images into clean Markdown. 
- Our ingestion script will call MinerU, text-split the Markdown, embed it using OpenAI/Cohere, and store the vectors with metadata in **Qdrant**.

### 3. Contextual Memory (mem0)
- **mem0** acts as the long-term semantic layer independent of LangGraph's short-term checkpoints.
- **Workflow Integration**: 
  1. *Retrieve*: Query mem0 based on user input.
  2. *Inject*: Add results to the system prompt.
  3. *Respond*: LLM generates the answer.
  4. *Persist*: The final user + assistant pair is given to mem0 to distill and compress into long-term facts.

### 4. Backend (FastAPI + LiteLLM)
- **FastAPI** handles the REST endpoints (Chat, Manage KBs, Users) asynchronously. 
- **LiteLLM** serves as the unified interface to call OpenAI, Gemini, Anthropic, or open-source models.
- **Tool Calling Segregation**: To avoid "schema confusion" in open-source models, we explicitly separate "Structured Output" nodes from "Tool Calling" nodes within the LangGraph conditional edges.
- **OAuth** (Microsoft & Google SSO) is enforced at the FastAPI middleware layer.

## Data Flow for a Query
1. UI sends query via HTTP to FastAPI `POST /chat`.
2. FastAPI validates OAuth token. Extracts `user_id`.
3. Query enters **LangGraph State Machine**:
   a. **Mem0 Node**: Injects user's past conversational memory.
   b. **Router Node**: Decides if retrieval is needed.
   c. **RAG Node** (if needed): Queries Qdrant for cited chunks.
   d. **Tool Node** (if needed): Calls external APIs or charts data.
   e. **Generator Node (LiteLLM)**: Crafts final response.
4. Response streamed back to UI via FastAPI, with citation metadata attached.

## Scalability and Future Extension
By keeping the components decentralized (LangGraph holding the logic, FastAPI holding the network, MinerU/Qdrant holding the data), adding a new "Knowledge Base Action Agent" is simply adding a new Node to the LangGraph state machine.
