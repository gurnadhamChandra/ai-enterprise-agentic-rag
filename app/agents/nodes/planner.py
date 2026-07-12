from app.agents.state import AgentState
import logfire
from app.config import settings
from langchain_groq import ChatGroq

llm= ChatGroq(model=settings.GROQ_MODEL,groq_api_key=settings.GROQ_API_KEY,temperature=0)

def planner_node(state:AgentState):
    """The Planner determines if a search is needed based on the ENTIRE conversation."""
    # Get the conversation history (excluding the latest message)
    history=""
    for msg in state["messages"][:-1]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history += f"{role}: {msg['content']}\n"
    
    # New Query
    user_message = state["messages"][-1]["content"] if state["messages"] else ""

    prompt=f"""
    You are an intelligent Assistant Planner. 
    Analyze the conversation history and the latest user message.
    
    CONVERSATION HISTORY:
    {history}
    
    LATEST MESSAGE:
    "{user_message}"
    
    Task:
    1. If the latest message is a greeting (hi, hello) or a question that can be answered using ONLY the conversation history above (e.g., "what is my name"), respond with 'CONVERSATIONAL'.
    2. If it is a technical question about Kubernetes, Intel, or Networking that requires fresh documentation, output a refined search query.
    
    Output ONLY 'CONVERSATIONAL' or the search query.
    """

    with logfire.span("🧠 planner Decision"):
        raw_content = llm.invoke(prompt).content
        # .content can be a list of content blocks instead of a plain string
        if isinstance(raw_content, list):
            decision = " ".join(
                block.get("text", str(block)) if isinstance(block, dict) else str(block)
                for block in raw_content
            ).strip()
        else:
            decision = raw_content.strip()
        logfire.info("Planner Decision",decision=decision)

        if "CONVERSATIONAL"in decision:
            return {
            "current_query": "CONVERSATIONAL",
            "status": "Handling conversationally (using memory)...",
            "plan": ["Intent: Conversational/Memory", "Retrieval: Skipped"]
        }
        return {
        "current_query": decision,
        "status": f"Technical research needed. Searching for: {decision}",
        "plan": ["Intent: Technical", f"Search Term: {decision}"]
    }