import os
from langchain_groq import ChatGroq
from state import MaternalHealthState

def reviewer_agent(state: MaternalHealthState) -> MaternalHealthState:
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.7,
        groq_api_key=groq_api_key
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
