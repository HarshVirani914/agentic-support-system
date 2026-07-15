from unittest.mock import patch, MagicMock
from app.agents.nodes.grade import grade_node, LOW_CONFIDENCE_FALLBACK


@patch("app.agents.nodes.grade.llm")
def test_grade_node_marks_grounded_answer(mock_llm):
    mock_llm.invoke.return_value = MagicMock(content="GROUNDED: yes\nREASON: matches source text")

    state = {
        "question": "What is your refund policy?",
        "answer": "Refunds within 30 days.",
        "documents": [{"text": "Refunds within 30 days.", "score": 0.9}],
        "retry_count": 0,
    }
    result = grade_node(state)

    assert result["grounded"] is True
    assert result["retry_count"] == 0


@patch("app.agents.nodes.grade.llm")
def test_grade_node_rewrites_query_when_ungrounded(mock_llm):
    mock_llm.invoke.side_effect = [
        MagicMock(content="GROUNDED: no\nREASON: answer not supported by sources"),
        MagicMock(content="refund policy timeframe days"),
    ]

    state = {
        "question": "What is your refund policy?",
        "answer": "We offer free shipping.",
        "documents": [{"text": "Shipping is free.", "score": 0.9}],
        "retry_count": 0,
    }
    result = grade_node(state)

    assert result["grounded"] is False
    assert result["retry_count"] == 1
    assert result["question"] == "refund policy timeframe days"


@patch("app.agents.nodes.grade.llm")
def test_grade_node_returns_fallback_answer_when_retries_exhausted(mock_llm):
    mock_llm.invoke.return_value = MagicMock(
        content="GROUNDED: no\nREASON: still not supported by sources"
    )

    state = {
        "question": "Why hasn't my return been refunded?",
        "answer": "Some ungrounded guess about a policy.",
        "documents": [{"text": "unrelated document", "score": 0.5}],
        "retry_count": 2,
    }
    result = grade_node(state)

    assert result["grounded"] is False
    assert result["retry_count"] == 2
    assert result["answer"] == LOW_CONFIDENCE_FALLBACK
    # No rewrite call should be made once retries are exhausted.
    assert mock_llm.invoke.call_count == 1
