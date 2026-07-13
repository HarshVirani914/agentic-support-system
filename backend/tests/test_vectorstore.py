from unittest.mock import MagicMock, patch
from qdrant_client.models import SparseVector
from app.core.vectorstore import VectorStore


@patch("app.core.vectorstore.sparse_embedding_model")
@patch("app.core.vectorstore.embedding_model")
@patch("app.core.vectorstore.QdrantClient")
def test_search_builds_hybrid_prefetch_query(
    mock_client_cls, mock_dense_model, mock_sparse_model
):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    mock_client.query_points.return_value.points = []
    mock_dense_model.embed_text.return_value = [0.1, 0.2, 0.3]
    mock_sparse_model.embed_text.return_value = SparseVector(
        indices=[1, 2], values=[0.5, 0.5]
    )

    store = VectorStore()
    store.search("refund policy", limit=5)

    _, kwargs = mock_client.query_points.call_args
    assert "prefetch" in kwargs
    assert len(kwargs["prefetch"]) == 2


@patch("app.core.vectorstore.sparse_embedding_model")
@patch("app.core.vectorstore.embedding_model")
@patch("app.core.vectorstore.QdrantClient")
def test_search_returns_expected_shape(
    mock_client_cls, mock_dense_model, mock_sparse_model
):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    mock_dense_model.embed_text.return_value = [0.1, 0.2, 0.3]
    mock_sparse_model.embed_text.return_value = SparseVector(
        indices=[1, 2], values=[0.5, 0.5]
    )

    hit = MagicMock()
    hit.payload = {"text": "Refunds within 30 days.", "metadata": {"source": "faq"}}
    hit.score = 0.87
    mock_client.query_points.return_value.points = [hit]

    store = VectorStore()
    results = store.search("refund policy", limit=5)

    assert results == [
        {
            "text": "Refunds within 30 days.",
            "score": 0.87,
            "metadata": {"source": "faq"},
        }
    ]


@patch("app.core.vectorstore.sparse_embedding_model")
@patch("app.core.vectorstore.embedding_model")
@patch("app.core.vectorstore.QdrantClient")
def test_search_uses_rrf_fusion_query(
    mock_client_cls, mock_dense_model, mock_sparse_model
):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    mock_client.query_points.return_value.points = []
    mock_dense_model.embed_text.return_value = [0.1, 0.2, 0.3]
    mock_sparse_model.embed_text.return_value = SparseVector(
        indices=[1, 2], values=[0.5, 0.5]
    )

    store = VectorStore()
    store.search("refund policy", limit=5)

    _, kwargs = mock_client.query_points.call_args
    assert kwargs["query"].fusion.value == "rrf"


@patch("app.core.vectorstore.QdrantClient")
def test_create_collection_configures_dense_and_sparse_vectors(mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    mock_client.get_collections.return_value.collections = []

    store = VectorStore()
    store.create_collection()

    _, kwargs = mock_client.create_collection.call_args
    assert "dense" in kwargs["vectors_config"]
    assert "sparse" in kwargs["sparse_vectors_config"]


@patch("app.core.vectorstore.sparse_embedding_model")
@patch("app.core.vectorstore.embedding_model")
@patch("app.core.vectorstore.QdrantClient")
def test_upsert_documents_writes_dense_and_sparse_vectors(
    mock_client_cls, mock_dense_model, mock_sparse_model
):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    mock_dense_model.embed_texts.return_value = [[0.1, 0.2, 0.3]]
    mock_sparse_model.embed_texts.return_value = [SparseVector(indices=[1], values=[0.5])]

    store = VectorStore()
    store.upsert_documents([{"text": "Refunds within 30 days.", "metadata": {}}])

    _, kwargs = mock_client.upsert.call_args
    points = kwargs["points"]
    assert len(points) == 1
    assert "dense" in points[0].vector
    assert "sparse" in points[0].vector
