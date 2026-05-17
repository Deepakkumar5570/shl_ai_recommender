from app.utils.helpers import get_metadata


def rerank_documents(docs, state):

    ranked = []

    for doc in docs:

        score = 0

        metadata = get_metadata(doc)

        job_levels = metadata.get("job_levels", [])
        keys = metadata.get("keys", [])
        name = metadata.get("name", "")

        if state["seniority"] in job_levels:
            score += 5

        if state["needs_personality"]:
            if any("Personality" in k for k in keys):
                score += 5

        if state["needs_technical"]:
            if any("Knowledge" in k for k in keys):
                score += 5

        if state["needs_leadership"]:
            if "leadership" in name.lower():
                score += 5

        if state["needs_cognitive"]:
            if any("Ability" in k for k in keys):
                score += 5

        ranked.append((score, doc))

    ranked.sort(key=lambda x: x[0], reverse=True)

    return [doc for score, doc in ranked]