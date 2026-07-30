from tools.retriever import search_moh_nutrition_knowledge_base
from state import MaternalHealthState

def retriever_agent(state: MaternalHealthState) -> dict:
    profile = state.get("patient_profile", {}).get("summary", "")
    query = f"{state['user_query']} {profile}"
    context = search_moh_nutrition_knowledge_base.invoke(query)
    return {"retrieved_guidelines": context}
