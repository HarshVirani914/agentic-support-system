from app.agents.state import AgentState
from app.core.vectorstore import vector_store
from app.core.reranker import reranker
from app.core.exceptions import VectorSearchError
from app.utils.logger import logger

CANDIDATE_LIMIT = 20


def _search_and_rerank(query: str, limit: int) -> list[dict]:
    candidates = vector_store.search(query, limit=CANDIDATE_LIMIT)
    return reranker.rerank(query, candidates, top_k=limit)


def order_search_node(state: AgentState) -> dict:
    question = state["question"]
    limit = state.get("limit", 3)

    if not question or not question.strip():
        raise VectorSearchError("Question cannot be empty")

    try:
        enhanced_query = f"order purchase refund return billing payment: {question}"
        results = _search_and_rerank(enhanced_query, limit)

        logger.info(f"Order Search | Found {len(results)} docs | Limit: {limit}")

        return {"documents": results}

    except Exception as e:
        logger.error(f"Order search failed | Error: {str(e)}")
        raise VectorSearchError(f"Failed to search order documents: {str(e)}")


def shipping_search_node(state: AgentState) -> dict:
    question = state["question"]
    limit = state.get("limit", 3)

    if not question or not question.strip():
        raise VectorSearchError("Question cannot be empty")

    try:
        enhanced_query = f"shipping delivery tracking package: {question}"
        results = _search_and_rerank(enhanced_query, limit)

        logger.info(f"Shipping Search | Found {len(results)} docs | Limit: {limit}")

        return {"documents": results}

    except Exception as e:
        logger.error(f"Shipping search failed | Error: {str(e)}")
        raise VectorSearchError(f"Failed to search shipping documents: {str(e)}")


def general_search_node(state: AgentState) -> dict:
    question = state["question"]
    limit = state.get("limit", 3)

    if not question or not question.strip():
        raise VectorSearchError("Question cannot be empty")

    try:
        results = _search_and_rerank(question, limit)

        logger.info(f"General Search | Found {len(results)} docs | Limit: {limit}")

        return {"documents": results}

    except Exception as e:
        logger.error(f"General search failed | Error: {str(e)}")
        raise VectorSearchError(f"Failed to search documents: {str(e)}")
