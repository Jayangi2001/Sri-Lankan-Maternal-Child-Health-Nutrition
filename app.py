import streamlit as st
from graph_builder import app

st.set_page_config(page_title="Maternal & Child Health Advisor", page_icon="👶")

st.title("👶 Sri Lankan Maternal & Child Health Nutrition Advisor")
st.caption("MOH Sri Lanka Guidelines Multi-Agent Clinical Support System")

user_query = st.text_area("Enter Patient Query / Case details:", placeholder="e.g., My 7-month-old infant is starting solid food. What MOH feeding rules should I follow?")

if st.button("Analyze & Advise"):
    if not user_query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Multi-Agent System is analyzing..."):
            initial_state = {"user_input": user_query}
            result = app.invoke(initial_state)
            
            st.subheader("📋 Patient Profile Breakdown")
            st.json(result.get("patient_profile", {}))
            
            st.subheader("📚 Retrieved MOH Guidelines Context")
            for doc in result.get("retrieved_docs", []):
                st.info(f"• {doc}")
                
            st.subheader("🩺 Final Clinical Recommendation")
            st.success(result.get("final_response"))
