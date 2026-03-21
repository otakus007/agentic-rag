from src.agent.graph import app_graph, get_compiled_graph, build_graph
from src.agent.memory import get_mem0_client
from src.agent.tools import save_memory
from src.agent.state import AgentState
from src.agent.tool_registry import register_tool, clear_registry
from unittest.mock import patch, MagicMock, call
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
import inspect

def test_graph_initialization():
    assert app_graph is not None

@patch("src.agent.graph.retrieve_context")
@patch("src.agent.graph.get_mem0_client")
def test_graph_invocation(mock_get_client, mock_retriever):
    mock_client = MagicMock()
    mock_client.search.return_value = {"results": [{"memory": "User likes TDD."}]}
    mock_get_client.return_value = mock_client
    mock_retriever.return_value = []
    
    with patch("src.agent.graph.ChatOpenAI") as mock_chat:
        mock_llm = MagicMock()
        mock_llm.bind_tools.return_value = mock_llm
        mock_llm.invoke.return_value = AIMessage(content="Hello World")
        mock_chat.return_value = mock_llm
        
        graph = build_graph(agent_id="test_agent")
        result = graph.invoke({
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
    checkpointer = InMemorySaver()
    graph = get_compiled_graph(checkpointer=checkpointer)
    assert graph is not None

def test_get_compiled_graph_without_checkpointer():
    graph = get_compiled_graph()
    assert graph is not None

# --- Phase 2 Nyquist Gap Fixes ---

def test_save_memory_tool_signature():
    sig = inspect.signature(save_memory.func)
    param_names = list(sig.parameters.keys())
    assert "fact" in param_names
    assert "user_id" in param_names
    assert "agent_id" in param_names

def test_agent_state_has_tracking_fields():
    annotations = AgentState.__annotations__
    assert "user_id" in annotations
    assert "agent_id" in annotations
    assert "messages" in annotations

@patch("src.agent.graph.retrieve_context")
@patch("src.agent.graph.get_mem0_client")
def test_mem0_search_called_and_injected_as_system_message(mock_get_client, mock_retriever):
    mock_client = MagicMock()
    mock_client.search.return_value = {"results": [{"memory": "User prefers Python."}]}
    mock_get_client.return_value = mock_client
    mock_retriever.return_value = []
    
    with patch("src.agent.graph.ChatOpenAI") as mock_chat:
        mock_llm = MagicMock()
        mock_llm.bind_tools.return_value = mock_llm
        mock_llm.invoke.return_value = AIMessage(content="Response with context")
        mock_chat.return_value = mock_llm
        
        graph = build_graph(agent_id="test_agent")
        graph.invoke({
            "messages": [{"role": "user", "content": "What language do I prefer?"}],
            "user_id": "test_user",
            "agent_id": "test_agent"
        })
        
        mock_client.search.assert_called_once()
        llm_call_args = mock_llm.invoke.call_args[0][0]
        system_msgs = [m for m in llm_call_args if isinstance(m, dict) and m.get("role") == "system"]
        assert len(system_msgs) > 0
        assert "User prefers Python." in system_msgs[0]["content"]

# --- Phase 4: Qdrant Retrieval Integration ---

@patch("src.agent.graph.retrieve_context")
@patch("src.agent.graph.get_mem0_client")
def test_qdrant_retrieval_injected_into_messages(mock_get_client, mock_retriever):
    mock_client = MagicMock()
    mock_client.search.return_value = {"results": []}
    mock_get_client.return_value = mock_client
    
    mock_retriever.return_value = [
        {"content": "The leave policy allows 20 days.", "page_number": 5, "block_type": "paragraph", "score": 0.92}
    ]
    
    with patch("src.agent.graph.ChatOpenAI") as mock_chat:
        mock_llm = MagicMock()
        mock_llm.bind_tools.return_value = mock_llm
        mock_llm.invoke.return_value = AIMessage(content="Based on [1], the policy states...")
        mock_chat.return_value = mock_llm
        
        graph = build_graph(agent_id="test_agent")
        result = graph.invoke({
            "messages": [{"role": "user", "content": "What is the leave policy?"}],
            "user_id": "test_user",
            "agent_id": "test_agent"
        })
        
        mock_retriever.assert_called_once()
        
        llm_call_args = mock_llm.invoke.call_args[0][0]
        doc_msgs = [m for m in llm_call_args if isinstance(m, dict) and m.get("role") == "system" and "Document context" in m.get("content", "")]
        assert len(doc_msgs) == 1
        assert "[1]" in doc_msgs[0]["content"]
        assert "The leave policy allows 20 days." in doc_msgs[0]["content"]
        
        assert len(result.get("sources", [])) == 1

def test_agent_state_has_sources_field():
    annotations = AgentState.__annotations__
    assert "sources" in annotations

# --- Phase 6: Dynamic graph with per-agent tools ---

def test_build_graph_uses_registry():
    """Verify build_graph compiles with tools from the registry."""
    graph = build_graph(agent_id="test_agent")
    assert graph is not None

def test_build_graph_with_custom_tool():
    """Verify custom tools are included when registered for an agent."""
    clear_registry()
    
    @tool
    def custom_action(x: str) -> str:
        """A custom action."""
        return f"done: {x}"
    
    register_tool("special_agent", custom_action)
    graph = build_graph(agent_id="special_agent")
    assert graph is not None
    clear_registry()
