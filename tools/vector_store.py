import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def build_vector_store():
    print("📖 Reading MOH Guidelines PDF files from 'data/' folder...")
    loader = PyPDFDirectoryLoader("data/")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    docs = text_splitter.split_documents(documents)
    print(f"📄 Created {len(docs)} text chunks from MOH Nutrition documents.")

    print("🧠 Generating Embeddings using HuggingFace...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("💾 Creating FAISS Vector Database for Maternal Health...")
    vector_db = FAISS.from_documents(docs, embeddings)
    vector_db.save_local("vectorstore_db")
    print("✅ Vector database created and saved locally as 'vectorstore_db'!")

if __name__ == "__main__":
    build_vector_store()
