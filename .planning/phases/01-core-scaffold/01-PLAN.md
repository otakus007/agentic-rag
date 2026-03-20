# Phase 1: Core Scaffold & LangGraph Hello World Implementation Plan

> **For Antigravity:** REQUIRED SUB-SKILL: Load `executing-plans` to implement this plan task-by-task.

**Goal:** Setup Poetry, FastAPI, basic LiteLLM integration, and a "Hello World" LangGraph state machine with memory persistence (PostgresSaver).

**Architecture:** We will initialize a standard Python layout using Poetry. The FastAPI app will use an async lifespan context manager to initialize the `PostgresSaver` connection pool. The LangGraph will be incredibly simple: a single node that evaluates the user input to return a hardcoded response, setting the foundation for LLM insertion in Phase 2.

**Tech Stack:** Python 3.11+, Poetry, FastAPI, Uvicorn, LangGraph, langgraph-checkpoint-postgres, LiteLLM, Pytest.

## Verification Plan
Every task below incorporates explicit Test-Driven Development (TDD). The verification plan centers around executing `pytest test_XYZ.py -v` before and after implementations to guarantee that:
1. Environment and dependencies install correctly.
2. The FastAPI lifespan and health endpoints boot without errors.
3. The LangGraph state schema initializes and compiles successfully without cyclic dependencies.
The tests are isolated and explicitly outlined in the steps below.

---

### Task 1: Project Initialization and Dependencies

**Files:**
- Create: `pyproject.toml`
- Create: `.env.example`
- Create: `tests/conftest.py`

<read_first>
- `docs/plans/2026-03-20-agentic-rag-design.md`
</read_first>

<acceptance_criteria>
- `pyproject.toml` contains `fastapi`, `uvicorn`, `langgraph`, `langgraph-checkpoint-postgres`, `litellm`, `psycopg-pool`, `pytest`, `httpx`
- `poetry check` passes valid configuration
</acceptance_criteria>

<action>
Run `poetry init -n` and `poetry add fastapi uvicorn langgraph langgraph-checkpoint-postgres psycopg-pool litellm python-dotenv pydantic`. Add `pytest httpx pytest-asyncio` to dev dependencies. Create a basic `.env.example` with `DATABASE_URL` and `OPENAI_API_KEY`.
</action>

**Step 1: Write the failing test**
(No logic yet, just setup `tests/conftest.py`)
```python
# tests/conftest.py
import pytest

@pytest.fixture
def test_client():
    pass # placeholder for FastAPI test client
```

**Step 2: Write minimal implementation**
Run dependency commands as described in Action.

**Step 3: Run test to verify**
Run: `poetry run pytest`
Expected: "collected 0 items" (Success, no errors)

**Step 4: Commit**
```bash
git add pyproject.toml poetry.lock tests/ .env.example
git commit -m "chore: setup project dependencies"
```

### Task 2: FastAPI Scaffold & Postgres Lifespan

**Files:**
- Create: `src/main.py`
- Test: `tests/test_api.py`

<read_first>
- `pyproject.toml`
</read_first>

<acceptance_criteria>
- `src/main.py` contains FastAPI initialization with `@asynccontextmanager`
- `tests/test_api.py` contains `test_health_check` which exits 0
</acceptance_criteria>

<action>
In `src/main.py`, create a lifespan event with `asynccontextmanager` yielding to the FastAPI app, along with a `/health` endpoint that returns `{"status": "ok"}`. Create the pytest to hit `/health`.
</action>

**Step 1: Write the failing test**
```python
# tests/test_api.py
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

**Step 2: Run test to verify it fails**
Run: `poetry run pytest tests/test_api.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.main'"

**Step 3: Write minimal implementation**
```python
# src/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB pool here later (Phase 1 part 2)
    yield
    # Close pool here

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}
```

**Step 4: Run test to verify it passes**
Run: `poetry run pytest tests/test_api.py -v`
Expected: PASS

**Step 5: Commit**
```bash
git add src/main.py tests/test_api.py
git commit -m "feat: add fastapi scaffold and health endpoint"
```

### Task 3: Setup basic LangGraph Node

**Files:**
- Create: `src/agent/state.py`
- Create: `src/agent/graph.py`
- Test: `tests/test_agent.py`

<read_first>
- `src/main.py`
</read_first>

<acceptance_criteria>
- `src/agent/state.py` contains a `TypedDict` for the graph state with `messages`
- `src/agent/graph.py` contains a `StateGraph` compilation
- `tests/test_agent.py` asserts the graph compiles without runtime errors
</acceptance_criteria>

<action>
Define `AgentState` in `state.py`. Create a single node graph in `graph.py` that parses the state messages and yields a fake LLM response. Connect `START` edge to node, and node to `END`.
</action>

**Step 1: Write the failing test**
```python
# tests/test_agent.py
from src.agent.graph import app_graph

def test_graph_initialization():
    assert app_graph is not None
```

**Step 2: Run test to verify it fails**
Run: `poetry run pytest tests/test_agent.py -v`
Expected: FAIL "No module named src.agent.graph"

**Step 3: Write minimal implementation**
```python
# src/agent/state.py
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

# src/agent/graph.py
from langgraph.graph import StateGraph, START, END
from .state import AgentState

def chatbot_node(state: AgentState):
    return {"messages": [{"role": "assistant", "content": "Hello World"}]}

builder = StateGraph(AgentState)
builder.add_node("chatbot", chatbot_node)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

app_graph = builder.compile()
```

**Step 4: Run test to verify it passes**
Run: `poetry run pytest tests/test_agent.py -v`
Expected: PASS

**Step 5: Commit**
```bash
git add src/agent/ tests/test_agent.py
git commit -m "feat: setup initial langgraph state machine"
```
