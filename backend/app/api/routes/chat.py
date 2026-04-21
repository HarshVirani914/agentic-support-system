from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.agents.graph import run_agent
from app.core.exceptions import InvalidInputError

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message or not request.message.strip():
        raise InvalidInputError("Message cannot be empty")
    
    if request.limit < 1 or request.limit > 10:
        raise InvalidInputError("Limit must be between 1 and 10")
    
    result = run_agent(request.message, limit=request.limit)
    return ChatResponse(**result)
