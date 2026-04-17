"""
Classifier Node - Categorizes user queries for routing

Determines the intent/category of the user's question to route it
to the appropriate specialized agent.
"""

from app.agents.state import AgentState
from app.core.llm import llm
from app.utils.logger import logger


def classifier_node(state: AgentState) -> dict:
    """
    Classifies the user's question into a category.
    
    Categories:
        - order: Orders, purchases, refunds, billing
        - shipping: Delivery, tracking, shipping issues
        - general: Everything else (account, general info, policies)
    
    Input from state:
        - question: User's query
    
    Adds to state:
        - category: Determined category
    
    Returns:
        dict with updates to merge into state
    """
    
    question = state["question"]
    
    # Create classification prompt
    prompt = f"""You are a customer support query classifier. Categorize the following question into ONE of these categories:

Categories:
1. "order" - Questions about orders, purchases, refunds, returns, billing, payments
2. "shipping" - Questions about delivery, tracking, shipping times, shipping costs
3. "general" - Questions about accounts, passwords, policies, or anything else

Question: {question}

Respond with ONLY the category name (order, shipping, or general). No explanation.

Category:"""
    
    try:
        # Get classification from LLM
        response = llm.invoke(prompt)
        category = response.content.strip().lower()
        
        # Validate category (fallback to general if invalid)
        valid_categories = ["order", "shipping", "general"]
        if category not in valid_categories:
            logger.warning(f"Invalid category '{category}', defaulting to 'general'")
            category = "general"
        
        logger.info(f"Classifier | Question: '{question[:50]}...' | Category: {category}")
        
        return {"category": category}
    
    except Exception as e:
        logger.error(f"Classification failed | Error: {str(e)} | Defaulting to 'general'")
        return {"category": "general"}
