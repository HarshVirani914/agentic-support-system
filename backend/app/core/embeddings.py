import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from fastembed import SparseTextEmbedding
from qdrant_client.models import SparseVector
from app.config import settings

os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY


class EmbeddingModel:
    def __init__(self):
        self.model = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-2-preview",
            google_api_key=settings.GOOGLE_API_KEY,
            output_dimensionality=768,
        )

    def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        return self.model.embed_query(text)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        return self.model.embed_documents(texts)

    @property
    def dimension(self) -> int:
        """Get embedding dimension."""
        return 768


embedding_model = EmbeddingModel()


class SparseEmbeddingModel:
    def __init__(self):
        self.model = SparseTextEmbedding(model_name="Qdrant/bm25")

    def embed_text(self, text: str) -> SparseVector:
        embedding = next(self.model.embed([text]))
        return SparseVector(
            indices=embedding.indices.tolist(), values=embedding.values.tolist()
        )

    def embed_texts(self, texts: list[str]) -> list[SparseVector]:
        embeddings = list(self.model.embed(texts))
        return [
            SparseVector(indices=e.indices.tolist(), values=e.values.tolist())
            for e in embeddings
        ]


sparse_embedding_model = SparseEmbeddingModel()
