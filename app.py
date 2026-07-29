import streamlit as st
from graph_builder import app

st.set_page_config(
    page_title="Sri Lankan MCH Nutrition Assistant",
    page_icon="👶",
    layout="wide"
)

st.title("👶 Sri Lankan Maternal & Child Health Nutrition System")
st.markdown("---")

user_query = st.text_area(
    "Enter patient query / scenario:",
    placeholder="e.g., A 6-month-old infant is underweight and refusing complementary food. What MOH guidelines apply?",
    height=100
)

if st.button("Analyze & Get Guidelines", type="primary"):
    if not user_query.strip():
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("Processing through AI Multi-Agent Pipeline..."):
            initial_state = {
                "messages": [],
                "user_query": user_query,
                "patient_profile": {},
                "retrieved_guidelines": "",
                "final_assessment": ""
            }

            result = app.invoke(initial_state)

            st.subheader("📋 Patient Profile Summary")
            st.info(result.get("patient_profile", {}).get("summary", "N/A"))

            st.subheader("📚 Retrieved MOH Guidelines")
            with st.expander("View Grounding Documents"):
                st.write(result.get("retrieved_guidelines", "No specific context retrieved."))

            st.subheader("💡 Expert Clinical Assessment & Recommendations")
            st.success(result.get("final_assessment", "No assessment generated."))
