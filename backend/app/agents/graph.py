"""
LangGraph Workflow Definition

Multi-agent system with conditional routing based on query category.
"""

from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes.classifier import classifier_node
from app.agents.nodes.specialized_search import (
    order_search_node,
    shipping_search_node,
    general_search_node
)
from app.agents.nodes.response import generate_node
from app.agents.router import route_by_category
from app.utils.logger import logger


def create_agent_graph():
    """
    Creates the multi-agent graph workflow with conditional routing.

    Flow:
        START → classifier → (conditional routing) → specialized_search → generate → END
        
    Conditional Routing:
        - "order" category → order_search_node
        - "shipping" category → shipping_search_node  
        - "general" category → general_search_node
        
    All search nodes converge to generate_node for response creation.

    Returns:
        Compiled graph ready for execution
    """

    # Initialize graph with state schema
    workflow = StateGraph(AgentState)

    # Add nodes (the actual work functions)
    workflow.add_node("classifier", classifier_node)
    workflow.add_node("order_search", order_search_node)
    workflow.add_node("shipping_search", shipping_search_node)
    workflow.add_node("general_search", general_search_node)
    workflow.add_node("generate", generate_node)

    # Define entry point
    workflow.set_entry_point("classifier")
    
    # Add conditional edges based on category
    # This is the KEY feature - dynamic routing!
    workflow.add_conditional_edges(
        "classifier",  # From this node
        route_by_category,  # Use this function to decide
        {
            "order_search": "order_search",  # If returns "order_search", go here
            "shipping_search": "shipping_search",  # If returns "shipping_search", go here
            "general_search": "general_search"  # If returns "general_search", go here
        }
    )
    
    # All search nodes flow to generate
    workflow.add_edge("order_search", "generate")
    workflow.add_edge("shipping_search", "generate")
    workflow.add_edge("general_search", "generate")
    
    # Generate flows to end
    workflow.add_edge("generate", END)

    # Compile into executable graph
    graph = workflow.compile()

    return graph


# Create global graph instance
agent_graph = create_agent_graph()


def run_agent(question: str, limit: int = 3) -> dict:
    """
    Execute the agent graph with a question.

    Args:
        question: User's question
        limit: Number of documents to retrieve (not used yet, for future)

    Returns:
        dict with answer and sources
    """

    # Initialize state with user question and parameters
    initial_state: AgentState = {
        "question": question,
        "limit": limit,
        "category": "",  # Will be set by classifier
        "documents": [],
        "answer": "",
        "sources": [],
    }

    # Execute graph
    logger.info(
        f"Agent execution started | Question: {question[:50]}... | Limit: {limit}"
    )

    try:
        result = agent_graph.invoke(initial_state)
        logger.info(
            f"Agent execution complete | Category: {result.get('category', 'unknown')} | Answer length: {len(result.get('answer', ''))} chars"
        )
    except Exception as e:
        logger.error(f"Agent execution failed | Error: {str(e)}")
        raise

    # Return final state
    return {"answer": result["answer"], "sources": result["sources"]}
