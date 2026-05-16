from app.retrieval.retriever import retrieve_assessments

SENIORITY_KEYWORDS = {
    "entry": [
        "entry-level",
        "graduate",
        "junior"
    ],

    "mid": [
        "mid-professional",
        "professional individual contributor"
    ],

    "senior": [
        "manager",
        "senior",
        "lead",
        "director",
        "executive"
    ]
}


def calculate_keyword_score(
    query: str,
    metadata: dict
):

    score = 0

    query_lower = query.lower()

    metadata_text = f"""
    {metadata.get('name', '')}
    {metadata.get('description', '')}
    {' '.join(metadata.get('job_levels', []))}
    {' '.join(metadata.get('keys', []))}
    """.lower()

    # =====================================================
    # MACHINE LEARNING / AI
    # =====================================================

    if (
        "machine learning" in query_lower
        or "ml" in query_lower
        or "ai" in query_lower
    ):

        good_words = [
            "python",
            "machine learning",
            "ai",
            "analytics",
            "data science",
            "tensorflow",
            "pytorch"
        ]

        bad_words = [
            "sap",
            "abap",
            "leadership",
            "frontend",
            "verbal",
            "manager",
            "sales",
            "finance"
        ]

        for word in good_words:

            if word in metadata_text:
                score += 15

        for word in bad_words:

            if word in metadata_text:
                score -= 25

    # =====================================================
    # BACKEND
    # =====================================================

    if "backend" in query_lower:

        backend_good = [
            "backend",
            "server",
            "api",
            "database",
            "software",
            "python",
            "java",
            "spring",
            "django",
            "flask",
            "fastapi"
        ]

        backend_bad = [
            "frontend",
            "leadership",
            "sales",
            "verbal",
            "personality",
            "behavior"
        ]

        for word in backend_good:

            if word in metadata_text:
                score += 15

        for word in backend_bad:

            if word in metadata_text:
                score -= 20

    # =====================================================
    # PYTHON
    # =====================================================

    if "python" in query_lower:

        python_good = [
            "python",
            "django",
            "flask",
            "fastapi",
            "backend",
            "api"
        ]

        python_bad = [
            "java",
            "sap",
            "abap"
        ]

        for word in python_good:

            if word in metadata_text:
                score += 15

        for word in python_bad:

            if word in metadata_text:
                score -= 15

    # =====================================================
    # JAVA
    # =====================================================

    if "java" in query_lower:

        java_good = [
            "java",
            "spring",
            "j2ee",
            "backend",
            "web services"
        ]

        java_bad = [
            "python",
            "machine learning",
            "tensorflow"
        ]

        for word in java_good:

            if word in metadata_text:
                score += 15

        for word in java_bad:

            if word in metadata_text:
                score -= 20

    # =====================================================
    # FRONTEND
    # =====================================================

    if "frontend" in query_lower:

        frontend_good = [
            "frontend",
            "react",
            "angular",
            "javascript",
            "css",
            "html",
            "ui"
        ]

        frontend_bad = [
            "backend",
            "server",
            "database"
        ]

        for word in frontend_good:

            if word in metadata_text:
                score += 15

        for word in frontend_bad:

            if word in metadata_text:
                score -= 20

    # =====================================================
    # GENERAL WORD MATCHING
    # =====================================================

    query_words = query_lower.split()

    for word in query_words:

        if len(word) <= 2:
            continue

        if word in metadata_text:
            score += 3

    # =====================================================
    # SENIORITY MATCHING
    # =====================================================

    for seniority, keywords in SENIORITY_KEYWORDS.items():

        if seniority in query_lower:

            for keyword in keywords:

                if keyword in metadata_text:
                    score += 5

    return score


def build_recommendation(
    doc,
    score
):

    metadata = doc.metadata

    return {

        "name": metadata.get(
            "name",
            "Unknown Assessment"
        ),

        "url": metadata.get(
            "url",
            ""
        ),

        "test_type": metadata.get(
            "test_type",
            "Assessment"
        ),

        "description": metadata.get(
            "description",
            "SHL assessment recommendation."
        ),

        "job_levels": metadata.get(
            "job_levels",
            []
        ),

        "score": score
    }


def generate_recommendations(
    query: str,
    state: dict
):

    docs = retrieve_assessments(query)

    ranked_results = []

    query_lower = query.lower()

    # =====================================================
    # SCORE DOCUMENTS
    # =====================================================

    for doc in docs:

        metadata = doc.metadata

        metadata_text = f"""
        {metadata.get('name', '')}
        {metadata.get('description', '')}
        """.lower()

        # =================================================
        # STRICT FILTERS
        # =================================================

        if "backend" in query_lower:

            backend_required = [
                "backend",
                "api",
                "server",
                "database",
                "java",
                "python",
                "software",
                "django",
                "flask",
                "spring",
                "fastapi"
            ]

            if not any(
                word in metadata_text
                for word in backend_required
            ):
                continue

        if "machine learning" in query_lower:

            ml_required = [
                "python",
                "machine learning",
                "ai",
                "analytics",
                "data science"
            ]

            if not any(
                word in metadata_text
                for word in ml_required
            ):
                continue

        if "java" in query_lower:

            java_required = [
                "java",
                "spring",
                "j2ee",
                "web services"
            ]

            if not any(
                word in metadata_text
                for word in java_required
            ):
                continue

        if "python" in query_lower:

            python_required = [
                "python",
                "django",
                "flask",
                "fastapi"
            ]

            if not any(
                word in metadata_text
                for word in python_required
            ):
                continue

        score = calculate_keyword_score(
            query,
            metadata
        )

        ranked_results.append({
            "doc": doc,
            "score": score
        })

    # =====================================================
    # SORT RESULTS
    # =====================================================

    ranked_results = sorted(
        ranked_results,
        key=lambda x: x["score"],
        reverse=True
    )

    # =====================================================
    # FILTER RESULTS
    # =====================================================

    filtered_results = []

    for item in ranked_results:

        if item["score"] >= 15:

            filtered_results.append(item)

    # =====================================================
    # TAKE TOP 5
    # =====================================================

    filtered_results = filtered_results[:5]

    recommendations = []

    for item in filtered_results:

        recommendations.append(

            build_recommendation(
                item["doc"],
                item["score"]
            )
        )

    # =====================================================
    # FALLBACK
    # =====================================================

    if len(recommendations) == 0:

        recommendations = [

            build_recommendation(
                doc,
                0
            )

            for doc in docs[:5]
        ]

    return recommendations