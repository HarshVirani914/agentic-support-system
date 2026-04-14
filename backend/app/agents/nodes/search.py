"""
Search Node - Retrieves relevant documents from vector store
"""

from app.agents.state import AgentState
from app.core.vectorstore import vector_store
from app.core.exceptions import VectorSearchError
from app.utils.logger import logger


def search_node(state: AgentState) -> dict:
    """
    Search node: Retrieves relevant documents based on the question.
    
    Input from state:
        - question: User's query
        - limit: Number of documents to retrieve
    
    Adds to state:
        - documents: Retrieved documents with scores
    
    Returns:
        dict with updates to merge into state
    """
    
    question = state["question"]
    limit = state.get("limit", 3)
    
    if not question or not question.strip():
        raise VectorSearchError("Question cannot be empty")
    
    try:
        # Search vector store for relevant documents
        results = vector_store.search(question, limit=limit)
        
        logger.info(f"Search complete | Found {len(results)} docs | Limit: {limit}")
        
        # Return updates to merge into state
        return {"documents": results}
    
    except Exception as e:
        logger.error(f"Search failed | Error: {str(e)}")
        raise VectorSearchError(f"Failed to search documents: {str(e)}")
