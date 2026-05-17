import json
import os


# =========================================================
# LOAD CATALOG
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

catalog_path = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "processed_catalog.json"
)

with open(catalog_path, "r", encoding="utf-8") as f:
    catalog = json.load(f)


# =========================================================
# KEYWORD GROUPS
# =========================================================

TECH_KEYWORDS = {
    "java": [
        "java",
        "backend",
        "spring",
        "developer",
        "programming",
        "software",
        "api"
    ],

    "python": [
        "python",
        "automation",
        "analytics",
        "data",
        "developer"
    ],

    "machine learning": [
        "machine learning",
        "ai",
        "data science",
        "python",
        "analytics",
        "ml"
    ],

    "database": [
        "database",
        "sql",
        "mysql",
        "oracle",
        "pl/sql",
        "dba"
    ],

    "frontend": [
        "frontend",
        "react",
        "javascript",
        "web",
        "ui"
    ]
}


# =========================================================
# RETRIEVAL FUNCTION
# =========================================================

def retrieve_assessments(query: str):

    query_lower = query.lower()

    results = []

    for item in catalog:

        metadata_text = (

            str(item.get("name", "")) + " " +
            str(item.get("description", "")) + " " +
            str(item.get("test_type", "")) + " " +
            str(item.get("job_levels", ""))

        ).lower()

        score = 0

        # =================================================
        # BASIC QUERY WORD MATCH
        # =================================================

        for word in query_lower.split():

            if word in metadata_text:
                score += 5

        # =================================================
        # SMART TECH MATCHING
        # =================================================

        for category, keywords in TECH_KEYWORDS.items():

            if category in query_lower:

                for keyword in keywords:

                    if keyword in metadata_text:
                        score += 15

        # =================================================
        # SENIORITY MATCHING
        # =================================================

        if "senior" in query_lower:

            senior_words = [
                "senior",
                "lead",
                "director",
                "executive"
            ]

            for word in senior_words:

                if word in metadata_text:
                    score += 10

        elif "mid" in query_lower:

            if "mid" in metadata_text:
                score += 10

        elif "entry" in query_lower:

            if "entry" in metadata_text:
                score += 10

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