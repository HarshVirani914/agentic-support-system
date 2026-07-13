from unittest.mock import patch
from app.core.reranker import Reranker


@patch("app.core.reranker.CrossEncoder")
def test_rerank_sorts_by_cross_encoder_score(mock_cross_encoder_cls):
    mock_model = mock_cross_encoder_cls.return_value
    mock_model.predict.return_value = [0.2, 0.9]

    reranker = Reranker()
    documents = [
        {"text": "low relevance doc", "score": 0.5, "metadata": {}},
        {"text": "high relevance doc", "score": 0.4, "metadata": {}},
    ]

    result = reranker.rerank("refund policy", documents, top_k=2)

    assert result[0]["text"] == "high relevance doc"
    assert result[0]["score"] == 0.9


@patch("app.core.reranker.CrossEncoder")
def test_rerank_truncates_to_top_k(mock_cross_encoder_cls):
    mock_model = mock_cross_encoder_cls.return_value
    mock_model.predict.return_value = [0.1, 0.5, 0.9, 0.3]

    reranker = Reranker()
    documents = [
        {"text": "doc1", "score": 0.5, "metadata": {}},
        {"text": "doc2", "score": 0.4, "metadata": {}},
        {"text": "doc3", "score": 0.3, "metadata": {}},
        {"text": "doc4", "score": 0.2, "metadata": {}},
    ]

    result = reranker.rerank("query", documents, top_k=2)

    assert len(result) == 2
    assert result[0]["text"] == "doc3"
    assert result[1]["text"] == "doc2"


@patch("app.core.reranker.CrossEncoder")
def test_rerank_returns_empty_list_for_empty_documents(mock_cross_encoder_cls):
    reranker = Reranker()
    result = reranker.rerank("query", [], top_k=5)

    assert result == []
    mock_cross_encoder_cls.return_value.predict.assert_not_called()


@patch("app.core.reranker.CrossEncoder")
def test_rerank_preserves_metadata(mock_cross_encoder_cls):
    mock_model = mock_cross_encoder_cls.return_value
    mock_model.predict.return_value = [0.8, 0.6]

    reranker = Reranker()
    documents = [
        {"text": "doc1", "score": 0.5, "metadata": {"source": "faq", "id": 1}},
        {"text": "doc2", "score": 0.4, "metadata": {"source": "blog", "id": 2}},
    ]

    result = reranker.rerank("query", documents, top_k=2)

    assert result[0]["metadata"]["source"] == "faq"
    assert result[0]["metadata"]["id"] == 1
    assert result[1]["metadata"]["source"] == "blog"
    assert result[1]["metadata"]["id"] == 2
