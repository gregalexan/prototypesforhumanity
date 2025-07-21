import os
from pathlib import Path
from dotenv import load_dotenv
 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# Setup
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data"
GREEK_DIR = DATA_DIR / "greek"
UN_DIR = DATA_DIR / "un"
HUMAN_RIGHTS_DIR = DATA_DIR / "human_rights"
INTL_HUMAN_LAW_DIR = DATA_DIR / "international_human_law"

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# -------------------------------
# Load Greek law documents
# -------------------------------
greek_docs = []
for filepath in GREEK_DIR.rglob("*.txt"):
    # print(f"📄 [GREEK] Found file: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    greek_docs.append(Document(page_content=text, metadata={"source": str(filepath)}))

# -------------------------------
# Load Human Rights documents
# -------------------------------
human_rights_docs = []
for filepath in HUMAN_RIGHTS_DIR.rglob("*.txt"):
    # print(f"📄 [HUMAN RIGHTS] Found file: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    human_rights_docs.append(Document(page_content=text, metadata={"source": str(filepath)}))

# -------------------------------
# Load International Human Law documents
# -------------------------------
intl_law_docs = []
for filepath in INTL_HUMAN_LAW_DIR.rglob("*.txt"):
    # print(f"📄 [INTL LAW] Found file: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    intl_law_docs.append(Document(page_content=text, metadata={"source": str(filepath)}))

# -------------------------------
# Load Remaining UN documents
# -------------------------------
un_docs = []
for filepath in UN_DIR.rglob("*.txt"):
    # print(f"📄 [UN GENERAL] Found file: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    un_docs.append(Document(page_content=text, metadata={"source": str(filepath)}))

# -------------------------------
# Summary
# -------------------------------
print(f"✅ Loaded {len(greek_docs)} Greek law documents")
print(f"✅ Loaded {len(human_rights_docs)} Human Rights documents")
print(f"✅ Loaded {len(intl_law_docs)} International Human Law documents")
print(f"✅ Loaded {len(un_docs)} General UN documents")

# -------------------------------
# Indexing
# -------------------------------

# Greek
greek_chunks = splitter.split_documents(greek_docs)
greek_index = FAISS.from_documents(greek_chunks, embeddings)
greek_index.save_local("greek_law_index")
print(f"🇬🇷 Greek law: {len(greek_chunks)} chunks saved to 'greek_law_index'")

# Human Rights
hr_chunks = splitter.split_documents(human_rights_docs)
hr_index = FAISS.from_documents(hr_chunks, embeddings)
hr_index.save_local("human_rights_index")
print(f"🕊️ Human Rights: {len(hr_chunks)} chunks saved to 'human_rights_index'")

# International Human Law
ihl_chunks = splitter.split_documents(intl_law_docs)
ihl_index = FAISS.from_documents(ihl_chunks, embeddings)
ihl_index.save_local("international_human_law_index")
print(f"⚖️ International Human Law: {len(ihl_chunks)} chunks saved to 'international_human_law_index'")

# General UN
un_chunks = splitter.split_documents(un_docs)
un_index = FAISS.from_documents(un_chunks, embeddings)
un_index.save_local("un_law_index")
print(f"🇺🇳 UN General: {len(un_chunks)} chunks saved to 'un_law_index'")
