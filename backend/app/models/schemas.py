from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    limit: int = 3
    thread_id: str = "default"


class Source(BaseModel):
    text: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    category: str
    retry_count: int = 0
    grounded: bool = True
    grading_reason: str = ""


class HealthResponse(BaseModel):
    status: str
    version: str
