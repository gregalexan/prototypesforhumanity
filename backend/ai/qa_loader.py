import os
from pathlib import Path
from dotenv import load_dotenv

from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain as load_langchain_qa_chain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.vectorstores.base import VectorStoreRetriever

load_dotenv()

# ─── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
PROCESSES_BASE = PROJECT_ROOT / "processes"

# ─── Models ────────────────────────────────────────────────────────────────────
llm = ChatOpenAI(model="gpt-4o")

universal_embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
greek_embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# ─── QA Chain Loader ───────────────────────────────────────────────────────────
def load_qa_chain_by_index(index_name: str) -> RetrievalQA:
    index_path = PROCESSES_BASE / index_name
    if not index_path.exists():
        raise FileNotFoundError(f"Index path does not exist: {index_path}")

    # Select embeddings based on index
    used_embeddings = greek_embeddings if "greek" in index_name.lower() else universal_embeddings
    vectorstore = FAISS.load_local(str(index_path), used_embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Custom prompt for Greek law
    if "greek" in index_name.lower():
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "Είσαι έμπειρος νομικός σύμβουλος. Διάβασε τα παρακάτω αποσπάσματα από ελληνικά νομικά κείμενα "
                "και απάντησε όσο πιο συγκεκριμένα και τεκμηριωμένα γίνεται στην ερώτηση.\n\n"
                "Αποσπάσματα:\n{context}\n\n"
                "Ερώτηση:\n{question}\n\n"
                "Απάντηση:"
            )
        )
        qa_chain = load_langchain_qa_chain(llm, chain_type="stuff", prompt=prompt)
        return RetrievalQA(combine_documents_chain=qa_chain, retriever=retriever, return_source_documents=True)

    # Default QA chain for non-Greek content
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

# ─── Retriever Loader ──────────────────────────────────────────────────────────
def load_retriever(index_name: str) -> VectorStoreRetriever:
    index_path = PROCESSES_BASE / index_name
    if not index_path.exists():
        raise FileNotFoundError(f"Index path does not exist: {index_path}")

    used_embeddings = greek_embeddings if "greek" in index_name.lower() else universal_embeddings
    vectorstore = FAISS.load_local(str(index_path), used_embeddings, allow_dangerous_deserialization=True)
    return vectorstore.as_retriever(search_kwargs={"k": 5})
