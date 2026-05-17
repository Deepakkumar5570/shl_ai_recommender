from app.retrieval.retriever import retrieve_assessments
from app.utils.helpers import get_metadata


def compare_assessments(query: str):

    docs = retrieve_assessments(query)

    if len(docs) < 2:

        return (
            "I could not find enough SHL assessments to compare.",
            []
        )

    first = docs[0]
    second = docs[1]

    first_metadata = get_metadata(first)
    second_metadata = get_metadata(second)

    comparison_reply = f"""
{first_metadata.get("name")} focuses on {first_metadata.get("test_type")}, while {second_metadata.get("name")} focuses on {second_metadata.get("test_type")}. Both assessments evaluate different capabilities based on SHL catalog information.
"""

    recommendations = []

    for doc in [first, second]:
        metadata = get_metadata(doc)

        recommendations.append({
            "name": metadata.get("name"),
            "url": metadata.get("url"),
            "test_type": str(metadata.get("test_type", "Unknown"))
        })

    return comparison_reply, recommendations