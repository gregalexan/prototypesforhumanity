import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# 🔐 Load OpenAI key
load_dotenv()
assert os.environ.get("OPENAI_API_KEY"), "Please set OPENAI_API_KEY in .env"

# 🧠 Choose which vector index to load
INDEX = "greek_law_index"  # or "un_law_index"

# 🔍 Load local FAISS vectorstore with HF embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vectorstore = FAISS.load_local(INDEX, embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# 💬 Set up GPT model
llm = ChatOpenAI(model="gpt-4o")

# 🔄 Retrieval-augmented QA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# 🧠 Ask
query = input("❓ Ask your legal question: ") 
result = qa(query)

# 📘 Answer
print("\n📘 Answer:")
print(result["result"])

# 📄 Sources
print("\n🔎 Sources:")
for doc in result["source_documents"]:
    print(f"– {doc.metadata['source']}")
    print(doc.page_content[:300].strip(), "...\n")
