import os
from langchain_groq import ChatGroq
from state import MaternalHealthState

def reviewer_agent(state: MaternalHealthState) -> MaternalHealthState:
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    user_text = str(state.get("user_input", ""))
    profile = state.get('patient_profile', {})
    docs = state.get('retrieved_docs', [])
    
    try:
        llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7, groq_api_key=groq_api_key)
        prompt = f"""
        You are an expert Sri Lankan MOH Maternal & Child Health Nutrition Advisor.
        Patient Profile: {profile}
        MOH Guidelines Context: {docs}
        User Question: {user_text}
        
        Provide detailed, clinical, empathetic nutritional advice based on Sri Lankan MOH guidelines.
        """
        res = llm.invoke(prompt)
        state['final_response'] = str(res.content)
    except Exception as e:
        state['final_response'] = f"Error generating advice: {str(e)}"
        
    return state
