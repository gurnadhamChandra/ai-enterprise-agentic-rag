from langgraph.graph import StateGraph  ,END
from langgraph.checkpoint.memory import MemorySaver
from app.agents.state import AgentState

from app.agents.nodes.planner import planner_node
from app.agents.nodes.retreival import retrieve_node
from app.agents.nodes.responder import generate_node

# 1. Initialize the State Graph
workflow = StateGraph(AgentState)  # type: ignore[type-var]

# 2. Add Nodes to the Graph
workflow.add_node("planner", planner_node)
workflow.add_node("retriever", retrieve_node)
workflow.add_node("generator", generate_node)


# 3. Define the Edges & Routing Logic
def route_planner(state: AgentState):
    """
    Routes the workflow based on the planner's decision.
    """
    if state["current_query"] == "CONVERSATIONAL":
        return "generator"
    return "retriever"

workflow.set_entry_point("planner")


# Conditional Edge: Planner -> Router -> (Retriever OR Responder)
workflow.add_conditional_edges(
    "planner",
    route_planner,
    {
        "retriever": "retriever",
        "generator": "generator"
    }
)


workflow.add_edge("retriever", "generator")
workflow.add_edge("generator", END)


# --- MEMORY UPGRADE ---
# MemorySaver allows the agent to remember conversations based on 'thread_id'
checkpointer = MemorySaver()


# 4. Compile the Graph with Memory
rag_agent = workflow.compile(checkpointer=checkpointer)