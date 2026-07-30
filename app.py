import os
import streamlit as st

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

from graph_builder import app

st.set_page_config(
    page_title="MOH Health & Nutrition Advisor", 
    page_icon="👶", 
    layout="centered"
)

st.markdown("""
    <style>
    /* Main Background adjustments */
    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    
    /* Header Card Style */
    .header-card {
        background: linear-gradient(135deg, #007bff 0%, #00c6ff 100%);
        padding: 30px;
        border-radius: 14px;
        color: white !important;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .header-card h1 { 
        color: white !important; 
        margin-bottom: 8px; 
        font-weight: 700;
        font-size: 2rem;
    }
    .header-card p { 
        color: white !important; 
        font-size: 1.05rem; 
        opacity: 0.95; 
        margin: 0;
    }

    /* Make Text Area Bigger and Wider */
    .stTextArea textarea {
        font-size: 1.1rem !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border: 2px solid #cbd5e1 !important;
    }
    .stTextArea textarea:focus {
        border-color: #007bff !important;
        box-shadow: 0 0 8px rgba(0, 123, 255, 0.25);
    }

    /* Highlighted Button */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #20c997 0%, #0d9488 100%);
        color: white !important;
        font-size: 1.15rem;
        font-weight: bold;
        border: none;
        padding: 14px 28px;
        border-radius: 10px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(32, 201, 151, 0.35);
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #1baa80 0%, #0f766e 100%);
        box-shadow: 0 6px 16px rgba(32, 201, 151, 0.45);
        transform: translateY(-2px);
    }

    /* Output Green Advice Card */
    .advice-card {
        background-color: #14532d;
        color: #ffffff !important;
        padding: 24px;
        border-radius: 12px;
        border-left: 6px solid #22c55e;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        font-size: 1.1rem;
        line-height: 1.7;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    
    .context-card {
        background-color: #1e293b;
        color: #f8fafc !important;
        padding: 14px 18px;
        border-radius: 8px;
        border-left: 4px solid #0284c7;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-card">
        <h1>👶 Sri Lankan Maternal & Child Health Nutrition Advisor</h1>
        <p>MOH Sri Lanka Guidelines Multi-Agent Clinical Support System</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("### 📝 Enter Case / Patient Details")
user_query = st.text_area(
    "Patient Query:",
    placeholder="Type patient details here... e.g., My 7-month-old infant is starting solid food. What MOH feeding rules should I follow?",
    height=160,
    label_visibility="collapsed"
)

submit_btn = st.button("🚀 Analyze & Generate Recommendation")

st.markdown("<br>", unsafe_allow_html=True)

if submit_btn:
    if not user_query.strip():
        st.warning("⚠️ Please enter a valid patient query or details.")
    elif "GROQ_API_KEY" not in os.environ or not os.environ["GROQ_API_KEY"]:
        st.error("🔑 GROQ_API_KEY is missing! Please set it in Streamlit Secrets.")
    else:
        with st.spinner("⏳ Multi-Agent System is analyzing MOH guidelines..."):
            try:
                initial_state = {"user_input": user_query}
                result = app.invoke(initial_state)
                
                final_advice = (
                    result.get("final_response") or 
                    result.get("response") or 
                    "No recommendation generated."
                )
                
                st.markdown("### 🩺 Final Clinical Recommendation")
                st.markdown(f"""
                    <div class="advice-card">
                        {final_advice}
                    </div>
                """, unsafe_allow_html=True)
           
                col_exp1, col_exp2 = st.columns(2)
                with col_exp1:
                    with st.expander("📋 View Extracted Patient Profile", expanded=False):
                        profile = result.get("patient_profile", {})
                        if profile:
                            st.json(profile)
                        else:
                            st.write("No profile extracted.")
                            
                with col_exp2:
                    with st.expander("📚 View Retrieved Guidelines", expanded=False):
                        retrieved_docs = result.get("retrieved_docs", [])
                        if isinstance(retrieved_docs, list) and len(retrieved_docs) > 0:
                            for doc in retrieved_docs:
                                st.markdown(f"""
                                    <div class="context-card">
                                        📌 {doc}
                                    </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.write("No context retrieved.")
                            
            except Exception as e:
                st.error(f"❌ Error during execution: {str(e)}")
