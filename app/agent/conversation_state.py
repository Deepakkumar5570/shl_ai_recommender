import re


def extract_context(messages):
    text = " ".join([m["content"] for m in messages])

    state = {
        "role": None,
        "seniority": None,
        "needs_personality": False,
        "needs_technical": False,
        "purpose": None
    }

    text_lower = text.lower()

    if "java" in text_lower:
        state["role"] = "Java Developer"

    if "senior" in text_lower:
        state["seniority"] = "Senior"

    if "mid" in text_lower:
        state["seniority"] = "Mid-Professional"

    if "personality" in text_lower:
        state["needs_personality"] = True

    if "technical" in text_lower:
        state["needs_technical"] = True

    if "selection" in text_lower:
        state["purpose"] = "Selection"

    return state