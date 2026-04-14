"""
Response Generation Node - Generates answers using LLM
"""

from app.agents.state import AgentState
from app.core.llm import llm
from app.core.exceptions import LLMError, DocumentNotFoundError
from app.utils.logger import logger


def generate_node(state: AgentState) -> dict:
    """
    Generate node: Creates answer using retrieved documents.
    
    Input from state:
        - question: User's query
        - documents: Retrieved documents from search node
    
    Adds to state:
        - answer: Generated answer
        - sources: Source documents for citation
    
    Returns:
        dict with updates to merge into state
    """
    
    question = state["question"]
    documents = state.get("documents", [])
    
    if not documents:
        raise DocumentNotFoundError(
            "No relevant documents found for the query. Please try rephrasing your question."
        )
    
    # Format context from documents
    context = "\n\n".join([
        f"Document {i+1}:\n{doc['text']}"
        for i, doc in enumerate(documents)
    ])
    
    # Create prompt for LLM
    prompt = f"""You are a helpful customer support assistant. Answer the question based on the context provided.

Context:
{context}

Question: {question}

Answer: Provide a clear, concise answer based on the context. If the context doesn't contain relevant information, say so."""
    
    try:
        # Generate answer
        response = llm.invoke(prompt)
        
        if not response.content or not response.content.strip():
            logger.error("LLM returned empty response")
            raise LLMError("LLM returned empty response")
        
        logger.info(f"Response generated | Length: {len(response.content)} chars")
    
    except Exception as e:
        logger.error(f"Response generation failed | Error: {str(e)}")
        raise LLMError(f"Failed to generate response: {str(e)}")
    
    # Prepare sources for response
    sources = [
        {
            "text": doc["text"],
            "score": doc["score"]
        }
        for doc in documents
    ]
    
    # Return updates to merge into state
    return {
        "answer": response.content,
        "sources": sources
    }
