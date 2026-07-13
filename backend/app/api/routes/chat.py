from fastapi import APIRouter, Response
from app.models.schemas import ChatRequest, ChatResponse
from app.agents.graph import run_agent, _checkpointer
from app.core.exceptions import InvalidInputError

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message or not request.message.strip():
        raise InvalidInputError("Message cannot be empty")

    if request.limit < 1 or request.limit > 10:
        raise InvalidInputError("Limit must be between 1 and 10")

    result = run_agent(request.message, limit=request.limit, thread_id=request.thread_id)
    return ChatResponse(**result)


@router.delete("/chat/{thread_id}", status_code=204)
async def clear_thread(thread_id: str):
    if not thread_id or not thread_id.strip():
        raise InvalidInputError("Thread ID cannot be empty")
    _checkpointer.delete_thread(thread_id)
    return Response(status_code=204)
