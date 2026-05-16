from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# CORRECT FAISS PATH

vectorstore = FAISS.load_local(
    "data/vectorstore/faiss_index",
    embedding_model,
    allow_dangerous_deserialization=True,
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 40},
)


def retrieve_assessments(query: str):

    results = retriever.invoke(query)

    return results