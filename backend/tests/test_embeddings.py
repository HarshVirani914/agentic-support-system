from app.core.embeddings import sparse_embedding_model


def test_sparse_embed_text_returns_indices_and_values():
    result = sparse_embedding_model.embed_text("refund policy")
    assert len(result.indices) > 0
    assert len(result.indices) == len(result.values)


def test_sparse_embed_texts_returns_one_per_input():
    results = sparse_embedding_model.embed_texts(["refund policy", "shipping time"])
    assert len(results) == 2
