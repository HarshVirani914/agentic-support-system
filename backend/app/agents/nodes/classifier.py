from app.agents.state import AgentState
from app.core.llm import llm
from app.utils.logger import logger


def classifier_node(state: AgentState) -> dict:
    question = state["question"]
    
    prompt = f"""You are a customer support query classifier. Categorize the following question into ONE of these categories:

Categories:
1. "order" - Questions about orders, purchases, refunds, returns, billing, payments
2. "shipping" - Questions about delivery, tracking, shipping times, shipping costs
3. "general" - Questions about accounts, passwords, policies, or anything else

Question: {question}

Respond with ONLY the category name (order, shipping, or general). No explanation.

Category:"""
    
    try:
        response = llm.invoke(prompt)
        category = response.content.strip().lower()
        
        valid_categories = ["order", "shipping", "general"]
        if category not in valid_categories:
            logger.warning(f"Invalid category '{category}', defaulting to 'general'")
            category = "general"
        
        logger.info(f"Classifier | Question: '{question[:50]}...' | Category: {category}")
        
        return {"category": category}
    
    except Exception as e:
        logger.error(f"Classification failed | Error: {str(e)} | Defaulting to 'general'")
        return {"category": "general"}
