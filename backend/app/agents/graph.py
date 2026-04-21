from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes.classifier import classifier_node
from app.agents.nodes.specialized_search import (
    order_search_node,
    shipping_search_node,
    general_search_node,
)
from app.agents.nodes.response import generate_node
from app.agents.router import route_by_category
from app.utils.logger import logger


def create_agent_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("classifier", classifier_node)
    workflow.add_node("order_search", order_search_node)
    workflow.add_node("shipping_search", shipping_search_node)
    workflow.add_node("general_search", general_search_node)
    workflow.add_node("generate", generate_node)

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
    workflow.add_edge("generate", END)

    graph = workflow.compile()
    return graph


agent_graph = create_agent_graph()


def run_agent(question: str, limit: int = 3) -> dict:
    initial_state: AgentState = {
        "question": question,
        "limit": limit,
        "category": "",
        "documents": [],
        "answer": "",
        "sources": [],
    }

    logger.info(
        f"Agent execution started | Question: {question[:50]}... | Limit: {limit}"
    )

    try:
        result = agent_graph.invoke(initial_state)
        logger.info(
            f"Agent execution complete | Category: {result.get('category', 'unknown')} | Answer length: {len(result.get('answer', ''))} chars"
        )
    except Exception as e:
        logger.error(f"Agent execution failed | Error: {str(e)}")
        raise

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "category": result.get("category", "general")
    }
