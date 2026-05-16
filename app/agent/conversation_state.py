import re


ROLE_KEYWORDS = {
    "java": "Java Developer",
    "python": "Python Developer",
    "backend": "Backend Engineer",
    "frontend": "Frontend Engineer",
    "data scientist": "Data Scientist",
    "manager": "Manager",
    "leadership": "Leadership"
}


SENIORITY_MAP = {
    "entry": "Entry-Level",
    "junior": "Entry-Level",
    "mid": "Mid-Professional",
    "senior": "Mid-Professional",
    "manager": "Manager",
    "director": "Director",
    "executive": "Executive",
    "cxo": "Executive"
}


def extract_context(messages):

    text = " ".join([m["content"] for m in messages])

    text_lower = text.lower()

    state = {
        "role": None,
        "seniority": None,
        "needs_personality": False,
        "needs_technical": False,
        "needs_leadership": False,
        "needs_cognitive": False,
        "purpose": None,
        "comparison_request": False,
        "off_topic": False
    }

    for keyword, role in ROLE_KEYWORDS.items():
        if keyword in text_lower:
            state["role"] = role

    for keyword, level in SENIORITY_MAP.items():
        if keyword in text_lower:
            state["seniority"] = level

    if "comparison" in text_lower:
        state["comparison_request"] = True

    if "difference between" in text_lower:
        state["comparison_request"] = True

    if "compare" in text_lower:
        state["comparison_request"] = True

    if "personality" in text_lower:
        state["needs_personality"] = True

    if "technical" in text_lower:
        state["needs_technical"] = True

    if "leadership" in text_lower:
        state["needs_leadership"] = True

    if "cognitive" in text_lower:
        state["needs_cognitive"] = True

    if "communication" in text_lower:
        state["needs_personality"] = True

    if "stakeholder" in text_lower:
        state["needs_personality"] = True

    if "behavior" in text_lower:
        state["needs_personality"] = True

    if "coding" in text_lower:
        state["needs_technical"] = True

    if "developer" in text_lower:
        state["needs_technical"] = True

    if "selection" in text_lower:
        state["purpose"] = "Selection"

    if "development" in text_lower:
        state["purpose"] = "Development"

    if "difference between" in text_lower:
        state["comparison_request"] = True

    off_topic_keywords = [
        "salary",
        "legal",
        "politics",
        "movie",
        "sports"
    ]

    for keyword in off_topic_keywords:
        if keyword in text_lower:
            state["off_topic"] = True

    return state


# A simple in-memory conversation state dict used by routes/chat.py.
# `chat.py` imports `conversation_state` and expects a mutable mapping
# with a `clear()` method, so expose a plain dict here.
conversation_state = {}