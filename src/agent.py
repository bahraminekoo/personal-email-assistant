from typing import Dict, Any
from langgraph.graph import StateGraph
from src.config import HF_API_KEY, DEFAULT_MODEL
from src.prompts import build_reply_prompt

# Import the new Hugging Face integration
from langchain_huggingface import HuggingFaceEndpoint

class State(dict):
    pass

def create_llm():
    return HuggingFaceEndpoint(
        repo_id=DEFAULT_MODEL,
        huggingfacehub_api_token=HF_API_KEY,
        task="text-generation",
        model_kwargs={"temperature": 0.6, "max_length": 512}
    )

def node_read_email(state: State) -> State:
    email = state.get("incoming_email", "").strip()
    return State({"email_context": email})

def node_decide_reply(state: State) -> State:
    email = state.get("email_context", "")
    needs_reply = bool(email) and not email.lower().startswith("newsletter")
    return State({"needs_reply": needs_reply})

def node_generate_reply(state: State) -> State:
    if not state.get("needs_reply", False):
        return State({"reply": "No reply needed."})
    llm = create_llm()
    prompt = build_reply_prompt(state.get("email_context", ""))
    reply_text = llm.invoke(prompt)   # HuggingFaceEndpoint returns plain text
    return State({"reply": reply_text})

def build_graph():
    graph = StateGraph()
    graph.add_node("read_email", node_read_email)
    graph.add_node("decide_reply", node_decide_reply)
    graph.add_node("generate_reply", node_generate_reply)

    graph.add_edge("read_email", "decide_reply")
    graph.add_edge("decide_reply", "generate_reply")

    return graph.compile()

def draft_reply(incoming_email: str) -> str:
    agent = build_graph()
    result: Dict[str, Any] = agent.invoke({"incoming_email": incoming_email})
    return result.get("reply", "")
