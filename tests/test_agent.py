from src.agent.graph import app_graph, get_compiled_graph
from src.agent.memory import get_mem0_client
from src.agent.tools import save_memory
from src.agent.state import AgentState
from unittest.mock import patch, MagicMock, call
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver
import inspect

def test_graph_initialization():
    assert app_graph is not None

@patch("src.agent.graph.get_mem0_client")
@patch("src.agent.graph.llm")
def test_graph_invocation(mock_llm, mock_get_client):
    mock_llm.invoke.return_value = AIMessage(content="Hello World")
    
    mock_client = MagicMock()
    mock_client.search.return_value = {"results": [{"memory": "User likes TDD."}]}
    mock_get_client.return_value = mock_client
    
    result = app_graph.invoke({
        "messages": [{"role": "user", "content": "test"}],
        "user_id": "test_user",
        "agent_id": "test_agent"
    })
    assert len(result["messages"]) > 1
    assert result["messages"][-1].content == "Hello World"

@patch("src.agent.memory.Memory.from_config")
def test_mem0_initialization(mock_from_config):
    mock_from_config.return_value = MagicMock()
    client = get_mem0_client()
    assert client is not None

def test_get_compiled_graph_with_checkpointer():
    """Verify that get_compiled_graph accepts a real BaseCheckpointSaver."""
    checkpointer = InMemorySaver()
    graph = get_compiled_graph(checkpointer=checkpointer)
    assert graph is not None

def test_get_compiled_graph_without_checkpointer():
    """Verify that get_compiled_graph works without a checkpointer (default offline mode)."""
    graph = get_compiled_graph()
    assert graph is not None

# --- Phase 2 Nyquist Gap Fixes ---

def test_save_memory_tool_signature():
    """Verify save_memory tool has the correct parameters: fact, user_id, agent_id."""
    sig = inspect.signature(save_memory.func)
    param_names = list(sig.parameters.keys())
    assert "fact" in param_names
    assert "user_id" in param_names
    assert "agent_id" in param_names

def test_agent_state_has_tracking_fields():
    """Verify AgentState TypedDict includes user_id and agent_id."""
    annotations = AgentState.__annotations__
    assert "user_id" in annotations, "AgentState missing user_id field"
    assert "agent_id" in annotations, "AgentState missing agent_id field"
    assert "messages" in annotations, "AgentState missing messages field"

@patch("src.agent.graph.get_mem0_client")
@patch("src.agent.graph.llm")
def test_mem0_search_called_and_injected_as_system_message(mock_llm, mock_get_client):
    """Verify mem0.search() is called and results are injected into the LLM messages."""
    mock_llm.invoke.return_value = AIMessage(content="Response with context")
    
    mock_client = MagicMock()
    mock_client.search.return_value = {"results": [{"memory": "User prefers Python."}]}
    mock_get_client.return_value = mock_client
    
    app_graph.invoke({
        "messages": [{"role": "user", "content": "What language do I prefer?"}],
        "user_id": "test_user",
        "agent_id": "test_agent"
    })
    
    # Verify mem0.search was actually called
    mock_client.search.assert_called_once()
    
    # Verify the LLM received a system message containing the memory
    llm_call_args = mock_llm.invoke.call_args[0][0]
    system_msgs = [m for m in llm_call_args if isinstance(m, dict) and m.get("role") == "system"]
    assert len(system_msgs) > 0, "No SystemMessage was injected from Mem0 search results"
    assert "User prefers Python." in system_msgs[0]["content"]
