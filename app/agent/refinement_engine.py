def detect_refinement(messages):

    if len(messages) < 2:
        return False

    latest_message = messages[-1]["content"].lower()

    refinement_keywords = [
        "add",
        "also",
        "include",
        "instead",
        "change",
        "update",
        "remove"
    ]

    for keyword in refinement_keywords:
        if keyword in latest_message:
            return True

    return False