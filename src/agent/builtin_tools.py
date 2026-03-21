"""Built-in tools available to all agents.

These extend the default tool set with visualization and
other utility capabilities.
"""
import json
from langchain_core.tools import tool


SUPPORTED_VIZ_TYPES = ["chart", "table", "mermaid"]


@tool
def visualize(data: str, viz_type: str) -> str:
    """Generate a structured visualization from data.

    Args:
        data: The data to visualize (text description or raw values).
        viz_type: Type of visualization — 'chart', 'table', or 'mermaid'.

    Returns:
        JSON string with {"type": str, "data": str} for the frontend to render.
    """
    if viz_type not in SUPPORTED_VIZ_TYPES:
        return json.dumps({
            "error": f"Unsupported viz_type '{viz_type}'. Supported: {SUPPORTED_VIZ_TYPES}"
        })

    return json.dumps({
        "type": viz_type,
        "data": data,
    })
