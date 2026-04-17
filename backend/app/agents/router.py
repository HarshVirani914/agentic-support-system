"""
Router Functions - Conditional routing logic for LangGraph

These functions determine which node to execute next based on state.
Used with LangGraph's conditional edges feature.
"""

from app.agents.state import AgentState
from app.utils.logger import logger


def route_by_category(state: AgentState) -> str:
    """
    Routes to specialized search nodes based on query category.
    
    This function is used by LangGraph's conditional_edges to determine
    which node to execute next.
    
    Input from state:
        - category: Query category determined by classifier
    
    Returns:
        str: Name of the next node to execute
            - "order_search" for order-related queries
            - "shipping_search" for shipping-related queries
            - "general_search" for everything else
    """
    
    category = state.get("category", "general")
    
    # Map category to node name
    route_map = {
        "order": "order_search",
        "shipping": "shipping_search",
        "general": "general_search"
    }
    
    next_node = route_map.get(category, "general_search")
    
    logger.info(f"Router | Category: {category} → Node: {next_node}")
    
    return next_node
