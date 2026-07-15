from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import HumanMessage, AIMessage
from psycopg_pool import ConnectionPool
from app.agents.state import AgentState
from app.agents.nodes.classifier import classifier_node
from app.agents.nodes.specialized_search import (
    order_search_node,
    shipping_search_node,
    general_search_node,
)
from app.agents.nodes.response import generate_node
from app.agents.nodes.grade import grade_node
from app.agents.router import route_by_category, route_after_grade
from app.config import settings
from app.utils.logger import logger


def create_agent_graph(checkpointer: BaseCheckpointSaver) -> CompiledStateGraph:
    workflow = StateGraph(AgentState)

    workflow.add_node("classifier", classifier_node)
    workflow.add_node("order_search", order_search_node)
    workflow.add_node("shipping_search", shipping_search_node)
    workflow.add_node("general_search", general_search_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("grade", grade_node)

    workflow.set_entry_point("classifier")

    workflow.add_conditional_edges(
        "classifier",
        route_by_category,
        {
            "order_search": "order_search",
            "shipping_search": "shipping_search",
            "general_search": "general_search",
        },
    )

    workflow.add_edge("order_search", "generate")
    workflow.add_edge("shipping_search", "generate")
    workflow.add_edge("general_search", "generate")
    workflow.add_edge("generate", "grade")

    workflow.add_conditional_edges(
        "grade",
        route_after_grade,
        {
            "order_search": "order_search",
            "shipping_search": "shipping_search",
            "general_search": "general_search",
            "end": END,
        },
    )

    return workflow.compile(checkpointer=checkpointer)


_pool = ConnectionPool(
    conninfo=settings.DATABASE_URL,
    min_size=0,
    max_size=5,
    max_idle=120,
    check=ConnectionPool.check_connection,
    kwargs={"autocommit": True, "prepare_threshold": 0},
)
_checkpointer = PostgresSaver(_pool)
_checkpointer.setup()

agent_graph = create_agent_graph(checkpointer=_checkpointer)


def run_agent(question: str, limit: int = 3, thread_id: str = "default") -> dict:
    initial_state: AgentState = {
        "question": question,
        "original_question": question,
        "limit": limit,
        "category": "",
        "documents": [],
        "answer": "",
        "sources": [],
        "messages": [],
        "retry_count": 0,
        "grounded": False,
        "grading_reason": "",
        "retries_exhausted": False,
    }

    config = {"configurable": {"thread_id": thread_id}}

    logger.info(
        f"Agent execution started | Question: {question[:50]}... | Limit: {limit} | Thread: {thread_id}"
    )

    try:
        result = agent_graph.invoke(initial_state, config=config)
        logger.info(
            f"Agent execution complete | Category: {result.get('category', 'unknown')} | Answer length: {len(result.get('answer', ''))} chars"
        )
        # Record the finished turn once, outside the internal retry loop, so
        # multi-turn context is available to the classifier/generator on the
        # next call without duplicating a message per reflection retry.
        agent_graph.update_state(
            config,
            {
                "messages": [
                    HumanMessage(content=question),
                    AIMessage(content=result["answer"]),
                ]
            },
        )
    except Exception as e:
        logger.error(f"Agent execution failed | Error: {str(e)}")
        raise

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "category": result.get("category", "general"),
        "retry_count": result.get("retry_count", 0),
        "grounded": result.get("grounded", True),
        "grading_reason": result.get("grading_reason", ""),
    }
