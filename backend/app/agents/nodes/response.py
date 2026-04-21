from app.agents.state import AgentState
from app.core.llm import llm
from app.core.exceptions import LLMError, DocumentNotFoundError
from app.utils.logger import logger


def generate_node(state: AgentState) -> dict:
    question = state["question"]
    category = state.get("category", "general")
    documents = state.get("documents", [])
    
    if not documents:
        raise DocumentNotFoundError(
            "No relevant documents found for the query. Please try rephrasing your question."
        )
    
    context = "\n\n".join([
        f"Document {i+1}:\n{doc['text']}"
        for i, doc in enumerate(documents)
    ])
    
    category_guidance = {
        "order": "Focus on order details, refund policies, return procedures, and billing information.",
        "shipping": "Focus on delivery times, tracking information, shipping costs, and package handling.",
        "general": "Provide helpful information about accounts, policies, and general inquiries."
    }
    
    guidance = category_guidance.get(category, category_guidance["general"])
    
    prompt = f"""You are a helpful customer support assistant specializing in {category}-related queries.
{guidance}

Answer the question based on the context provided.

Context:
{context}

Question: {question}

Answer: Provide a clear, concise answer based on the context. If the context doesn't contain relevant information, say so."""
    
    try:
        response = llm.invoke(prompt)
        
        if not response.content or not response.content.strip():
            logger.error("LLM returned empty response")
            raise LLMError("LLM returned empty response")
        
        logger.info(f"Response generated | Category: {category} | Length: {len(response.content)} chars")
    
    except Exception as e:
        logger.error(f"Response generation failed | Error: {str(e)}")
        raise LLMError(f"Failed to generate response: {str(e)}")
    
    sources = [
        {
            "text": doc["text"],
            "score": doc["score"]
        }
        for doc in documents
    ]
    
    return {
        "answer": response.content,
        "sources": sources
    }
