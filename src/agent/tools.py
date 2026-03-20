from langchain_core.tools import tool
from src.agent.memory import get_mem0_client

@tool
def save_memory(fact: str, user_id: str, agent_id: str) -> str:
    """Save a semantic fact or memory for the specific user and agent."""
    client = get_mem0_client()
    client.add(fact, user_id=user_id, agent_id=agent_id)
    return "Memory successfully saved."
