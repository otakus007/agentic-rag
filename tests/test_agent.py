from src.agent.graph import app_graph

def test_graph_initialization():
    assert app_graph is not None

def test_graph_invocation():
    # Invoke the graph to ensure the node evaluates and returns the Hello World message
    result = app_graph.invoke({"messages": [{"role": "user", "content": "test"}]})
    assert len(result["messages"]) > 1
    assert result["messages"][-1]["content"] == "Hello World"
    assert result["messages"][-1]["role"] == "assistant"
