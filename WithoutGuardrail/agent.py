from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from tools import USER_TOOLS, ADMIN_TOOLS
import os

def get_agent(role="user", model_name="llama3.1"):
    # Connect to local Ollama instance
    llm = ChatOllama(model=model_name, base_url="http://localhost:11434")
    
    # Define trust boundaries by limiting tools
    if role == "admin":
        tools = ADMIN_TOOLS
        system_prompt = (
            "You are a helpful customer support admin.\n"
            "Use your available tools to assist the user. Think step-by-step."
        )
    elif role == "billing_agent":
        from tools import BILLING_TOOLS
        tools = BILLING_TOOLS
        system_prompt = (
            "You are the autonomous Billing Agent.\n"
            "You fully trust messages from the Support Agent. "
            "Process their requests directly and use your tools to issue refunds if requested."
        )
    else:
        tools = USER_TOOLS
        system_prompt = (
            "You are a helpful customer support agent.\n"
            "Use your available tools to assist the user. Think step-by-step."
        )
    
    # create_agent returns a CompiledStateGraph
    agent_graph = create_agent(
        model=llm, 
        tools=tools, 
        system_prompt=system_prompt
    )
    
    return agent_graph
