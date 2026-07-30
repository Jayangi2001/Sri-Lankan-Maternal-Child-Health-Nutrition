import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

def search_moh_nutrition_knowledge_base(query: str):
   
    safe_query = str(query)
    
    sample_docs = [
        Document(page_content="MOH Sri Lanka Infant Feeding Guidelines: Exclusive breastfeeding is recommended for the first 6 months of life."),
        Document(page_content="Complementary feeding should begin at 6 months alongside continued breastfeeding up to 2 years or beyond."),
        Document(page_content="Maternal Nutrition: Pregnant and lactating mothers require daily Iron and Folic Acid supplements provided by MOH clinics."),
        Document(page_content="Growth Monitoring: Growth faltering occurs if a child's weight curve flattens on the CHDR (Child Health Development Record) card.")
    ]
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(sample_docs, embeddings)
    
    docs = vectorstore.similarity_search(safe_query, k=2)
    
    return [doc.page_content for doc in docs]
