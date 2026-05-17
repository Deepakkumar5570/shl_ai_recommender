# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings


# embedding_model = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# # CORRECT FAISS PATH

# vectorstore = FAISS.load_local(
#     "data/vectorstore/faiss_index",
#     embedding_model,
#     allow_dangerous_deserialization=True,
# )

# retriever = vectorstore.as_retriever(
#     search_type="similarity",
#     search_kwargs={"k": 40},
# )


# def retrieve_assessments(query: str):

#     results = retriever.invoke(query)

#     return results






import json


# =========================================================
# LOAD CATALOG
# =========================================================

with open(
    "data/processed/processed_catalog.json",
    "r",
    encoding="utf-8"
) as f:

    catalog = json.load(f)


# =========================================================
# MAIN RETRIEVAL FUNCTION
# =========================================================

def retrieve_assessments(query: str):

    query_lower = query.lower()

    results = []

    # =====================================================
    # LOOP THROUGH ALL ASSESSMENTS
    # =====================================================

    for item in catalog:

        # =================================================
        # COMBINE TEXT
        # =================================================

        metadata_text = (

            str(item.get("name", "")) + " " +
            str(item.get("description", "")) + " " +
            str(item.get("test_type", "")) + " " +
            str(item.get("job_levels", ""))

        ).lower()

        score = 0

        # =================================================
        # BASIC KEYWORD MATCH
        # =================================================

        for word in query_lower.split():

            if word in metadata_text:
                score += 5

        # =================================================
        # MACHINE LEARNING LOGIC
        # =================================================

        if "machine learning" in query_lower:

            ml_words = [
                "machine learning",
                "data science",
                "python",
                "analytics",
                "ai",
                "data"
            ]

            for word in ml_words:

                if word in metadata_text:
                    score += 12

            bad_words = [
                "java",
                "verbal",
                "geoinformatics",
                "leadership",
                "competency",
                "sales",
                "finance",
                "sap"
            ]

            for word in bad_words:

                if word in metadata_text:
                    score -= 15

        # =================================================
        # BACKEND LOGIC
        # =================================================

        if "backend" in query_lower:

            backend_words = [
                "backend",
                "server",
                "api",
                "database",
                "software",
                "java",
                "python",
                "sql"
            ]

            for word in backend_words:

                if word in metadata_text:
                    score += 10

            bad_backend_words = [
                "frontend",
                "sales",
                "leadership",
                "verbal",
                "competency"
            ]

            for word in bad_backend_words:

                if word in metadata_text:
                    score -= 10

        # =================================================
        # JAVA LOGIC
        # =================================================

        if "java" in query_lower:

            java_words = [
                "java",
                "spring",
                "backend",
                "api",
                "server",
                "oop",
                "software"
            ]

            for word in java_words:

                if word in metadata_text:
                    score += 15

            bad_java_words = [
                "python",
                "machine learning",
                "data science",
                "finance",
                "leadership"
            ]

            for word in bad_java_words:

                if word in metadata_text:
                    score -= 12

        # =================================================
        # PYTHON LOGIC
        # =================================================

        if "python" in query_lower:

            python_words = [
                "python",
                "data",
                "automation",
                "machine learning",
                "analytics"
            ]

            for word in python_words:

                if word in metadata_text:
                    score += 14

            bad_python_words = [
                "java",
                "sap",
                "sales",
                "leadership"
            ]

            for word in bad_python_words:

                if word in metadata_text:
                    score -= 10

        # =================================================
        # DATABASE LOGIC
        # =================================================

        if "database" in query_lower:

            db_words = [
                "database",
                "sql",
                "oracle",
                "mysql",
                "pl/sql",
                "dba"
            ]

            for word in db_words:

                if word in metadata_text:
                    score += 15

        # =================================================
        # ENTRY LEVEL LOGIC
        # =================================================

        if "entry" in query_lower:

            if "entry" in metadata_text:
                score += 15

        # =================================================
        # MID LEVEL LOGIC
        # =================================================

        if "mid" in query_lower:

            if "mid" in metadata_text:
                score += 15

        # =================================================
        # SENIOR LEVEL LOGIC
        # =================================================

        if "senior" in query_lower:

            senior_words = [
                "senior",
                "director",
                "executive",
                "lead"
            ]

            for word in senior_words:

                if word in metadata_text:
                    score += 15

        # =================================================
        # SAVE RESULTS
        # =================================================

        if score > 0:

            results.append({
                "doc": item,
                "score": score
            })

    # =====================================================
    # SORT RESULTS
    # =====================================================

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    # =====================================================
    # RETURN TOP RESULTS
    # =====================================================

    final_results = []

    for r in results[:10]:

        final_results.append(r["doc"])

    return final_results