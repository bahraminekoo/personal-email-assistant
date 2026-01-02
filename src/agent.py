# src/agent.py

from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, START, END
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline
from src.config import DEFAULT_MODEL   # comes from .env via config.py
from src.config import SIGNATURE_NAME, SIGNATURE_EMAIL, SIGNATURE_COMPANY

# Define the schema for your graph state
class EmailState(TypedDict):
    incoming_email: str
    email_context: str
    needs_reply: bool
    reply: str

# Create a local Hugging Face pipeline using model from .env
def create_llm():
    generator = pipeline(
        "text-generation",   
        model=DEFAULT_MODEL, 
        device=-1, # cpu
        max_new_tokens=256,
        temperature=0.6
    )
    return HuggingFacePipeline(pipeline=generator)

# Node functions
def node_read_email(state: EmailState) -> EmailState:
    email = state.get("incoming_email", "").strip()
    return {**state, "email_context": email}

def node_decide_reply(state: EmailState) -> EmailState:
    email = state.get("email_context", "")
    needs_reply = bool(email) and not email.lower().startswith("newsletter")
    return {**state, "needs_reply": needs_reply}

def node_generate_reply(state: EmailState) -> EmailState:
    if not state.get("needs_reply", False):
        return {**state, "reply": "No reply needed."}
    llm = create_llm()
    email_text = state.get("email_context", "")
    prompt = (
        f"Reply politely to the following email:\n\n{email_text}\n\n"
        f"End the reply with:\n\nBest regards,\n{SIGNATURE_NAME}\n{SIGNATURE_EMAIL}\n{SIGNATURE_COMPANY}"
    )
    reply_text = llm.invoke(prompt)
    return {**state, "reply": reply_text}


# Build the graph
def build_graph():
    graph = StateGraph(EmailState)

    graph.add_node("read_email", node_read_email)
    graph.add_node("decide_reply", node_decide_reply)
    graph.add_node("generate_reply", node_generate_reply)

    graph.add_edge(START, "read_email")
    graph.add_edge("read_email", "decide_reply")
    graph.add_edge("decide_reply", "generate_reply")
    graph.add_edge("generate_reply", END)

    return graph.compile()

# Public function
def draft_reply(incoming_email: str) -> str:
    agent = build_graph()
    result: Dict[str, Any] = agent.invoke({"incoming_email": incoming_email})
    return result.get("reply", "")
