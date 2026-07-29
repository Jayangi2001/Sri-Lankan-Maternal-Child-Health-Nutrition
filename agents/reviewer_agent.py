import os
from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import HumanMessage
from state import MaternalHealthState

def reviewer_agent(state: MaternalHealthState) -> dict:
    llm = ChatOpenRouter(model="openai/gpt-3.5-turbo", temperature=0.2)
    
    prompt = f"""You are a Senior Maternal & Child Health Specialist (MOH Sri Lanka).
    User Query: {state['user_query']}
    Profile: {state.get('patient_profile', {})}
    MOH Guidelines: {state.get('retrieved_guidelines', '')}

    Provide a safe, clinical-backed answer and mention red flags if any."""
    
    res = llm.invoke([HumanMessage(content=prompt)])
    return {"final_assessment": res.content}
