import json
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import HuggingFaceEmbeddings

with open("data/processed/processed_catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


docs = []

for item in data:
    doc = Document(
        page_content=item["search_text"],
        metadata={
            "name": item["name"],
            "url": item["url"],
            "test_type": item["test_type"],
            "job_levels": item["job_levels"],
            "keys": item["keys"]
        }
    )

    docs.append(doc)

vectorstore = FAISS.from_documents(docs, embedding_model)

vectorstore.save_local("data/vectorstore/faiss_index")

print("FAISS index built successfully")