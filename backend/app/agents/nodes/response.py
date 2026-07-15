from app.agents.state import AgentState
from app.core.llm import llm
from app.core.exceptions import LLMError, DocumentNotFoundError
from app.utils.conversation import format_history
from app.utils.logger import logger


def generate_node(state: AgentState) -> dict:
    question = state.get("original_question") or state["question"]
    category = state.get("category", "general")
    documents = state.get("documents", [])
    history = format_history(state.get("messages", []))

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

    history_block = f"\nPrior conversation:\n{history}\n" if history else ""

    prompt = f"""You are a helpful customer support assistant specializing in {category}-related queries.
{guidance}

Answer the question using both the prior conversation and the context documents below, whichever
is actually relevant:
- If the user is asking you to recall something from earlier in this conversation (e.g. "do you
  remember my issue?", "what did I ask before?"), answer directly from the prior conversation —
  summarize what they told you. Don't ignore this in favor of unrelated policy documents.
- If the user is asking a policy question (refund windows, fees, timelines, eligibility), ground
  that factual content in the context documents below, not in your own guess.
- If neither the conversation nor the context actually answers the question, say so plainly and
  suggest contacting support with specifics (e.g. an order number) rather than guessing.
{history_block}
Context:
{context}

Question: {question}

Answer: Provide a clear, concise answer using the conversation and/or context above as appropriate."""
    
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
