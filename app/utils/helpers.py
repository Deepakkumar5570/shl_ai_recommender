def build_reply(state, recommendations):

    total = len(recommendations)

    role = state.get("role") or "professionals"

    seniority = state.get("seniority") or ""

    capabilities = []

    if state["needs_technical"]:
        capabilities.append("technical")

    if state["needs_personality"]:
        capabilities.append("personality")

    if state["needs_leadership"]:
        capabilities.append("leadership")

    capability_text = ", ".join(capabilities)

    return (
        f"Here are {total} SHL assessments suitable for "
        f"{seniority} {role} hiring needs focusing on {capability_text} evaluation."
    )