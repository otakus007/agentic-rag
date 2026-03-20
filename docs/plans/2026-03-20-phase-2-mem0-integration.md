# Phase 2: Mem0 Integration & User Memory - Implementation Plan

> **For Antigravity:** REQUIRED SUB-SKILL: Load `executing-plans` to implement this plan task-by-task.

**Goal:** Connect Mem0 for retrieving and storing cross-session semantic facts per `user_id` and `agent_id`, independent of LangGraph's short-term message checkpoints.

**Architecture:** Mem0 will be integrated using the explicit **Tool extraction** pattern. We will define a LangChain-compatible `Save_Memory` tool that the LLM can call to persist facts. Before evaluating user input, the graph will perform a semantic search against Mem0 and inject the results as a dynamic `SystemMessage`. Both systems (PostgresSaver and Mem0) will share the exact same physical Postgres connection URI.

**Tech Stack:** Python, LangGraph, LiteLLM, `mem0ai`

---

## Verification Plan
We will follow Test-Driven Development (TDD). 
For each task, `poetry run pytest` must be executed to ensure the graph safely compiles, authenticates with tools, and seamlessly integrates context without runtime exceptions.

### Task 1: Setup Mem0 Base Integration

**Files:**
- Modify: `pyproject.toml`
- Create: `src/agent/memory.py`
- Test: `tests/test_agent.py`

<acceptance_criteria>
- `mem0ai` is installed.
- `src/agent/memory.py` defines a utility class or function `get_mem0_client()` initialized with Postgres configurations targeting `DATABASE_URL`.
</acceptance_criteria>

<action>
Execute `poetry add "mem0ai[postgres]"`. In `src/agent/memory.py`, instantiate the `Memory` class from `mem0` using the PostgreSQL vector config block. 
</action>

**Step 1: Write the failing test**
```python
# tests/test_agent.py (append)
from src.agent.memory import get_mem0_client

def test_mem0_initialization():
    client = get_mem0_client()
    assert client is not None
```

**Step 2: Run test to verify it fails**
Expected: FAIL "No module named src.agent.memory"

**Step 3: Write minimal implementation**
```python
# src/agent/memory.py
import os
from mem0 import Memory

def get_mem0_client() -> Memory:
    config = {
        "vector_store": {
            "provider": "pgvector",
            "config": {
                "uri": os.getenv("DATABASE_URL")
            }
        }
    }
    return Memory.from_config(config)
```

**Step 4: Run test to verify it passes**
Expected: PASS 

**Step 5: Commit**
`git add pyproject.toml poetry.lock src/agent/memory.py tests/test_agent.py -m "feat(02): add mem0ai initialization logic"`

---

### Task 2: Create LLM and SaveMemory Tool

**Files:**
- Create: `src/agent/tools.py`
- Modify: `src/agent/graph.py`

<acceptance_criteria>
- `Save_Memory` tool is properly defined with `user_id` and `agent_id` inputs.
- The state graph's `chatbot_node` invokes a real LiteLLM execution bound with the tool, replacing the hardcoded "Hello World".
</acceptance_criteria>

<action>
Create `src/agent/tools.py`. Define a `@tool` `save_memory` wrapping `get_mem0_client().add()`. In `src/agent/graph.py`, initialize a LiteLLM/LangChain chat model (e.g., via `ChatOpenAI` pointing to `gpt-4o-mini`), bind the `save_memory` tool using `.bind_tools()`, and replace the chatbot_node logic to actually `invoke` the model. Also, update `AgentState` to include `user_id` and `agent_id` tracking fields.
</action>

**Step 1: Write the failing test**
Update `test_graph_invocation` in `tests/test_agent.py` to assert the model returns an AIMessage rather than a raw dict.

**Step 2: Run test to verify it fails**
Expected: FAIL 

**Step 3: Write minimal implementation**
Update `graph.py` to use LangChain's `tool_node` pattern (or manual tool evaluation). Since Phase 2 just needs the tool available to the LLM, bind it to the model.

**Step 4: Run test to verify it passes**
Expected: PASS

**Step 5: Commit**
`git add src/agent/ tests/test_agent.py -m "feat(02): integrate save_memory tool and actual llm bindings"`

---

### Task 3: Inject SystemContext from Mem0 History

**Files:**
- Modify: `src/agent/graph.py`

<acceptance_criteria>
- Before sending `state["messages"]` to the LLM, perform `get_mem0_client().search(...)` on the latest user message.
- Dynamically format the findings into a `SystemMessage` representing long-term memory.
</acceptance_criteria>

<action>
In `chatbot_node`, extract the last HumanMessage. Run `mem0.search(query)`. Combine the results into a string, create a `SystemMessage(content=...)`, prepend it to the raw `state["messages"]`, and execute the `llm.invoke()`. Return the LLM response.
</action>

**Step 1: Write the failing test**
Add a mock test confirming search is called.

**Step 2: Write minimal implementation**
As per action.

**Step 3: Run test to verify it passes**
Expected: PASS

**Step 4: Commit**
`git add src/agent/graph.py -m "feat(02): inject mem0 history as system prompt dynamically"`
