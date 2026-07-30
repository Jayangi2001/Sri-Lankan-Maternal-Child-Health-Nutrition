from langchain_openai import ChatOpenAI
from state import MaternalHealthState

def reviewer_agent(state: MaternalHealthState) -> MaternalHealthState:
    
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo",
        openai_api_base="https://openrouter.ai/api/v1"
    )
    
    prompt = f"""
    You are an expert Sri Lankan MOH Maternal & Child Health Nutrition Advisor.
    Patient Profile: {state.get('patient_profile')}
    MOH Guidelines Context: {state.get('retrieved_docs')}
    User Question: {state['user_input']}
    
    Provide a clear, clinical, empathetic response and actionable nutritional advice.
    """
    res = llm.invoke(prompt)
    state['final_response'] = res.content
    return state
