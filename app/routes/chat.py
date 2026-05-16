from fastapi import APIRouter

from app.models.request_models import ChatRequest
from app.models.response_models import ChatResponse

from app.agent.conversation_state import extract_context
from app.agent.clarification_engine import needs_clarification
from app.agent.recommendation_engine import generate_recommendations

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):

    messages = [m.dict() for m in request.messages]

    state = extract_context(messages)

    clarification_needed, question = needs_clarification(state)

    if clarification_needed:
        return {
            "reply": question,
            "recommendations": [],
            "end_of_conversation": False
        }

    query = " ".join([m["content"] for m in messages])

    recommendations = generate_recommendations(query)

    return {
        "reply": "Here are recommended SHL assessments.",
        "recommendations": recommendations,
        "end_of_conversation": False
    }