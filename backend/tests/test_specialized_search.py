from unittest.mock import patch
from app.agents.nodes.specialized_search import general_search_node


@patch("app.agents.nodes.specialized_search.reranker")
@patch("app.agents.nodes.specialized_search.vector_store")
def test_general_search_reranks_candidates(mock_store, mock_reranker):
    mock_store.search.return_value = [
        {"text": "a", "score": 0.5, "metadata": {}},
        {"text": "b", "score": 0.4, "metadata": {}},
    ]
    mock_reranker.rerank.return_value = [{"text": "b", "score": 0.9, "metadata": {}}]

    state = {"question": "refund policy", "limit": 1}
    result = general_search_node(state)

    mock_store.search.assert_called_once()
    call_args = mock_store.search.call_args
    assert call_args.kwargs["limit"] >= 20  # over-fetch before reranking
    mock_reranker.rerank.assert_called_once_with("refund policy", mock_store.search.return_value, top_k=1)
    assert result == {"documents": [{"text": "b", "score": 0.9, "metadata": {}}]}
