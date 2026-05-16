SATISFACTION_KEYWORDS = [
    "perfect",
    "thanks",
    "thank you",
    "great",
    "looks good",
    "done",
    "that works",
    "exactly"
]


def should_end_conversation(messages):

    if not messages:
        return False

    latest_message = messages[-1]["content"].lower()

    for keyword in SATISFACTION_KEYWORDS:
        if keyword in latest_message:
            return True

    return False