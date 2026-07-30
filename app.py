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

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .header-card {
        background: linear-gradient(135deg, #0d6efd 0%, #00d2ff 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-card h1 { color: white !important; margin-bottom: 5px; font-weight: 700; }
    .header-card p { font-size: 1.1rem; opacity: 0.9; }

    div.stButton > button:first-child {
        background: linear-gradient(90deg, #198754 0%, #20c997 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        border: none;
        padding: 12px 28px;
        border-radius: 8px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(25, 135, 84, 0.3);
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #146c43 0%, #1baa80 100%);
        box-shadow: 0 6px 15px rgba(25, 135, 84, 0.4);
        transform: translateY(-2px);
    }

    .info-card {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 10px;
        border-left: 5px solid #0d6efd;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .context-card {
        background-color: #eef7ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #0284c7;
        margin-bottom: 10px;
    }
    .advice-card {
        background-color: #f0fdf4;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #16a34a;
        box-shadow: 0 3px 8px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-card">
        <h1>👶 Sri Lankan Maternal & Child Health Nutrition Advisor</h1>
        <p>MOH Sri Lanka Guidelines Multi-Agent Clinical Support System</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📝 Enter Case / Patient Details")
    user_query = st.text_area(
        "Patient Query:",
        placeholder="e.g., My 7-month-old infant is starting solid food. What MOH feeding rules should I follow?",
        height=180,
        label_visibility="collapsed"
    )
    
    submit_btn = st.button("🚀 Analyze & Generate Recommendation")

with col2:
    if submit_btn:
        if not user_query.strip():
            st.warning("⚠️ Please enter a valid patient query or details.")
        elif "GROQ_API_KEY" not in os.environ or not os.environ["GROQ_API_KEY"]:
            st.error("🔑 GROQ_API_KEY is missing! Please set it in Streamlit Secrets.")
        else:
            with st.spinner("⏳ Multi-Agent System is analyzing guidelines..."):
                initial_state = {"user_input": user_query}
                result = app.invoke(initial_state)
                
                st.markdown("### 🩺 Final Clinical Recommendation")
                st.markdown(f"""
                    <div class="advice-card">
                        {result.get("final_response", "No recommendation generated.")}
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                with st.expander("📋 View Extracted Patient Profile", expanded=False):
                    st.json(result.get("patient_profile", {}))
                    
                with st.expander("📚 View Retrieved MOH Context Guidelines", expanded=False):
                    for doc in result.get("retrieved_docs", []):
                        st.markdown(f"""
                            <div class="context-card">
                                📌 {doc}
                            </div>
                        """, unsafe_allow_html=True)
