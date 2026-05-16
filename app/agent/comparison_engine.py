from app.retrieval.retriever import retrieve_assessments


def compare_assessments(query: str):

    docs = retrieve_assessments(query)

    if len(docs) < 2:

        return (
            "I could not find enough SHL assessments to compare.",
            []
        )

    first = docs[0]
    second = docs[1]

    comparison_reply = f"""
{first.metadata.get("name")} focuses on {first.metadata.get("test_type")}, while {second.metadata.get("name")} focuses on {second.metadata.get("test_type")}. Both assessments evaluate different capabilities based on SHL catalog information.
"""

    recommendations = []

    for doc in [first, second]:

        recommendations.append({
            "name": doc.metadata.get("name"),
            "url": doc.metadata.get("url"),
            "test_type": str(doc.metadata.get("test_type", "Unknown"))
        })

    return comparison_reply, recommendations