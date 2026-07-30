import os
import streamlit as st

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

from graph_builder import app

st.set_page_config(
    page_title="MOH Health & Nutrition Advisor", 
    page_icon="👶", 
    layout="wide"
)

st.title("👶 Sri Lankan Maternal & Child Health Nutrition Advisor")
st.caption("MOH Sri Lanka Guidelines Multi-Agent Clinical Support System")
st.divider()

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Enter Case / Patient Details")
    user_query = st.text_area(
        "Patient Query:",
        placeholder="e.g., My 6-month-old infant is starting solid food. What MOH feeding rules should I follow?",
        height=180,
        label_visibility="collapsed"
    )
    
    submit_btn = st.button("🚀 Analyze & Generate Recommendation", type="primary", use_container_width=True)

with col2:
    st.subheader("🩺 Final Clinical Recommendation")
    if submit_btn:
        if not user_query.strip():
            st.warning("⚠️ Please enter a valid patient query or details.")
        elif "GROQ_API_KEY" not in os.environ or not os.environ["GROQ_API_KEY"]:
            st.error("🔑 GROQ_API_KEY is missing! Please set it in Streamlit Secrets.")
        else:
            with st.spinner("⏳ Multi-Agent System is analyzing guidelines..."):
                initial_state = {"user_input": user_query}
             
                result = app.invoke(initial_state)
                
                final_advice = result.get("final_response")
                
                if final_advice:
                    st.success(final_advice)
                else:
                    st.error("Failed to fetch recommendation. State did not return 'final_response'.")
                
                st.divider()
                
                with st.expander("📋 View Extracted Patient Profile", expanded=False):
                    st.json(result.get("patient_profile", {}))
                    
                with st.expander("📚 View Retrieved MOH Context Guidelines", expanded=False):
                    retrieved_docs = result.get("retrieved_docs", [])
                    if isinstance(retrieved_docs, list) and len(retrieved_docs) > 0:
                        for doc in retrieved_docs:
                            st.info(f"📌 {doc}")
                    else:
                        st.write("No specific guidelines retrieved.")
