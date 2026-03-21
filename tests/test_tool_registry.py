import json
from langchain_core.tools import tool
from src.agent.tool_registry import (
    get_tools_for_agent, register_tool, clear_registry, get_default_tools
)
from src.agent.builtin_tools import visualize


# --- Task 1: Tool Registry ---

def test_default_agent_gets_save_memory():
    tools = get_tools_for_agent("any_agent")
    tool_names = [t.name for t in tools]
    assert "save_memory" in tool_names


def test_register_custom_tool():
    clear_registry()

    @tool
    def my_tool(x: str) -> str:
        """A custom tool."""
        return x

    register_tool("custom_agent", my_tool)
    tools = get_tools_for_agent("custom_agent")
    tool_names = [t.name for t in tools]
    assert "my_tool" in tool_names
    assert "save_memory" in tool_names
    clear_registry()


def test_unknown_agent_gets_defaults():
    clear_registry()
    tools = get_tools_for_agent("nonexistent_agent")
    default_tools = get_default_tools()
    assert len(tools) == len(default_tools)


def test_register_duplicate_tool_ignored():
    clear_registry()

    @tool
    def dup_tool(x: str) -> str:
        """Dup tool."""
        return x

    register_tool("agent_a", dup_tool)
    register_tool("agent_a", dup_tool)
    tools = get_tools_for_agent("agent_a")
    tool_names = [t.name for t in tools]
    assert tool_names.count("dup_tool") == 1
    clear_registry()


# --- Task 3: Visualizer Tool ---

def test_visualize_chart_returns_structured_json():
    result = visualize.invoke({"data": "Sales: 100, 200, 300", "viz_type": "chart"})
    parsed = json.loads(result)
    assert parsed["type"] == "chart"
    assert "data" in parsed


def test_visualize_table_returns_structured_json():
    result = visualize.invoke({"data": "Name|Score\nAlice|95\nBob|87", "viz_type": "table"})
    parsed = json.loads(result)
    assert parsed["type"] == "table"


def test_visualize_mermaid_returns_structured_json():
    result = visualize.invoke({"data": "graph TD; A-->B;", "viz_type": "mermaid"})
    parsed = json.loads(result)
    assert parsed["type"] == "mermaid"


def test_visualize_invalid_type_returns_error():
    result = visualize.invoke({"data": "test", "viz_type": "invalid"})
    parsed = json.loads(result)
    assert "error" in parsed
    assert "Unsupported" in parsed["error"]
