def needs_clarification(state):

    if not state["role"]:
        return True, "What role are you hiring for?"

    if not state["seniority"]:
        return True, "What seniority level is this role for?"

    return False, None