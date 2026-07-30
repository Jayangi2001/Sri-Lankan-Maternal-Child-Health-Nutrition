from langgraph.graph import StateGraph, END
from state import MaternalHealthState
from agents.profiler_agent import profiler_agent
from agents.retriever_agent import retriever_agent
from agents.reviewer_agent import reviewer_agent

def build_graph():
    builder = StateGraph(MaternalHealthState)
    builder.add_node("profiler", profiler_agent)
    builder.add_node("retriever", retriever_agent)
    builder.add_node("reviewer", reviewer_agent)

    builder.set_entry_point("profiler")
    builder.add_edge("profiler", "retriever")
    builder.add_edge("retriever", "reviewer")
    builder.add_edge("reviewer", END)

    return builder.compile()

app = build_graph()
