from app.agents.state import AgentState
from app.utils.logger import logger


def route_by_category(state: AgentState) -> str:
    category = state.get("category", "general")
    
    route_map = {
        "order": "order_search",
        "shipping": "shipping_search",
        "general": "general_search"
    }
    
    next_node = route_map.get(category, "general_search")
    
    logger.info(f"Router | Category: {category} → Node: {next_node}")
    
    return next_node
