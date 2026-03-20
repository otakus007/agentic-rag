from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os
load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "sk-mock-key"
from langgraph.prebuilt import ToolNode
from src.agent.state import AgentState
from src.agent.tools import save_memory
from src.agent.memory import get_mem0_client

llm = ChatOpenAI(model="gpt-4o-mini").bind_tools([save_memory])

def chatbot_node(state: AgentState):
    messages = list(state["messages"])
    last_message = messages[-1]
    
    content = last_message.content if hasattr(last_message, "content") else last_message.get("content", "")
    role = last_message.type if hasattr(last_message, "type") else last_message.get("role", "")
    
    if role in ["user", "human"]:
        try:
            client = get_mem0_client()
            search_res = client.search(content, user_id=state.get("user_id"), agent_id=state.get("agent_id"))
            
            results = search_res if isinstance(search_res, list) else search_res.get("results", [])
            facts = "\n".join([r.get("memory", "") if isinstance(r, dict) else r.memory for r in results])
            
            if facts.strip():
                sys_msg = {"role": "system", "content": f"Relevant context from previous memory:\n{facts}"}
                messages = [sys_msg] + messages
        except Exception as e:
            print(f"Mem0 search error (DB might be offline in test): {e}")
            pass
            
    response = llm.invoke(messages)
    return {"messages": [response]}

tools_node = ToolNode([save_memory])

def route_tools(state: AgentState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    elif isinstance(last_message, dict) and last_message.get("tool_calls"):
        return "tools"
    return END

builder = StateGraph(AgentState)
builder.add_node("chatbot", chatbot_node)
builder.add_node("tools", tools_node)
builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", route_tools)
builder.add_edge("tools", "chatbot")

app_graph = builder.compile()
