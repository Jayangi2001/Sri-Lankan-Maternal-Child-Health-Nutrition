%%writefile agents/retriever_agent.py
from tools.retriever import search_moh_nutrition_knowledge_base
from state import MedicalState

def retriever_agent(state: MedicalState) -> MedicalState:
    query = state['user_input']
    docs = search_moh_nutrition_knowledge_base(query)
    state['retrieved_docs'] = docs
    return state