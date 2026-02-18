"""
Create a knowledge base with sample content for RAG
This helps the AI generate more informed, contextual content
"""

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os

def create_knowledge_base():
    """Create a FAISS vector store with multilingual sample content"""
    
    # Sample content about different topics
    sample_content = """
    # Technology Content
    Artificial Intelligence is revolutionizing industries by automating tasks and improving decision-making.
    Machine Learning algorithms learn from data to make predictions without being explicitly programmed.
    
    # Health Content
    Regular exercise improves cardiovascular health and boosts mental well-being.
    A balanced diet with proteins, vitamins, and minerals is essential for optimal health.
    
    # Business Content
    Digital marketing has transformed how businesses reach their customers.
    Social media engagement is crucial for brand building and customer loyalty.
    
    # Education Content
    Online learning provides flexibility and access to quality education globally.
    Critical thinking skills are essential for success in the modern world.
    """
    
    # Save sample content
    with open("sample_content.txt", "w", encoding="utf-8") as f:
        f.write(sample_content)
    
    # Load and split documents
    loader = TextLoader("sample_content.txt")
    documents = loader.load()
    
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    
    # Create embeddings using multilingual model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    # Create vector store
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_index")
    
    print("✅ Knowledge base created successfully!")
    return vectorstore

if __name__ == "__main__":
    create_knowledge_base()