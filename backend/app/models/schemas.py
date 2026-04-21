from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    limit: int = 3


class Source(BaseModel):
    text: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    category: str


class HealthResponse(BaseModel):
    status: str
    version: str
