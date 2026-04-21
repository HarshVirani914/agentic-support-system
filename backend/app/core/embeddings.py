import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
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
