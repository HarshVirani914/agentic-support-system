import os
import time
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from fastembed import SparseTextEmbedding
from qdrant_client.models import SparseVector
from app.config import settings

os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

# Gemini's free tier allows 100 embed_content requests/minute, and the
# LangChain wrapper issues one request per text (no server-side batching).
# Chunking with a pause between chunks keeps ingestion of larger knowledge
# bases working within that limit instead of failing outright.
GEMINI_FREE_TIER_RPM = 100
EMBED_BATCH_SIZE = 90
EMBED_BATCH_COOLDOWN_SECONDS = 65


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
        """Generate embeddings for multiple texts, respecting the free-tier RPM limit."""
        embeddings: list[list[float]] = []
        for i in range(0, len(texts), EMBED_BATCH_SIZE):
            batch = texts[i : i + EMBED_BATCH_SIZE]
            embeddings.extend(self.model.embed_documents(batch))
            if i + EMBED_BATCH_SIZE < len(texts):
                time.sleep(EMBED_BATCH_COOLDOWN_SECONDS)
        return embeddings

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
