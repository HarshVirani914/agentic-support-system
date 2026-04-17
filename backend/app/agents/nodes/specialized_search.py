"""
Specialized Search Nodes - Category-specific document retrieval

Each search node is optimized for a specific query category,
providing more accurate and relevant results.
"""

from app.agents.state import AgentState
from app.core.vectorstore import vector_store
from app.core.exceptions import VectorSearchError
from app.utils.logger import logger


def order_search_node(state: AgentState) -> dict:
    """
    Specialized search for order-related queries.
    
    Optimized for: orders, refunds, returns, billing, payments
    
    Input from state:
        - question: User's query
        - limit: Number of documents to retrieve
    
    Adds to state:
        - documents: Retrieved documents
    
    Returns:
        dict with updates to merge into state
    """
    
    question = state["question"]
    limit = state.get("limit", 3)
    
    if not question or not question.strip():
        raise VectorSearchError("Question cannot be empty")
    
    try:
        # Enhance query with category context for better retrieval
        enhanced_query = f"order purchase refund return billing payment: {question}"
        
        results = vector_store.search(enhanced_query, limit=limit)
        
        logger.info(f"Order Search | Found {len(results)} docs | Limit: {limit}")
        
        return {"documents": results}
    
    except Exception as e:
        logger.error(f"Order search failed | Error: {str(e)}")
        raise VectorSearchError(f"Failed to search order documents: {str(e)}")


def shipping_search_node(state: AgentState) -> dict:
    """
    Specialized search for shipping-related queries.
    
    Optimized for: delivery, tracking, shipping times, costs
    
    Input from state:
        - question: User's query
        - limit: Number of documents to retrieve
    
    Adds to state:
        - documents: Retrieved documents
    
    Returns:
        dict with updates to merge into state
    """
    
    question = state["question"]
    limit = state.get("limit", 3)
    
    if not question or not question.strip():
        raise VectorSearchError("Question cannot be empty")
    
    try:
        # Enhance query with category context
        enhanced_query = f"shipping delivery tracking package: {question}"
        
        results = vector_store.search(enhanced_query, limit=limit)
        
        logger.info(f"Shipping Search | Found {len(results)} docs | Limit: {limit}")
        
        return {"documents": results}
    
    except Exception as e:
        logger.error(f"Shipping search failed | Error: {str(e)}")
        raise VectorSearchError(f"Failed to search shipping documents: {str(e)}")


def general_search_node(state: AgentState) -> dict:
    """
    General search for all other queries.
    
    Optimized for: account, policies, general information
    
    Input from state:
        - question: User's query
        - limit: Number of documents to retrieve
    
    Adds to state:
        - documents: Retrieved documents
    
    Returns:
        dict with updates to merge into state
    """
    
    question = state["question"]
    limit = state.get("limit", 3)
    
    if not question or not question.strip():
        raise VectorSearchError("Question cannot be empty")
    
    try:
        # Use original query without enhancement (general search)
        results = vector_store.search(question, limit=limit)
        
        logger.info(f"General Search | Found {len(results)} docs | Limit: {limit}")
        
        return {"documents": results}
    
    except Exception as e:
        logger.error(f"General search failed | Error: {str(e)}")
        raise VectorSearchError(f"Failed to search documents: {str(e)}")
