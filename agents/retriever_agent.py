from tools.retriever import search_moh_nutrition_knowledge_base
from state import MaternalHealthState

def retriever_agent(state: MaternalHealthState) -> MaternalHealthState:
    query = state.get("user_input") or state.get("user_query", "")
    docs = search_moh_nutrition_knowledge_base(query)
    state['retrieved_docs'] = docs
    return state
