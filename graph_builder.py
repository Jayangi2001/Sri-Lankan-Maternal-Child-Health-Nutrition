from langgraph.graph import StateGraph, END
from state import MedicalState
from agents.profiler import profiler_agent
from agents.retriever_agent import retriever_agent
from agents.reviewer import reviewer_agent

workflow = StateGraph(MedicalState)

workflow.add_node("profiler", profiler_agent)
workflow.add_node("retriever", retriever_agent)
workflow.add_node("reviewer", reviewer_agent)

workflow.set_entry_point("profiler")
workflow.add_edge("profiler", "retriever")
workflow.add_edge("retriever", "reviewer")
workflow.add_edge("reviewer", END)

app = workflow.compile()
