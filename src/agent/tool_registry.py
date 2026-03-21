"""Tool registry for per-agent_id dynamic tool sets.

Manages which tools are available for each agent. Defaults include
save_memory for all agents; custom tools can be registered per agent_id.
"""
from typing import Dict, List
from src.agent.tools import save_memory


# Internal registry: agent_id -> list of custom tools (not including defaults)
_custom_tools: Dict[str, list] = {}


def get_default_tools() -> list:
    """Return the default tools available to all agents."""
    return [save_memory]


def register_tool(agent_id: str, tool_func) -> None:
    """Register a custom tool for a specific agent_id."""
    if agent_id not in _custom_tools:
        _custom_tools[agent_id] = []
    # Avoid duplicates
    existing_names = [t.name for t in _custom_tools[agent_id]]
    if tool_func.name not in existing_names:
        _custom_tools[agent_id].append(tool_func)


def get_tools_for_agent(agent_id: str) -> list:
    """Return the full tool set for an agent (defaults + custom).

    Unknown agent_ids get the default set only.
    """
    defaults = get_default_tools()
    custom = _custom_tools.get(agent_id, [])
    return defaults + custom


def clear_registry() -> None:
    """Clear all custom tool registrations (for testing)."""
    _custom_tools.clear()
