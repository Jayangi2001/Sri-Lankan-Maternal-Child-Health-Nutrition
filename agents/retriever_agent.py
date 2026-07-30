from tools.retriever import search_moh_nutrition_knowledge_base
from state import MaternalHealthState

def retriever_agent(state: MaternalHealthState) -> MaternalHealthState:
 
    query = str(state.get("user_input", ""))
    
    docs = search_moh_nutrition_knowledge_base(query)
    
    state['retrieved_docs'] = docs
    return state
