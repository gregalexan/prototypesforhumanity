import os
from pathlib import Path
from dotenv import load_dotenv

from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.retrievers import EnsembleRetriever 
load_dotenv()

# --- Paths ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
INDEX_BASE = PROJECT_ROOT  # root project folder

# --- Embeddings and LLM ---
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
llm = ChatOpenAI(model="gpt-4o")

# --- Function: Load QA chain by index name ---
def load_qa_chain(index_name: str) -> RetrievalQA:
    index_path = INDEX_BASE / index_name
    if not index_path.exists():
        raise FileNotFoundError(f"Index path does not exist: {index_path}")
    
    vectorstore = FAISS.load_local(str(index_path), embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa

def load_retriever(index_name: str) -> VectorStoreRetriever:
    index_path = INDEX_BASE / index_name
    vectorstore = FAISS.load_local(str(index_path), embeddings, allow_dangerous_deserialization=True)
    return vectorstore.as_retriever(search_kwargs={"k": 5})