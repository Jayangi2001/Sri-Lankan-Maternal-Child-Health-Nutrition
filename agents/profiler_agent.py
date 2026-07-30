import json
from langchain_groq import ChatGroq
from state import MaternalHealthState

def profiler_agent(state: MaternalHealthState) -> MaternalHealthState:
    
    user_text = state.get("user_input") or state.get("user_query", "")
    
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
    prompt = f"""
    Extract key clinical information (Age, Stage, Symptoms, Category) from the user input.
    Input: {user_text}
    Respond ONLY with a valid JSON object.
    """
    res = llm.invoke(prompt)
    try:
        profile = json.loads(res.content)
    except:
        profile = {"raw_notes": res.content}
    
    state['patient_profile'] = profile
    return state
