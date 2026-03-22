# Agentic RAG Platform

## What This Is

An admin-managed Agentic RAG chatbot platform aimed at providing high-precision Q&A with source citations. Built from scratch as a foundational learning project, the system supports multiple authentication methods (Google, Microsoft), cross-session memory, and an extensible tool architecture designed for visual report generation and external API triggering.

## Current State

**Shipped: v1.0** (2026-03-21) — Full backend platform with RAG pipeline, OAuth, and tool extensions.

**Active: v1.1** — Frontend UI (Vue 3 + Vite + Tailwind + UUPM design system)

## Core Value

A highly extensible, from-scratch Agentic RAG pipeline that delivers precise, cited answers while retaining conversational context across sessions.

## Requirements

### Validated (v1.0)

- [x] OAuth integration (Google, Microsoft) via JWT Bearer tokens
- [x] Document ingestion pipeline (MinerU PDF → Qdrant)
- [x] Cross-session user memory management using Mem0
- [x] Extensible agent framework with per-agent tool registry
- [x] Full RAG flow with inline citations

### Active (v1.1)

- [ ] End-user chat interface with streaming, citations, dark mode
- [ ] Admin dashboard to manage knowledge bases (upload, view, delete)
- [ ] Admin chatbot builder (create, assign KB, select LLM, test)

### Future (v1.2+)

- [ ] Multi-LLM routing (OpenAI, Gemini, Anthropic) via unified interface
- [ ] User management / role-based access control
- [ ] Real-time WebSocket streaming

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
| Vue 3 frontend | Balance of DX, ecosystem, and bundle size | v1.1 active |
| UUPM design system | AI-generated design intelligence for professional UI | v1.1 active |

---
*Last updated: 2026-03-22 — v1.1 milestone started*
