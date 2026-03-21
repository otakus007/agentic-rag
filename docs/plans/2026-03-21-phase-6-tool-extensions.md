# Phase 6: Custom Tool/Visualizer Extensions - Implementation Plan

> **For Antigravity:** REQUIRED SUB-SKILL: Load `executing-plans` to implement this plan task-by-task.

**Goal:** Introduce Tool Nodes safely isolated via conditional edges for executing action plans or generating UI graphs.

**Architecture:** A new `src/agent/tool_registry.py` module stores per-`agent_id` tool configurations. The graph builder is refactored to compile dynamically with the appropriate tool set. A sample `visualize` tool returns structured JSON with a `type` field for frontend rendering.

---

## Verification Plan
TDD approach. `PYTHONPATH=$PWD poetry run pytest -v` must pass after each task.

### Task 1: Tool Registry Module

**Files:**
- Create: `src/agent/tool_registry.py`
- Test: `tests/test_tool_registry.py`

<acceptance_criteria>
- `get_tools_for_agent(agent_id: str) -> list` returns the tool functions registered for a given agent.
- Default agent gets `[save_memory]` (backward compatible).
- Registry supports adding custom tools per agent_id.
- Unknown agent_id returns the default tool set.
</acceptance_criteria>

**Step 1: Write the failing test**
```python
# tests/test_tool_registry.py
from src.agent.tool_registry import get_tools_for_agent, register_tool

def test_default_agent_gets_save_memory():
    tools = get_tools_for_agent("any_agent")
    tool_names = [t.name for t in tools]
    assert "save_memory" in tool_names

def test_register_custom_tool():
    from langchain_core.tools import tool
    @tool
    def my_tool(x: str) -> str:
        """A custom tool."""
        return x
    register_tool("custom_agent", my_tool)
    tools = get_tools_for_agent("custom_agent")
    tool_names = [t.name for t in tools]
    assert "my_tool" in tool_names
    assert "save_memory" in tool_names
```

**Step 2: Write minimal implementation**

**Step 3: Commit**
`git commit -m "feat(06): add tool registry module"`

---

### Task 2: Dynamic Graph Compilation with Per-Agent Tools

**Files:**
- Modify: `src/agent/graph.py`
- Test: `tests/test_agent.py`

<acceptance_criteria>
- `get_compiled_graph(agent_id, checkpointer)` compiles the graph with tools specific to the `agent_id`.
- LLM is bound with the correct tools from the registry.
- `ToolNode` is created with the correct tools.
- Tool execution errors are caught and returned as messages (not crashes).
</acceptance_criteria>

**Step 1: Write the failing test**
```python
@patch("src.agent.graph.get_tools_for_agent")
def test_dynamic_graph_uses_agent_tools(mock_registry):
    mock_registry.return_value = [save_memory]
    graph = get_compiled_graph(agent_id="test_agent")
    assert graph is not None
    mock_registry.assert_called_with("test_agent")
```

**Step 2: Write minimal implementation**

**Step 3: Commit**
`git commit -m "feat(06): dynamic graph compilation with per-agent tools"`

---

### Task 3: Visualizer Tool with Structured JSON Output

**Files:**
- Create: `src/agent/builtin_tools.py`
- Test: `tests/test_tool_registry.py`

<acceptance_criteria>
- `visualize(data: str, viz_type: str) -> str` returns JSON with `{"type": str, "data": ...}`.
- Supported viz_types: `chart`, `table`, `mermaid`.
- Invalid viz_type returns an error message (not exception).
- Tool is registered as a built-in available to all agents.
</acceptance_criteria>

**Step 1: Write the failing test**
```python
from src.agent.builtin_tools import visualize
import json

def test_visualize_returns_structured_json():
    result = visualize.invoke({"data": "Sales: 100, 200, 300", "viz_type": "chart"})
    parsed = json.loads(result)
    assert parsed["type"] == "chart"
    assert "data" in parsed

def test_visualize_invalid_type():
    result = visualize.invoke({"data": "test", "viz_type": "invalid"})
    assert "error" in result.lower() or "unsupported" in result.lower()
```

**Step 2: Write minimal implementation**

**Step 3: Commit**
`git commit -m "feat(06): add visualizer tool with structured JSON output"`
