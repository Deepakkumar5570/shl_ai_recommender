def needs_clarification(state):

    if "role" not in state:
        return True

    if "seniority" not in state:
        return True

    return False


def generate_clarification_question(state):

    if "role" not in state:
        return "What role are you hiring for?"

    if "seniority" not in state:
        return "What seniority level is this role for?"

    return None