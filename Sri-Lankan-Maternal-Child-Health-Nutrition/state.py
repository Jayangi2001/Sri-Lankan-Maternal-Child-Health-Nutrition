from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages

class MaternalHealthState(TypedDict):
    messages: Annotated[List, add_messages]
    user_query: str
    patient_profile: dict
    retrieved_guidelines: str
    final_assessment: str
