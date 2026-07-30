import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from state import MaternalHealthState

def profiler_agent(state: MaternalHealthState) -> dict:
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    query = state["user_query"]
    
    prompt = f"""Extract patient profile details from this query:
    Category: (Pregnant / Lactating / Infant 0-6m / Child 6-24m)
    Nutritional Issue: (Anemia, Thriposha, Underweight, etc.)
    Query: {query}"""
    
    res = llm.invoke([HumanMessage(content=prompt)])
    return {"patient_profile": {"summary": res.content}}
