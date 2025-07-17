import os
from pathlib import Path
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()
assert os.environ.get("OPENAI_API_KEY"), "Please set the OPENAI_API_KEY environment variable."

DATA_DIR = Path("data")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
embeddings = OpenAIEmbeddings()

greek_docs = []
un_docs = []

# Walk through all subfolders and files
for filepath in DATA_DIR.rglob("*.txt"):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Check if path contains 'un'
    if "un" in filepath.parts:
        un_docs.append(Document(page_content=text, metadata={"source": str(filepath)}))
    else:
        greek_docs.append(Document(page_content=text, metadata={"source": str(filepath)}))

# Index Greek law
greek_chunks = splitter.split_documents(greek_docs)
greek_index = FAISS.from_documents(greek_chunks, embeddings)
greek_index.save_local("greek_law_index")
print(f"🇬🇷 Greek law: {len(greek_chunks)} chunks saved to 'greek_law_index'")

# Index UN law
un_chunks = splitter.split_documents(un_docs)
un_index = FAISS.from_documents(un_chunks, embeddings)
un_index.save_local("un_law_index")
print(f"🇺🇳 UN law: {len(un_chunks)} chunks saved to 'un_law_index'")
