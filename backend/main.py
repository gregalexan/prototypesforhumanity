# ─── Imports ───────────────────────────────────────────────────────────────────
import os
import re
from collections import defaultdict
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from langchain.chains import RetrievalQA
from langchain.retrievers import EnsembleRetriever
from langchain_openai import ChatOpenAI

from ai.qa_loader import load_qa_chain_by_index, load_retriever

# ─── FastAPI Setup ─────────────────────────────────────────────────────────────
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Model Setup ───────────────────────────────────────────────────────────────
llm = ChatOpenAI(model="gpt-4o")

# ─── Request Schema ────────────────────────────────────────────────────────────
class Message(BaseModel):
    user_message: str
    law_type: str  # "greek" or "un"

# ─── Utility Functions ─────────────────────────────────────────────────────────
def extract_article_numbers(text):
    matches = re.findall(r"(?:Article|Άρθρο)\s+(\d+)", text, flags=re.IGNORECASE)
    return sorted(set(matches), key=int)

def clean_source_path(path):
    filename = os.path.basename(path)
    name = os.path.splitext(filename)[0]
    return name.replace("_", " ").strip()

def group_sources(documents):
    grouped = defaultdict(lambda: {"snippets": [], "articles": set()})

    for doc in documents:
        raw_path = doc.metadata.get("source", "unknown")
        clean_name = clean_source_path(raw_path)
        grouped[clean_name]["snippets"].append(doc.page_content[:300])
        articles = extract_article_numbers(doc.page_content)
        grouped[clean_name]["articles"].update(articles)

    result = []
    for name, data in grouped.items():
        result.append({
            "source": name,
            "articles": sorted(data["articles"], key=int),
            "snippet": "\n".join(data["snippets"])
        })

    return result

# ─── Chat Endpoint ─────────────────────────────────────────────────────────────
@app.post("/chat")
def chat_endpoint(message: Message):
    law_type = message.law_type.lower()

    if law_type == "greek":
        qa = load_qa_chain_by_index("greek_law_index")

    elif law_type == "un":
        retrievers = [
            load_retriever("un_law_index"),
            load_retriever("human_rights_index"),
            load_retriever("international_human_law_index"),
        ]
        ensemble = EnsembleRetriever(retrievers=retrievers)
        qa = RetrievalQA.from_chain_type(llm=llm, retriever=ensemble, return_source_documents=True)

    else:
        return {"error": f"Invalid law_type '{law_type}' — must be 'greek' or 'un'"}

    result = qa(message.user_message)

    return {
        "response": result["result"],
        "sources": group_sources(result["source_documents"])
    }
