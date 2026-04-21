from app.agents.state import AgentState
from app.core.vectorstore import vector_store
from app.core.exceptions import VectorSearchError
from app.utils.logger import logger


def order_search_node(state: AgentState) -> dict:
    question = state["question"]
    limit = state.get("limit", 3)
    
    if not question or not question.strip():
        raise VectorSearchError("Question cannot be empty")
    
    try:
        enhanced_query = f"order purchase refund return billing payment: {question}"
        
        results = vector_store.search(enhanced_query, limit=limit)
        
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
        
        results = vector_store.search(enhanced_query, limit=limit)
        
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
        results = vector_store.search(question, limit=limit)
        
        logger.info(f"General Search | Found {len(results)} docs | Limit: {limit}")
        
        return {"documents": results}
    
    except Exception as e:
        logger.error(f"General search failed | Error: {str(e)}")
        raise VectorSearchError(f"Failed to search documents: {str(e)}")
