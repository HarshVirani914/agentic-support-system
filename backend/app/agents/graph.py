"""
LangGraph Workflow Definition

Connects search and generate nodes into a sequential workflow.
"""

from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes.search import search_node
from app.agents.nodes.response import generate_node
from app.utils.logger import logger


def create_agent_graph():
    """
    Creates the agent graph workflow.

    Flow:
        START → search_node → generate_node → END

    Returns:
        Compiled graph ready for execution
    """

    # Initialize graph with state schema
    workflow = StateGraph(AgentState)

    # Add nodes (the actual work functions)
    workflow.add_node("search", search_node)
    workflow.add_node("generate", generate_node)

    # Define edges (execution flow)
    workflow.set_entry_point("search")  # Start here
    workflow.add_edge("search", "generate")  # Then go here
    workflow.add_edge("generate", END)  # Then finish

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
        "limit": limit,  # Pass limit through state
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
            f"Agent execution complete | Answer length: {len(result.get('answer', ''))} chars"
        )
    except Exception as e:
        logger.error(f"Agent execution failed | Error: {str(e)}")
        raise

    # Return final state
    return {"answer": result["answer"], "sources": result["sources"]}
