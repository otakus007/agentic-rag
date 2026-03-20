# Agentic RAG Platform

## What This Is

An admin-managed Agentic RAG chatbot platform aimed at providing high-precision Q&A with source citations. Built from scratch as a foundational learning project, the system will support multiple LLMs, multiple authentication methods (Google, Microsoft), and sophisticated cross-session memory, with an architecture designed to extend into visual report generation and external API triggering.

## Core Value

A highly extensible, from-scratch Agentic RAG pipeline that delivers precise, cited answers while retaining conversational context across sessions.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Admin dashboard to manage users, chatbots, associated knowledge bases, and LLM models per bot.
- [ ] End-user interface for chatting with assigned bots.
- [ ] OAuth integration (Google, Microsoft Personal, Microsoft Work/School).
- [ ] Multi-LLM routing (OpenAI, Gemini, Anthropic) via a unified interface.
- [ ] Document ingestion pipeline supporting high-precision parsing (e.g., MinerU for PDFs) and vector storage.
- [ ] Cross-session user memory management using `mem0`.
- [ ] Extensible agent framework capable of routing to tools for graphing, action plans, or external APIs.

### Out of Scope

- [ ] SaaS Billing / Subscription management — Purely admin-managed internally.
- [ ] End-user knowledge base creation — Only admins assign KBs to chatbots.

## Context

- The project serves as a step-by-step learning journey to master Agentic RAG.
- Inspired by repositories like `autogen`, `mem0`, `MinerU`, `RAG-Anything`.
- Avoids monolithic wrappers (like Dify) to gain deep control over the agent loop for future additions like generating plotted charts or calling external action APIs.

## Constraints

- **Tech Stack**: Python-centric backend to leverage top-tier AI and RAG libraries (LangGraph, LlamaIndex, mem0).
- **Authentication**: Must robustly handle Microsoft's complex OAuth options (Personal vs. Work/School) alongside Google.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Build from scratch | User wants to learn the process step-by-step and have fine-grained control for complex workflows. | — Pending |

---
*Last updated: 2026-03-20 after initialization*
