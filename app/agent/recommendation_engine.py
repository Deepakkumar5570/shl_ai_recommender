from app.retrieval.retriever import retrieve_assessments


def generate_recommendations(query: str):

    docs = retrieve_assessments(query)

    recommendations = []

    for doc in docs[:5]:
        recommendations.append({
            "name": doc.metadata.get("name"),
            "url": doc.metadata.get("url"),
            "test_type": doc.metadata.get("test_type")
        })

    return recommendations