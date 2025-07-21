import os
from pathlib import Path
from dotenv import load_dotenv
 
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from typing import List
 
# 🔐 Load OpenAI key
load_dotenv()
assert os.environ.get("OPENAI_API_KEY"), "Please set OPENAI_API_KEY in .env"
 
# 📁 Load all FAISS indexes from folder
INDEX_DIR = Path("greek_indexers")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
 
vectorstores = []
for subdir in INDEX_DIR.iterdir():
    if subdir.is_dir():
        try:
            vs = FAISS.load_local(subdir, embeddings, allow_dangerous_deserialization=True)
            vectorstores.append(vs)
            print(f"✅ Loaded index from {subdir.name}")
        except Exception as e:
            print(f"❌ Failed to load {subdir.name}: {e}")
 
if not vectorstores:
    raise RuntimeError("❌ No FAISS indexes were loaded.")
 
# 🔁 Combined Retriever (Multi-index support)
class CombinedRetriever(BaseRetriever):
    def __init__(self, retrievers: List[BaseRetriever]):
        super().__init__()
        self._retrievers = retrievers
 
    def _get_relevant_documents(self, query: str) -> List[Document]:
        docs = []
        for retriever in self._retrievers:
            try:
                docs.extend(retriever.get_relevant_documents(query))
            except Exception as e:
                print(f"⚠️ Sub-retriever failed: {e}")
        return docs
# ➕ Convert all FAISS stores into retrievers
retrievers = [vs.as_retriever(search_kwargs={"k": 5}) for vs in vectorstores]
retriever = CombinedRetriever(retrievers=retrievers)
 
# 💬 LLM
llm = ChatOpenAI(model="gpt-4o")
 
# 🔄 Retrieval-Augmented Generation (RAG)
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)
 
# ❓ Prompt user
query = input("❓ Ask your legal question: ")
 
# 🔍 Show what was retrieved
retrieved_docs = retriever.invoke(query)
if not retrieved_docs:
    print("⚠️ No documents retrieved.")
else:
    print("\n🔍 Retrieved Chunks:")
    for i, doc in enumerate(retrieved_docs):
        print(f"\n--- Document {i+1} from {doc.metadata.get('source', 'unknown')} ---")
        print(doc.page_content[:500].strip())
 
# 💬 Answer
if retrieved_docs:
    result = qa(query)
 
    print("\n📘 Answer:")
    print(result["result"])
 
    print("\n🔎 Sources:")
    for doc in result["source_documents"]:
        print(f"– {doc.metadata.get('source', 'unknown')}")
        print(doc.page_content[:300].strip(), "...\n")
 
 