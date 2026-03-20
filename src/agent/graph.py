from langgraph.graph import StateGraph, START, END
from .state import AgentState

def chatbot_node(state: AgentState):
    return {"messages": [{"role": "assistant", "content": "Hello World"}]}

builder = StateGraph(AgentState)
builder.add_node("chatbot", chatbot_node)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

app_graph = builder.compile()
