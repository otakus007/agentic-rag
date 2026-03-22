# Agentic RAG Platform

## What This Is

An admin-managed Agentic RAG chatbot platform aimed at providing high-precision Q&A with source citations. Built from scratch as a foundational learning project, the system supports multiple authentication methods (Google, Microsoft), cross-session memory, and an extensible tool architecture designed for visual report generation and external API triggering.

## Current State

**Shipped: v1.1** (2026-03-22) — Full-stack platform with Vue 3 frontend, admin dashboard, and chatbot builder.

**Active: v1.2** — Production Polish (streaming, multi-LLM, RBAC, doc CRUD)

### Key Accomplishments (v1.1)
- Vue 3 + Vite + Tailwind v4 frontend with UUPM Dark OLED design system
- User chat interface with citation markers, sources panel, and conversation sidebar
- Admin KB management dashboard with drag-and-drop PDF upload
- Admin chatbot builder with Postgres CRUD and inline test chat
- 80 total tests (46 backend + 34 frontend), 44KB gzipped production bundle

### Next Milestone Goals (v1.2)
- SSE streaming chat with progressive text rendering
- Multi-provider LLM routing (OpenAI, Gemini, Anthropic)
- User management with role-based access control
- Ingestion progress tracking + document-level CRUD
- Dark/light mode toggle, API versioning

## Core Value

A highly extensible, from-scratch Agentic RAG pipeline that delivers precise, cited answers while retaining conversational context across sessions.

## Requirements

### Validated (v1.0)
- [x] OAuth integration (Google, Microsoft) via JWT Bearer tokens
- [x] Document ingestion pipeline (MinerU PDF → Qdrant)
- [x] Cross-session user memory management using Mem0
- [x] Extensible agent framework with per-agent tool registry
- [x] Full RAG flow with inline citations

### Validated (v1.1)
- [x] End-user chat interface with citations and dark mode
- [x] Admin dashboard to manage knowledge bases (upload, view, delete)
- [x] Admin chatbot builder (create, assign KB, select LLM, test)
- [x] Vue 3 + Vite + Tailwind frontend scaffold with UUPM design system
- [x] API client with JWT token management

### Future (v1.2+)
- [ ] Multi-LLM routing (OpenAI, Gemini, Anthropic) via unified interface
- [ ] User management / role-based access control
- [ ] Real-time WebSocket streaming
- [ ] Dark/light mode toggle
- [ ] Dynamic LLM model discovery

### Out of Scope
- SaaS Billing / Subscription management — Admin-managed internally
- End-user knowledge base creation — Only admins assign KBs to chatbots

## Context

- The project serves as a step-by-step learning journey to master Agentic RAG.
- Inspired by repositories like `autogen`, `mem0`, `MinerU`, `RAG-Anything`.
- Avoids monolithic wrappers (like Dify) to gain deep control over the agent loop.

## Constraints

- **Backend**: Python-centric (LangGraph, mem0, Qdrant, FastAPI)
- **Frontend**: Vue 3 + Vite + Tailwind CSS (lightest practical runtime)
- **Design**: UUPM (ui-ux-pro-max-skill) for design system generation
- **Auth**: Must handle Microsoft's complex OAuth (Personal vs. Work/School) + Google

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Build from scratch | Learn step-by-step, fine-grained control | ✅ v1.0 shipped |
| Vue 3 frontend | Balance of DX, ecosystem, and bundle size | ✅ v1.1 shipped |
| UUPM design system | AI-generated design intelligence for professional UI | ✅ v1.1 shipped |
| Postgres for chatbot config | Reuse existing pool, simple SQL | ✅ v1.1 shipped |

<details>
<summary>Previous milestones</summary>

### v1.0 — Backend Platform (2026-03-21)
6 phases, 41 tests, 1,190 LOC. Core scaffold, Mem0, document ingestion, RAG flow, OAuth, tool extensions.

### v1.1 — Frontend UI (2026-03-22)
4 phases (7-10), 80 tests, 2,570 LOC. Vue 3 scaffold, chat interface, admin KB dashboard, chatbot builder.
</details>

---
*Last updated: 2026-03-22 — v1.1 milestone completed*
