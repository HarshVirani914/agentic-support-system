from sentence_transformers import CrossEncoder
from torch.nn import Sigmoid


class Reranker:
    def __init__(self) -> None:
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, query: str, documents: list[dict], top_k: int = 3) -> list[dict]:
        """
        Rerank documents using a cross-encoder model.

        Args:
            query: The search query
            documents: List of documents with format {"text": str, "score": float, "metadata": dict}
            top_k: Number of top results to return (default: 3)

        Returns:
            Reranked documents sorted by cross-encoder relevance score (descending), truncated to
            top_k. Scores are passed through a sigmoid so they land in (0, 1) like the rest of the
            pipeline's scores — the model's raw output is an unbounded logit, not a probability.
        """
        if not documents:
            return []

        pairs = [(query, doc["text"]) for doc in documents]
        scores = self.model.predict(pairs, activation_fn=Sigmoid())

        reranked = [
            {**doc, "score": float(score)}
            for doc, score in zip(documents, scores)
        ]
        reranked.sort(key=lambda d: d["score"], reverse=True)

        return reranked[:top_k]


reranker = Reranker()
