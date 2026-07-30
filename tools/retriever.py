import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import tool

# 1. Load HuggingFace Embeddings & FAISS Vector DB
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

if os.path.exists("vectorstore_db"):
    vector_db = FAISS.load_local("vectorstore_db", embeddings, allow_dangerous_deserialization=True)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
else:
    retriever = None

@tool
def search_moh_nutrition_knowledge_base(query: str) -> str:
    """Useful to search Sri Lanka MOH Maternal and Child Health Nutrition Guidelines, Thriposha rules, and supplement dosages. Use this tool for nutritional context."""
    if not retriever:
        return "Vector database 'vectorstore_db' not found. Please run vector_store.py first."
    
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant MOH guidelines found."
    
    return "\n\n".join([doc.page_content for doc in docs])
