from typing import TypedDict, Annotated, List, Dict, Any
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    user_id: str
    agent_id: str
    sources: List[Dict[str, Any]]
