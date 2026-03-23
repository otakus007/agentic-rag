# Phase 18: Custom System Prompts

**Goal:** Eliminate hard-coded global prompts and enable true multi-agent character tailoring upon Chatbot creation.

## Tasks
1. Alter `chatbots` table to contain `system_prompt`.
2. Update the Admin Chatbot build UI/schema to capture and validate `system_prompt`.
3. Provide LLM adapters the new `system_prompt` overriding base template configuration per-invocation.
