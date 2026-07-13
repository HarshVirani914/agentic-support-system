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


MAX_RETRIES = 2


def route_after_grade(state: AgentState) -> str:
    if state.get("grounded", False):
        return "end"

    if state.get("retry_count", 0) >= MAX_RETRIES:
        return "end"

    category = state.get("category", "general")
    route_map = {
        "order": "order_search",
        "shipping": "shipping_search",
        "general": "general_search",
    }
    next_node = route_map.get(category, "general_search")

    logger.info(f"Grade Router | Retry {state.get('retry_count', 0)} → Node: {next_node}")

    return next_node
