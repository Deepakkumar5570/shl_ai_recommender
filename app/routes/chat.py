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
    # FINAL QUERY
    # =========================

    final_query = f"""
    {state.get('role', '')}
    {state.get('seniority', '')}
    """

    recommendations = generate_recommendations(
        final_query,
        state
    )

    reply = (
        f"Here are {len(recommendations)} SHL assessments "
        f"suitable for {state.get('seniority')} "
        f"{state.get('role')} hiring needs."
    )

    # =========================
    # CLEAR STATE AFTER RESULT
    # =========================

    conversation_state.clear()

    return {
        "reply": reply,
        "recommendations": recommendations
    }