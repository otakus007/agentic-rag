# Phase 6: Custom Tool/Visualizer Extensions - Context

**Gathered:** 2026-03-21
**Status:** Ready for planning

<domain>
## Phase Boundary
Introduce Tool Nodes safely isolated via conditional edges for executing action plans or generating UI graphs.
</domain>

<decisions>
## Implementation Decisions

### Tool Registration Model
- Dynamic per-`agent_id` registration from a JSON tool registry.
- Each agent can have a different tool set defined in config/storage.
- Graph compiled with appropriate tools at request time.

### Tool Isolation & Safety
- Tools run in-process, wrapped in try/except with timeout enforcement.
- Tool node catches all exceptions, returns error messages instead of crashing.
- Full sandboxing (subprocess/container) deferred to a future hardening phase.

### Visualizer Output Format
- Return structured JSON with a `type` field (`chart`, `table`, `mermaid`) and data payload.
- Backend stays format-agnostic — frontend decides rendering.
</decisions>

<canonical_refs>
## Canonical References
- `src/agent/graph.py` — Current graph with `chatbot_node` → `tools_node` and `route_tools()`.
- `src/agent/tools.py` — Existing `save_memory` tool pattern to replicate.
- `src/agent/state.py` — AgentState with fields to extend for tool outputs.
</canonical_refs>

<code_context>
## Existing Code Insights
### Reusable Assets
- `src/agent/graph.py::route_tools` — Conditional routing pattern for tool calls.
- `src/agent/tools.py::save_memory` — `@tool` decorator pattern for new tools.
- `src/agent/graph.py::builder` — StateGraph builder where new tool nodes get registered.
### Integration Points
- LLM `.bind_tools()` call — needs to include dynamically registered tools.
- `ToolNode([...])` — needs to accept variable tool lists per agent.
</code_context>

<deferred>
## Deferred Ideas
- Full subprocess/container sandboxing for untrusted tool code.
- Tool marketplace / plugin store for community-contributed tools.
- Tool versioning and deprecation flow.
</deferred>

---
*Phase: 06-custom-tool-visualizer-extensions*
*Context gathered: 2026-03-21*
