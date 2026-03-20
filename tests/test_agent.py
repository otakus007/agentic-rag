from src.agent.graph import app_graph
from src.agent.memory import get_mem0_client
from unittest.mock import patch, MagicMock
from langchain_core.messages import AIMessage

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
