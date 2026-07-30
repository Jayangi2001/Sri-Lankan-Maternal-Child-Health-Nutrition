import os
import json
from langchain_groq import ChatGroq
from state import MaternalHealthState

def profiler_agent(state: MaternalHealthState) -> MaternalHealthState:
    user_text = str(state.get("user_input", ""))
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    try:
        llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0, groq_api_key=groq_api_key)
        prompt = f"Extract key clinical information (Age, Stage, Category) as JSON from: {user_text}"
        res = llm.invoke(prompt)
        state['patient_profile'] = json.loads(res.content)
    except Exception:
        state['patient_profile'] = {"raw_query": user_text}
        
    return state
