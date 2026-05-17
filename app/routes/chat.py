from fastapi import APIRouter
from pydantic import BaseModel

from app.agent.clarification_engine import (
    needs_clarification,
    generate_clarification_question
)

from app.agent.recommendation_engine import (
    generate_recommendations
)

from app.agent.conversation_state import (
    conversation_state
)

router = APIRouter()


class ChatRequest(BaseModel):
    messages: list


@router.post("/chat")
def chat(request: ChatRequest):

    # =========================
    # VALIDATION
    # =========================

    if not request.messages:
        return {
            "reply": "No messages received.",
            "recommendations": []
        }

    query = request.messages[-1]["content"]

    lower_query = query.lower()

    # =========================
    # RESET STATE FOR NEW ROLE
    # =========================

    new_role_keywords = [
        "developer",
        "engineer",
        "analyst",
        "manager",
        "python",
        "java",
        "hiring",
        "frontend",
        "backend",
        "data scientist",
        "devops"
    ]

    if any(word in lower_query for word in new_role_keywords):

        conversation_state.clear()

    state = conversation_state

    # =========================
    # STORE USER INPUT
    # =========================

    if "role" not in state:

        state["role"] = query

    elif "seniority" not in state:

        state["seniority"] = query

    # =========================
    # ASK CLARIFICATION
    # =========================

    if needs_clarification(state):

        question = generate_clarification_question(state)

        return {
            "reply": question,
            "recommendations": []
        }

    # =========================
    # BUILD FINAL QUERY
    # =========================

    final_query = f"""
    {state.get('role', '')}
    {state.get('seniority', '')}
    """

    # =========================
    # GENERATE RECOMMENDATIONS
    # =========================

    try:

        recommendations = generate_recommendations(
            final_query,
            state
        )

    except Exception as e:

        print("RECOMMENDATION ERROR:", str(e))

        return {
            "reply": "Recommendation engine failed.",
            "recommendations": []
        }

    # =========================
    # REPLY
    # =========================

    reply = (
        f"Here are {len(recommendations)} SHL assessments "
        f"suitable for {state.get('seniority')} "
        f"{state.get('role')} hiring needs."
    )

    # =========================
    # CLEAR STATE
    # =========================

    conversation_state.clear()

    # =========================
    # RETURN RESPONSE
    # =========================

    return {
        "reply": reply,
        "recommendations": recommendations
    }