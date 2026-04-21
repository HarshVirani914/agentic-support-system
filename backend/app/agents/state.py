from typing import TypedDict, Annotated
from langgraph.graph import add_messages


class AgentState(TypedDict):
    question: str
    limit: int
    category: str
    documents: list[dict]
    answer: str
    sources: list[dict]
