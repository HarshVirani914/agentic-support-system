from typing import TypedDict, Annotated
from langgraph.graph import add_messages


class AgentState(TypedDict):
    question: str
    limit: int
    category: str
    documents: list[dict]
    answer: str
    sources: list[dict]
    messages: Annotated[list[dict], add_messages]
    retry_count: int
    grounded: bool
    grading_reason: str
