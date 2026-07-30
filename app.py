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
    /* Header Card Style */
    .header-card {
        background: linear-gradient(135deg, #007bff 0%, #00c6ff 100%);
        padding: 30px;
        border-radius: 12px;
        color: white !important;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    }
    .header-card h1 { 
        color: white !important; 
        margin-bottom: 8px; 
        font-weight: 700;
        font-size: 2.2rem;
    }
    .header-card p { 
        color: white !important; 
        font-size: 1.1rem; 
        opacity: 0.95; 
        margin: 0;
    }

    /* Highlighted Button */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #20c997 0%, #0d9488 100%);
        color: white !important;
        font-size: 1.05rem;
        font-weight: bold;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(32, 201, 151, 0.3);
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #1baa80 0%, #0f766e 100%);
        box-shadow: 0 6px 15px rgba(32, 201, 151, 0.4);
        transform: translateY(-2px);
    }

    /* Output Green Advice Card */
    .advice-card {
        background-color: #14532d;
        color: #ffffff !important;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #22c55e;
        box-shadow: 0 3px 8px rgba(0,0,0,0.2);
        font-size: 1.05rem;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    
    .context-card {
        background-color: #1e293b;
        color: #f8fafc !important;
        padding: 12px 16px;
        border-radius: 8px;
        border-left: 4px solid #0284c7;
        margin-bottom: 10px;
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
        placeholder="My 7-month-old infant is starting solid food. What MOH feeding rules should I follow?",
        height=200,
        label_visibility="collapsed"
    )
    
    submit_btn = st.button("🚀 Analyze & Generate Recommendation")

with col2:
    st.markdown("### 🩺 Final Clinical Recommendation")
    
    if submit_btn:
        if not user_query.strip():
            st.warning("⚠️ Please enter a valid patient query or details.")
        elif "GROQ_API_KEY" not in os.environ or not os.environ["GROQ_API_KEY"]:
            st.error("🔑 GROQ_API_KEY is missing! Please set it in Streamlit Secrets.")
        else:
            with st.spinner("⏳ Multi-Agent System is analyzing guidelines..."):
                try:
                    initial_state = {"user_input": user_query}
                    result = app.invoke(initial_state)
                   
                    final_advice = (
                        result.get("final_response") or 
                        result.get("response") or 
                        "No recommendation generated."
                    )
                   
                    st.markdown(f"""
                        <div class="advice-card">
                            {final_advice}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    with st.expander("📋 View Extracted Patient Profile", expanded=False):
                        profile = result.get("patient_profile", {})
                        if profile:
                            st.json(profile)
                        else:
                            st.write("No patient profile extracted.")
                        
                    with st.expander("📚 View Retrieved MOH Context Guidelines", expanded=False):
                        retrieved_docs = result.get("retrieved_docs", [])
                        if isinstance(retrieved_docs, list) and len(retrieved_docs) > 0:
                            for doc in retrieved_docs:
                                st.markdown(f"""
                                    <div class="context-card">
                                        📌 {doc}
                                    </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.write("No specific context retrieved.")
                            
                except Exception as e:
                    st.error(f"❌ Error during execution: {str(e)}")
