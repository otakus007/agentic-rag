# Agentic RAG Chatbot System Design

## Overview
A multi-tenant, admin-managed Agentic RAG platform built from scratch in Python to facilitate complex workflows like visualizations, action planning, and external tool usage.

## Architecture

### 1. Orchestration Layer (LangGraph)
We will use **LangGraph** as the core agent state machine. 
- A Supervisor Agent routes user queries to the appropriate sub-graphs (e.g., General Chat, RAG Retrieval, Graphing Tool, Action Planner).
- It explicitly passes the `state` between nodes, ensuring reliability when agents loop or retry API calls.

### 2. Document Ingestion (MinerU + Qdrant)
- **MinerU** is an independent data extraction tool. It parses chaotic PDFs/images into clean Markdown. 
- Our ingestion script will call MinerU, text-split the Markdown, embed it using OpenAI/Cohere, and store the vectors with metadata in **Qdrant**.

### 3. Contextual Memory (mem0)
- Instead of just stuffing previous chat items into the prompt, **mem0** sits as a transparent layer over the LLM. 
- Each user session (and cross-session globally) passes through `mem0.add(user_id=X, content=Y)` to update their personal preferences and historical context.

### 4. Backend (FastAPI + LiteLLM)
- **FastAPI** handles the REST endpoints (Chat, Manage KBs, Users).
- **LiteLLM** serves as the unified interface to call OpenAI, Gemini, or Anthropic models transparently depending on the chatbot's configuration.
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
