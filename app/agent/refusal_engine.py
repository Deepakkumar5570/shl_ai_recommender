def should_refuse(state):

    if state["off_topic"]:
        return True

    return False


def refusal_response():

    return {
        "reply": "I can only help with SHL assessment recommendations and comparisons.",
        "recommendations": [],
        "end_of_conversation": False
    }