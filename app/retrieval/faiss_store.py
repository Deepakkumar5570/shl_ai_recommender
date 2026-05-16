import json

from langchain_core.documents import Document

from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings


# =====================================================
# LOAD JSON DATA
# =====================================================

with open(
    "data/processed/processed_catalog.json",
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)


# =====================================================
# CREATE DOCUMENTS
# =====================================================

documents = []

for item in data:

    text = item.get("search_text", "")

    metadata = {

        "name": item.get("name", ""),

        "url": item.get("url", ""),

        "test_type": item.get(
            "test_type",
            ""
        ),

        "description": item.get(
            "description",
            ""
        ),

        "job_levels": item.get(
            "job_levels",
            []
        ),

        "keys": item.get(
            "keys",
            []
        )
    }

    documents.append(

        Document(
            page_content=text,
            metadata=metadata
        )
    )


print(f"Loaded {len(documents)} documents")


# =====================================================
# EMBEDDING MODEL
# =====================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded")


# =====================================================
# CREATE VECTORSTORE
# =====================================================

vectorstore = FAISS.from_documents(
    documents,
    embedding_model
)

print("FAISS vectorstore created")


# =====================================================
# SAVE VECTORSTORE
# =====================================================

vectorstore.save_local(
    "data/vectorstore/faiss_index"
)

print("FAISS index saved successfully")