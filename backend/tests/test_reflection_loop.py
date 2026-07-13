from unittest.mock import patch, MagicMock
from langgraph.checkpoint.memory import MemorySaver
from app.agents.graph import create_agent_graph


@patch("app.agents.nodes.grade.llm")
@patch("app.agents.nodes.specialized_search.reranker")
@patch("app.agents.nodes.specialized_search.vector_store")
@patch("app.agents.graph.generate_node")
@patch("app.agents.graph.classifier_node")
def test_reflection_loop_retries_once_then_ends(
    mock_classifier, mock_generate, mock_store, mock_reranker, mock_llm
):
    mock_classifier.return_value = {"category": "general"}
    mock_store.search.return_value = [{"text": "doc", "score": 0.5, "metadata": {}}]
    mock_reranker.rerank.return_value = [{"text": "doc", "score": 0.5, "metadata": {}}]
    mock_generate.return_value = {"answer": "answer", "sources": []}
    mock_llm.invoke.side_effect = [
        MagicMock(content="GROUNDED: no\nREASON: not supported"),
        MagicMock(content="rewritten query"),
        MagicMock(content="GROUNDED: yes\nREASON: now supported"),
    ]

    graph = create_agent_graph(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "t1"}}
    initial_state = {
        "question": "refund?",
        "limit": 3,
        "category": "",
        "documents": [],
        "answer": "",
        "sources": [],
        "messages": [],
        "retry_count": 0,
        "grounded": False,
        "grading_reason": "",
    }

    result = graph.invoke(initial_state, config=config)

    assert result["grounded"] is True
    assert result["retry_count"] == 1
    assert mock_store.search.call_count == 2  # initial + one retry
