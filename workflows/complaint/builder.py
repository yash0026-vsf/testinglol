from langgraph.graph import END, START, StateGraph

from graph.state import SupportState
from nodes.complaint_nodes import process_complaint


def route_complaint(state: SupportState) -> str:
    if state.get("needs_human_escalation"):
        return "escalate"
    
    # If the root cause is not identified, we just finalize and wait for the user to respond
    # to the clarifying questions.
    return "finalize"


def build_complaint_graph():
    builder = StateGraph(SupportState)

    builder.add_node(
        "process_complaint",
        process_complaint,
    )

    builder.add_edge(
        START,
        "process_complaint",
    )

    builder.add_conditional_edges(
        "process_complaint",
        route_complaint,
        {
            "finalize": END,
            "escalate": END,
        },
    )

    return builder.compile()
